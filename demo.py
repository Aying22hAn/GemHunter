from pysat.solvers import Glucose3
from pysat.formula import CNF

# Xây dựng mệnh đề ràng buộc (CNF)
cnf = CNF()
cnf.append([-1, -2])
cnf.append([-1, -3]) 
cnf.append([-1, -4]) 
cnf.append([-2, -3])
cnf.append([-2, -4])
cnf.append([-3, -4])
cnf.append([1, 2, 3, 4])

# cnf.append([1, 5]) -8, -12])
cnf.append([2, -4, -6, 8, -12])
cnf.append([2, -4, -6, -8, 12])
cnf.append([-2, 4, 6, -8, -12])
cnf.append([-2, 4, -6, 8, -12])
cnf.append([-2, 4, -6, -8, 12])
cnf.append([-2, -4, 6, 8, -12])
cnf.append([-2, -4, 6, -8, 12])
cnf.append([-2, -4, -6, 8, 12])
cnf.append([5, 6, 9])
cnf.append([6, -8, -12])
cnf.append([-6, 8, -12])
cnf.append([-6, -8, 12])




solver = Glucose3()
solver.append_formula(cnf.clauses)
if solver.solve():
    print("Satisfiable!")
    # In ra tất cả các model khác nhau
    while solver.solve():
        model = solver.get_model()
        print("Model:", model)
        solver.add_clause([-literal for literal in model]) 
else:
    print("Unsatisfiable!")
    
    