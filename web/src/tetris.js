import player from "./player";
import { useActions } from "./actions"

import * as utils from "./utils"
import { colors, shapes, GRID_STATE } from "./consts"

// Tetris
const tetris = new class Tetris {

    virtualGrid = []
    DOMElement = undefined;
    DOMGrid = undefined;

    interval = 80;
    initialInterval = 80;
    lineCompletedInterval = 1000;

    activeBlock = undefined;
    activeColor = undefined
    loopFn = undefined
    blockPosition = []

    DOMNextblock = undefined;
    nextBlock = []

    drop = false

    // Init
    init(DOMSelector, width, height) {
        this.__setSize(width, height)
        this.__createVirtualGrid(width, height);
        this.__createDOMElement(DOMSelector, width, height)
        this.nextBlock = shapes[utils.generateRandomNumber(0, shapes.length - 1)];
        this.__setupEventListeners();
    }

    __setSize(width, height) {
        this.width = width;
        this.height = height
    }

    __createVirtualGrid(width, height) {
        let grid = Array.from({ length: height }, (_, index) =>
            Array.from({ length: width }, () => GRID_STATE.EMPTY_BLOCK)
        );
        this.virtualGrid = grid;
    }

    __createDOMElement(DOMSelector, width, height) {
        let element = document.querySelector(DOMSelector);
        element.classList.add('tetris')
        element.style.setProperty('--width', width);
        element.style.setProperty('--height', height);

        let DOMGrid = `<table class="tetris-table">`
        for (let row of this.virtualGrid) {
            DOMGrid += `<tr>`
            for (let cell of row) {
                DOMGrid += `<td></td>`
            }
            DOMGrid += `</tr>`
        }
        DOMGrid += `</table>`

        // Add the message element
        DOMGrid += `<div id="message"></div>`

        element.innerHTML += DOMGrid

        this.DOMGrid = element.children[0];
        this.DOMElement = element;
    }
    // End - Init

    // Input events
    __setupEventListeners() {
        document.body.addEventListener('keydown', (ev) => {
            this.__commandDown(ev);
        });
        document.body.addEventListener('keyup', (ev) => {
            this.__commandUp(ev);
        });
    }

    save() {
        // Save grid without 2's (active block)
        let grid = JSON.parse(JSON.stringify(this.virtualGrid).replaceAll('2', '0'))

        // Update the history
        player.checkAndUpdateHistory()

        let data = {
            tetris: {
                virtualGrid: grid
            },
            player: {
                date: player.date,
                lines: player.lines,
                score: player.score,
                pointPerLine: player.pointPerLine,
                history: player.history
            }
        }

        pycmd(`tetris::save::${JSON.stringify(data)}`)
    }

    load(data) {
        this.virtualGrid = data.tetris.virtualGrid
        player.loadPlayerData(data.player);
        this.start()
    }
    loadSettings(settings) {
        console.table(settings)
        if(settings.backgroundImage != "") {
            // console.log(settings.backgroundImage)
            this.usePictureAsBackground(settings.backgroundImage)
        }
    }

    usePictureAsBackground(src) {
        this.DOMElement.classList.add('bg-img');
        this.DOMElement.style.setProperty("--bg-grid", `url("${src}")`)
    }

    // Input event listener
    __commandDown(ev) {
        let key = ev.key;
        switch (key) {
            case 'ArrowLeft':
                this.__moveLeft()
                if (this.drop == false) this.__gameLoop()
                ev.preventDefault()
                break;
            case 'ArrowRight':
                this.__moveRight()
                if (this.drop == false) this.__gameLoop()
                ev.preventDefault()
                break;
            case 'z':
                this.__rotate()
                if (this.drop == false) this.__gameLoop()
                ev.preventDefault()
                break;
            case 'ArrowDown':
                if (this.drop == false) {
                    this.drop = true
                    this.loopFn = this.__gameLoop.bind(this)
                    this.__gameLoop()
                } else {
                    this.__increaseSpeedDown();
                }
                ev.preventDefault()
                break;

            default:
                break;
        }
    }

    // Input event listener
    __commandUp(ev) {
        let key = ev.key;
        switch (key) {
            case 'ArrowDown':
                this.__normalizeSpeedDown()
                ev.preventDefault()
                break;
            default:
                break;
        }
    }

    // Start / Stop Functions
    start() {
        this.__addRandomBlock()
        this.interval = this.initialInterval
        this.loopFn = this.__waitForCommand.bind(this)
        this.__gameLoop()
    }

    stop() {
        this.loopFn = null;
    }
    // End - Start / Stop Functions

    __waitForCommand() {
    }

    // Block Functions
    __addRandomBlock() {
        let shape = { ...this.nextBlock };
        this.blockShape = shape;
        let x = Math.floor((this.width / 2) - (shape.width / 2));
        let y = 3;

        this.activeColor = colors[utils.generateRandomNumber(0, colors.length - 1)]

        this.__addBlockToMatrix(shape, x, y)

        this.nextBlock = shapes[utils.generateRandomNumber(0, shapes.length - 1)]

        this.__paintNextBlock()
    }

    // Add the block to the matrix
    __addBlockToMatrix(shape, x, y) {

        let overlap = false;

        // Vertical
        for (let i = 0; i < shape.height; i++) {
            // Horizontal
            for (let j = 0; j < shape.width; j++) {
                if (shape.matrix[i][j] == 0) continue;
                if (this.virtualGrid[y + i][x + j] != GRID_STATE.EMPTY_BLOCK) overlap = true;
                this.virtualGrid[y + i][x + j] = GRID_STATE.ACTIVE_BLOCK;
            }
        }

        if (overlap == true) this.__lose();

    }

    __lose() {
        this.stop();
        window.displayMessage("Oh no! Press the reset button to play again.")
    }

    // Game Loop
    __gameLoop() {
        this.__getUpdatedPosition()
        if (this.drop == true) {
            this.__moveDown().then(() => {
                this.__updateDOM()
                this.__delay()
            })
        } else {
            this.__updateDOM()
            this.__delay()
        }
    }

    __delay() {
        setTimeout(this.loopFn, this.interval)
    }

    async __moveDown() {

        // Check to make sure it the future coordinates are empty
        let moveAllowed = this.__canMoveTo(0, 1)
        if (moveAllowed) {
            for (let cell of this.blockPosition) {
                let x = cell.x
                let y = cell.y
                this.virtualGrid[y][x] = GRID_STATE.EMPTY_BLOCK;
            }
            for (let cell of this.blockPosition) {
                let x = cell.x
                let y = cell.y
                this.virtualGrid[y + 1][x] = GRID_STATE.ACTIVE_BLOCK;
            }

            // If hit bottom
        } else {
            await this.__placeBlock()
        }
    }

    async __placeBlock() {
        this.__undraw(GRID_STATE.INACTIVE_BLOCK)

        await this.__checkLines()

        this.__addRandomBlock()

        // Stop loop
        this.drop = false
        this.loopFn = null
    }

    async __checkLines() {
        let completedLines = []
        for (let y = 0; y < this.height; y++) {
            let lineCompleted = true;
            for (let x = 0; x < this.width; x++) {
                if (this.virtualGrid[y][x] != GRID_STATE.INACTIVE_BLOCK) lineCompleted = false
            }
            if (lineCompleted) completedLines.push(y)
        }

        if (completedLines.length > 0) {
            // Update the virtual grid
            for (let line of completedLines) {
                this.virtualGrid.splice(line, 1)
                this.virtualGrid.unshift(Array.from({ length: this.width }, () => GRID_STATE.EMPTY_BLOCK))
            }

            await this.__lineCompletedAnimation(completedLines)

            // Add points to the player
            player.linesScored(completedLines.length);
        }
    }

    async __lineCompletedAnimation(completedLines) {
        for (let line of completedLines) {
            for (let cell of this.DOMGrid.querySelectorAll('tr')[line].children) {
                cell.classList.add('completed-animation')
                cell.style.setProperty('--color-completed', this.activeColor)
            }
        }
        await new Promise(r => setTimeout(r, this.lineCompletedInterval));
        for (let line of completedLines) {
            for (let cell of this.DOMGrid.querySelectorAll('tr')[line].children) {
                cell.classList.remove('completed-animation')
            }
        }
        setTimeout(() => {
            pycmd('tetris::done')
        }, 250)
    }

    __moveLeft() {
        this.__getUpdatedPosition()
        this.__moveHorizontally(-1)
    }

    __moveRight() {
        this.__getUpdatedPosition()
        this.__moveHorizontally(1)
    }

    __increaseSpeedDown() {
        this.interval = this.initialInterval / 3;
    }

    __normalizeSpeedDown() {
        this.interval = this.initialInterval;
    }

    __rotate() {
        this.__getUpdatedPosition();
        this.__undraw()
        let oldWidth = this.blockShape.width;
        let oldHeight = this.blockShape.height;
        let oldX = this.blockTopLeft.x;
        let oldY = this.blockTopLeft.y;

        let newWidth = this.blockShape.height
        let newHeight = this.blockShape.width
        this.blockShape.height = newHeight
        this.blockShape.width = newWidth

        let newMatrix = utils.rotateMatrix(this.blockShape.matrix);
        this.blockShape.matrix = newMatrix

        let x = oldX;
        let y = (oldY + oldHeight) - newHeight;

        // Adjust X and Y if out of bounds
        if (x + this.blockShape.width > this.width) x = this.width - this.blockShape.width

        this.__addBlockToMatrix(this.blockShape, x, y)
    }

    __undraw(state = GRID_STATE.EMPTY_BLOCK) {
        for (let cell of this.blockPosition) {
            let x = cell.x
            let y = cell.y
            this.virtualGrid[y][x] = state;
        }
    }

    __moveHorizontally(xIncrement) {

        // Check to make sure it the future coordinates are empty
        let moveAllowed = this.__canMoveTo(xIncrement, 0)
        if (moveAllowed) {
            for (let cell of this.blockPosition) {
                let x = cell.x
                let y = cell.y
                this.virtualGrid[y][x] = GRID_STATE.EMPTY_BLOCK;
            }
            for (let cell of this.blockPosition) {
                let x = cell.x
                let y = cell.y
                this.virtualGrid[y][x + xIncrement] = GRID_STATE.ACTIVE_BLOCK;
            }
        }
    }

    __canMoveTo(xIncrement, yIncrement) {
        let moveAllowed = true;
        // Check for inactive blocks on the way
        // No need to check for empty or active
        // Also checks for edges
        for (let cell of this.blockPosition) {
            let x = cell.x + xIncrement
            let y = cell.y + yIncrement
            if (y >= this.height) {
                moveAllowed = false;
                break;
            } else if (
                x >= this.width ||
                x < 0) {
                moveAllowed = false;
                break;
            } else if (this.virtualGrid[y][x] == GRID_STATE.INACTIVE_BLOCK) {
                moveAllowed = false;
                break;
            }
        }
        return moveAllowed
    }

    __getUpdatedPosition() {
        let top = null;
        let left = null;
        let centerX = 0;
        let centerY = 0;
        let totalPoints = 0;

        // Get the position of the active block
        let blockPosition = []
        this.virtualGrid.map((row, y) => {
            row.map((value, x) => {
                if (value === GRID_STATE.ACTIVE_BLOCK) {
                    blockPosition.push({ x, y });

                    if (top == null || y < top) top = y
                    if (left == null || x < left) left = x

                    centerX += x
                    centerY += y
                    totalPoints++
                }
            })
        })
        this.blockPosition = blockPosition

        // Get the center of the block for rotation
        this.blockCenter = {
            x: Math.floor(centerX / totalPoints),
            y: Math.floor(centerY / totalPoints)
        }
        this.blockTopLeft = {
            x: left,
            y: top
        }
    }

    __updateDOM() {
        // Update the DOM based on the virtual grid
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                let color = 'var(--bg-empty)'
                if (this.virtualGrid[y][x] == GRID_STATE.INACTIVE_BLOCK)
                    color = 'var(--bg-inactive)'
                if (this.virtualGrid[y][x] == GRID_STATE.ACTIVE_BLOCK)
                    color = this.activeColor

                this.DOMGrid.children[0].children[y].children[x].style.backgroundColor = color;
            }
        }
    }

    useNextBlock(element) {
        element.innerHTML = `
            <div class="title">Next block:</div>
            <table class="tetris-table">
                <tr>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            </table>
        `
        this.DOMNextblock = element
    }

    __paintNextBlock() {
        let block = this.nextBlock;
        let startingX = 0;
        let startingY = 0;

        // Undraw
        for (let cell of this.DOMNextblock.querySelectorAll('td')) {
            cell.style.setProperty('--color', '')
        }

        // Update the DOM based on the virtual grid
        for (let y = 0; y < block.height; y++) {
            for (let x = 0; x < block.width; x++) {
                let color = 'none'
                if (block.matrix[y][x] == 1)
                    color = 'var(--bg-inactive)';

                this.DOMNextblock.querySelectorAll('tr')[y].children[x].style.setProperty('--color', color);
            }
        }
    }
    resetGrid() {
        this.__createVirtualGrid(this.width, this.height)
        this.__addRandomBlock()
        this.__updateDOM()
    }
}

window.toggleMessage = (msg) => {
    if(window.DOMMessage.classList.contains('active')) window.closeMessage()
    else window.displayMessage(msg)
}


window.displayMessage = (msg) => {
    window.DOMMessage.innerHTML = msg;
    window.DOMMessage.classList.add('active');
}

window.closeMessage = () => {
    window.DOMMessage.classList.remove('active');
}

function startTetris() {
    tetris.init('#grid', 14, 14 * 2)
    tetris.useNextBlock(document.querySelector('#nextblock'))
    player.useScoreboard(document.querySelector("#scoreboard"))
    player.useHistory(document.querySelector("#history"))

    window.tetris = tetris
    window.player = player
    window.DOMMessage = document.querySelector("#message")
    setTimeout(() => {
        pycmd('tetris::load')
    }, 250);
}

// DARK MODE
const darkMode = new URLSearchParams(window.location.search).get('dark');
if (darkMode == "True") {
    document.documentElement.classList.add('night-mode')
}

startTetris()
useActions(document.querySelector("#actions"))

export default tetris;