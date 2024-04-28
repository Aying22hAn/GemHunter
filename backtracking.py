import os
import itertools
from itertools import product


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


def write_file(filename, solution, map_grid):
    with open(filename, 'w') as file:
        for i, row in enumerate(map_grid):
            for j, cell in enumerate(row):
                if cell == '_':
                    var = var_map.get((i, j), None)  
                    value = solution[var] if var is not None and var in solution else None
                    file.write('T' if value else 'G')
                else:
                    file.write(str(cell))
                if j < len(row) - 1:
                    file.write(', ')
            file.write('\n')

            
map_grid = read_file('input.txt')

print(map_grid)

def generateCNF(grid):
    """ Generate CNF from the grid provided """
    n = len(grid)
    m = len(grid[0])
    cnf = []
    var_map = {}
    next_var = 1
    for i in range(n):
        for j in range(m):
            if grid[i][j] != '_':
                num_traps = int(grid[i][j])
                neighbors = [
                    (x, y) for x in range(max(0, i-1), min(n, i+2))
                    for y in range(max(0, j-1), min(m, j+2))
                    if (x, y) != (i, j) and grid[x][y] == '_'
                ]
                # Gán biến cho các hàng xóm
                for x, y in neighbors:
                    if (x, y) not in var_map:
                        var_map[(x, y)] = next_var
                        next_var += 1
                        
                # Tạo mệnh đề cho số bẫy
                if neighbors:
                    # Các mệnh đề cho trường hợp có nhiều hơn num_traps bẫy
                    if len(neighbors) >= num_traps:
                        for comb in itertools.combinations(neighbors, num_traps + 1):
                            cnf.append([-var_map[x, y] for x, y in comb])
                    # Các mệnh đề cho trường hợp có ít hơn num_traps bẫy
                    if len(neighbors) >= (len(neighbors) - num_traps + 1):
                        for comb in itertools.combinations(neighbors, len(neighbors) - num_traps + 1):
                            cnf.append([var_map[x, y] for x, y in comb])
    return cnf, var_map, n, m


clauses, var_map, row_size, col_size = generateCNF(map_grid)


''' Brute force Algorithm'''

def evaluate_clause(clause, assignment):
    for literal in clause:
        if literal in assignment:
            if assignment[literal]:
                return True
        elif -literal in assignment:
            if not assignment[-literal]:
                return True
    return False

def evaluate_cnf(cnf, assignment):
    for clause in cnf:
        if not evaluate_clause(clause, assignment):
            return False
    return True

def brute_force(cnf):
    num_vars = max([abs(literal) for clause in cnf for literal in clause])
    for i in range(2 ** num_vars):
        assignment = {}
        for j in range(num_vars):
            assignment[j + 1] = bool(i & (1 << j))
        if evaluate_cnf(cnf, assignment):
            return assignment
    return None


''' Backtracking '''
def extract_variables(clauses):
    variables = set()
    for clause in clauses:
        for literal in clause:
            variables.add(abs(literal))
    return variables

def is_satisfied(clauses, assignment):
    for clause in clauses:
        satisfied = False
        for literal in clause:
            var = abs(literal)
            is_true = literal > 0
            if var in assignment and assignment[var] == is_true:
                satisfied = True
                break
        if not satisfied:
            return False
    return True

def backtracking(assignment, variables, clauses):
    if len(assignment) == len(variables):
        if is_satisfied(clauses, assignment):
            return assignment
        else:
            return None

    var = next(v for v in variables if v not in assignment)
    for value in [True, False]:
        assignment[var] = value
        result = backtracking(assignment.copy(), variables, clauses)
        if result is not None:
            return result
    return None




def solve(option):
    if option == 0:
        solution = brute_force(clauses)
    elif option == 1:
        variables = extract_variables(clauses)
        solution = backtracking({}, variables, clauses)
        pass
    elif option == 2:
        #solution = optimal(clauses)
        pass
    else:
        print("Invalid!")
        return
        
    if solution:
        write_file("output.txt", solution, map_grid)
    else:
        print("No solution is found!.")




solve(1)
