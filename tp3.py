#################################################
# tp3.py: nonogram.112 
# 
# Name: Farid Khuri-Makdisi
# andrew id: fkhurima
#################################################

# I've done my best to add comments to explain the complex functions used in generating the puzzles and such :) 

# credit to TA Aaron for helping me edit cmu_112_graphics
from cmu_112_graphics import*
import math, string, copy, random, itertools

##################################
# Main App:
##################################

def appStarted(app):    
    app.mode = 'splashScreenMode' 
    app._root.resizable(False, False)
    app._root.title("nonogram.112")     
    restartSplashScreen(app)
    restartPlay(app)
    restartPlayWithColor(app)
    restartCreate(app)
    restartCreateWithColors(app)
    restartNonorikabe(app)

##################################
# Debugging Helpers:
##################################

# from https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
def maxItemLength(a):
    maxLen = 0
    for row in range(len(a)):
        for col in range(len(a[row])):
            maxLen = max(maxLen, len(repr(a[row][col])))
    return maxLen

def print2dList(a):
    if a == []:
        print([])
        return
    print()
    rows, cols = len(a), len(a[0])
    maxCols = max([len(row) for row in a])
    fieldWidth = max(maxItemLength(a), len(f'col={maxCols-1}'))
    rowLabelSize = 5 + len(str(rows-1))
    rowPrefix = ' '*rowLabelSize+' '
    rowSeparator = rowPrefix + '|' + ('-'*(fieldWidth+3) + '|')*maxCols
    print(rowPrefix, end='  ')
    # Prints the column labels centered
    for col in range(maxCols):
        print(f'col={col}'.center(fieldWidth+2), end='  ')
    print('\n' + rowSeparator)
    for row in range(rows):
        # Prints the row labels
        print(f'row={row}'.center(rowLabelSize), end=' | ')
        # Prints each item of the row flushed-right but the same width
        for col in range(len(a[row])):
            print(repr(a[row][col]).center(fieldWidth+1), end=' | ')
        # Prints out missing cells in each column in case the list is ragged
        missingCellChar = chr(10006)
        for col in range(len(a[row]), maxCols):
            print(missingCellChar*(fieldWidth+1), end=' | ')
        print('\n' + rowSeparator)
    print()

##################################################################################################################
# SplashScreen mode: modes adapted from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes
##################################################################################################################

def restartSplashScreen(app):
# splashScreen attributes
    app.gameModeList = [['play', 'gray79'], 
                        ['play_with_colors', 'gray79'], 
                        ['create', 'gray79'], 
                        ['create_with_colors', 'gray79'], 
                        ['nonorikabe', 'gray79']]

    # if i add the png -> nonogram feature, it's here
    #['image', 'gray79']
    app.helpColor = 'gray79'

def splashScreenMode_mousePressed(app, event):
    # if inside box, change box color
    for i in range(len(app.gameModeList)):
        if (app.width/2 - 135 < event.x < app.width/2 + 135 and
            (300 + i * 60) - 24 < event.y < (300 + i * 60) + 24):
            app.gameModeList[i][1] = 'gray60'

    # help screen
    if (app.width - 50 - 75 < event.x < app.width - 50 + 5 and
         10 < event.y < 50):
         app.helpColor = 'gray60'

# go to game mode
def splashScreenMode_mouseReleased(app, event):
    for i in range(len(app.gameModeList)):
        if (app.width/2 - 135 < event.x < app.width/2 + 135 and
            (300 + i * 60) - 24 < event.y < (300 + i * 60) + 24):
            app.mode = f'{app.gameModeList[i][0]}'
        app.gameModeList[i][1] = 'gray79'
    # help screen
    if (app.width - 50 - 75 < event.x < app.width - 50 + 5 and
         10 < event.y < 50):
         app.mode = 'helpScreen'
         app.helpColor = 'gray79'
        
def splashScreenMode_redrawAll(app, canvas):
    titleFont = 'Cambria 40 bold'
    boxFont = 'Cambria 23 bold'
    helpFont = 'Cambria 20 bold'
    # title
    canvas.create_text(app.width/2, 0, text='nonogram.112', font=titleFont, anchor = 'n')
    # gamemodes
    for i in range(len(app.gameModeList)):
        canvas.create_rectangle(app.width/2 - 135, (300 + i * 60) - 24, app.width/2 + 135, (300 + i * 60) + 24, 
                                fill = app.gameModeList[i][1], width = 3)
        name = (app.gameModeList[i][0]).replace('_', ' ')
        canvas.create_text(app.width/2, 300 + i*60, text=name, font=boxFont)
    # help
    canvas.create_rectangle(app.width - 50 - 75, 10, app.width - 50 + 5, 50, 
                                fill = app.helpColor, width = 3)
    canvas.create_text(app.width - 50 , 30, text="help?", font=helpFont, anchor = 'e')

##########################################################
# 'helpScreen' mode: (how to play, what the features are, some nice graphics)
##########################################################

def helpScreen_redrawAll(app, canvas):
    canvas.create_text(app.width/2, 0, anchor = 'n', text =
    
     '''
     Nonograms are Japanese logic puzzles. The base rules are simple. Each row and column of a grid must be 
     shaded according to clues. Each clue is comprised of numbers. In their order of appearance, there must 
     be an island of length equal to each clue number. For black and white nonograms, these islands must be 
     separated by at least one space. For color nonograms, islands of different colors may touch.

     For example, here is a legal row for each variant:







    nonogram.112 also allows you to create boards as well and checks whether they're unique.
    
    The "nonorikabe" variant I created has the same rules, but some clues are blurred out 
    and the numbers inside the grid indicate the size of each "pool" of blank spaces in the solution. They 
    appear at the most northern, then most western point of each "pool". 

    have fun :> ! -farid
    ''',
     
      font = 'Cambria 20' )

    for i in range(2):
        canvas.create_rectangle(200 + 50 + 500*i, 300, 200 + 150 + 500*i, 350, width = 4)
        if i == 0:
            canvas.create_text((200 + 50 + 500*i + 200 + 150 + 500*i)/2, 325, text = '3  1', font = 'Arial 26 bold')
        elif i == 1:
            canvas.create_text((200 + 50 + 500*i + 200 + 150 + 500*i)/2 - 5, 325, text = '3   ', font = 'Arial 26 bold', fill = 'orange')
            canvas.create_text((200 + 50 + 500*i + 200 + 150 + 500*i)/2 + 20 , 325, text = '1', font = 'Arial 26 bold', fill = 'deep sky blue')
        for j in range(5):
            canvas.create_rectangle(200 + 150 + 500*i + 50*j,300, 200 + 150 + 500*i + 50*(j+1),350, width = 4 )
            if i == 0:
                if j != 3:
                    canvas.create_rectangle(200 + 150 + 500*i + 50*j + 5 ,300 + 5, 200 + 150 + 500*i + 50*(j+1) - 5 ,350 - 5, fill = 'black')
                else:
                    canvas.create_text((200 + 150 + 500*i + 50*j + 200 + 150 + 500*i + 50*(j+1))/2  ,325, text = 'X', fill = 'red', font = 'Arial 26 bold')
            elif i == 1:
                if j < 3:
                    canvas.create_rectangle(200 + 150 + 500*i + 50*j + 5 ,300 + 5, 200 + 150 + 500*i + 50*(j+1) - 5 ,350 - 5, fill = 'orange', width = 0)
                elif j == 3:
                    canvas.create_rectangle(200 + 150 + 500*i + 50*j + 5 ,300 + 5, 200 + 150 + 500*i + 50*(j+1) - 5 ,350 - 5, fill = 'deep sky blue', width = 0)
                elif j == 4:
                    canvas.create_text((200 + 150 + 500*i + 50*j + 200 + 150 + 500*i + 50*(j+1))/2  ,325, text = 'X', fill = 'red', font = 'Arial 26 bold')
    canvas.create_text(app.width/2, app.height, anchor = 's', text =
    
     '''
     press enter to return to main menu     
     ''',
     
      font = 'Cambria 20 bold' )

def helpScreen_keyPressed(app, event):
    if event.key == 'Enter':
        app.mode = 'splashScreenMode'

#####################################
# 'play' mode: (random b/w generator) 
#####################################
def restartPlay(app):
# play attributes
    app.BWSize = 5
    app.BWSolvedGrid = generateSolvedBWGrid(app.BWSize)
    # for numbers on edges
    app.BWHorizontalIslands = BWcountHorizontalIslands(app.BWSolvedGrid)
    app.BWVerticalIslands = BWcountVerticalIslands(app.BWSolvedGrid)
    # for drawing
    app.BWSolverGrid = [([False] * app.BWSize) for row in range(app.BWSize)]
    app.BWTopHeightMargin = 1350 * (1 / app.BWSize)
    app.BWBottomHeightMargin = 500 * (1 / app.BWSize)
    app.BWWidthMargin = (app.width / 2 - app.BWTopHeightMargin) / 1.9
    
    # keeping score
    app.BWTime = 0.0
    app.BWSessionBest = [0.0] * (4)
    app.BWSolved = False

    app.BWSubmissionMessage = ''
    app.BWSubmissionMessageColor = 'red'
    app.BWSubmitButtonMessage = 'submit'
    app.BWReturnColor = 'gray79'
    app.BWSubmitColor = 'gray79'

