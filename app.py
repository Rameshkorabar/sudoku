from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'f9b2ac7d8abed6c6c7b5e8bc92cd3c52dbfdb4eaf9c2f9b5a1d8f24f7e8a1b61'
  # Change to a real secret key for production

# Fake database for demo purposes
users = {}


# Example of setting session['solution'] when generating a new puzzle



# Generate a random Sudoku puzzle (for simplicity, not solving it fully)
def generate_sudoku():
    grid = [[0] * 9 for _ in range(9)]  # Create an empty 9x9 grid

    # Function to check if placing a number in a cell is valid
    def is_valid(grid, row, col, num):
        # Check the row and column
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False

        # Check the 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num:
                    return False
        return True

    # Backtracking function to fill the grid
    def solve(grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:  # Find the first empty cell
                    random_numbers = list(range(1, 10))
                    random.shuffle(random_numbers)  # Shuffle numbers 1 to 9 for randomness

                    for num in random_numbers:
                        if is_valid(grid, row, col, num):
                            grid[row][col] = num  # Place the number

                            if solve(grid):  # Recursively solve the next cell
                                return True

                            grid[row][col] = 0  # Backtrack if no valid number is found
                    return False  # Return false if no valid number is found
        return True  # Return true when all cells are filled

    # Fill the grid using backtracking
    solve(grid)

    # Make a copy of the filled grid as the solution
    solution = [row[:] for row in grid]

    # Remove some cells randomly to create the puzzle (we'll remove up to 40 cells)
    puzzle = [row[:] for row in grid]
    for _ in range(random.randint(35, 50)):  # Random number of empty cells
        row, col = random.randint(0, 8), random.randint(0, 8)
        while puzzle[row][col] == 0:  # Ensure we're not removing already empty cells
            row, col = random.randint(0, 8), random.randint(0, 8)
        puzzle[row][col] = 0

    return puzzle, solution

# Check if the user's solution is correct
def is_solved(puzzle, user_solution):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != user_solution[i][j]:
                return False
    return True

@app.route('/')
def index():
    if 'username' in session:
        puzzle, solution = generate_sudoku()
        session['solution'] = solution  # Store the solution in the session
        return render_template('sudoku.html', puzzle=puzzle)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists in our "database"
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = "Invalid credentials! Please check your username and password."
            return render_template('login.html', error=error)
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        if username in users:
            error = "Username already exists! Please choose a different one."
            return render_template('signup.html', error=error)
        
        # Save user to the "database"
        users[username] = password
        return redirect(url_for('login'))
    
    return render_template('signup.html')



@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('solution', None)
    return redirect(url_for('login'))
@app.route('/check_solution', methods=['POST'])
def check_solution():
    # Handle the user's solution here
    user_solution = []
    for i in range(9):
        row = []
        for j in range(9):
            cell_value = request.form.get(f'cell-{i}-{j}')
            row.append(int(cell_value) if cell_value else 0)
        user_solution.append(row)
    
    if is_solved(session['solution'], user_solution):
        message = "Congratulations! You solved the puzzle!"
    else:
        message = "Oops! Incorrect solution, try again."
    
    return render_template('sudoku.html', message=message, puzzle=session['solution'])


# Function to check if the solution is correct
def is_solved(actual_solution, user_solution):
    # Compare the actual solution with the user input solution
    return actual_solution == user_solution


@app.route('/reset', methods=['GET'])
def reset():
    if 'username' in session:
        puzzle, solution = generate_sudoku()
        session['solution'] = solution  # Store the solution in the session
        return render_template('sudoku.html', puzzle=puzzle)
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)
