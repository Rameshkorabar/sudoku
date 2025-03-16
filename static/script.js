// Add any JavaScript functionality for customization or animation
document.addEventListener('DOMContentLoaded', () => {
    // Example: add animation to Sudoku grid cells
    const cells = document.querySelectorAll('.sudoku-cell');
    cells.forEach(cell => {
        cell.addEventListener('focus', (e) => {
            e.target.style.backgroundColor = "#e0e0e0";
        });
        cell.addEventListener('blur', (e) => {
            e.target.style.backgroundColor = "red";
        });
    });
});
