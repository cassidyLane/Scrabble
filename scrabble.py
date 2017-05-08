#Scrabble AI                                                                   
import random
import string
word_list = []

f = open('words.txt', 'r')

for word in f:
    word_list.append(word.strip().lower())

class Board:
    def __init__(self, size, board, trie):
        self.size = size
        self.board = board
        self.trie = trie


    #this can print out an empty board if needed
    def boardSize(self):
        board = []
        row = [int('-1')] * self.size

        for x in range(self.size):
            board.append(row)
            
        return board

    def printBoard(self):
        for row in self.board:
            print ('\n', end = ' ')
            for letter in row:
                if letter == -1:
                    print ('__', end = ' ')
                else:
                    print (letter.upper() + ' ', end = ' ')

    #Calculates the score of the boad
    #Based only on the letters, as we didn't use the board scoring spaces
    def score(self, word):
        total = 0
        score_dict = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, "x": 8, "z": 10}
        word = word.lower()
        
        for letter in word:
            total += score_dict[letter]
        return total
    
    #Gets a column of a given index
    def getCol(self, colNum):
        colList = []
        for x in range(self.size):
            colList.append(self.board[x][colNum])
        return(colList)

    #Makes sure every collection of letters on the board is a word
    def validBoard(self):
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if(self.board[x][y] != -1):
                    col = self.getCol(y)
                    row = self.board[x]
                    rowChunk = ""
                    for entry in range(y-1, -1, -1):
                        if(row[entry] == -1):
                            break
                        else:
                            rowChunk += row[entry]
                    rowChunk = rowChunk[::-1]
                    rowChunk = rowChunk + row[y]
                    for entry in range(y+1, len(row)):
                        if(row[entry] == -1):
                            break
                        else:
                            rowChunk += row[entry]
                    colChunk = ""
                    for entry in range(x-1, -1, -1):
                        if(col[entry] == -1):
                            break
                        else:
                            colChunk += col[entry]
                    colChunk = colChunk[::-1]
                    colChunk = colChunk + col[x]
                    for entry in range(x+1, len(col)):
                        if(col[entry] == -1):
                            break
                        else:
                            colChunk += col[entry]
                    oneLetterWord = True
                    if(len(rowChunk) > 1):
                        oneLetterWord = False
                        if(not(self.trie.isWord(rowChunk.lower()))):
                            return False
                    if(len(colChunk) > 1):
                        oneLetterWord = False
                        if(not(self.trie.isWord(colChunk.lower()))):
                            return False
                    if(oneLetterWord):
                        return False
        return True

    #Updates a certain column on the board
    def replaceRow(self, newRow, rowInd):
        self.board[rowInd] = newRow
    
    #Updates a certain row on the board
    def replaceCol(self, newCol, colInd):
        for x in range(self.size):
            self.board[x][colInd] = newCol[x]
                
    #Converts a move to a playable row/col
    def convertToRowCol(self, move):
        newRowCol = []
        for x in range(0, move[1]):
            if(move[3] == "row"):
                newRowCol.append(self.board[move[4]][x])
            else:
                newRowCol.append(self.board[x][move[4]])
        for letter in move[0]:
            newRowCol.append(letter)
        for x in range(move[1] + len(move[0]), self.size):
            if(move[3] == "row"):
                newRowCol.append(self.board[move[4]][x])
            else:
                newRowCol.append(self.board[x][move[4]])
        return(newRowCol)

    #Makes sure that a move is valid
    def validMove(self, rowCol, move):
        newBoard = []
        for x in self.board:
            r = []
            for y in x:
                r.append(y)
            newBoard.append(r)
        nBoard = Board(self.size, newBoard, self.trie)
        if(move[3] == "row"):
            nBoard.replaceRow(rowCol, move[4])
        else:
            nBoard.replaceCol(rowCol, move[4])
        if(nBoard.validBoard()):
            return True
        else:
            return False

    #Finds all the words a player can make
    def findWords(self, rack):
        pMoves = []
        for x in range(self.size):
            row = self.board[x]
            self.trie.findAllWords(row, row, rack, self.trie.head, "", 0, self.trie.getChunkNumber(row), 0, self.size)
            rowMoves = self.trie.possWords
            self.trie.possWords = []
            col = self.getCol(x)
            self.trie.findAllWords(col, col, rack, self.trie.head, "", 0, self.trie.getChunkNumber(col), 0, self.size)
            colMoves = self.trie.possWords
            self.trie.possWords = []
            for move in rowMoves:
                moveAdd = move + ("row",x)
                nRow = self.convertToRowCol(moveAdd)
                if(self.validMove(nRow, moveAdd)):
                    pMoves.append(moveAdd)
            for move in colMoves:
                moveAdd = move + ("col",x)
                nCol = self.convertToRowCol(moveAdd)
                if(self.validMove(nCol, moveAdd)):
                    pMoves.append(moveAdd)
        return(pMoves)

    def getAllWordsOnBoard(self):
        words = []
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if(self.board[x][y] != -1):
                    col = self.getCol(y)
                    row = self.board[x]
                    rowChunk = ""
                    for entry in range(y-1, -1, -1):
                        if(row[entry] == -1):
                            break
                        else:
                            rowChunk += row[entry]
                    rowChunk = rowChunk[::-1]
                    rowChunk = rowChunk + row[y]
                    for entry in range(y+1, len(row)):
                        if(row[entry] == -1):
                            break
                        else:
                            rowChunk += row[entry]
                    colChunk = ""
                    for entry in range(x-1, -1, -1):
                        if(col[entry] == -1):
                            break
                        else:
                            colChunk += col[entry]
                    colChunk = colChunk[::-1]
                    colChunk = colChunk + col[x]
                    for entry in range(x+1, len(col)):
                        if(col[entry] == -1):
                            break
                        else:
                            colChunk += col[entry]
                    rowChunk = rowChunk.upper()
                    colChunk = colChunk.upper()
                    if(len(rowChunk) > 1):
                        if(self.trie.isWord(rowChunk.lower())):
                            if(rowChunk not in words):
                                words.append(rowChunk)
                    if(len(colChunk) > 1):
                        if(self.trie.isWord(colChunk.lower())):
                            if(colChunk not in words):
                                words.append(colChunk)
        return(words)

                
                

    #Chooses the word with the highest score from a list of moves
    def pickWord(self, lom):
        maxMove = lom[0]
        maxPoint = self.score(maxMove[0])
        for move in lom:
            possPoint = 0
            newBoard = []
            for x in self.board:
                r = []
                for y in x:
                    r.append(y)
                newBoard.append(r)
            nBoard = Board(self.size, newBoard, self.trie)
            if(move[3] == "row"):
                rowCol = self.convertToRowCol(move)
                nBoard.replaceRow(rowCol, move[4])
            else:
                rowCol = self.convertToRowCol(move)
                nBoard.replaceCol(rowCol, move[4])
            
            wordsOnOrigBoard = self.getAllWordsOnBoard()
            wordsOnNewBoard = nBoard.getAllWordsOnBoard()
            for w in wordsOnNewBoard:
                if(w not in wordsOnOrigBoard):
                    possPoint += self.score(w)

            if(possPoint > maxPoint):
                maxMove = move
                maxPoint = possPoint
            
        return((maxMove, maxPoint))

    #Def called on a board and given a rack, tells the player which move they should make.
    def whichWord(self, rack):
        print("\nThe player's board is: ")
        self.printBoard()
        print("\nThe player's rack is: " + str(rack))
        pMoves = self.findWords(rack)
        if(len(pMoves) == 0):
            print("\nSorry; it looks like you can't make any moves with that board!")
        else:
            print("\n")
            moveToMake = self.pickWord(pMoves)
            print("The player should play " + moveToMake[0][0] + " in " + moveToMake[0][3] + " " + str(moveToMake[0][4]) + " at index " + str(moveToMake[0][1]) + " for " + str(moveToMake[1]) + " points.")
            print("\nThis will result in the board:\n ")
            if(moveToMake[0][3] == "row"):
                self.replaceRow(self.convertToRowCol(moveToMake[0]), moveToMake[0][4])
            else:
                self.replaceCol(self.convertToRowCol(moveToMake[0]), moveToMake[0][4])
            self.printBoard()
            print("\n")


