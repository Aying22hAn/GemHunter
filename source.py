import itertools
import copy
from itertools import product
from pysat.solvers import Solver

# Đọc file
def readInput(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()
    
    
    matrix = []

    for l in lines:
        row = l.strip().split(", ")
        matrix.append(row)
    
    return matrix
grid = readInput("input.txt")
print(grid)

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
                    print(i,' ', j, ' ', len(neighbors), ' ', num_traps)
                    # Các mệnh đề cho trường hợp có nhiều hơn num_traps bẫy
                    if len(neighbors) > num_traps:
                        for comb in itertools.combinations(neighbors, num_traps + 1):
                            cnf.append([-var_map[x, y] for x, y in comb])
                            print([-var_map[x, y] for x, y in comb])
                    # Các mệnh đề cho trường hợp có ít hơn num_traps bẫy
                    if len(neighbors) >= (len(neighbors) - num_traps + 1):
                        for comb in itertools.combinations(neighbors, len(neighbors) - num_traps + 1):
                            cnf.append([var_map[x, y] for x, y in comb])
                            print([var_map[x, y] for x, y in comb])
    
    return  cnf, var_map, n, m

def solveCNF(grid, cnf, var_map, n, m):
    solver = Solver(name='Glucose3')
    for clause in cnf:
        solver.add_clause(clause)
    is_solvable = solver.solve()
    solution = [['_' for _ in range(m)] for _ in range(n)]
    if is_solvable:
        model = solver.get_model()
        for (i, j), var in var_map.items():
            solution[i][j] = 'T' if model[var - 1] > 0 else 'G'
    solver.delete()
    
    #thêm các số trong grid ban đầu vào solution:
    for i in range(len(solution)):
        for j in range(len(solution[0])):
            if solution[i][j] == '_':
                solution[i][j] = grid[i][j]

    return solution

# Brute-Force
def bruteorce(grid):
    """ Implement a brute-force solution """
    # This is a placeholder for the actual brute-force algorithm
    def countTrapsAround(board, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == 'T':
                    count += 1
        return count

    def isValid(board):
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y].isdigit():
                    expected_count = int(board[x][y])
                    if countTrapsAround(board, x, y) != expected_count:
                        return False
        return True

    def processBruteFore(grid):
        rows = len(grid)
        cols = len(grid[0])
        indices = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == '_']

        # Mặc định tất cả là đá quý không có số liền kề
        for i, j in indices:
            if all(not grid[x][y].isdigit() for x in range(max(0, i-1), min(rows, i+2)) for y in range(max(0, j-1), min(cols, j+2))):
                grid[i][j] = 'F'
        
        # Chỉ xem xét kết hợp cho các ô chưa được chỉ định còn lại
        remaining_indices = [(i, j) for i, j in indices if grid[i][j] == '_']
        
        for combo in product(['T', 'G'], repeat=len(remaining_indices)):
            # Đặt ô dựa trên trạng thái hiện tại
            for (index, value) in zip(remaining_indices, combo):
                grid[index[0]][index[1]] = value
            
            if isValid(grid):
                return  # Tìm thấy giải pháp hợp lệ đầu tiên thì thoát
            
            else:
                # Đặt lại các ô để kiểm tra sự kết hợp tiếp theo
                for index, value in zip(remaining_indices, combo):
                    grid[index[0]][index[1]] = '_'
        
        print("No valid solutions found.")
        
    def resetFgrid(grid): # Chuyển F lại thành '_'
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 'F':
                    grid[i][j] = '_'
            
    def solveBruteFore(grid):
        processBruteFore(grid)
        resetFgrid(grid)
        return grid

def backtracking(grid):
    """ Implement a backtracking solution """
    # This is a placeholder for the actual backtracking algorithm
    return grid

def print2D(cnf):
    for i in range(len(cnf)):
        print(cnf[i])
        print()

def run_tests(grid):
    """ Run tests on various grid sizes """
    test_cases = [
        (grid, 4),
        # Add more test cases with varying sizes
    ]
    results = {}
    for grid, n in test_cases:
        # print(n)
        
        cnf, var_map, n, m = generateCNF(grid)
        
        sat_solution = solveCNF(grid, cnf, var_map, n, m)
        results[(tuple(map(tuple, grid)), n)] = sat_solution
    return results

if __name__ == "__main__":
    test_results = run_tests(grid)
    for test_case, result in test_results.items():
        print("Test Case:", test_case)
        print("SAT Solver Solution:", result)
    
    
