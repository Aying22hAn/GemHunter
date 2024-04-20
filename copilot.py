from sympy.logic.boolalg import to_cnf
from sympy.abc import symbols

def minesweeper_to_cnf(grid):
    """
    Chuyển đổi mảng thông tin Minesweeper thành CNF.

    Args:
        grid (list[list[Union[int, str]]]): Mảng thông tin Minesweeper. Mỗi ô chứa số lượng mìn xung quanh hoặc '_'.

    Returns:
        list[str]: Danh sách các mệnh đề CNF biểu diễn ràng buộc.
    """
    n = len(grid)
    cnf_clauses = []

    for i in range(n):
        for j in range(n):
            cell = grid[i][j]
            if isinstance(cell, int):
                neighbors = []
                for r in range(max(0, i - 1), min(n, i + 2)):
                    for c in range(max(0, j - 1), min(n, j + 2)):
                        if (r, c) != (i, j):
                            neighbors.append(symbols[f"x_{r}_{c}"])
                cnf_clauses.append(to_cnf(neighbors, True) if cell > 0 else to_cnf(neighbors, False))

    return cnf_clauses

# Example usage:
minesweeper_grid = [
    [3, "_", 2, "_"],
    ["_", "_", 2, "_"],
    ["_", 3, 1, "_"],
]

cnf_clauses = minesweeper_to_cnf(minesweeper_grid)
for clause in cnf_clauses:
    print(clause)
