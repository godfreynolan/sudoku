from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret_key"

# Example Sudoku grid (0 represents empty cells)
initial_grid = [
    [5, 3, 0],
    [6, 0, 0],
    [0, 9, 8],
]

def is_valid_grid(grid):
    """
    Validate the 3x3 Sudoku grid.
    """
    # Check rows
    for row in grid:
        if not is_valid_unit(row):
            return False

    # Check columns
    for col in range(3):
        column = [grid[row][col] for row in range(3)]
        if not is_valid_unit(column):
            return False

    return True

def is_valid_unit(unit):
    """
    Check if a unit (row or column) contains unique non-zero values.
    """
    non_zero_values = [num for num in unit if num != 0]
    return len(non_zero_values) == len(set(non_zero_values))

@app.route("/", methods=["GET", "POST"])
def sudoku():
    if request.method == "POST":
        try:
            # Get the grid values from the form
            grid = []
            for i in range(3):
                row = []
                for j in range(3):
                    value = request.form.get(f"cell-{i}-{j}")
                    row.append(int(value) if value.isdigit() else 0)
                grid.append(row)

            # Validate the grid
            if is_valid_grid(grid):
                flash("The grid is valid!", "success")
            else:
                flash("The grid is invalid!", "danger")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        return redirect(url_for("sudoku"))

    return render_template("index.html", grid=initial_grid)

if __name__ == "__main__":
    app.run(debug=True)
