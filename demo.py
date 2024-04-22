from pysat.solvers import Glucose3

def solve_knapsack(values, weights, capacity):
    num_items = len(values)

    # Create a SAT solver instance
    solver = Glucose3()

    # Create boolean variables for each item
    items = [solver.new_var() for _ in range(num_items)]

    # Add constraints: each item can be either selected or not
    for item in items:
        solver.add_clause([item])
        solver.add_clause([-item])

    # Add constraint: total weight of selected items cannot exceed capacity
    for i in range(num_items):
        solver.add_clause([-items[i]] + [items[j] for j in range(num_items) if j != i])

    # Add constraint: total value of selected items should be maximized
    objective = [values[i] * items[i] for i in range(num_items)]
    solver.add_clause(objective)

    # Solve the SAT problem
    if solver.solve():
        # Get the selected items
        selected_items = [i for i in range(num_items) if solver.model[i] > 0]
        return selected_items
    else:
        return []

# Example usage
values = [10, 20, 30, 40]
weights = [1, 2, 3, 4]
capacity = 6

selected_items = solve_knapsack(values, weights, capacity)
print("Selected items:", selected_items)