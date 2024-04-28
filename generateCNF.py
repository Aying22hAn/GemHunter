from itertools import combinations

def readFile(filename):
    array = []
    
    with open(filename, 'r') as file:
        for line in file:
            # Split the line into elements based on comma
            elements = line.split(',')
            # Remove spaces from each element and add to the array
            array.append([element.strip() for element in elements])
            
    return array


def writeArrayToFile(array, filename):
    with open(filename, 'w') as file:
        for row in array:
            line = ' '.join(row)
            file.write(line + '\n')
    file.close()
    
def printArray(array):
    for row in array:
        print(row)
    
def markTraps(array):
    trapNum = [[0] * len(array[0]) for _ in range(len(array))]
    count = 0
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == '_':
                count += 1
                trapNum[i][j] = count
                
    return trapNum

def getSurround(array, trapNum, i, j):
    surrounded = []
    for x in range(i-1, i+2):
        for y in range(j-1, j+2):
            if x >= 0 and x < len(array) and y >= 0 and y < len(array[0]):
                if array[x][y] == '_':
                    surrounded.append(trapNum[x][y])
    return surrounded
                    
            
def generateCNF(array, trapNum):
    kb = []
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] != '_': 
                surrounded = getSurround(array, trapNum, i, j)
                if len(surrounded) == int(array[i][j]):
                    for trap in surrounded:
                        if [trap] not in kb:
                            kb.append([trap])
                else:
                    # At least one variable in the combinations is not mine 
                    # Because the number K = the number of mine surrounding the cell + 1
                    atLeastOneNotMine = list(combinations(surrounded, int(array[i][j]) + 1))
                    for n in range(len(atLeastOneNotMine)):
                        clause = [x * -1 for x in atLeastOneNotMine[n]]
                        if clause not in kb:
                            kb.append(clause)
                    
                    # At least one variable in the combinations is mine
                    # Because the number K = the number of cell, surrounding the cell, can not be mine + 1
                    atLeastOneIsMine = list(combinations(surrounded, len(surrounded) - int(array[i][j]) + 1))
                    for n in range(len(atLeastOneIsMine)):  
                        clause = list(atLeastOneIsMine[n])
                        if clause not in kb:
                            kb.append(clause)
                            
    return kb
                             
                            
def solveByPySAT(array, kb):
    from pysat.solvers import Solver
    solver = Solver(name='Glucose3')
    for clause in kb:
        solver.add_clause(clause)
    if solver.solve():
        return solver.get_model()
    else:
        return None
                                 
def showSolution(array, solution, trapNum):
    
    showArray = array.copy()
    for var in solution:
        for i in range(len(trapNum)):
            for j in range(len(trapNum[0])):
                if trapNum[i][j] == abs(var):
                    if var > 0:
                        showArray[i][j] = 'T'
                    else:
                        showArray[i][j] = 'G'
                        
    with open(filename, 'w') as file:
        for i in range(len(showArray)):
            for j in range(len(showArray[0])):
                file.write(showArray[i][j] + ', ')
            file.write('\n')


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

def showSolution2(filename, array, solution, trapNum): 
    showArray = array.copy()
    for i in range(len(trapNum)):
            for j in range(len(trapNum[0])):
                if trapNum[i][j] != 0:
                    if(solution[trapNum[i][j]]):
                        showArray[i][j] = 'T'
                    else:
                        showArray[i][j] = 'G'
                        
    with open(filename, 'w') as file:
        for i in range(len(showArray)):
            for j in range(len(showArray[0])):
                file.write(showArray[i][j] + ', ')
            file.write('\n')
        
        
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
                 
                 
                 
'''Main function''' 
def main():
    array = readFile("input.txt")
    # writeArrayToFile(array, "output.txt")
    
    trapNum = markTraps(array)
    kb = generateCNF(array, trapNum)
    
    # #PySAT solution
    # pySatSolution = solveByPySAT(array, kb)
    # showSolution("output.txt", array, pySatSolution, trapNum)
    
    # #Brute force solution
    # brute_force_Solution = brute_force(kb)
    # showSolution2("output.txt", array, brute_force_Solution, trapNum)
    
    #Backtracking solution
    variables = extract_variables(kb)
    backTrackingSolution = backtracking({}, variables, kb)
    showSolution2("output.txt", array, backTrackingSolution, trapNum) 
    
    
if __name__ == "__main__":
    main()