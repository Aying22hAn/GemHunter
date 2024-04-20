from pysat.solvers import Glucose3

def generate_cnf(matrix):
    cnf = []
    n = len(matrix)
    m = len(matrix[0])

    # Step 1: Assign logical variables to each cell
    variables = [[Glucose3().new_var() for _ in range(m)] for _ in range(n)]

    # Step 2: Write constraints for cells containing numbers
    for i in range(n):
        for j in range(m):
            if matrix[i][j] != '_':
                traps = int(matrix[i][j])
                neighbors = []
                if i > 0:
                    neighbors.append(variables[i-1][j])
                if i < n-1:
                    neighbors.append(variables[i+1][j])
                if j > 0:
                    neighbors.append(variables[i][j-1])
                if j < m-1:
                    neighbors.append(variables[i][j+1])
                cnf.append(neighbors + [-variables[i][j]] * traps)
                cnf.append([-x for x in neighbors] + [variables[i][j]] * (len(neighbors) - traps))

    # Step 3: Generate CNFs automatically
    cnf = [list(set(clause)) for clause in cnf]  # Remove duplicate clauses

    return cnf

def solve_cnf(cnf):
    with Glucose3() as solver:
        for clause in cnf:
            solver.add_clause(clause)
        result = solver.solve()
        if result:
            model = solver.get_model()
            return [var > 0 for var in model]
        else:
            return None

# Step 4: Using the pysat library to find the value for each variable and infer the result
matrix = [
    [3, '_', 2, '_'],
    ['_', '_', 2, '_'],
    ['_', 3, 1, '_']
]

cnf = generate_cnf(matrix)
result = solve_cnf(cnf)

if result is not None:
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == '_':
                if result[i][j]:
                    print(f"Cell ({i}, {j}) is a trap")
                else:
                    print(f"Cell ({i}, {j}) is a gem")
else:
    print("No solution found")