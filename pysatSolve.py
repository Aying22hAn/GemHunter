from pysat.solvers import Glucose3

import itertools as it

''' File handling '''
def read_file(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            row = line.strip().split(', ')
            processed_row = []
            for item in row:
                if item.isdigit():
                    processed_row.append(int(item))
                else:
                    processed_row.append(item)
            grid.append(processed_row)
    
    return grid


def wirte_file(filename, final_grid):
    with open(filename, 'w') as file:
        for row in final_grid:  
            line = ', '.join(row)
            file.write(line + '\n')
            
map_grid = read_file('input.txt')
row_size = len(map_grid)
col_size = len(map_grid[0])

# print(map_grid)

''' Support function '''
# Sample grid (underscores are unknowns, numbers are constraints)

# Define the function to convert grid indices to variable numbers
def varnum(i, j, width):
    return i * width + j + 1

# Function to generate CNF clauses based on the number constraints in the grid
def generate_cnf(grid):
    clauses = []
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    # Iterate through each cell in the grid
    for i in range(height):
        for j in range(width):
            if isinstance(grid[i][j], int):
                num = grid[i][j]
                # Collect variables for neighbors
                neighbors = []
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        ni, nj = i + di, j + dj
                        if 0 <= ni < height and 0 <= nj < width and (di != 0 or dj != 0):
                            if not isinstance(grid[ni][nj], int):
                                neighbors.append(varnum(ni, nj, width))

                # Generate clauses only if the cell is not determined as a trap or a gem
                if len(neighbors) > 0:
                    clauses += generate_exact_k_clauses(neighbors, num)

    return clauses


# Placeholder function for generating exact k combinations as CNF
def generate_exact_k_clauses(variables, k):
    from itertools import combinations
    # This is a simplified placeholder for demonstration. Actual implementation
    # would need to correctly format these into CNF.
    # You would typically need to create combinations for exactly k true and the rest false.
    all_combinations = list(combinations(variables, k))
    exact_k_clauses = []
    for combo in all_combinations:
        clause = []
        for var in variables:
            if var in combo:
                clause.append(var)   # True if in the combination
            else:
                clause.append(-var)  # False if not in the combination
        exact_k_clauses.append(clause)
    return exact_k_clauses



def solve_cnf_clause(clause):
    solver = Glucose3()
    for c in clause:
        solver.add_clause(c)    
    result = solver.solve()
    if result:
        model = solver.get_model()
        return model
    else:
        return None

# Example usage
# Generate CNF for the example grid
cnf_clauses = generate_cnf(map_grid)

# print (cnf_clauses)
with open('output.txt', 'w') as f:
    for i in range(cnf_clauses.__len__()):
        f.write(str(cnf_clauses[i]))
        f.write('\n')
    
    solution = solve_cnf_clause(cnf_clauses)
    if solution:
        f.write("\n")
        f.write("Satisfiable: " + str(solution))
    else:
        f.write("Unsatisfiable")