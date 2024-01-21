// Generate a random number within a range
export function generateRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min)
}

// Rotate the matrix
export function rotateMatrix(matrix) {
    let output = Array.from({ length: matrix[0].length }, () => {
        return Array.from({ length: matrix.length }, () => 0)
    })
    matrix.map((row, i) =>
        row.map((val, j) =>
            output[j][i] = matrix[matrix.length - 1 - i][j]
        )
    );

    return output;
}