class Node:
    val = ""
    aWord = False
    children = dict()

    def __init__(self):
        self.val = ""
        self.aWord = False
        self.children = dict()

    def __init__(self, val, aWord, children):
        self.val = val
        self.aWord = aWord
        self.children = children

    def __getitem__(self, key):
        return(self.children[key])

    def addChild(self,key):
        self.children[key] = Node(key, False, dict())

    def getChildren(self):
        return(self.children)

class Trie:
    def __init__(self):
        self.head = Node("",False,dict())

    def __getitem__(self, key):
        return self.head.children[key]

    def add_word(self, word):
        current = self.head
        letter = 0

        c_child = []
        for child in current.children:
            c_child.append(child)
 
        for i in range(len(word)):
            if word[0:i+1] in c_child:
                current = current.children[word[0:i+1]]
                letter += 1

                c_child = []
                for child in current.children:
                    c_child.append(child)

            else:
                while letter < len(word):
                    current.addChild(word[0:letter+1])
                    current = current.children[word[0:letter+1]]
                    letter += 1

                    c_child = []
                    for child in current.children:
                        c_child.append(child)

        current.aWord = True


    #The following are all helper functions for findAllWords
    #Gets the number of "chunks" in a given section of the board
    #Takes a section of a board(a row/column) as a list, and returns an integer that 
    # represents the amount of collections of adjacent letters.
    def getChunkNumber(self, row_col):
        chunkz = []
        curr = ""
        for x in row_col:
            if(x == -1):
                if(curr != ""):
                    chunkz.append(curr)
                curr = ""
            else:
                curr += x

        return len(chunkz)
    
    #Checks whether or not a give section of the board is empty
    #Takes a section of a board(a row/column) as a list, and returns a boolean
    def isEmpty(self, row_col):
        for x in row_col:
            if(x != -1):
                return False
        return True

    #Finds the beginning of the first "chunk" on the board
    #Takes a section of a board(a row/column) as a list, and returns a tuple of a
    # letter, which is the first letter in the section, and an integer, which is that
    # letter's index on the board.
    def findBeginning(self, row_col):
        for x in range(len(row_col)):
            if(row_col[x] != -1):
                return(row_col[x], x)

    #Finds the end of the first "chunk" on the board
    #Takes a section of a board(a row/column) as a list, and returns
    # an integer which is the index of the last letter in the first chunk
    # on the board
    def findEnding(self, row_col):
        for x in range(len(row_col)):
            if(row_col[x] == -1):
                return(x-1)
        return(-5)
    
    #Ensures that if this word is placed in the section of the board,
    # it will be a valid move.
    #Takes a section of a board(a row/column) as a list, a word to add to the section, and 
    # an integer that is the index that the word will be added at
    #Returns a boolean
    def isValid(self, row_col, word, startingInd):
        wordCheck = ""
        #If there are letters right before this word, it will be a part of the word on the board
        #We don't want these letters to be included in the word.
        if(startingInd > 0):
            for a in range(startingInd-1, -1, -1):
                if(row_col[a] != -1):
                    wordCheck += row_col[a]
                else:
                    break
        
        #Don't want to overwrite any letters already on the board
        for x  in range(len(word)):
            if(row_col[x+startingInd] != -1):
                wordCheck += row_col[x+startingInd].lower()
            else:
                wordCheck += word[x]

        #If there are letters right after this word, they will be a part of the word on the board
        #Don't want these letters to be included in the word.
        y = len(wordCheck) + startingInd
        if(len(row_col) > y):
            for z in range(y, len(row_col)):
                if(row_col[z] == -1):
                    break
                else:
                    wordCheck += row_col[z].lower()
        #If putting the word on the board won't change its value, it's a valid word to play.
        if(wordCheck == word):
            return True
        else:
            return False

    #To hold possible words for DP
    possWords = []

    #A monster of a function
    #Finds all the words that the player could play based on one section of the board and their rack
    #Takes: a section of a board(a row/column) as a list -- to keep track of the original value of the section
    #       the same section of the board that is mutable
    #       a list of strings that represents the player's rack
    #       a node that represents the current node the function should look at -- the initial call should always be self.head
    #       a string that represents the current string that is being built as a possible word -- the initial call should always be ""
    #       an integer that represents the number of "chunks" the program has already added to the path -- the initial call should always be 0
    #       an integer that represents the total number of "chunks" on the board
    #       an integer that represents where the word will be placed on the board -- to keep track of where the word will start -- the initial call should always be 0
    #Adds tuples to the possWords list in the form of (String - word to play, Integer - starting index of the word to play, Set of Strings - The player's rack after using letters
    #                                                                                                                                         to make the word to play)
    def findAllWords(self, origRow_col, row_col, rack, currNode, currPath, currChunks, totChunks, startingInd, boardSize):
        # Looks at the possibility of playing every letter in the player's rack
        for x in range(len(rack)):
            #Initializes the values that will change by the next call of the function
            newStartingInd = startingInd
            newChunks = currChunks
            letter = rack[x].lower()
            potNodVal = currPath+letter
            begOfBoard = ("",-1)
            if(not(self.isEmpty(row_col))):
                begOfBoard = self.findBeginning(row_col)
            potVal = "NULLNULLNULL"
            if(not(begOfBoard[0] == "")):
                potVal = currPath + begOfBoard[0].lower()
            
            #First tries to make words with the letters in the player's rack
            #if the path + the next letter in the rack is a child of the current node in the trie, add it to the path,
            # check if it's a word, and keep going.
            if(potNodVal in currNode.children):
                newNode = currNode.children[potNodVal]
                newRack = rack[:x] + rack[x+1:]
                potWord = (potNodVal, startingInd, set(newRack))
                if(self.isWord(potNodVal) and (newChunks >= 1) and (potWord not in self.possWords) and (startingInd > -1) and (startingInd+len(potNodVal) < boardSize)):
                    if(self.isValid(origRow_col, potNodVal, startingInd)):
                        self.possWords.append((potNodVal, startingInd, set(newRack)))
                
                #If there are no more letters in the player's rack, the function ends
                if(not(len(rack) == 0)):
                    self.findAllWords(origRow_col, row_col, newRack, newNode, potNodVal, newChunks, totChunks, startingInd, boardSize)

            #Then tries to make words with the letters already on the board
            #if the path + the first letter on the board is a child of the current node in the trie, add it and all the letters after it(until an empty space) to the path,
            # check it it's a word, then continue on
            if(potVal in currNode.children):
                if(newStartingInd == 0):
                    newStartingInd = begOfBoard[1] - len(potVal) + 1
                newNode = currNode.children[potVal]
                newRowCol = row_col[begOfBoard[1] + 1:]
                endOfChunk = self.findEnding(newRowCol)
                y = 1
                broke = False
                while(y < endOfChunk+2):
                    potVal = potVal + newRowCol[y-1].lower()
                    if(potVal in newNode.children):
                        newNode = newNode.children[potVal]
                        y += 1
                    else:
                        broke = True
                        break
 #               if(y == -5):
  #                  broke = True
                if(not(broke)):
                    newChunks += 1 
                    newRowCol = newRowCol[endOfChunk+1:]
                potWord = (potVal, newStartingInd, set(rack))
                if(self.isWord(potVal) and (newChunks >= 1) and (potWord not in self.possWords) and (newStartingInd > -1) and (newStartingInd+len(potVal) < boardSize)):
                    if(self.isValid(origRow_col, potVal, newStartingInd)):
                        if(potVal == "belcog"):
                            print("Belcog found")
                        self.possWords.append((potVal, newStartingInd, set(rack)))
                self.findAllWords(origRow_col, newRowCol, rack, newNode, potVal, newChunks, totChunks, newStartingInd, boardSize)
            

    
            
    def printTrie(self, start): 
        print(start.val)
        for key in start.children:
            self.printTrie(start.children[key])

    #this function returns True/False depending on if the word is a word or not
    def isWord(self, word):
        current = self.head
        exists = True

        for letter in range(len(word)):
            if word[0:letter+1] in current.children:
                current = current.children[word[0:letter+1]]
            else:
                exists = False
                break

        if exists:
            if current.aWord == False:
                exists = False

        return exists

