// DOM Actions
const DOMActions = new class Actions {
    DOMElement;
    buttons = [
        {
            label: "Show Controls",
            name: "controls",
            action: () => {
                window.toggleMessage(`
                <p>
                    Use <span class="key"><img src="./media/arrow-left-solid.svg" /></span>
                    <span class="key"><img src="./media/arrow-right-solid.svg" /></span>
                    to move the blocks
                </p>
                <p>
                    Press <span class="key">Z</span>
                    to rotate the blocks
                </p>
                <p>
                    Press <span class="key"><img src="./media/arrow-down-solid.svg" /></span>
                    to drop the blocks
                </p>
                `)
            },
            active: true
        },
        {
            label: "Show / Hide History",
            name: "history",
            action: () => {
                player.DOMHistory.classList.toggle('active')
            },
            active: true
        },
        {
            label: "Reset",
            name: "reset",
            action: () => {
                tetris.resetGrid()
                window.closeMessage();
            },
            active: true
        },
    ]

    registerActions() {
        // Register each active action
        for(let act of this.buttons.filter((button) => button.active == true)) {
            let DOMAct = document.createElement('button')
            DOMAct.name = act.name;
            DOMAct.onclick = act.action;
            DOMAct.textContent = act.label

            // Add to DOM
            this.DOMElement.appendChild(DOMAct)
        }
    }
}

export function useActions(element) {
    DOMActions.DOMElement = element
    DOMActions.registerActions()
}