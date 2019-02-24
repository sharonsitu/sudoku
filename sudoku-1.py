### define a empty matrix first
matrix = [
    [0,0,0,0,0,0,0,9,0],
    [0,0,0,0,0,0,0,0,8],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]]

### To find an empty cell in the puzzle, if found, return the corresponding row and column, o.w. return [-1,-1]
def EmptyCell():
    for i in range(0,9):
        for j in range(0,9):
            if matrix[i][j] == 0:
                cell = [i,j]
                return cell
    return [-1,-1]

### Check the constraints, if it is valid to assign the value to the cell, return True, ow. False
def ValidCell(row,col,value):
    ### check row constraints
    for j in range(0,9):
        if matrix[row][j] == value:
            return False
    ### check column constraints    
    for i in range(0,9):
        if matrix[i][col] == value:
            return False
    ### check sub-square constraints
    first_row = (row//3)*3
    first_col = (col//3)*3
    last_row = (row//3)*3+3
    last_col = (col//3)*3+3
    for i in range(first_row,last_row):
        for j in range(first_col,last_col):
            if matrix[i][j] == value:
                return False
    return True

### print the sudoku result
def PrintSudoku():
    for value in matrix:
        print(value)

### To count how many variables have been assigned        
assign_variable = 0

### solve the sudoku with backtracking
def sudoku():
    cell = EmptyCell()
    if cell[0] == -1:
        ##PrintSudoku()
        return True
    row = cell[0]
    col = cell[1]
    for k in range(1,10):
        global assign_variable  
        if ValidCell(row,col,k):                 
            matrix[row][col] = k
            assign_variable += 1
            if (assign_variable > 10000):
                return False             
            complet = sudoku()
            if (complet): return True
            matrix[row][col] = 0    
    return False

def main():
    ### try all instances ###
    ##for i in range(1,72):
        assign = 0
        for k in range(1,11): 
            path = './sudoku_problems/'+ str(1) + '/'+ str(k) + '.sd'
            word_index = 0
            file = open(path,'r')
            for i in range (0,9):
                token_index = 0
                values = file.readline().split()
                for j in range (0,9):
                    value = int(values[token_index])
                    matrix[i][j] = value
                    token_index += 1
            file.close()             
            if sudoku():
                global assign_variable
                assign += assign_variable
                print(assign_variable)
            else:
                print("no solution")
            assign_variable = 0
        assign_avg = assign/10
        outputfile = open("Output1.txt","a")
        outputfile.write(str(assign_avg)+'\n')
        ##outputfile.close()       
    
main()            