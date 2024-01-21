// Colors
export const colors = [
    'var(--color-red)',
    'var(--color-orange)',
    'var(--color-yellow)',
    'var(--color-green)',
    'var(--color-blue)',
]

// Shapes
export const shapes = [
    // L
    {
        name: "L",
        width: 3,
        height: 2,
        matrix: [
            [1, 0, 0],
            [1, 1, 1]
        ]
    },
    // Inverted L
    {
        name: "Inverted L",
        width: 3,
        height: 2,
        matrix: [
            [1, 1, 1],
            [1, 0, 0]
        ]
    },
    // T
    {
        name: "T",
        width: 3,
        height: 2,
        matrix: [
            [0, 1, 0],
            [1, 1, 1]
        ]
    },
    // Square
    {
        name: "Square",
        width: 2,
        height: 2,
        matrix: [
            [1, 1],
            [1, 1]
        ]
    },
    // Line
    {
        name: "Line",
        width: 4,
        height: 1,
        matrix: [
            [1, 1, 1, 1]
        ]
    },
    // Skewed Left
    {
        name: "Skewed Left",
        width: 3,
        height: 2,
        matrix: [
            [0, 1, 1],
            [1, 1, 0]
        ]
    },
    // Skewed Right
    {
        name: "Skewed Right",
        width: 3,
        height: 2,
        matrix: [
            [1, 1, 0],
            [0, 1, 1]
        ]
    },
]

export const GRID_STATE = {
    EMPTY_BLOCK: 0,
    INACTIVE_BLOCK: 1,
    ACTIVE_BLOCK: 2,
}