# generates a random unique grid of Booleans: True = Shaded and False = Space, islands are shaded cells, and pools are spaces
def generateSolvedBWGrid(size):
    result = [([False] * size) for row in range(size)]
    totalSquares = 0
    for row in range(size):
        totalLength = 0 
        # maybe start off with spaces
        totalLength += random.randrange(0, size - 1, 1)
        while totalLength < size:
            # make a new island
            if totalLength < size - 1:
                newIslandLength = random.randrange(1, size - totalLength, 1)
                totalSquares += newIslandLength
            # if we're at the edge, we can only make a cell
            elif totalLength == size - 1:
                newIslandLength = random.randint(0, 1)
                totalSquares += newIslandLength
            # shade all squares in island
            for square in range(0, newIslandLength):
                    result[row][square + totalLength] = True
            # maybe add a bunch of spaces after an island, at least 1
            totalLength += newIslandLength + 1
            if totalLength < size - 1:
                totalLength += random.randrange(1, size - totalLength, 1)
            else:
              totalLength += 1
    # add squares until we have good density (this is one of the ways I guarantee uniqueness)
    if size == 5:
        if totalSquares < ((size ** 2) // 2) + 1:
            while totalSquares < ((size ** 2) // 2) + 1:
                row, col = random.randrange(0, size), random.randrange(0, size)
                if result[row][col] == False:
                    result[row][col] = True
                    totalSquares += 1
    elif size == 10:
        if totalSquares < ((size ** 2) // 2) + 10:
            while totalSquares < ((size ** 2) // 2) + 10:
                row, col = random.randrange(0, size), random.randrange(0, size)
                if result[row][col] == False:
                    result[row][col] = True
                    totalSquares += 1
            return result
    elif size == 15:
        if totalSquares < ((size ** 2) // 2) + 25:
            while totalSquares < ((size ** 2) // 2) + 20:
                row, col = random.randrange(0, size), random.randrange(0, size)
                if result[row][col] == False:
                    result[row][col] = True
                    totalSquares += 1
            return result
    elif size == 20:
        if totalSquares < ((size ** 2) // 2) + 38:
            while totalSquares < ((size ** 2) // 2) + 30:
                row, col = random.randrange(0, size), random.randrange(0, size)
                if result[row][col] == False:
                    result[row][col] = True
                    totalSquares += 1
            return result
    if BWUnique(result) == True: # check for uniqueness: for 5x5 I bruteforce, and I check for density for greater
        return result
    else:
        # if the solution is not unique, generate a new grid 
        return generateSolvedBWGrid(size)

# for a row of clues, returns the possible island configs (only fast enough for 5x5)
def BWPotentialRowShifts(row, size):
    if size >= 10:
        return
    maxSpacing = size - sum(row)
    badShifts = [[] for row in range(maxSpacing)] 
    for i in range(maxSpacing):
        row.append(False)
    # makes all possible permutations, so 1x3, x13, 31x, 3x1, 
    # I wish I found a better way to do this for all grid sizes~ but all my puzzles are unique so it's okay
    badShifts = [list(permutation) for permutation in itertools.permutations(row)]
    lengthOfShift = len(badShifts[0])
    # removes duplicates
    shifts = []
    for shift in badShifts:
        if shift not in shifts:
            shifts.append(shift)
    # remove things not in order
    for shift in copy.deepcopy(shifts):
        index = 0
        for elem in range(len(shift)):
            # if number
            if shift[elem] != False:
                # if number not in row clue order
                if row[index] != shift[elem]: 
                    if shift in shifts:
                        shifts.remove(shift)
                index += 1
    # removes permutations with consecutive numbers like 13x 
    for shift in copy.deepcopy(shifts):
        for i in range(lengthOfShift - 1):
            if shift[i] in shift and shift[i+1] in shift and (shift[i] != False and shift[i+1] != False):
                if shift in shifts:
                    shifts.remove(shift)
    # makes them into booleans so it returns TTTFT TFTTT
    for shift in copy.deepcopy(shifts):
        fullShift = []
        for elem in range(len(shift)):
            if shift[elem] == False:
                fullShift.append(False)
            if shift[elem] != False:
                for i in range(shift[elem]):
                    fullShift.append(True)
        shifts.append(fullShift)
        shifts.remove(shift)
    return shifts

# from the last function, makes all possible grids of possible configs
def BWPotentialSolutionListMaker(rowClues):
    size = len(rowClues)
    rowDict = dict() # all permutations of each row are in here DICT
    numberOfRowSols = []
    solutions = []
    for row in range(size):
        rowDict[row] = (BWPotentialRowShifts(rowClues[row], size))
        numberOfRowSols.append(range(len(rowDict[row])))
    # this is a list of all lists [0,0,0,0,0] - > [len(rowsol1),... ]
    # i had to look up how to do that efficiently 
# from https://stackoverflow.com/questions/10975045/python-return-combinations-of-a-list-of-ranges/10975088
    numberOfRowSolsPermutations = list(itertools.product(*numberOfRowSols))
    for permutation in numberOfRowSolsPermutations:
        generated = []
        for i in range(len(permutation)):
            generated.append(rowDict[i][permutation[i]])
        solutions.append(generated)
    return solutions

# checks how many solutions there are, and returns True if there's just 1
def BWUnique(grid):
    size = len(grid)
    # for larger grid sizes, I'm 99.999% sure boards are unique
    if size >= 10:
        totalSquares = 0
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == True:
                    totalSquares += 1
    if size == 10:
        return totalSquares >= ((size ** 2) // 2) + 10
    elif size == 15:
        return totalSquares >= ((size ** 2) // 2) + 25
    elif size == 20:
        return totalSquares > ((size ** 2) // 2) + 38
    # for 5x5
    rowClues = BWcountHorizontalIslands(grid)
    colClues = BWcountVerticalIslands(grid)
    potentialSolutions = BWPotentialSolutionListMaker(rowClues) 
    actualSolutions = []
    for sol in potentialSolutions:
        if BWcountVerticalIslands(sol) == colClues:
            actualSolutions.append(sol)
    return len(actualSolutions) == 1

# recursively return the counts for each island in each row (very cool)
def BWcountHorizontalIslands(grid):
    #app.BWSolvedGrid

    numbers = []
    for row in range(len(grid)):
         numbers.append(BWcountHorizontalIslandsHelper(grid[row], []))
    return numbers

# recursive helper
def BWcountHorizontalIslandsHelper(solvedGridRow, result):
    if solvedGridRow == []:
        return result
    else:
        counter = 0
        if solvedGridRow[0] == True and isinstance(solvedGridRow[0], bool):
            i = 0
            while 0 <= i < len(solvedGridRow) and solvedGridRow[i] == True and isinstance(solvedGridRow[i], bool):
                counter += 1
                i += 1
            result.append(counter)
            return BWcountHorizontalIslandsHelper(solvedGridRow[counter + 1:], result)
        else:
            return BWcountHorizontalIslandsHelper(solvedGridRow[1:], result)

# recursively return the counts for each island in each col, same as rows, but from a transposed copy (also very cool)
def BWcountVerticalIslands(grid):
    flipList = copy.deepcopy(grid)
    transposed = transpose(flipList)
    numbers = []
    for row in range(len(transposed)):
         numbers.append(BWcountHorizontalIslandsHelper(transposed[row], []))
    return numbers

# flips rows n cols
def transpose(L):
    result = []
    for col in range(len(L[0])):
        newRow = []
        for row in range(len(L)):
            newRow.append(L[row][col])
        result.append(newRow)
    return result            

# draw/remove a square or an x or select a menu option
def play_mousePressed(app, event):
    # left click, vs right click to draw an x
    # if i click on a box ..
    # submission attempt
    if ((4/5)*app.width - 60 < event.x < (4/5)*app.width + 60 and
        app.height/3 - 100 - 20 < event.y < app.height/3 - 100 + 20):
        app.BWSubmitColor = 'gray60'
    # return to main menu
    elif ( (4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
    app.height/3 + 150 - 20 < event.y < app.height/3 + 150 + 20):
        app.BWReturnColor = 'gray60'

    elif getCell(app, event.x, event.y) != None:
        row, col = getCell(app, event.x, event.y)
        if 0 <= row < app.BWSize and 0 <= col < app.BWSize:
            # draw square if click on empty
            if app.BWSolverGrid[row][col] == False:
                app.BWSolverGrid[row][col] = True
            # remove square if click on square
            elif app.BWSolverGrid[row][col] == True:
                app.BWSolverGrid[row][col] = False
            # remove x if click on x
            elif app.BWSolverGrid[row][col] == 'X':
                app.BWSolverGrid[row][col] = False

# after correct submission click 1
def submittedOnce(app):
    app.BWSubmissionMessage = 'complete! press enter again to refresh'
    app.BWSubmitButtonMessage = 'new'
    app.BWSubmissionMessageColor = 'green'
    app.BWSolved = True
    if app.BWTime < app.BWSessionBest[app.BWSize // 5 - 1] or app.BWSessionBest[app.BWSize // 5 - 1] == 0.0:
        app.BWSessionBest[app.BWSize // 5 - 1] = app.BWTime
    app.BWTime = 0

#after correct submission click 2
def submittedTwice(app):
    app.BWSolved = False
    app.BWTime = 0
    app.BWSolvedGrid = generateSolvedBWGrid(app.BWSize)
    app.BWHorizontalIslands = BWcountHorizontalIslands(app.BWSolvedGrid)
    app.BWVerticalIslands = BWcountVerticalIslands(app.BWSolvedGrid)
    app.BWSolverGrid = [([False] * app.BWSize) for row in range(app.BWSize)]
    app.BWSubmissionMessage = ''

# for box selection highlighting
def play_mouseReleased(app, event):
    # submit
    if ((4/5)*app.width - 60 < event.x < (4/5)*app.width + 60 and
        app.height/3 - 100 - 20 < event.y < app.height/3 - 100 + 20 and
        app.BWSolved == False):
        if solverMatchesSolved(app.BWSolverGrid, app.BWSolvedGrid):
                submittedOnce(app)
                app.BWSubmitColor = 'gray79'
            # counter stop
        else:
            app.BWSubmissionMessage = 'solution is incomplete or incorrect'
            app.BWSubmissionMessageColor = 'red'
            app.BWSubmitColor = 'gray79'
    elif ((4/5)*app.width - 60 < event.x < (4/5)*app.width + 60 and
        app.height/3 - 100 - 20 < event.y < app.height/3 + 100 + 20 and
        app.BWSolved == True):
            submittedTwice(app)
            app.BWSubmitColor = 'gray79'
    # return
    elif ( (4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
    app.height/3 + 150 - 20 < event.y < app.height/3 + 150 + 20):
        app.mode = 'splashScreenMode'
        app.BWReturnColor = 'gray79'

# draw x'es
def play_rightMousePressed(app, event):
    if getCell(app, event.x, event.y) != None:
            row, col = getCell(app, event.x, event.y)
            if 0 <= row < app.BWSize and 0 <= col < app.BWSize:
                # right click empty -> x
                if app.BWSolverGrid[row][col] == False:
                    app.BWSolverGrid[row][col] = 'X'
                # right click shaded -> x
                elif app.BWSolverGrid[row][col] == True:
                    app.BWSolverGrid[row][col] = 'X'
                # right click x -> empty
                elif app.BWSolverGrid[row][col] == 'X':
                    app.BWSolverGrid[row][col] = False
                
# keep drawing squares 
def play_mouseDragged(app, event):
    if getCell(app, event.x, event.y) != None:
            row, col = getCell(app, event.x, event.y)
            if 0 <= row < app.BWSize and 0 <= col < app.BWSize:
                # draw square if click on empty or X
                if app.BWSolverGrid[row][col] == 'X':
                    app.BWSolverGrid[row][col] = True
                elif app.BWSolverGrid[row][col] == False:
                    app.BWSolverGrid[row][col] = True
                
# keep drawing x'es
def play_rightMouseDragged(app, event):
    if getCell(app, event.x, event.y) != None:
            row, col = getCell(app, event.x, event.y)
            if 0 <= row < app.BWSize and 0 <= col < app.BWSize:
                # right click empty -> x
                if app.BWSolverGrid[row][col] == False:
                    app.BWSolverGrid[row][col] = 'X'
                # right click shaded -> x
                elif app.BWSolverGrid[row][col] == True:
                    app.BWSolverGrid[row][col] = 'X'

# adapted from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
# if you click a square 
def getCell(app, x, y):
    cellW = (app.height - 2*app.BWWidthMargin) / app.BWSize
    cellH = (app.height - app.BWTopHeightMargin - app.BWBottomHeightMargin ) / app.BWSize
    if  (app.BWWidthMargin < x < app.width - app.BWWidthMargin
        and app.BWTopHeightMargin < y < app.height - app.BWBottomHeightMargin):
        row = int((y - app.BWTopHeightMargin) / cellH)
        col = int((x - app.BWWidthMargin) / cellH)
        return row, col
    else:
        return None

# adapted from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
def getCellBounds(app, row, col):
    cellW = (app.height - 2*app.BWWidthMargin)/app.BWSize
    cellH = (app.height - app.BWTopHeightMargin - app.BWBottomHeightMargin )/app.BWSize
    x0 = app.BWWidthMargin + col*cellH
    y0 = app.BWTopHeightMargin + row*cellH
    x1 = x0 + cellH
    y1 = y0 + cellH
    return (x0, y0, x1, y1)

# draws the squares / x'es inputted by users
def drawSolverBWGrid(app, canvas):
    for row in range(app.BWSize):
        for col in range(app.BWSize):
            if 0 <= row < len(app.BWSolverGrid) and 0 <= col < len(app.BWSolverGrid[0]):
                if app.BWSolverGrid[row][col] == True:
                    (BWx0, BWx1, BWy0, BWy1) = getSquareBounds(app, row, col)
                    canvas.create_rectangle(BWx0, BWx1, 
                                            BWy0, BWy1,
                                            fill = 'black')
                elif app.BWSolverGrid[row][col] == 'X':
                    x0, y0, x1, y1 = getCellBounds(app, row, col)
                    canvas.create_text((x0 + x1)/2, 
                                        (y0 + y1)/2, 
                                        text = 'X', fill = 'red', 
                                        font = f'Arial { (36 * 5) // app.BWSize } bold')
                elif app.BWSolverGrid[row][col] == False:
                    pass

# tiny part of this was adapted from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
# draw the empty grid with the number clues
def drawVisibleBWGrid(app, canvas):
    if app.BWSize < 11:
        gridWidth = 4
    else:
        gridWidth = 2
    # determine longest row clue:
    longestRow = 0
    for row in range(len(app.BWHorizontalIslands)):
        counter = 0
        for clue in range(len(app.BWHorizontalIslands[row])):
            counter += 1
        if counter >= longestRow:
            longestRow = counter
    # determine longest column clue
    longestCol = 0
    for row in range(len(app.BWVerticalIslands)):
        counter = 0
        for clue in range(len(app.BWVerticalIslands[row])):
            counter += 1
        if counter >= longestCol:
            longestCol = counter
    # draw grid
    for row in range(app.BWSize):
        for col in range(app.BWSize):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, width = gridWidth)
    # draw row clues
    for row in range(len(app.BWHorizontalIslands)):
        x0, y0, x1, y1 = getCellBounds(app, row, 0)
        canvas.create_rectangle(x0 - longestRow * (x1 - x0), y0, x0, y1, width = gridWidth)
        s = ''
        if app.BWHorizontalIslands[row] == []:
            s += '0'
        else:
            for clue in range(len(app.BWHorizontalIslands[row])):
                s += str(app.BWHorizontalIslands[row][clue])
                s += '  '    
        canvas.create_text((x0 - longestRow * (x1 - x0) + x0)/2, (y0 + y1)/2,
                            text = s, font = f'Arial {(50 * 5) // app.BWSize} bold')
    # draw col clues
    for row in range(len(app.BWVerticalIslands)):
        x0, y0, x1, y1 = getCellBounds(app, 0, row)
        canvas.create_rectangle(x0, y0 - longestCol * (y1 - y0), x1, y0, width = gridWidth)
        s = ''
        if app.BWVerticalIslands[row] == []:
            s += '0'
            s += '\n'
        else:
            for clue in range(len(app.BWVerticalIslands[row])):
                s += str(app.BWVerticalIslands[row][clue])
                s += '\n'    
        canvas.create_text((x0 + x1)/2, ((y0 - longestCol * (y1 - y0)) + y0 )/2 + 140 // app.BWSize,
                            text = s, font = f'Arial {(50 * 5) // app.BWSize} bold')

# drawn square bounds (inside each cell)
def getSquareBounds(app, row, col):
    cellW = (app.height - 2*app.BWWidthMargin)/app.BWSize
    cellH = (app.height - app.BWTopHeightMargin - app.BWBottomHeightMargin )/app.BWSize
    x0, y0, x1, y1 = getCellBounds(app, row, col)
    if app.BWSize == 20:
        x0 += 0.18*cellH
        x1 -= 0.18*cellH
        y0 += 0.18*cellH
        y1 -= 0.18*cellH
    elif app.BWSize == 15:
        x0 += 0.15*cellH
        x1 -= 0.15*cellH
        y0 += 0.15*cellH
        y1 -= 0.15*cellH
    elif app.BWSize == 10:
        x0 += 0.1*cellH
        x1 -= 0.1*cellH
        y0 += 0.1*cellH
        y1 -= 0.1*cellH
    else:
        x0 += 0.07*cellH
        x1 -= 0.07*cellH
        y0 += 0.07*cellH
        y1 -= 0.07*cellH
    return x0, y0, x1, y1
    
# restart or change grid size or submit
def play_keyPressed(app, event):
    if event.key == 'r':
        app.BWSolved = False
        app.BWSolvedGrid = generateSolvedBWGrid(app.BWSize)
        app.BWHorizontalIslands = BWcountHorizontalIslands(app.BWSolvedGrid)
        app.BWVerticalIslands = BWcountVerticalIslands(app.BWSolvedGrid)
        app.BWSolverGrid = [([False] * app.BWSize) for row in range(app.BWSize)]
        app.BWSubmissionMessage = ''
        app.BWTime = 0
    # choose grid size
    elif event.key in string.digits:
        for i in range(1, 5):
            if int(event.key) == i:
                if app.BWSize != 5 *i: 
                    app.BWSize = 5 * i
                    app.BWSolved = False
                    app.BWSubmissionMessage = ''
                    app.BWTime = 0
                    app.BWSolverGrid = [([False] * app.BWSize) for row in range(app.BWSize)]
                    app.BWSolvedGrid = generateSolvedBWGrid(app.BWSize)
                    app.BWHorizontalIslands = BWcountHorizontalIslands(app.BWSolvedGrid)
                    app.BWVerticalIslands = BWcountVerticalIslands(app.BWSolvedGrid)
    elif event.key == 'Enter' and app.BWSolved != True:
        if solverMatchesSolved(app.BWSolverGrid, app.BWSolvedGrid):
            submittedOnce(app)
        else:
            app.BWSubmissionMessage = 'solution is incomplete or incorrect'
            app.BWSubmissionMessageColor = 'red'
    elif event.key == 'Enter' and app.BWSolved == True:
            submittedTwice(app)

#check if the input matches the generated solution
def solverMatchesSolved(solver, solved):
    counter = 0
    for row in range(len(solver)):
        for col in range(len(solver[0])):
            if solver[row][col] == True and solved[row][col] == False and isinstance(solver[row][col], bool) and isinstance(solved[row][col], bool):
                return False
            elif solver[row][col] == False and solved[row][col] == True and isinstance(solver[row][col], bool) and isinstance(solved[row][col], bool):
                return False
    return True
            
# keep a counter for each run
def play_timerFired(app):
    if app.BWSolved == False:
        app.BWTime += 0.1

# draws boxes for menu
def drawBWMenu(app, canvas):
    # back button to main mode, submit
    # display: size, score, correctness, best session time
    canvas.create_text((4/5)*app.width, app.height/3 - 180, 
                    text = f"{app.BWSize}x{app.BWSize}", 
                    font = 'Cambria 24 bold')

    canvas.create_text((4/5)*app.width, app.height/3 -150, 
                    text = f"{app.BWSubmissionMessage}", 
                    font = 'Cambria 18 bold', fill = app.BWSubmissionMessageColor)   

    canvas.create_rectangle((4/5)*app.width - 60, app.height/3 - 100 - 20, 
                            (4/5)*app.width + 60, app.height/3 -100 + 20,
                                fill = app.BWSubmitColor, width = 3)
    canvas.create_text((4/5)*app.width, app.height/3 - 100, 
                        text = "submit", 
                        font = 'Cambria 24 bold')   

    canvas.create_text((4/5)*app.width, app.height/3 - 20, 
                        text = "press 1-4 to change grid size \n         press enter to submit \n       press r for a new puzzle", 
                        font = 'Cambria 24 bold')
                    
    canvas.create_text((4/5)*app.width, app.height/3 + 70, 
                        text = f"session best: {round(app.BWSessionBest[app.BWSize // 5 - 1], 3)} \n latest time: {round(app.BWTime, 3)}", 
                        font = 'Cambria 24 bold')   


    canvas.create_rectangle((4/5)*app.width - 160, app.height/3 + 150 - 20, 
                            (4/5)*app.width + 160, app.height/3 + 150 + 20,
                                fill = app.BWReturnColor, width = 3)
    canvas.create_text((4/5)*app.width, app.height/3 + 150, 
                        text = f"return to main menu", 
                        font = 'Cambria 24 bold')   

def play_redrawAll(app, canvas):
    drawVisibleBWGrid(app, canvas)
    drawSolverBWGrid(app, canvas)
    drawBWMenu(app, canvas)

#####################################
# 'play_with_colors' mode: 
#####################################

# how is this different from b/w?
# make that a string app.ColorSet = [red, orange, yellow, green, purple] 
# generate unique BW board
# then randomize colors for each island so store the color as well
# then when you calculate rows n cols, make the number store the color as well
# menu also has a little palette 

def restartPlayWithColor(app):
    app.colorSet = ['orange', 'forest green', 'purple2', 'deep sky blue', 'firebrick2']
    app.colorSize = 5
    app.stillBWGrid = generateSolvedBWGrid(app.colorSize)
    app.colorGrid = randomizeIslandColor(app.stillBWGrid, app.colorSet)
    app.colorHorizontalIslands = colorCountHorizontalIslands(app.colorGrid )
    app.colorVerticalIslands = colorCountVerticalIslands(app.colorGrid)
   
    # for drawing
    app.colorSolverGrid = [([False] * app.colorSize) for row in range(app.colorSize)]
    app.colorTopHeightMargin = 1900 * (1 / app.colorSize)
    app.colorBottomHeightMargin = 400 * (1 / app.colorSize)
    app.colorWidthMargin = (app.width / 2 - app.colorTopHeightMargin)
    app.selectedColor = 'orange'

    # keeping score
    app.colorTime = 0.0
    app.colorSessionBest = [0.0] * (4)
    app.colorSolved = False

    app.colorSubmissionMessage = ''
    app.colorSubmissionMessageColor = 'red'
    app.colorSubmitButtonMessage = 'submit'
    app.colorReturnColor = 'gray79'
    app.colorSubmitColor = 'gray79'

# for each island in a BW grid, pick a color and assign it to it
# make each boolean a tuple (True, app.colorSet[i]) 
# also note that islands of different colors can touch (very cool)
def randomizeIslandColor(stillBWGrid, colorList):
    for row in range(len(stillBWGrid)):
        for col in range(len(stillBWGrid[0])):
            # if we hit an island
            if stillBWGrid[row][col] == True:
                # pick a color for the island
                islandRandomColorIndex = random.randrange(len(colorList))
                islandRandomColor = colorList[islandRandomColorIndex] # this is a string
                while stillBWGrid[row][col] == True:
                    stillBWGrid[row][col] = (True, islandRandomColor) # this is a tuple
    return stillBWGrid

# now, go through each island in our colored grid rows and make the result a list of tuples:
# [(3, 'orange'), (1, 'purple2')] (this function is still cool)
def colorCountHorizontalIslands(colorGrid):
    rowClues = []
    for row in range(len(colorGrid)):
        rowClues.append(colorCountHorizontalIslandsHelper(colorGrid[row], []))
    return rowClues

# note this needs to stop for diff
def colorCountHorizontalIslandsHelper(colorGridRow, result):
    if colorGridRow == []:
        return result
    else:
        counter = 0
        if isinstance(colorGridRow[0], tuple):
            i = 0
            while 0 <= i < len(colorGridRow) and isinstance(colorGridRow[i], tuple) and colorGridRow[i] == colorGridRow[0]:
                counter += 1
                i += 1
            result.append((counter, colorGridRow[i - 1]))
            return colorCountHorizontalIslandsHelper(colorGridRow[counter:], result)
        else:
            return colorCountHorizontalIslandsHelper(colorGridRow[1:], result)

# again, go through each island in our colored grid COLS and make the result a list of tuples:
# [(3, 'orange'), (1, 'purple2')]
def colorCountVerticalIslands(colorGrid):
    flipList = copy.deepcopy(colorGrid)
    transposed = transpose(flipList)
    colClues = []
    for row in range(len(transposed)):
         colClues.append(colorCountHorizontalIslandsHelper(transposed[row], []))
    return colClues

# adapted from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
# if you click a square 
def colorGetCell(app, x, y):
    cellW = (app.height - 2*app.colorWidthMargin) / app.colorSize
    cellH = (app.height - app.colorTopHeightMargin - app.colorBottomHeightMargin ) / app.colorSize
    if  (app.colorWidthMargin < x < app.width - app.colorWidthMargin
        and app.colorTopHeightMargin < y < app.height - app.colorBottomHeightMargin):
        row = int((y - app.colorTopHeightMargin) / cellH)
        col = int((x - app.colorWidthMargin) / cellH)
        return row, col
    else:
        return None

# adapted from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
def colorGetCellBounds(app, row, col):
    cellW = (app.height - 2*app.colorWidthMargin)/app.colorSize
    cellH = (app.height - app.colorTopHeightMargin - app.colorBottomHeightMargin)/app.colorSize
    x0 = app.colorWidthMargin + col*cellH
    y0 = app.colorTopHeightMargin + row*cellH
    x1 = x0 + cellH
    y1 = y0 + cellH
    return (x0, y0, x1, y1)

def colorGetSquareBounds(app, row, col):
    cellW = (app.height - 2*app.colorWidthMargin)/app.colorSize
    cellH = (app.height - app.colorTopHeightMargin - app.colorBottomHeightMargin )/app.colorSize
    x0, y0, x1, y1 = colorGetCellBounds(app, row, col)
    if app.colorSize == 20:
        x0 += 0.18*cellH
        x1 -= 0.18*cellH
        y0 += 0.18*cellH
        y1 -= 0.18*cellH
    elif app.colorSize == 15:
        x0 += 0.15*cellH
        x1 -= 0.15*cellH
        y0 += 0.15*cellH
        y1 -= 0.15*cellH
    elif app.colorSize == 10:
        x0 += 0.1*cellH
        x1 -= 0.1*cellH
        y0 += 0.1*cellH
        y1 -= 0.1*cellH
    else:
        x0 += 0.1*cellH
        x1 -= 0.1*cellH
        y0 += 0.1*cellH
        y1 -= 0.1*cellH
    return x0, y0, x1, y1

# this draws the squares based on the selected color or the x'es 
def drawSolverColorGrid(app, canvas):
    for row in range(app.colorSize):
        for col in range(app.colorSize):
            if 0 <= row < len(app.colorSolverGrid) and 0 <= col < len(app.colorSolverGrid[0]):
                # key step: is it a tuple (i.e. not false)
                if isinstance(app.colorSolverGrid[row][col], tuple):
                    (BWx0, BWx1, BWy0, BWy1) = colorGetSquareBounds(app, row, col)
                    canvas.create_rectangle(BWx0, BWx1, 
                                            BWy0, BWy1,
                                            # this is the key part, return the color from the tuple created by mouse released
                                            fill = app.colorSolverGrid[row][col][1], width = 0)
                elif app.colorSolverGrid[row][col] == 'X':
                    x0, y0, x1, y1 = colorGetCellBounds(app, row, col)
                    canvas.create_text((x0 + x1)/2, 
                                        (y0 + y1)/2, 
                                        text = 'X', fill = 'red', 
                                        font = f'Arial { (36 * 5) // app.colorSize } bold')
                elif app.colorSolverGrid[row][col] == False:
                    pass

# this draws the empty grid and the clues in their color! 
def drawVisibleColorGrid(app, canvas):
    # width of lines
    if app.colorSize < 11:
        gridWidth = 4
    else:
        gridWidth = 2
    # determine longest row clue:
    longestRow = 0
    for row in range(len(app.colorHorizontalIslands)):
        counter = 0
        for clue in range(len(app.colorHorizontalIslands[row])):
            if clue < len(app.colorHorizontalIslands[row]): 
                #if app.colorHorizontalIslands[row][clue][1][1] != app.colorHorizontalIslands[row][clue - 1][1][1]:   
                    counter += 1
        if counter >= longestRow:
            longestRow = counter
    # determine longest column clue
    longestCol = 0
    for row in range(len(app.colorVerticalIslands)):
        counter = 0
        for clue in range(len(app.colorVerticalIslands[row])):
            if clue < len(app.colorVerticalIslands[row]):
                # if app.colorVerticalIslands[row][clue][1][1] != app.colorVerticalIslands[row][clue - 1][1][1]:
                    counter += 1
        if counter >= longestCol:
            longestCol = counter
    # draw grid
    # adapted from: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
    for row in range(app.colorSize):
        for col in range(app.colorSize):
            x0, y0, x1, y1 = colorGetCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, width = gridWidth)
    # draw row clues
    for row in range(len(app.colorHorizontalIslands)):
        # draw the box
        x0, y0, x1, y1 = colorGetCellBounds(app, row, 0)
        canvas.create_rectangle(x0 - longestRow * (x1 - x0), y0, x0, y1, width = gridWidth)
        # draw the numbers
        if app.colorHorizontalIslands[row] == []:
            s = '0'
            canvas.create_text((x0 - longestRow * (x1 - x0) + x0)/2, (y0 + y1)/2,
                            text = s, font = f'Arial {(36 * 5) // app.colorSize} bold', 
                            fill = 'black')
        else:
            s = ''
            spaceCounter = 0
            for clue in app.colorHorizontalIslands[row]: # this clue is (n, (True, color))
                # key change: number is first tuple elem
                s = str(clue[0])
                s += '  '
                spaceCounter += 300 / app.colorSize
                canvas.create_text(x0 - longestRow * (x1 - x0) + spaceCounter, (y0 + y1)/2,
                            text = s, font = f'Arial {(36 * 5) // app.colorSize} bold', 
                            # key change: color is second tuple elem
                            fill = (clue[1][1]))
            s = ''
    # draw col clues
    for row in range(len(app.colorVerticalIslands)):
        x0, y0, x1, y1 = colorGetCellBounds(app, 0, row)
        canvas.create_rectangle(x0, y0 - longestCol * (y1 - y0), x1, y0, width = gridWidth)
        
        if app.colorVerticalIslands[row] == []:
            s = ''
            s += '0'
            s += '\n'
            canvas.create_text((x0 + x1)/2, ((y0 - longestCol * (y1 - y0)) + y0)/2 + 140 // app.colorSize,
                            text = s, font = f'Arial {(36 * 5) // app.colorSize} bold',
                            fill = 'black')
            s = ''
        else:
            s = ''
            spaceCounter = 0
            for clue in app.colorVerticalIslands[row]:
                s = str(clue[0])    
                canvas.create_text((x0 + x1)/2, y0 - longestCol * (x1 - x0) + spaceCounter + 130/app.colorSize,
                            text = s, font = f'Arial {(36 * 5) // app.colorSize} bold',
                            fill = clue[1][1])
                spaceCounter += 300 / app.colorSize
            s = ''

# draws the menu palette that you can select "brush" color with
def drawColorPalette(app, canvas):
    # width of lines
    gridWidth = 4

    for color in range(len(app.colorSet)):
        if app.selectedColor == app.colorSet[color]:
            canvas.create_rectangle(3.4*app.width//5 + color * 80, 3.5*app.height//5, 
                                3.4*app.width//5 + 60 + color * 80, 3.5*app.height//5 + 60,
                                fill = app.colorSet[color], width = gridWidth, outline = 'black')
        else:
            canvas.create_rectangle(3.4*app.width//5 + color * 80, 3.5*app.height//5, 
                                3.4*app.width//5 + 60 + color * 80, 3.5*app.height//5 + 60,
                                fill = app.colorSet[color], width = 0)
            
# check that the colors are the same too! tuple checks
def colorSolverMatchSolved(solver, solved):
    counter = 0
    for row in range(len(solver)):
        for col in range(len(solver[0])):
            if isinstance(solver[row][col], tuple)  and solved[row][col] == False:
                return False
            elif isinstance(solver[row][col], tuple) == False and isinstance(solved[row][col], tuple):
                return False
            elif isinstance(solved[row][col], tuple) and isinstance(solver[row][col], tuple):
                if solved[row][col] != solver[row][col]:
                    return False
    return True

# restart, timer, etc...
def drawColorMenu(app, canvas):
    canvas.create_text((4/5)*app.width, app.height/3 - 180, 
                    text = f"{app.colorSize}x{app.colorSize}", 
                    font = 'Cambria 24 bold')

    canvas.create_text((4/5)*app.width, app.height/3 -150, 
                    text = f"{app.colorSubmissionMessage}", 
                    font = 'Cambria 18 bold', fill = app.colorSubmissionMessageColor)   

    canvas.create_rectangle((4/5)*app.width - 60, app.height/3 - 100 - 20, 
                            (4/5)*app.width + 60, app.height/3 -100 + 20,
                                fill = app.colorSubmitColor, width = 3)
    canvas.create_text((4/5)*app.width, app.height/3 - 100, 
                        text = "submit", 
                        font = 'Cambria 24 bold')   

    canvas.create_text((4/5)*app.width, app.height/3 - 20, 
                        text = "press 1-4 to change grid size \n         press enter to submit \n       press r for a new puzzle", 
                        font = 'Cambria 24 bold')
                    
    canvas.create_text((4/5)*app.width, app.height/3 + 70, 
                        text = f"session best: {round(app.colorSessionBest[app.colorSize // 5 - 1], 3)} \n latest time: {round(app.colorTime, 3)}", 
                        font = 'Cambria 24 bold')   


    canvas.create_rectangle((4/5)*app.width - 160, app.height/3 + 150 - 20, 
                            (4/5)*app.width + 160, app.height/3 + 150 + 20,
                                fill = app.colorReturnColor, width = 3)
    canvas.create_text((4/5)*app.width, app.height/3 + 150, 
                        text = f"return to main menu", 
                        font = 'Cambria 24 bold')

    canvas.create_text((4/5)*app.width, app.height/3 + 240, 
                        text = f"select color", 
                        font = 'Cambria 24 bold')
    
# draw/remove a square or an x or select a menu option
def play_with_colors_mousePressed(app, event):
    # left click, vs right click to draw an x
    # if i click on a box ..
    # submission attempt
    for color in range(len(app.colorSet)):
        if (3.4*app.width//5 + color * 80 < event.x < 3.4*app.width//5 + color * 80 + 60 and
             3.5*app.height//5 < event.y < 3.5*app.height//5 + 60):
            app.selectedColor = app.colorSet[color]
    
    if ((4/5)*app.width - 60 < event.x < (4/5)*app.width + 60 and
        app.height/3 - 100 - 20 < event.y < app.height/3 - 100 + 20):
        app.colorSubmitColor = 'gray60'
    # return to main menu
    elif ( (4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
    app.height/3 + 150 - 20 < event.y < app.height/3 + 150 + 20):
        app.colorReturnColor = 'gray60'

    elif colorGetCell(app, event.x, event.y) != None:
        row, col = colorGetCell(app, event.x, event.y)
        if 0 <= row < app.colorSize and 0 <= col < app.colorSize:
            # draw square if click on empty AHA KEY CHANGE 
            if app.colorSolverGrid[row][col] == False:
                cellColor = (app.selectedColor)
                app.colorSolverGrid[row][col] = (True, cellColor)
            # remove square if click on square
            elif isinstance(app.colorSolverGrid[row][col], tuple):
                app.colorSolverGrid[row][col] = False
            # remove x if click on x
            elif app.colorSolverGrid[row][col] == 'X':
                app.colorSolverGrid[row][col] = False
    
# after correct submission click 1
def submittedOnceColor(app):
    app.colorSubmissionMessage = 'complete! press enter again to refresh'
    app.colorSubmitButtonMessage = 'new'
    app.colorSubmissionMessageColor = 'green'
    app.colorSolved = True
    if app.colorTime < app.colorSessionBest[app.colorSize // 5 - 1] or app.colorSessionBest[app.colorSize // 5 - 1] == 0.0:
        app.colorSessionBest[app.colorSize // 5 - 1] = app.colorTime
    app.colorTime = 0

# after correct submission click 2
def submittedTwiceColor(app):
    app.colorSolved = False
    app.colorTime = 0
    app.stillBWGrid = generateSolvedBWGrid(app.colorSize)
    app.colorGrid = randomizeIslandColor(app.stillBWGrid, app.colorSet)
    app.colorHorizontalIslands = colorCountHorizontalIslands(app.colorGrid)
    app.colorVerticalIslands = colorCountVerticalIslands(app.colorGrid)
    app.colorSolverGrid = [([False] * app.colorSize) for row in range(app.colorSize)]
    app.colorSubmissionMessage = ''

# for box selection highlighting
def play_with_colors_mouseReleased(app, event):
    # submit
    if ((4/5)*app.width - 60 < event.x < (4/5)*app.width + 60 and
        app.height/3 - 100 - 20 < event.y < app.height/3 - 100 + 20 and
        app.colorSolved == False):
        if colorSolverMatchSolved(app.colorSolverGrid, app.colorGrid):
                submittedOnceColor(app)
                app.colorSubmitColor = 'gray79'
            # counter stop
        else:
            app.colorSubmissionMessage = 'solution is incomplete or incorrect'
            app.colorSubmissionMessageColor = 'red'
            app.colorSubmitColor = 'gray79'
    elif ((4/5)*app.width - 60 < event.x < (4/5)*app.width + 60 and
        app.height/3 - 100 - 20 < event.y < app.height/3 + 100 + 20 and
        app.colorSolved == True):
            submittedTwiceColor(app)
            app.colorSubmitColor = 'gray79'
    # return
    elif ( (4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
    app.height/3 + 150 - 20 < event.y < app.height/3 + 150 + 20):
        app.mode = 'splashScreenMode'
        app.colorReturnColor = 'gray79'

# draw x'es
def play_with_colors_rightMousePressed(app, event):
    if colorGetCell(app, event.x, event.y) != None:
            row, col = colorGetCell(app, event.x, event.y)
            if 0 <= row < app.colorSize and 0 <= col < app.colorSize:
                # right click empty -> x
                if app.colorSolverGrid[row][col] == False:
                    app.colorSolverGrid[row][col] = 'X'
                # right click shaded -> x
                elif isinstance(app.colorSolverGrid[row][col], tuple):
                    app.colorSolverGrid[row][col] = 'X'
                # right click x -> empty
                elif app.colorSolverGrid[row][col] == 'X':
                    app.colorSolverGrid[row][col] = False
                
# keep drawing squares 
def play_with_colors_mouseDragged(app, event):
    if colorGetCell(app, event.x, event.y) != None:
            row, col = colorGetCell(app, event.x, event.y)
            if 0 <= row < app.colorSize and 0 <= col < app.colorSize:
                # draw square if click on empty or X
                if app.colorSolverGrid[row][col] == 'X':
                    app.colorSolverGrid[row][col] = True
                elif app.colorSolverGrid[row][col] == False:
                    app.colorSolverGrid[row][col] = (True, app.selectedColor)
                
# keep drawing x'es
def play_with_colors_rightMouseDragged(app, event):
    if colorGetCell(app, event.x, event.y) != None:
            row, col = colorGetCell(app, event.x, event.y)
            if 0 <= row < app.colorSize and 0 <= col < app.colorSize:
                # right click empty -> x
                if app.colorSolverGrid[row][col] == False:
                    app.colorSolverGrid[row][col] = 'X'
                # right click shaded -> x
                elif isinstance(app.colorSolverGrid[row][col], tuple):
                    app.colorSolverGrid[row][col] = 'X'

def play_with_colors_keyPressed(app, event):
    if event.key == 'r':
        app.colorSolved = False
        app.stillBWGrid = generateSolvedBWGrid(app.colorSize)
        app.colorGrid = randomizeIslandColor(app.stillBWGrid, app.colorSet)
        app.colorHorizontalIslands = colorCountHorizontalIslands(app.colorGrid)
        app.colorVerticalIslands = colorCountVerticalIslands(app.colorGrid)
        app.colorSolverGrid = [([False] * app.colorSize) for row in range(app.colorSize)]
        app.colorSubmissionMessage = ''
        app.colorTime = 0
    # choose grid size
    elif event.key in string.digits:
        for i in range(1, 5):
            if int(event.key) == i:
                if app.colorSize != 5 *i: 
                    app.colorSize = 5 * i
                    app.colorSolved = False
                    app.colorSubmissionMessage = ''
                    app.colorTime = 0
                    app.colorSolverGrid = [([False] * app.colorSize) for row in range(app.colorSize)]
                    app.stillBWGrid = generateSolvedBWGrid(app.colorSize)
                    app.colorGrid = randomizeIslandColor(app.stillBWGrid, app.colorSet)
                    app.colorHorizontalIslands = colorCountHorizontalIslands(app.colorGrid)
                    app.colorVerticalIslands = colorCountVerticalIslands(app.colorGrid)
    elif event.key == 'Enter' and app.colorSolved != True:
        if colorSolverMatchSolved(app.colorSolverGrid, app.colorGrid):
            submittedOnceColor(app)
        else:
            app.colorSubmissionMessage = 'solution is incomplete or incorrect'
            app.colorSubmissionMessageColor = 'red'
    elif event.key == 'Enter' and app.colorSolved == True:
            submittedTwiceColor(app)

def play_with_colors_timerFired(app):
    if app.colorSolved == False:
        app.colorTime += 0.1

def play_with_colors_redrawAll(app, canvas):    
    drawSolverColorGrid(app, canvas)
    drawColorPalette(app, canvas)
    drawVisibleColorGrid(app, canvas)
    drawColorMenu(app, canvas)

#####################################
# 'create' mode: this is only B/W, next mode has color
#####################################

def restartCreate(app):
    
    app.createSize = 5  

    # update this in mouse released/mouse dragged
    app.createInputGrid = [([False] * app.createSize) for row in range(app.createSize)]
    # update in key pressed
    
    # v False -> we're drawing, True -> it passed and we're solving
    app.createSolvingMode = False
    # when you're solving
    app.createSolverGrid = [([False] * app.createSize) for row in range(app.createSize)]

    # use the following in redrawAll or just update them each time a cell is filled in
    app.createHorizontalIslands = BWcountHorizontalIslands(app.createInputGrid)
    app.createVerticalIslands = BWcountVerticalIslands(app.createInputGrid)

    # for drawing
    app.createTopHeightMargin = 1350 * (1 / app.createSize)
    app.createBottomHeightMargin = 500 * (1 / app.createSize)
    app.createWidthMargin = (app.width / 2 - app.createTopHeightMargin) / 1.9

    # for the menu
    app.createSubmissionMessage = '' # 'this puzzle is unique' / 'this puzzle either has {len(solutions)} solutions so maybe modify BW unique.
    app.createSubmissionMessageColor = 'red' # non unique
    app.createSubmitButtonMessage = 'submit' # unique
    app.createReturnColor = 'gray79'
    app.createSubmitColor = 'gray79'

# this is drawn based on user input but not the cells
def drawVisibleCreateGrid(app, canvas):
    if app.createSize < 11:
        gridWidth = 4
    else:
        gridWidth = 2
    # determine longest row clue:
    longestRow = 0
    for row in range(len(app.createHorizontalIslands)):
        counter = 0
        for clue in range(len(app.createHorizontalIslands[row])):
            counter += 1
        if counter >= longestRow:
            longestRow = counter
        if longestRow == 0:
            longestRow = 1
    # determine longest column clue
    longestCol = 0
    for row in range(len(app.createVerticalIslands)):
        counter = 0
        for clue in range(len(app.createVerticalIslands[row])):
            counter += 1
        if counter >= longestCol:
            longestCol = counter
        if longestCol == 0:
            longestCol = 1
    # draw grid
    for row in range(app.createSize):
        for col in range(app.createSize):
            x0, y0, x1, y1 = getCellBoundsCreate(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, width = gridWidth)
    # draw row clues
    for row in range(len(app.createHorizontalIslands)):
        x0, y0, x1, y1 = getCellBoundsCreate(app, row, 0)
        canvas.create_rectangle(x0 - longestRow * (x1 - x0), y0, x0, y1, width = gridWidth)
        s = ''
        if app.createHorizontalIslands[row] == []:
            s += '0'
        else:
            for clue in range(len(app.createHorizontalIslands[row])):
                s += str(app.createHorizontalIslands[row][clue])
                s += '  '    
        canvas.create_text((x0 - longestRow * (x1 - x0) + x0)/2, (y0 + y1)/2,
                            text = s, font = f'Arial {(50 * 5) // app.createSize} bold')
    # draw col clues
    for row in range(len(app.createVerticalIslands)):
        x0, y0, x1, y1 = getCellBoundsCreate(app, 0, row)
        canvas.create_rectangle(x0, y0 - longestCol * (y1 - y0), x1, y0, width = gridWidth)
        s = ''
        if app.createVerticalIslands[row] == []:
            s += '0'
            s += '\n'
        else:
            for clue in range(len(app.createVerticalIslands[row])):
                s += str(app.createVerticalIslands[row][clue])
                s += '\n'    
        canvas.create_text((x0 + x1)/2, ((y0 - longestCol * (y1 - y0)) + y0 )/2 + 140 // app.createSize,
                            text = s, font = f'Arial {(50 * 5) // app.createSize} bold')

# draws the squares / x'es for the editor or the test solver
def drawSolverCreateGrid(app, canvas):
    if app.createSolvingMode == False:
        for row in range(app.createSize):
            for col in range(app.createSize):
                if 0 <= row < len(app.createInputGrid) and 0 <= col < len(app.createInputGrid[0]):
                    if app.createInputGrid[row][col] == True:
                        (BWx0, BWx1, BWy0, BWy1) = getSquareBoundsCreate(app, row, col)
                        canvas.create_rectangle(BWx0, BWx1, 
                                                BWy0, BWy1,
                                                fill = 'black')
                    elif app.createInputGrid[row][col] == 'X':
                        x0, y0, x1, y1 = getCellBoundsCreate(app, row, col)
                        canvas.create_text((x0 + x1)/2, 
                                            (y0 + y1)/2, 
                                            text = 'X', fill = 'red', 
                                            font = f'Arial { (36 * 5) // app.createSize } bold')
                    elif app.createInputGrid[row][col] == False:
                        pass
    elif app.createSolvingMode == True:
        for row in range(app.createSize):
            for col in range(app.createSize):
                if 0 <= row < len(app.createSolverGrid) and 0 <= col < len(app.createSolverGrid[0]):
                    if app.createSolverGrid[row][col] == True:
                        (BWx0, BWx1, BWy0, BWy1) = getSquareBoundsCreate(app, row, col)
                        canvas.create_rectangle(BWx0, BWx1, 
                                                BWy0, BWy1,
                                                fill = 'black')
                    elif app.createSolverGrid[row][col] == 'X':
                        x0, y0, x1, y1 = getCellBoundsCreate(app, row, col)
                        canvas.create_text((x0 + x1)/2, 
                                            (y0 + y1)/2, 
                                            text = 'X', fill = 'red', 
                                            font = f'Arial { (36 * 5) // app.createSize } bold')
                    elif app.createSolverGrid[row][col] == False:
                        pass

# to update clues live! 
def updateClues(app):
    if app.createSolvingMode == False:
        app.createHorizontalIslands = BWcountHorizontalIslands(app.createInputGrid)
        app.createVerticalIslands = BWcountVerticalIslands(app.createInputGrid)

#draws boxes for menu
def drawCreateMenu(app, canvas):
    # back button to main mode, submit
    # display: size, score, correctness, best session time
    if app.createSolvingMode == False:
        canvas.create_text((4/5)*app.width, app.height/3 - 200, 
                        text = f"{app.createSize}x{app.createSize}: draw a grid", 
                        font = 'Cambria 24 bold')
    elif app.createSolvingMode == True:
        canvas.create_text((4/5)*app.width, app.height/3 - 200, 
                        text = f"{app.createSize}x{app.createSize}: test the solve", 
                        font = 'Cambria 24 bold')

    canvas.create_text((4/5)*app.width, app.height/3 - 150, 
                    text = f"{app.createSubmissionMessage}", 
                    font = 'Cambria 18 bold', fill = app.createSubmissionMessageColor)   

    canvas.create_rectangle((4/5)*app.width - 160, app.height/3 - 100 - 20, 
                            (4/5)*app.width + 160, app.height/3 -100 + 20,
                                fill = app.createSubmitColor, width = 3)
    canvas.create_text((4/5)*app.width, app.height/3 - 100, 
                        text = "check for uniqueness", 
                        font = 'Cambria 24 bold')   

    canvas.create_text((4/5)*app.width, app.height/3 + 20, 
                        text = "press 1-4 to change grid size \n\npress c to clear the board \n\npress s to toggle test solve", 
                        font = 'Cambria 24 bold')
                    

    canvas.create_rectangle((4/5)*app.width - 160, app.height/3 + 150 - 20, 
                            (4/5)*app.width + 160, app.height/3 + 150 + 20,
                                fill = app.createReturnColor, width = 3)
    canvas.create_text((4/5)*app.width, app.height/3 + 150, 
                        text = f"return to main menu", 
                        font = 'Cambria 24 bold')

#FIX draw/remove a square or an x or select a menu option
def create_mousePressed(app, event):
    # left click, vs right click to draw an x
    # if i click on a box ..
    
    # submission attempt uniqueness check
    if ((4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
        app.height/3 - 100 - 20 < event.y < app.height/3 - 100 + 20):
        app.createSubmitColor = 'gray60'
    # return to main menu
    elif ( (4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
    app.height/3 + 150 - 20 < event.y < app.height/3 + 150 + 20):
        app.createReturnColor = 'gray60'

    elif getCellCreate(app, event.x, event.y) != None:
        row, col = getCellCreate(app, event.x, event.y)
        if 0 <= row < app.createSize and 0 <= col < app.createSize:
            # draw square if click on empty
            if app.createSolvingMode == False:
                if app.createInputGrid[row][col] == False:
                    app.createInputGrid[row][col] = True
                    updateClues(app)
                # remove square if click on square
                elif app.createInputGrid[row][col] == True:
                    app.createInputGrid[row][col] = False
                    updateClues(app)
                # remove x if click on x
                elif app.createInputGrid[row][col] == 'X':
                    app.createInputGrid[row][col] = False
            elif app.createSolvingMode == True:
                if app.createSolverGrid[row][col] == False:
                    app.createSolverGrid[row][col] = True
                # remove square if click on square
                elif app.createSolverGrid[row][col] == True:
                    app.createSolverGrid[row][col] = False
                # remove x if click on x
                elif app.createSolverGrid[row][col] == 'X':
                    app.createSolverGrid[row][col] = False

# returns the number of cells needed to reach probable uniqueness threshold
def howManyCellsDoWeStillNeed(grid):
    size = len(grid)
    totalSquares = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == True:
                totalSquares += 1
    if size == 10:
        return ((size ** 2) // 2) + 10 - totalSquares
    elif size == 15:
        return ((size ** 2) // 2) + 25 - totalSquares
    elif size == 20:
        return ((size ** 2) // 2) + 38 - totalSquares 

# as usual 
def create_mouseReleased(app, event):
    # submit CHANGE BOUNDS
    if ((4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
        app.height/3 - 100 - 20 < event.y < app.height/3 - 100 + 20):
 
        if BWUnique(app.createInputGrid) == True:
            # check for uniqueness
            app.createSubmitColor = 'gray79'
            app.createSubmissionMessage = 'this nonogram is unique'
            app.createSubmissionMessageColor = 'green'
        else:
            if app.createSize == 5:
                app.createSubmissionMessage = 'this nonogram is not unique'
            elif app.createSize == 10:
                app.createSubmissionMessage = f'add {howManyCellsDoWeStillNeed(app.createInputGrid)} more cells and i can almost guarantee\n       uniqueness, otherwise be careful!'
            elif app.createSize == 15:
                app.createSubmissionMessage = f'add {howManyCellsDoWeStillNeed(app.createInputGrid)} more cells and i can almost guarantee\n       uniqueness, otherwise be careful!'
            elif app.createSize == 20: 
                app.createSubmissionMessage = f'add {howManyCellsDoWeStillNeed(app.createInputGrid)} more cells and i can almost guarantee\n       uniqueness, otherwise be careful!'
            app.createSubmissionMessageColor = 'red'
            app.createSubmitColor = 'gray79'

    # return
    elif ( (4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
    app.height/3 + 150 - 20 < event.y < app.height/3 + 150 + 20):
        app.mode = 'splashScreenMode'
        app.createReturnColor = 'gray79'

# draw x'es
def create_rightMousePressed(app, event):
    if getCellCreate(app, event.x, event.y) != None:
            row, col = getCellCreate(app, event.x, event.y)
            if 0 <= row < app.createSize and 0 <= col < app.createSize:
                # right click empty -> x
                if app.createSolvingMode == False:
                    if app.createInputGrid[row][col] == False:
                        app.createInputGrid[row][col] = 'X'
                    # right click shaded -> x
                    elif app.createInputGrid[row][col] == True:
                        app.createInputGrid[row][col] = 'X'
                        updateClues(app)
                    # right click x -> empty
                    elif app.createInputGrid[row][col] == 'X':
                        app.createInputGrid[row][col] = False
                        
                elif app.createSolvingMode == True:
                    if app.createSolverGrid[row][col] == False:
                        app.createSolverGrid[row][col] = 'X'
                    # right click shaded -> x
                    elif app.createSolverGrid[row][col] == True:
                        app.createSolverGrid[row][col] = 'X'
                    # right click x -> empty
                    elif app.createSolverGrid[row][col] == 'X':
                        app.createSolverGrid[row][col] = False
                
# keep drawing squares
def create_mouseDragged(app, event):
    if getCellCreate(app, event.x, event.y) != None:
            row, col = getCellCreate(app, event.x, event.y)
            if 0 <= row < app.createSize and 0 <= col < app.createSize:
                # draw square if click on empty or X
                if app.createSolvingMode == False:
                    if app.createInputGrid[row][col] == 'X':
                        app.createInputGrid[row][col] = True
                        updateClues(app)
                    elif app.createInputGrid[row][col] == False:
                        app.createInputGrid[row][col] = True
                        updateClues(app)
                elif app.createSolvingMode == True:
                    if app.createSolverGrid[row][col] == 'X':
                        app.createSolverGrid[row][col] = True
                    elif app.createSolverGrid[row][col] == False:
                        app.createSolverGrid[row][col] = True
                    
# keep drawing x'es
def create_rightMouseDragged(app, event):
    if getCellCreate(app, event.x, event.y) != None:
            row, col = getCellCreate(app, event.x, event.y)
            if 0 <= row < app.createSize and 0 <= col < app.createSize:
                if app.createSolvingMode == False:
                    # right click empty -> x
                    if app.createInputGrid[row][col] == False:
                        app.createInputGrid[row][col] = 'X'
                    # right click shaded -> x
                    elif app.createInputGrid[row][col] == True:
                        app.createInputGrid[row][col] = 'X'
                        updateClues(app)
                elif app.createSolvingMode == True:
                    if app.createSolverGrid[row][col] == False:
                        app.createSolverGrid[row][col] = 'X'
                    # right click shaded -> x
                    elif app.createSolverGrid[row][col] == True:
                        app.createSolverGrid[row][col] = 'X'

# restart or change grid size or toggle solve
def create_keyPressed(app, event):
    # solve it! clues will freeze
    if event.key == 's':
        if app.createSolvingMode == False:
            app.createSolvingMode = True
            app.createSubmissionMessage = ''
        elif app.createSolvingMode == True:
            app.createSolvingMode = False
    # clear
    elif event.key == 'c':
            app.createInputGrid = [([False] * app.createSize) for row in range(app.createSize)]
            app.createSolverGrid = [([False] * app.createSize) for row in range(app.createSize)]
            app.createHorizontalIslands = BWcountHorizontalIslands(app.createInputGrid)
            app.createVerticalIslands = BWcountVerticalIslands(app.createInputGrid)
            app.createSolvingMode = False
            app.createSubmissionMessage = ''

    # choose grid size
    elif event.key in string.digits:
        for i in range(1, 5):
            if int(event.key) == i:
                if app.createSize != 5 *i: 
                    app.createSize = 5 * i
                    app.createSolved = False
                    app.createSubmissionMessage = ''
                    app.createInputGrid = [([False] * app.createSize) for row in range(app.createSize)]
                    app.createSolverGrid = [([False] * app.createSize) for row in range(app.createSize)]
                    app.createHorizontalIslands = BWcountHorizontalIslands(app.createInputGrid)
                    app.createVerticalIslands = BWcountVerticalIslands(app.createInputGrid)

# adapted from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
# if you click a square 
def getCellCreate(app, x, y):
    cellW = (app.height - 2*app.createWidthMargin) / app.createSize
    cellH = (app.height - app.createTopHeightMargin - app.createBottomHeightMargin ) / app.createSize
    if  (app.createWidthMargin < x < app.width - app.createWidthMargin
        and app.createTopHeightMargin < y < app.height - app.createBottomHeightMargin):
        row = int((y - app.createTopHeightMargin) / cellH)
        col = int((x - app.createWidthMargin) / cellH)
        return row, col
    else:
        return None

# adapted from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
def getCellBoundsCreate(app, row, col):
    cellW = (app.height - 2*app.createWidthMargin)/app.createSize
    cellH = (app.height - app.createTopHeightMargin - app.createBottomHeightMargin )/app.createSize
    x0 = app.createWidthMargin + col*cellH
    y0 = app.createTopHeightMargin + row*cellH
    x1 = x0 + cellH
    y1 = y0 + cellH
    return (x0, y0, x1, y1)

# drawn square bound
def getSquareBoundsCreate(app, row, col):
    cellW = (app.height - 2*app.createWidthMargin)/app.createSize
    cellH = (app.height - app.createTopHeightMargin - app.createBottomHeightMargin )/app.createSize
    x0, y0, x1, y1 = getCellBoundsCreate(app, row, col)
    if app.createSize == 20:
        x0 += 0.18*cellH
        x1 -= 0.18*cellH
        y0 += 0.18*cellH
        y1 -= 0.18*cellH
    elif app.createSize == 15:
        x0 += 0.15*cellH
        x1 -= 0.15*cellH
        y0 += 0.15*cellH
        y1 -= 0.15*cellH
    elif app.createSize == 10:
        x0 += 0.1*cellH
        x1 -= 0.1*cellH
        y0 += 0.1*cellH
        y1 -= 0.1*cellH
    else:
        x0 += 0.07*cellH
        x1 -= 0.07*cellH
        y0 += 0.07*cellH
        y1 -= 0.07*cellH
    return x0, y0, x1, y1

def create_redrawAll(app, canvas):
    drawCreateMenu(app, canvas)
    drawVisibleCreateGrid(app, canvas)
    drawSolverCreateGrid(app, canvas)

#####################################
# 'create_with_colors' mode: 
#####################################

# things i added from create
# a palette to draw with the colors 
# the uniqueness checker is for BWequivalent

# makes a BW grid to check for uniqueness
def createBWequivalent(colorGrid):
    newGrid = copy.deepcopy(colorGrid)
    for row in range(len(colorGrid)):
        for col in range(len(colorGrid)):
            if isinstance(colorGrid[row][col], tuple):
                newGrid[row][col] = True
    return newGrid

def restartCreateWithColors(app):
    
    app.createSizeColor = 5

    # for the color play stuff
    app.colorSetColor = ['orange', 'forest green', 'purple2', 'deep sky blue', 'firebrick2']
    app.selectedColorColor = 'orange'

    # update this in mouse released/mouse dragged
    app.createInputGridColor = [([False] * app.createSizeColor) for row in range(app.createSizeColor)]
    # update in key pressed
    
    # v False -> we're drawing, True -> it passed and we're solving
    app.createSolvingModeColor = False
    # when you're solving
    app.createSolverGridColor = [([False] * app.createSizeColor) for row in range(app.createSizeColor)]

    # use the following in redrawAll or just update them each time a cell is filled in
    app.createHorizontalIslandsColor = colorCountHorizontalIslands(app.createInputGridColor)
    app.createVerticalIslandsColor = colorCountVerticalIslands(app.createInputGridColor)

    # for drawing
    app.createTopHeightMarginColor = 1900 * (1 / app.createSizeColor)
    app.createBottomHeightMarginColor = 400 * (1 / app.createSizeColor)
    app.createWidthMarginColor = (app.width / 2 - app.createTopHeightMarginColor)

    # for the menu
    app.createSubmissionMessageColor1 = '' # 'this puzzle is unique' / 'this puzzle either has {len(solutions)} solutions so maybe modify BW unique.
    app.createSubmissionMessageColorColor = 'red' # non unique
    app.createSubmitButtonMessageColor1 = 'submit' # unique
    app.createReturnColorColor = 'gray79'
    app.createSubmitColorColor = 'gray79'
  
# this draws the empty grid and the clues in their color! 
def drawVisibleCreateGridColor(app, canvas):
    # width of lines
    if app.createSizeColor < 11:
        gridWidth = 4
    else:
        gridWidth = 2
    # determine longest row clue:
    longestRow = 0
    for row in range(len(app.createHorizontalIslandsColor)):
        counter = 0
        for clue in range(len(app.createHorizontalIslandsColor[row])):
            if clue < len(app.createHorizontalIslandsColor[row]): 
                #if app.colorHorizontalIslands[row][clue][1][1] != app.colorHorizontalIslands[row][clue - 1][1][1]:   
                    counter += 1
        if counter >= longestRow:
            longestRow = counter
        if longestRow == 0:
            longestRow = 1
    # determine longest column clue
    longestCol = 0
    for row in range(len(app.createVerticalIslandsColor)):
        counter = 0
        for clue in range(len(app.createVerticalIslandsColor[row])):
            if clue < len(app.createVerticalIslandsColor[row]):
                # if app.colorVerticalIslands[row][clue][1][1] != app.colorVerticalIslands[row][clue - 1][1][1]:
                    counter += 1
        if counter >= longestCol:
            longestCol = counter
        if longestCol == 0:
            longestCol = 1
    # draw grid
    # adapted from: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
    for row in range(app.createSizeColor):
        for col in range(app.createSizeColor):
            x0, y0, x1, y1 = getCellBoundsCreateColor(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, width = gridWidth)
    # draw row clues
    for row in range(len(app.createHorizontalIslandsColor)):
        # draw the box
        x0, y0, x1, y1 = getCellBoundsCreateColor(app, row, 0)
        canvas.create_rectangle(x0 - longestRow * (x1 - x0), y0, x0, y1, width = gridWidth)
        # draw the numbers
        if app.createHorizontalIslandsColor[row] == []:
            s = '0'
            canvas.create_text((x0 - longestRow * (x1 - x0) + x0)/2, (y0 + y1)/2,
                            text = s, font = f'Arial {(36 * 5) // app.createSizeColor} bold', 
                            fill = 'black')
        else:
            s = ''
            spaceCounter = 0
            for clue in app.createHorizontalIslandsColor[row]: # this clue is (n, (True, color))
                # key change: number is first tuple elem
                s = str(clue[0])
                s += '  '
                spaceCounter += 300 / app.createSizeColor
                canvas.create_text(x0 - longestRow * (x1 - x0) + spaceCounter, (y0 + y1)/2,
                            text = s, font = f'Arial {(36 * 5) // app.createSizeColor} bold', 
                            # key change: color is second tuple elem
                            fill = (clue[1][1]))
            s = ''
    # draw col clues
    for row in range(len(app.createVerticalIslandsColor)):
        x0, y0, x1, y1 = getCellBoundsCreateColor(app, 0, row)
        canvas.create_rectangle(x0, y0 - longestCol * (y1 - y0), x1, y0, width = gridWidth)
        
        if app.createVerticalIslandsColor[row] == []:
            s = ''
            s += '0'
            s += '\n'
            canvas.create_text((x0 + x1)/2, ((y0 - longestCol * (y1 - y0)) + y0)/2 + 140 // app.createSizeColor,
                            text = s, font = f'Arial {(36 * 5) // app.createSizeColor} bold',
                            fill = 'black')
            s = ''
        else:
            s = ''
            spaceCounter = 0
            for clue in app.createVerticalIslandsColor[row]:
                s = str(clue[0])    
                canvas.create_text((x0 + x1)/2, y0 - longestCol * (x1 - x0) + spaceCounter + 130/app.createSizeColor,
                            text = s, font = f'Arial {(36 * 5) // app.createSizeColor} bold',
                            fill = clue[1][1])
                spaceCounter += 300 / app.createSizeColor
            s = ''

# draws the squares / x'es for the editor or the test solver
def drawSolverCreateGridColor(app, canvas):
    if app.createSolvingModeColor == False:
        for row in range(app.createSizeColor):
            for col in range(app.createSizeColor):
                if 0 <= row < len(app.createInputGridColor) and 0 <= col < len(app.createInputGridColor[0]):
                    if isinstance(app.createInputGridColor[row][col], tuple):
                        (BWx0, BWx1, BWy0, BWy1) = getSquareBoundsCreateColor(app, row, col)
                        canvas.create_rectangle(BWx0, BWx1, 
                                            BWy0, BWy1,
                                            # this is the key part, return the color from the tuple created by mouse released
                                            fill = app.createInputGridColor[row][col][1], width = 0)
                    elif app.createInputGridColor[row][col] == 'X':
                        x0, y0, x1, y1 = getCellBoundsCreateColor(app, row, col)
                        canvas.create_text((x0 + x1)/2, 
                                            (y0 + y1)/2, 
                                            text = 'X', fill = 'red', 
                                            font = f'Arial { (36 * 5) // app.createSizeColor} bold')
                    elif app.createInputGridColor[row][col] == False:
                        pass
    elif app.createSolvingModeColor == True:
        for row in range(app.createSizeColor):
            for col in range(app.createSizeColor):
                if 0 <= row < len(app.createSolverGridColor) and 0 <= col < len(app.createSolverGridColor[0]):
                    if isinstance(app.createSolverGridColor[row][col], tuple):
                        (BWx0, BWx1, BWy0, BWy1) = getSquareBoundsCreateColor(app, row, col)
                        canvas.create_rectangle(BWx0, BWx1, 
                                                BWy0, BWy1,
                                                fill = app.createSolverGridColor[row][col][1], width = 0)
                    elif app.createSolverGridColor[row][col] == 'X':
                        x0, y0, x1, y1 = getCellBoundsCreateColor(app, row, col)
                        canvas.create_text((x0 + x1)/2, 
                                            (y0 + y1)/2, 
                                            text = 'X', fill = 'red', 
                                            font = f'Arial { (36 * 5) // app.createSizeColor } bold')
                    elif app.createSolverGridColor[row][col] == False:
                        pass

# to update clues live! 
def updateCluesColor(app):
    if app.createSolvingModeColor == False:
        app.createHorizontalIslandsColor = colorCountHorizontalIslands(app.createInputGridColor)
        app.createVerticalIslandsColor = colorCountVerticalIslands(app.createInputGridColor)

# draws boxes for menu
def drawCreateMenuColor(app, canvas):
    # back button to main mode, submit
    # display: size, score, correctness, best session time
    if app.createSolvingModeColor == False:
        canvas.create_text((4/5)*app.width, app.height/3 - 200, 
                        text = f"{app.createSizeColor}x{app.createSizeColor}: draw a grid", 
                        font = 'Cambria 24 bold')
    elif app.createSolvingModeColor == True:
        canvas.create_text((4/5)*app.width, app.height/3 - 200, 
                        text = f"{app.createSizeColor}x{app.createSizeColor}: test the solve", 
                        font = 'Cambria 24 bold')

    canvas.create_text((4/5)*app.width, app.height/3 - 150, 
                    text = f"{app.createSubmissionMessageColor1}", 
                    font = 'Cambria 18 bold', fill = app.createSubmissionMessageColorColor)   

    canvas.create_rectangle((4/5)*app.width - 160, app.height/3 - 100 - 20, 
                            (4/5)*app.width + 160, app.height/3 -100 + 20,
                                fill = app.createSubmitColorColor, width = 3)
    canvas.create_text((4/5)*app.width, app.height/3 - 100, 
                        text = "check for uniqueness", 
                        font = 'Cambria 24 bold')   

    canvas.create_text((4/5)*app.width, app.height/3 + 20, 
                        text = "press 1-4 to change grid size \n\npress c to clear the board \n\npress s to toggle test solve", 
                        font = 'Cambria 24 bold')
                    

    canvas.create_rectangle((4/5)*app.width - 160, app.height/3 + 150 - 20, 
                            (4/5)*app.width + 160, app.height/3 + 150 + 20,
                                fill = app.createReturnColorColor, width = 3)
    canvas.create_text((4/5)*app.width, app.height/3 + 150, 
                        text = f"return to main menu", 
                        font = 'Cambria 24 bold')

# draw/remove a square or an x or select a menu option
def create_with_colors_mousePressed(app, event):
    # left click, vs right click to draw an x
    # if i click on a box ..
    for color in range(len(app.colorSetColor)):
        if (3.4*app.width//5 + color * 80 < event.x < 3.4*app.width//5 + color * 80 + 60 and
                3.5*app.height//5 < event.y < 3.5*app.height//5 + 60):
            app.selectedColorColor = app.colorSetColor[color]

    # submission attempt uniqueness check
    if ((4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
        app.height/3 - 100 - 20 < event.y < app.height/3 - 100 + 20):
        app.createSubmitColorColor = 'gray60'
    # return to main menu
    elif ( (4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
    app.height/3 + 150 - 20 < event.y < app.height/3 + 150 + 20):
        app.createReturnColorColor = 'gray60'

    elif getCellCreateColor(app, event.x, event.y) != None:
        row, col = getCellCreateColor(app, event.x, event.y)
        if 0 <= row < app.createSizeColor and 0 <= col < app.createSizeColor:
            # draw square if click on empty
            if app.createSolvingModeColor == False:
                if app.createInputGridColor[row][col] == False:
                    cellColor = (app.selectedColorColor)
                    app.createInputGridColor[row][col] = (True, cellColor)
                    updateCluesColor(app)
                # remove square if click on square
                elif isinstance(app.createInputGridColor[row][col], tuple):
                    app.createInputGridColor[row][col] = False
                    updateCluesColor(app)
                # remove x if click on x
                elif app.createInputGridColor[row][col] == 'X':
                    app.createInputGridColor[row][col] = False

            elif app.createSolvingModeColor == True:
                if app.createSolverGridColor[row][col] == False:
                    cellColor = (app.selectedColorColor)
                    app.createSolverGridColor[row][col] = (True, cellColor)
                # remove square if click on square
                elif isinstance(app.createSolverGridColor[row][col], tuple):
                    app.createSolverGridColor[row][col] = False
                # remove x if click on x
                elif app.createSolverGridColor[row][col] == 'X':
                    app.createSolverGridColor[row][col] = False

# as usual
def create_with_colors_mouseReleased(app, event):
    # submit 
    if ((4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
        app.height/3 - 100 - 20 < event.y < app.height/3 - 100 + 20):
        BWequivalent = createBWequivalent(app.createInputGridColor)
        if BWUnique(BWequivalent) == True:
            # check for uniqueness
            app.createSubmitColorColor = 'gray79'
            app.createSubmissionMessageColor1 = 'this nonogram is unique'
            app.createSubmissionMessageColorColor = 'green'
        else:
            if app.createSizeColor == 5:
                app.createSubmissionMessageColor1 = 'the b/w version of this nonogram is not unique\n                                        so be careful!'
            elif app.createSizeColor == 10:
                app.createSubmissionMessageColor1 = f'add {howManyCellsDoWeStillNeed(BWequivalent)} more cells and i can almost guarantee\n       uniqueness, otherwise be careful!'
            elif app.createSizeColor == 15:
                app.createSubmissionMessageColor1 = f'add {howManyCellsDoWeStillNeed(BWequivalent)} more cells and i can almost guarantee\n       uniqueness, otherwise be careful!'
            elif app.createSizeColor == 20: 
                app.createSubmissionMessageColor1 = f'add {howManyCellsDoWeStillNeed(BWequivalent)} more cells and i can almost guarantee\n       uniqueness, otherwise be careful!'
            app.createSubmissionMessageColorColor = 'red'
        app.createSubmitColorColor = 'gray79'

    # return
    elif ( (4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
    app.height/3 + 150 - 20 < event.y < app.height/3 + 150 + 20):
        app.mode = 'splashScreenMode'
        app.createReturnColorColor = 'gray79'

# draws the menu palette that you can select "brush" color with
def drawColorPaletteColor(app, canvas):
    # width of lines
    gridWidth = 4
    for color in range(len(app.colorSetColor)):
        if app.selectedColorColor == app.colorSetColor[color]:
            canvas.create_rectangle(3.4*app.width//5 + color * 80, 3.5*app.height//5, 
                                3.4*app.width//5 + 60 + color * 80, 3.5*app.height//5 + 60,
                                fill = app.colorSetColor[color], width = gridWidth, outline = 'black')
        else:
            canvas.create_rectangle(3.4*app.width//5 + color * 80, 3.5*app.height//5, 
                                3.4*app.width//5 + 60 + color * 80, 3.5*app.height//5 + 60,
                                fill = app.colorSetColor[color], width = 0)

# draw x'es
def create_with_colors_rightMousePressed(app, event):
    if getCellCreateColor(app, event.x, event.y) != None:
            row, col = getCellCreateColor(app, event.x, event.y)
            if 0 <= row < app.createSizeColor and 0 <= col < app.createSizeColor:
                # right click empty -> x
                if app.createSolvingModeColor == False:
                    if app.createInputGridColor[row][col] == False:
                        app.createInputGridColor[row][col] = 'X'
                    # right click shaded -> x
                    elif isinstance(app.createInputGridColor[row][col], tuple):
                        app.createInputGridColor[row][col] = 'X'
                        updateCluesColor(app)
                    # right click x -> empty
                    elif app.createInputGridColor[row][col] == 'X':
                        app.createInputGridColor[row][col] = False
                        

                elif app.createSolvingModeColor == True:
                    if app.createSolverGridColor[row][col] == False:
                        app.createSolverGridColor[row][col] = 'X'
                    # right click shaded -> x
                    elif isinstance(app.createSolverGridColor[row][col], tuple):
                        app.createSolverGridColor[row][col] = 'X'
                    # right click x -> empty
                    elif app.createSolverGridColor[row][col] == 'X':
                        app.createSolverGridColor[row][col] = False
                
# keep drawing squares (some way to make dragging smoother?)
def create_with_colors_mouseDragged(app, event):
    if getCellCreateColor(app, event.x, event.y) != None:
            row, col = getCellCreateColor(app, event.x, event.y)
            if 0 <= row < app.createSizeColor and 0 <= col < app.createSizeColor:
                # draw square if click on empty or X
                if app.createSolvingModeColor == False:
                    if app.createInputGridColor[row][col] == False:
                        cellColor = (app.selectedColorColor)
                        app.createInputGridColor[row][col] = (True, cellColor)
                        updateCluesColor(app)
                    # remove x if click on x
                    elif app.createInputGridColor[row][col] == 'X':
                        app.createInputGridColor[row][col] = False

                elif app.createSolvingModeColor == True:
                    if app.createSolverGridColor[row][col] == False:
                        cellColor = (app.selectedColorColor)
                        app.createSolverGridColor[row][col] = (True, cellColor)

                    # remove x if click on x
                    elif app.createSolverGridColor[row][col] == 'X':
                        app.createSolverGridColor[row][col] = False
                    
# keep drawing x'es
def create_with_colors_rightMouseDragged(app, event):
    if getCellCreateColor(app, event.x, event.y) != None:
            row, col = getCellCreateColor(app, event.x, event.y)
            if 0 <= row < app.createSizeColor and 0 <= col < app.createSizeColor:
                # right click empty -> x
                if app.createSolvingModeColor == False:
                    if app.createInputGridColor[row][col] == False:
                        app.createInputGridColor[row][col] = 'X'
                    # right click shaded -> x
                    elif isinstance(app.createInputGridColor[row][col], tuple):
                        app.createInputGridColor[row][col] = 'X'
                        updateCluesColor(app)
                        

                elif app.createSolvingModeColor == True:
                    if app.createSolverGridColor[row][col] == False:
                        app.createSolverGridColor[row][col] = 'X'
                    # right click shaded -> x
                    elif isinstance(app.createSolverGridColor[row][col], tuple):
                        app.createSolverGridColor[row][col] = 'X'

# restart or change grid size or toggle solve
def create_with_colors_keyPressed(app, event):
    # solve it! clues will freeze
    if event.key == 's':
        if app.createSolvingModeColor == False:
            app.createSolvingModeColor = True
        elif app.createSolvingModeColor == True:
            app.createSolvingModeColor = False
    # clear
    elif event.key == 'c':
            app.createInputGridColor = [([False] * app.createSizeColor) for row in range(app.createSizeColor)]
            app.createSolverGridColor = [([False] * app.createSizeColor) for row in range(app.createSizeColor)]
            app.createHorizontalIslandsColor = colorCountHorizontalIslands(app.createInputGridColor)
            app.createVerticalIslandsColor = colorCountVerticalIslands(app.createInputGridColor)
            app.createSolvingModeColor = False
            app.createSubmissionMessageColor1 = ''

    # choose grid size
    elif event.key in string.digits:
        for i in range(1, 5):
            if int(event.key) == i:
                if app.createSizeColor != 5 *i: 
                    app.createSizeColor = 5 * i
                    app.createSolvedColor = False
                    app.createSubmissionMessageColor1 = ''
                    app.createInputGridColor = [([False] * app.createSizeColor) for row in range(app.createSizeColor)]
                    app.createSolverGridColor = [([False] * app.createSizeColor) for row in range(app.createSizeColor)]
                    app.createHorizontalIslandsColor = colorCountHorizontalIslands(app.createInputGridColor)
                    app.createVerticalIslandsColor = colorCountVerticalIslands(app.createInputGridColor)

# adapted from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
# if you click a square 
def getCellCreateColor(app, x, y):
    cellW = (app.height - 2*app.createWidthMarginColor) / app.createSizeColor
    cellH = (app.height - app.createTopHeightMarginColor - app.createBottomHeightMarginColor ) / app.createSizeColor
    if  (app.createWidthMarginColor < x < app.width - app.createWidthMarginColor
        and app.createTopHeightMarginColor < y < app.height - app.createBottomHeightMarginColor):
        row = int((y - app.createTopHeightMarginColor) / cellH)
        col = int((x - app.createWidthMarginColor) / cellH)
        return row, col
    else:
        return None

# adapted from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
def getCellBoundsCreateColor(app, row, col):
    cellW = (app.height - 2*app.createWidthMarginColor)/app.createSizeColor
    cellH = (app.height - app.createTopHeightMarginColor - app.createBottomHeightMarginColor )/app.createSizeColor
    x0 = app.createWidthMarginColor + col*cellH
    y0 = app.createTopHeightMarginColor + row*cellH
    x1 = x0 + cellH
    y1 = y0 + cellH
    return (x0, y0, x1, y1)

# drawn square bound
def getSquareBoundsCreateColor(app, row, col):
    cellW = (app.height - 2*app.createWidthMarginColor)/app.createSizeColor
    cellH = (app.height - app.createTopHeightMarginColor - app.createBottomHeightMarginColor)/app.createSizeColor
    x0, y0, x1, y1 = getCellBoundsCreateColor(app, row, col)
    if app.createSizeColor == 20:
        x0 += 0.18*cellH
        x1 -= 0.18*cellH
        y0 += 0.18*cellH
        y1 -= 0.18*cellH
    elif app.createSizeColor == 15:
        x0 += 0.15*cellH
        x1 -= 0.15*cellH
        y0 += 0.15*cellH
        y1 -= 0.15*cellH
    elif app.createSizeColor == 10:
        x0 += 0.1*cellH
        x1 -= 0.1*cellH
        y0 += 0.1*cellH
        y1 -= 0.1*cellH
    else:
        x0 += 0.07*cellH
        x1 -= 0.07*cellH
        y0 += 0.07*cellH
        y1 -= 0.07*cellH
    return x0, y0, x1, y1

def create_with_colors_redrawAll(app, canvas):
    drawCreateMenuColor(app, canvas)
    drawVisibleCreateGridColor(app, canvas)
    drawSolverCreateGridColor(app, canvas)
    drawColorPaletteColor(app, canvas)

#####################################
# 'nonorikabe' mode: 
#####################################

# this variant is very cool if you're into logic puzzles
# check out nurikabe
# it's also pretty challenging

def restartNonorikabe(app):
    app.BWSizeNono = 5
    app.BWSolvedGridNono = generateSolvedBWGrid(app.BWSizeNono)
    replaceSpaceIslandsNono(app.BWSolvedGridNono)

    # for numbers on edges
    app.BWHorizontalIslandsNono = BWcountHorizontalIslands(app.BWSolvedGridNono)
    app.BWVerticalIslandsNono = BWcountVerticalIslands(app.BWSolvedGridNono)
    # for drawing
    app.BWSolverGridNono = [([False] * app.BWSizeNono) for row in range(app.BWSizeNono)]
    app.BWTopHeightMarginNono = 1350 * (1 / app.BWSizeNono)
    app.BWBottomHeightMarginNono = 500 * (1 / app.BWSizeNono)
    app.BWWidthMarginNono = (app.width / 2 - app.BWTopHeightMarginNono) / 1.9
    
    # keeping score
    app.BWTimeNono = 0.0
    app.BWSessionBestNono = [0.0] * (4)
    app.BWSolvedNono = False

    app.BWSubmissionMessageNono = ''
    app.BWSubmissionMessageColorNono = 'red'
    app.BWSubmitButtonMessageNono = 'submit'
    app.BWReturnColorNono = 'gray79'
    app.BWSubmitColorNono = 'gray79'

# draws at the toppest then leftest cell of each space island: the value of that spaceisland
# by replacing False with str(number of touching falses) for each false island
# this is very cool 
# it uses backtracking to count the number of Falses in each pool of Falses
def replaceSpaceIslandsNono(grid):
    size = len(grid)
    markedGrid = copy.deepcopy(grid)
    gridClues = dict()
    for row in range(size):
        for col in range(size):
            if markedGrid[row][col] == False: # new island
                totalSpaces = 0
                startRow, startCol = row, col # store coords of the space we're marking
                gridClues[startRow, startCol] = 0
                # ok we hit a False, so we want to count every False that touches it
                addedSpaces, oceanCoords = countFalseOcean(markedGrid, row, col) # return how many were covered and what they were
                totalSpaces += addedSpaces
                for row3 in range(size):
                    for col3 in range(size):
                        if (row3, col3) in oceanCoords:
                            markedGrid[row3][col3] = 'passed'
                gridClues[startRow, startCol] += totalSpaces
    for clue in gridClues:
        row, col = clue
        grid[row][col] = gridClues[clue]

# counts each pool               
def countFalseOcean(markedGrid, startRow, startCol):
    size = len(markedGrid)
    oceanSpaces = 0
    covered = set() # set of passed coords
    for row1 in range(size):
        for col1 in range(size):
            if markedGrid[row1][col1] == False:
                if existsPath(markedGrid, startRow, startCol, row1, col1): 
                    oceanSpaces += 1
                    covered.add((row1, col1))
    return oceanSpaces, covered

# backtracking! are the Falses touching?
def existsPath(markedGrid, startRow, startCol, row, col):
    return existsPathHelper(markedGrid, startRow, startCol, row, col , set())

# yeah this is cool
# with help from https://www.kosbie.net/cmu/spring-21/15-112/notes/notes-recursion-part2.html#mazeSolving
def existsPathHelper(markedGrid, startRow, startCol, row, col , visited):
    # base case
    if (row, col) in visited: 
        return False
    visited.add((row, col))
    if (row,col) == (startRow, startCol): # they're the same so they touch
        return True
    # recursive case
    else:
        directions = [(-1,0), (0,-1), (0,1), (1,0)]
        for dir in directions:
            drow, dcol = dir
            if (0 <= row + drow < len(markedGrid) and 
                0 <= col + dcol < len(markedGrid)):
                if markedGrid[row+drow][col+dcol] == False: # if it is touching the next False
                    if existsPathHelper(markedGrid, startRow, startCol, row + drow , col + dcol, visited):
                        return True
        visited.remove((row, col))
        return False

# draw/remove a square or an x or select a menu option
def nonorikabe_mousePressed(app, event):
    # left click, vs right click to draw an x
    # if i click on a box ..
    # submission attempt
    if ((4/5)*app.width - 60 < event.x < (4/5)*app.width + 60 and
        app.height/3 - 100 - 20 < event.y < app.height/3 - 100 + 20):
        app.BWSubmitColorNono = 'gray60'
    # return to main menu
    elif ( (4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
    app.height/3 + 150 - 20 < event.y < app.height/3 + 150 + 20):
        app.BWReturnColorNono = 'gray60'

    elif getCellNono(app, event.x, event.y) != None:
        row, col = getCellNono(app, event.x, event.y)
        if 0 <= row < app.BWSizeNono and 0 <= col < app.BWSizeNono:
            if isinstance(app.BWSolvedGridNono[row][col], int) and not isinstance(app.BWSolvedGridNono[row][col], bool):
                pass
            # draw square if click on empty
            elif app.BWSolverGridNono[row][col] == False:
                app.BWSolverGridNono[row][col] = True
             
            # remove square if click on square
            elif app.BWSolverGridNono[row][col] == True:
                app.BWSolverGridNono[row][col] = False
            # remove x if click on x
            elif app.BWSolverGridNono[row][col] == 'X':
                app.BWSolverGridNono[row][col] = False

# after correct submission click 1
def submittedOnceNono(app):
    app.BWSubmissionMessageNono = 'complete! press enter again to refresh'
    app.BWSubmitButtonMessageNono = 'new'
    app.BWSubmissionMessageColorNono = 'green'
    app.BWSolvedNono = True
    if app.BWTimeNono < app.BWSessionBestNono[app.BWSizeNono // 5 - 1] or app.BWSessionBestNono[app.BWSizeNono // 5 - 1] == 0.0:
        app.BWSessionBestNono[app.BWSizeNono // 5 - 1] = app.BWTimeNono
    app.BWTimeNono = 0

#after correct submission click 2
def submittedTwiceNono(app):
    app.BWSolvedNono = False
    app.BWTimeNono = 0
    app.BWSolvedGridNono = generateSolvedBWGrid(app.BWSizeNono)
    replaceSpaceIslandsNono(app.BWSolvedGridNono)
    app.BWHorizontalIslandsNono = BWcountHorizontalIslands(app.BWSolvedGridNono)
    app.BWVerticalIslandsNono = BWcountVerticalIslands(app.BWSolvedGridNono)
    app.BWSolverGridNono = [([False] * app.BWSizeNono) for row in range(app.BWSizeNono)]
    app.BWSubmissionMessageNono = ''

# for box selection highlighting
def nonorikabe_mouseReleased(app, event):
    # submit
    if ((4/5)*app.width - 60 < event.x < (4/5)*app.width + 60 and
        app.height/3 - 100 - 20 < event.y < app.height/3 - 100 + 20 and
        app.BWSolvedNono == False):
        if solverMatchesSolved(app.BWSolverGridNono, app.BWSolvedGridNono):
                submittedOnceNono(app)
                app.BWSubmitColorNono = 'gray79'
            # counter stop
        else:
            app.BWSubmissionMessageNono = 'solution is incomplete or incorrect'
            app.BWSubmissionMessageColorNono = 'red'
            app.BWSubmitColorNono = 'gray79'
    elif ((4/5)*app.width - 60 < event.x < (4/5)*app.width + 60 and
        app.height/3 - 100 - 20 < event.y < app.height/3 + 100 + 20 and
        app.BWSolvedNono == True):
            submittedTwiceNono(app)
            app.BWSubmitColorNono = 'gray79'
    # return
    elif ( (4/5)*app.width - 160 < event.x < (4/5)*app.width + 160 and
    app.height/3 + 150 - 20 < event.y < app.height/3 + 150 + 20):
        app.mode = 'splashScreenMode'
        app.BWReturnColorNono = 'gray79'

# draw x'es
def nonorikabe_rightMousePressed(app, event):
    if getCellNono(app, event.x, event.y) != None:
            row, col = getCellNono(app, event.x, event.y)
            if 0 <= row < app.BWSizeNono and 0 <= col < app.BWSizeNono:
                # right click empty -> x
                if isinstance(app.BWSolvedGridNono[row][col], int) and not isinstance(app.BWSolvedGridNono[row][col], bool):
                    pass
                elif app.BWSolverGridNono[row][col] == False:
                    app.BWSolverGridNono[row][col] = 'X'
                # right click shaded -> x
                elif app.BWSolverGridNono[row][col] == True:
                    app.BWSolverGridNono[row][col] = 'X'
                # right click x -> empty
                elif app.BWSolverGridNono[row][col] == 'X':
                    app.BWSolverGridNono[row][col] = False
                
# keep drawing squares 
def nonorikabe_mouseDragged(app, event):
    if getCellNono(app, event.x, event.y) != None:
            row, col = getCellNono(app, event.x, event.y)
            if 0 <= row < app.BWSizeNono and 0 <= col < app.BWSizeNono:
                # draw square if click on empty or X
                if isinstance(app.BWSolvedGridNono[row][col], int) and not isinstance(app.BWSolvedGridNono[row][col], bool):
                    pass
                elif app.BWSolverGridNono[row][col] == 'X':
                    app.BWSolverGridNono[row][col] = True
                elif app.BWSolverGridNono[row][col] == False:
                    app.BWSolverGridNono[row][col] = True
                
# keep drawing x'es
def nonorikabe_rightMouseDragged(app, event):
    if getCellNono(app, event.x, event.y) != None:
            row, col = getCellNono(app, event.x, event.y)
            if 0 <= row < app.BWSizeNono and 0 <= col < app.BWSizeNono:
                if isinstance(app.BWSolvedGridNono[row][col], int) and not isinstance(app.BWSolvedGridNono[row][col], bool):
                    pass
                # right click empty -> x
                elif app.BWSolverGridNono[row][col] == False:
                    app.BWSolverGridNono[row][col] = 'X'
                # right click shaded -> x
                elif app.BWSolverGridNono[row][col] == True:
                    app.BWSolverGridNono[row][col] = 'X'

# adapted from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
# if you click a square 
def getCellNono(app, x, y):
    cellW = (app.height - 2*app.BWWidthMarginNono) / app.BWSizeNono
    cellH = (app.height - app.BWTopHeightMarginNono - app.BWBottomHeightMarginNono ) / app.BWSizeNono
    if  (app.BWWidthMarginNono < x < app.width - app.BWWidthMarginNono
        and app.BWTopHeightMarginNono < y < app.height - app.BWBottomHeightMarginNono):
        row = int((y - app.BWTopHeightMarginNono) / cellH)
        col = int((x - app.BWWidthMarginNono) / cellH)
        return row, col
    else:
        return None

# adapted from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
def getCellBoundsNono(app, row, col):
    cellW = (app.height - 2*app.BWWidthMarginNono)/app.BWSizeNono
    cellH = (app.height - app.BWTopHeightMarginNono - app.BWBottomHeightMarginNono )/app.BWSizeNono
    x0 = app.BWWidthMarginNono + col*cellH
    y0 = app.BWTopHeightMarginNono + row*cellH
    x1 = x0 + cellH
    y1 = y0 + cellH
    return (x0, y0, x1, y1)

# draws the squares / x'es 
def drawSolverBWGridNono(app, canvas):
    for row in range(app.BWSizeNono):
        for col in range(app.BWSizeNono):
            if 0 <= row < len(app.BWSolverGridNono) and 0 <= col < len(app.BWSolverGridNono[0]):
                if app.BWSolverGridNono[row][col] == True:
                    (BWx0, BWx1, BWy0, BWy1) = getSquareBoundsNono(app, row, col)
                    canvas.create_rectangle(BWx0, BWx1, 
                                            BWy0, BWy1,
                                            fill = 'black')
                elif app.BWSolverGridNono[row][col] == 'X':
                    x0, y0, x1, y1 = getCellBoundsNono(app, row, col)
                    canvas.create_text((x0 + x1)/2, 
                                        (y0 + y1)/2, 
                                        text = 'X', fill = 'red', 
                                        font = f'Arial { (36 * 5) // app.BWSizeNono } bold')
                elif isinstance(app.BWSolvedGridNono[row][col], bool) == False:
                        x0, y0, x1, y1 = getCellBoundsNono(app, row, col)
                        if app.BWSolvedGridNono[row][col] != False:
                            canvas.create_text((x0 + x1)/2, 
                                        (y0 + y1)/2, 
                                        text = str(app.BWSolvedGridNono[row][col]), fill = 'black', 
                                        font = f'Arial { (36 * 5) // app.BWSizeNono } bold')

# tiny part of this was adapted from: 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
# draw the empty grid with the number clues
def drawVisibleBWGridNono(app, canvas):
    if app.BWSizeNono < 11:
        gridWidth = 4
    else:
        gridWidth = 2
    # determine longest row clue:
    longestRow = 0
    for row in range(len(app.BWHorizontalIslandsNono)):
        counter = 0
        for clue in range(len(app.BWHorizontalIslandsNono[row])):
            counter += 1
        if counter >= longestRow:
            longestRow = counter
    # determine longest column clue
    longestCol = 0
    for row in range(len(app.BWVerticalIslandsNono)):
        counter = 0
        for clue in range(len(app.BWVerticalIslandsNono[row])):
            counter += 1
        if counter >= longestCol:
            longestCol = counter
    # draw grid
    for row in range(app.BWSizeNono):
        for col in range(app.BWSizeNono):
            x0, y0, x1, y1 = getCellBoundsNono(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, width = gridWidth)
    # draw row clues
    for row in range(len(app.BWHorizontalIslandsNono)):
        if row % 2 == 0:
            x0, y0, x1, y1 = getCellBoundsNono(app, row, 0)
            canvas.create_rectangle(x0 - longestRow * (x1 - x0), y0, x0, y1, width = gridWidth)
            s = ''
            if app.BWHorizontalIslandsNono[row] == []:
                s += '0'
            else:
                for clue in range(len(app.BWHorizontalIslandsNono[row])):
                    s += str(app.BWHorizontalIslandsNono[row][clue])
                    s += '  '    
            canvas.create_text((x0 - longestRow * (x1 - x0) + x0)/2, (y0 + y1)/2,
                                text = s, font = f'Arial {(50 * 5) // app.BWSizeNono} bold')
        else:
            x0, y0, x1, y1 = getCellBoundsNono(app, row, 0)
            canvas.create_rectangle(x0 - longestRow * (x1 - x0), y0, x0, y1, width = gridWidth)
            s = ''
            if app.BWHorizontalIslandsNono[row] == []:
                s += '?'
            else:
                for clue in range(len(app.BWHorizontalIslandsNono[row])):
                    s += '?'
                    s += '  '    
            canvas.create_text((x0 - longestRow * (x1 - x0) + x0)/2, (y0 + y1)/2,
                                text = s, font = f'Arial {(50 * 5) // app.BWSizeNono} bold')
    # draw col clues
    for row in range(len(app.BWVerticalIslandsNono)):
        if row % 2 == 0:
            x0, y0, x1, y1 = getCellBoundsNono(app, 0, row)
            canvas.create_rectangle(x0, y0 - longestCol * (y1 - y0), x1, y0, width = gridWidth)
            s = ''
            if app.BWVerticalIslandsNono[row] == []:
                s += '0'
                s += '\n'
            else:
                for clue in range(len(app.BWVerticalIslandsNono[row])):
                    s += str(app.BWVerticalIslandsNono[row][clue])
                    s += '\n'    
            canvas.create_text((x0 + x1)/2, ((y0 - longestCol * (y1 - y0)) + y0 )/2 + 140 // app.BWSizeNono,
                                text = s, font = f'Arial {(50 * 5) // app.BWSizeNono} bold')
        else:
            x0, y0, x1, y1 = getCellBoundsNono(app, 0, row)
            canvas.create_rectangle(x0, y0 - longestCol * (y1 - y0), x1, y0, width = gridWidth)
            s = ''
            if app.BWVerticalIslandsNono[row] == []:
                s += '?'
                s += '\n'
            else:
                for clue in range(len(app.BWVerticalIslandsNono[row])):
                    s += '?'
                    s += '\n'    
            canvas.create_text((x0 + x1)/2, ((y0 - longestCol * (y1 - y0)) + y0 )/2 + 140 // app.BWSizeNono,
                                text = s, font = f'Arial {(50 * 5) // app.BWSizeNono} bold')
            
# drawn square bound
def getSquareBoundsNono(app, row, col):
    cellW = (app.height - 2*app.BWWidthMarginNono)/app.BWSizeNono
    cellH = (app.height - app.BWTopHeightMarginNono - app.BWBottomHeightMarginNono )/app.BWSizeNono
    x0, y0, x1, y1 = getCellBoundsNono(app, row, col)
    if app.BWSizeNono == 20:
        x0 += 0.18*cellH
        x1 -= 0.18*cellH
        y0 += 0.18*cellH
        y1 -= 0.18*cellH
    elif app.BWSizeNono == 15:
        x0 += 0.15*cellH
        x1 -= 0.15*cellH
        y0 += 0.15*cellH
        y1 -= 0.15*cellH
    elif app.BWSizeNono == 10:
        x0 += 0.1*cellH
        x1 -= 0.1*cellH
        y0 += 0.1*cellH
        y1 -= 0.1*cellH
    else:
        x0 += 0.07*cellH
        x1 -= 0.07*cellH
        y0 += 0.07*cellH
        y1 -= 0.07*cellH
    return x0, y0, x1, y1
    
# restart or change grid size 
def nonorikabe_keyPressed(app, event):
    if event.key == 'r':
        app.BWSolvedNono = False
        app.BWSolvedGridNono = generateSolvedBWGrid(app.BWSizeNono)
        replaceSpaceIslandsNono(app.BWSolvedGridNono)
        app.BWHorizontalIslandsNono = BWcountHorizontalIslands(app.BWSolvedGridNono)
        app.BWVerticalIslandsNono = BWcountVerticalIslands(app.BWSolvedGridNono)
        app.BWSolverGridNono = [([False] * app.BWSizeNono) for row in range(app.BWSizeNono)]
        app.BWSubmissionMessageNono = ''
        app.BWTimeNono = 0
    # choose grid size
    elif event.key in string.digits:
        for i in range(1, 5):
            if int(event.key) == i:
                if app.BWSizeNono != 5 *i: 
                    app.BWSizeNono = 5 * i
                    app.BWSolvedNono = False
                    app.BWSubmissionMessageNono = ''
                    app.BWTimeNono = 0
                    app.BWSolverGridNono = [([False] * app.BWSizeNono) for row in range(app.BWSizeNono)]
                    app.BWSolvedGridNono = generateSolvedBWGrid(app.BWSizeNono)
                    replaceSpaceIslandsNono(app.BWSolvedGridNono)
                    app.BWHorizontalIslandsNono = BWcountHorizontalIslands(app.BWSolvedGridNono)
                    app.BWVerticalIslandsNono = BWcountVerticalIslands(app.BWSolvedGridNono)
    elif event.key == 'Enter' and app.BWSolvedNono != True:
        if solverMatchesSolved(app.BWSolverGridNono, app.BWSolvedGridNono):
            submittedOnceNono(app)
        else:
            app.BWSubmissionMessageNono = 'solution is incomplete or incorrect'
            app.BWSubmissionMessageColorNono = 'red'
    elif event.key == 'Enter' and app.BWSolvedNono == True:
            submittedTwiceNono(app)
           
# keep a counter for each run
def nonorikabe_timerFired(app):
    if app.BWSolvedNono == False:
        app.BWTimeNono += 0.1

# draws boxes for menu
def drawBWMenuNono(app, canvas):
    # back button to main mode, submit
    # display: size, score, correctness, best session time
    canvas.create_text((4/5)*app.width, app.height/3 - 180, 
                    text = f"{app.BWSizeNono}x{app.BWSizeNono} nonorikabe", 
                    font = 'Cambria 24 bold')

    canvas.create_text((4/5)*app.width, app.height/3 -150, 
                    text = f"{app.BWSubmissionMessageNono}", 
                    font = 'Cambria 18 bold', fill = app.BWSubmissionMessageColorNono)   

    canvas.create_rectangle((4/5)*app.width - 60, app.height/3 - 100 - 20, 
                            (4/5)*app.width + 60, app.height/3 -100 + 20,
                                fill = app.BWSubmitColorNono, width = 3)
    canvas.create_text((4/5)*app.width, app.height/3 - 100, 
                        text = "submit", 
                        font = 'Cambria 24 bold')   

    canvas.create_text((4/5)*app.width, app.height/3 - 20, 
                        text = "press 1-4 to change grid size \n         press enter to submit \n       press r for a new puzzle", 
                        font = 'Cambria 24 bold')
                    
    canvas.create_text((4/5)*app.width, app.height/3 + 70, 
                        text = f"session best: {round(app.BWSessionBestNono[app.BWSizeNono // 5 - 1], 3)} \n latest time: {round(app.BWTimeNono, 3)}", 
                        font = 'Cambria 24 bold')   


    canvas.create_rectangle((4/5)*app.width - 160, app.height/3 + 150 - 20, 
                            (4/5)*app.width + 160, app.height/3 + 150 + 20,
                                fill = app.BWReturnColorNono, width = 3)
    canvas.create_text((4/5)*app.width, app.height/3 + 150, 
                        text = f"return to main menu", 
                        font = 'Cambria 24 bold')

def nonorikabe_redrawAll(app, canvas):
    drawVisibleBWGridNono(app, canvas)
    drawSolverBWGridNono(app, canvas)
    drawBWMenuNono(app, canvas)

# and finally...
runApp(width=1536, height=801)

