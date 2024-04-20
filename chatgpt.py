from itertools import combinations

def generate_CNF(matrix):
    cnf = []

    rows = len(matrix)
    cols = len(matrix[0])

    # Helper function to map cell index to variable name
    def cell_var(i, j):
        return m * i + j + 1

    # Helper function to get neighboring cells
    def neighbors(i, j):
        return [(i+di, j+dj) for di in [-1, 0, 1] for dj in [-1, 0, 1]
                if (di != 0 or dj != 0) and 0 <= i+di < rows and 0 <= j+dj < cols]

    # Iterate through the matrix to generate CNF clauses
    for i in range(rows):
        for j in range(cols):
            # Cell with a number
            if isinstance(matrix[i][j], int):
                n = matrix[i][j]
                cell = cell_var(i, j)
                neighboring_traps = [cell_var(x, y) for x, y in neighbors(i, j)]

                # If the cell is surrounded by n traps, it cannot be a gem
                clause = [-cell] + neighboring_traps
                cnf.append(clause)

                # If the cell is surrounded by less than n traps, it cannot be a trap
                for combination in combinations(neighboring_traps, n):
                    clause = [cell] + list(combination)
                    cnf.append(clause)

            # Cell without a number
            else:
                cell = cell_var(i, j)
                cnf.append([cell, -cell])

    return cnf

# Example matrix
matrix = [
    [3, '_', 2, '_'],
    ['_', '_', 2, '_'],
    ['_', 3, 1, '_']
]

# Define the size of the matrix
m = len(matrix[0])

# Generate CNF clauses
cnf = generate_CNF(matrix)
for clause in cnf:
    print(clause)