def getRandomRack():
    rack = []
    for x in range(8):
        rack.append(random.choice(string.ascii_uppercase))
    return(rack)

trie = Trie()
print("Welcome to Scrabble Move-Maker!")
print("Initializing Scrabble dictionary...")
for word in word_list:
    trie.add_word(word)
print("Dictionary initialized!")

def getRandomRack():
    rack = []
    for x in range(7):
        rack.append(random.choice(string.ascii_uppercase))
    return(rack)

b1 = Board(15,[[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]], trie)

b2 = Board(10,[["A",-1,-1,-1,-1,-1,-1,-1,-1,-1],["N",-1,-1,-1,-1,-1,-1,-1,-1,-1],["G",-1,"B",-1,-1,-1,-1,-1,-1,-1],["E",-1,"E","N","Q","U","I","R","E",-1],["R",-1,"A",-1,-1,-1,-1,-1,-1,-1],["E","N","R","A","G","E","D",-1,-1,-1],["D",-1,"I",-1,-1,-1,-1,-1,-1,-1],[-1,-1,"N",-1,-1,-1,-1,-1,-1,-1],[-1,-1,"G",-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]], trie)
b2.printBoard()
print("\n")
b3 = Board(10,[["C",-1,-1,-1,-1,-1,-1,-1,-1,-1],["L",-1,-1,-1,-1,-1,-1,-1,-1,-1],["E",-1,-1,-1,-1,-1,-1,-1,-1,-1],["A",-1,-1,-1,-1,-1,-1,-1,-1,-1],["V",-1,-1,-1,-1,-1,-1,-1,-1,-1],["E",-1,-1,-1,"B","I","T","E","S",-1],["R","A","I","N","Y",-1,-1,-1,-1,-1],[-1,-1,-1,-1,"E","N","D",-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]], trie)
b3.printBoard()
print("\n")

