### define a matrix first
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


### count the total number of empty cells relatived to particular cell
### ie. for variable X[row,col], count the empty cells in this row, this col and the sub-square
### this is used for degree heuristic
def emptycells(row,col):
    empty = 0
    ## row
    for j in range(0,9):
        if (matrix[row][j] == 0):
            empty +=1
    ## col
    for i in range(0,9):
        if (matrix[i][col] == 0):
            empty +=1
    ### check sub-square constraints
    first_row = (row//3)*3
    first_col = (col//3)*3
    last_row = (row//3)*3+3
    last_col = (col//3)*3+3
    for i in range(first_row,last_row):
        for j in range(first_col,last_col):
            if (matrix[i][j] == 0):
                empty +=1
    return empty

### compare 2 empty cells: A[a,b] and B[c,d]
### return the one having the most empty neighbours
### this is used for degree heuristic
def comparetries(a,b,c,d):
    ## a,b for one cell A
    ## c,d for other cell B
    emptycellsA = emptycells(a,b)
    emptycellsB = emptycells(c,d)
    if (emptycellsA > emptycellsB):
        return [a,b]
    else:
        return [c,d]

### To find an empty cell in the puzzle, if found, return the corresponding row and column, o.w. return [-1,-1]
### For those empty cells, return the cell which domain has least values, which is minimum-remaining-values heuristic
### If more than one empty cell has the minimum remaining values, use degree heuristic to selet
def EmptyCell():
    firsttry = []
    d = 9 ## number of remaining values
    for i in range(0,9):
        for j in range(0,9):
            if matrix[i][j] == 0:
                variables = domain(i,j)
                ### minimum-remaing-values heuristic
                if (len(variables) <= d):
                    if (len(variables) < d):
                        firsttry = [i,j]
                        d = len(variables)
                    else:
                        ### use degree heuristic to select variable with the same least remaing varibales
                        if (len(firsttry) != 0):
                            firsttry = comparetries(i,j,firsttry[0],firsttry[1])
                        else:
                            firsttry = [i,j]
    if (len(firsttry) == 0):
        return [-1,-1]
    else:
        return firsttry

## sort the values in a domain
def SortValues(row,col,values):
    ## count the number of neighbouring variables for which X will be eliminated from their domains because of this
    count = []
    for k in values:
        c = 0
        ## row
        for j in range(0,9):
            if (matrix[row][j] == 0):
                c += domain(row,j).count(k)
        ## col
        for i in range(0,9):
            if (matrix[i][col] == 0):
                c += domain(i,col).count(k)
        ### check sub-square constraints
        first_row = (row//3)*3
        first_col = (col//3)*3
        last_row = (row//3)*3+3
        last_col = (col//3)*3+3
        for i in range(first_row,last_row):
            for j in range(first_col,last_col):
                c += domain(i,j).count(k)
        count.append([c,k])
    ## sort the key by increasing order
    count.sort(key=lambda x: x[0])
    newvalues = []
    for i in range(len(count)):
        newvalues.append(count[i][1])
    return newvalues
    
        
### Give the domain for particular cell, based on exiting "assigned variables"
### This domain is used for forward checking
def domain(row,col):
    values = [1,2,3,4,5,6,7,8,9]
    for k in range(1,10):
        ### check row constraints
        for j in range(0,9):
            if (matrix[row][j] == k):
                if (values.count(k) != 0):
                    values.remove(k)
        ### check column constraints    
        for i in range(0,9):
            if (matrix[i][col] == k):
                if (values.count(k) != 0):
                    values.remove(k)
        ### check sub-square constraints
        first_row = (row//3)*3
        first_col = (col//3)*3
        last_row = (row//3)*3+3
        last_col = (col//3)*3+3
        for i in range(first_row,last_row):
            for j in range(first_col,last_col):
                if (matrix[i][j] == k):
                    if (values.count(k) != 0):
                        values.remove(k)
    return values

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
    dom = domain(row,col)
    ## sort the domain, least-constraining-value heuristic
    values = SortValues(row,col,dom)
    for k in values:
        matrix[row][col] = k
        global assign_variable
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
        ##outputfile = open("Output3.txt","a")
        ##outputfile.write(str(assign_avg)+'\n')
        ##outputfile.close()       
main()