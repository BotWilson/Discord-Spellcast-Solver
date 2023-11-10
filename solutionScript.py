import os

class Node:
    def __init__(self):
        self.children = {}
        self.word = False

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word: str) -> None:
        root = self.root

        for ch in word:
            if ch not in root.children:
                root.children[ch] = Node()
            root = root.children[ch]
        root.word = True


class Solution:
    def __init__(self):
        # Initialize trie
        self.trie = Trie()
        self.result = {
            'word': '',
            'path': [],
            'points': 0,
            'swaps': []
        }

        self.rows = 5
        self.cols = 5
        self.letterValues = letterValues = {'A': 1,'E': 1,'I': 1,'O': 1,'N': 2,'R': 2,'S': 2,'T': 2,'D': 3,'G': 3,'L': 3,'B': 4,'H': 4,'P': 4,'M': 4,'U': 4,'Y': 4,'C': 5,'F': 5,'V': 5,'W': 5,'K': 6,'J': 7,'X': 7,'Q': 8,'Z': 8}

        #Adds all the words from out dictionary.txt file to the trie
        current_directory = os.path.dirname(os.path.abspath(__file__))
        dictionary_path = os.path.join(current_directory, "dictionary.txt")

        with open(dictionary_path, "r") as file:
            dictionary = file.readlines()
            for word in dictionary:
                self.trie.insert(word.strip().upper())

    def findWords(self, board, doubleLetter, doublePoint, tripleLetter, swaps):
        self.doubleLetter = doubleLetter
        self.doublePoint = doublePoint
        self.tripleLetter = tripleLetter

        #go through entire board and dfs to find viable words
        for i in range(self.rows):
            for j in range(self.cols):
                self.dfs(board, i, j, [], self.trie.root, 0, '', swaps)

        #return highest score word
        return self.result
    
    def dfs(self, board, i, j, path, root, points, currentWord, swaps, isSwap = False):
        char = board[i][j]

        # Check if current character is in trie
        if swaps != 0 and isSwap == False:
            # if swap is available and we have not already swapped this letter, swap the letter and dfs every other possible path
            for key in root.children:
                if key == char:
                    continue

                original = board[i][j]
                board[i][j] = key
                self.dfs(board, i, j, path, root, points, currentWord, swaps - 1, True)
                board[i][j] = original

        #move down trie
        root = root.children.get(char)
        if root is None:
            return

        # Update variables and mark visited
        path = path + [(i, j)]
        points += self.letterValues[char]
        currentWord = currentWord + char
        board[i][j] = False

        # Add to solution if node is marked as a word in trie
        if root.word:
            longWordBonus = 0
            doubleLetterBonus = 0
            tripleLetterBonus = 0
            doublePointBonus = 1

            if len(currentWord) >= 6:
                longWordBonus = 10

            #check for bonus points
            if self.doubleLetter in path:
                letterIndex = path.index(self.doubleLetter)
                doubleLetterBonus = self.letterValues[currentWord[letterIndex]]
            if self.tripleLetter in path:
                letterIndex = path.index(self.tripleLetter)
                tripleLetterBonus = self.letterValues[currentWord[letterIndex]]
            if self.doublePoint in path:
                doublePointBonus = 2

            #calculate total score and replaced result if higher
            wordTotalScore = (points + doubleLetterBonus + tripleLetterBonus) * doublePointBonus + longWordBonus
            if wordTotalScore > self.result['points']:
                self.result['word'] = currentWord
                self.result['path'] = path
                self.result['points'] = wordTotalScore

        # DFS in all directions

        # Right
        if j + 1 < self.cols and board[i][j+1]:
            self.dfs(board, i, j+1, path, root, points, currentWord, swaps)
        
        #Left
        if j - 1 >= 0 and board[i][j-1]:
            self.dfs(board, i, j-1, path, root, points, currentWord, swaps)

        # Down
        if i + 1 < self.rows and board[i+1][j]:
            self.dfs(board, i+1, j, path, root, points, currentWord, swaps)

        # Up
        if i - 1 >= 0 and board[i-1][j]:
            self.dfs(board, i-1, j, path, root, points, currentWord, swaps)

        #Diagonals

        if j + 1 < self.cols and i + 1 < self.rows:
            self.dfs(board, i + 1, j + 1, path, root, points, currentWord, swaps)
        
        if j + 1 < self.cols and i - 1 >= 0:
            self.dfs(board, i - 1, j + 1, path, root, points, currentWord, swaps)

        if j - 1 >= 0 and i + 1 < self.rows:
            self.dfs(board, i + 1, j - 1, path, root, points, currentWord, swaps)

        if j - 1 >= 0 and i - 1 >= 0:
            self.dfs(board, i - 1, j - 1, path, root, points, currentWord, swaps)
        
        # Reset board to original state
        board[i][j] = char

    #function to reset result data
    def resetData(self):
        self.result = {
            'word': '',
            'path': [],
            'points': 0,
            'swaps': []
        }

    #function to solve the board and return the result with swap data
    def solve(self, board, doubleLetter, tripleLetter, doublePoint, swaps):
        result = self.findWords(board, doubleLetter, doublePoint, tripleLetter, swaps)
        self.resetData()    

        swappedLetters = []
        for i in range(len(result['word'])):
            letter, coords = result['word'][i], result['path'][i]
            if letter != board[coords[0]][coords[1]]:
                swappedLetters.append((coords[0], coords[1], letter, board[coords[0]][coords[1]]))

        result['swaps'] = swappedLetters
        return result