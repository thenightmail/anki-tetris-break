import moment from "moment/moment";

function dateFormat(date, format = 'YYYY-MM-DD') {
    return moment(date).format(format)
}

const player = new class Player {
    date = new Date()
    lines = 0
    score = 0

    pointPerLine = 1000
    history = []

    DOMScoreboard = document.createElement('div');

    DOMScore = document.createElement('div');
    DOMLines = document.createElement('div');
    DOMHistory = document.createElement('div');
    DOMHistoryTable = undefined;

    linesScored(n) {
        let extraMultipler = ((n - 1) / 10) * n

        this.lines += n
        this.score += this.pointPerLine * (n + extraMultipler)

        this.__updateDOM()
    }

    __updateDOM() {
        this.DOMScore.textContent = this.score
        this.DOMLines.textContent = this.lines
        this.__updateHistoryDOM();
    }

    useScoreboard(DOMScoreboard) {
        if (!DOMScoreboard) return;
        this.DOMScoreboard = DOMScoreboard
        this.DOMScore.classList.add('scoreboard-score')
        this.DOMScore.textContent = '0'
        
        this.DOMLines.classList.add('scoreboard-lines')
        this.DOMLines.textContent = '0'
        
        let DOMScoreTitle = document.createElement('div')
        DOMScoreTitle.classList.add('scoreboard-score-title')
        DOMScoreTitle.textContent = "Today's Score"
        
        let DOMLinesTitle = document.createElement('div')
        DOMLinesTitle.classList.add('scoreboard-lines-title')
        DOMLinesTitle.textContent = "Lines Cleared"
        
        DOMScoreboard.appendChild(DOMScoreTitle)
        DOMScoreboard.appendChild(this.DOMScore)
        DOMScoreboard.appendChild(DOMLinesTitle)
        DOMScoreboard.appendChild(this.DOMLines)
    }
    useHistory(DOMHistory) {
        if (!DOMHistory) return;
        this.__updateHistoryDOM()
        this.DOMHistory = DOMHistory
    }
    __updateHistoryDOM() {
        this.DOMHistory.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Score</th>
                        <th>Lines</th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            </table>
        `
        this.DOMHistoryTable = this.DOMHistory.querySelector('tbody');
        for(let record of this.history) {
            this.DOMHistoryTable.innerHTML += `
                <tr>
                    <td>${dateFormat(record.date, 'MM/DD/YYYY')}</td>
                    <td>${record.score}</td>
                    <td>${record.lines}</td>
                </tr>
            `
        }
        if(this.history.length == 0) {
            this.DOMHistoryTable.innerHTML += `
                <tr><td colspan="3">No history to display</td></tr>
            `
        }
    }

    loadPlayerData(playerData) {
        this.date = playerData.date;
        this.score = playerData.score;
        this.lines = playerData.lines;
        this.pointPerLine = playerData.pointPerLine;
        this.history = playerData.history;
        this.checkAndUpdateHistory()
        this.__updateDOM()
    }

    checkAndUpdateHistory() {
        let now = dateFormat(Date.now(), 'YYYY-MM-DD')
        // If current stats are from a past day, store it in the history and reset stats
        if(moment(now).isAfter(this.date)) {
            this.history.push({
                date: dateFormat(this.date, 'YYYY-MM-DD'),
                score: this.score,
                lines: this.lines,
                pointPerLine: this.pointPerLine
            })

            this.resetStats()
            window.tetris.nextBlock = []
            window.tetris.resetGrid()
        }
    }

    resetStats() {
        this.score = 0
        this.lines = 0
        this.date = dateFormat(new Date(), 'YYYY-MM-DD')
    }
}
export default player;