b4 = Board(10,[[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,"J","U","T",-1,-1,-1],[-1,-1,-1,-1,-1,"G","A","P","Y",-1],[-1,-1,-1,-1,-1,-1,"L",-1,-1,-1],["U","N","V","I","T","A","L",-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]], trie)
b4.printBoard()
print("\n")

b5 = Board(10,[[-1,-1,-1,-1,-1,-1,-1,"T",-1,-1],[-1,-1,-1,"J","O","U","L","E","S",-1],[-1,-1,-1,-1,-1,-1,-1,"E",-1,-1],[-1,-1,-1,-1,-1,"G",-1,"N",-1,-1],[-1,-1,-1,-1,"B","U","S","Y",-1,-1],[-1,-1,-1,-1,-1,"T",-1,-1,-1,-1],[-1,-1,-1,-1,-1,"T",-1,-1,-1,-1],[-1,-1,-1,-1,-1,"E","F",-1,-1,-1],[-1,-1,-1,"Z","E","R","O",-1,-1,-1],[-1,-1,-1,-1,-1,-1,"X",-1,-1,-1]], trie)
b5.printBoard()
print("\n")

b6 = Board(10,[[-1,-1,"B","K","R","S",-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]], trie)
b6.printBoard()
print("\n")

b7 = Board(15,[[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,"A","P","P","L","E",-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]], trie)

b8 = Board(15,[[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,"O","R","D","E","A","L","S",-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,"I","N","G","O","T","E","D"], [-1,-1,-1,-1,-1,"J","U","T",-1,-1,-1,-1,-1,"Y","E"], [-1,-1,-1,-1,-1,-1,"G","A","P","Y",-1,-1,"Z","E","X"], [-1,-1,-1,-1,-1,-1,-1,"L","E","A","D","M","A","N",-1], [-1,"U","N","V","I","T","A","L",-1,-1,-1,-1,"G",-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]], trie)

b1.whichWord(getRandomRack())

b2.whichWord(getRandomRack())

b3.whichWord(getRandomRack())

b4.whichWord(getRandomRack())

b5.whichWord(getRandomRack())

b6.whichWord(getRandomRack())

b7.whichWord(getRandomRack())

b8.whichWord(getRandomRack())

#### SAMPLE INPUT ####
board = Board(15,[[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,"O","R","D","E","A","L","S",-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,"I","N","G","O","T","E","D"], [-1,-1,-1,-1,-1,"J","U","T",-1,-1,-1,-1,-1,"Y","E"], [-1,-1,-1,-1,-1,-1,"G","A","P","Y",-1,-1,"Z","E","X"], [-1,-1,-1,-1,-1,-1,-1,"L","E","A","D","M","A","N",-1], [-1,"U","N","V","I","T","A","L",-1,-1,-1,-1,"G",-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]], trie)

rack = ["A","B","C","D","E","F","G"]

board.whichWord(rack)
