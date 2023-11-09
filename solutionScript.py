import os

current_directory = os.path.dirname(os.path.abspath(__file__))
dictionary_path = os.path.join(current_directory, "dictionary.txt")

class Node:
    def __init__(self):
        self.children = {}
        self.word = False


class Trie:
    def __init__(self):
        self.root = Node()
        self.size = 0

    def __len__(self):
        return self.size

    def insert(self, word: str) -> None:
        root = self.root

        for ch in word:
            if ch not in root.children:
                root.children[ch] = Node()
            root = root.children[ch]

        self.size += 1
        root.word = True   


class Solution:
    def __init__(self):
        self.trie = Trie()
        self.result = ''
        self.resultPath = []
        self.resultPoints = 0
        self.rows = 5
        self.cols = 5

        with open(dictionary_path, "r") as file:
            dictionary = file.readlines()
            for word in dictionary:
                self.trie.insert(word.strip().upper())

    def findWords(self, board, doubleLetter, doublePoint, tripleLetter, skips):
        self.doubleLetter = doubleLetter
        self.doublePoint = doublePoint
        self.tripleLetter = tripleLetter

        for i in range(self.rows):
            for j in range(self.cols):
                self.dfs(board, i, j, [], self.trie.root, 0, '', skips)

        return [self.result, self.resultPath, self.resultPoints]
    
    def dfs(self, board, i, j, path, root, points, currentWord, skips, isSkip = False):
        char = board[i][j]

        # Check if current character is in trie
        if skips != 0 and isSkip == False:
            for key in root.children:
                if key == char:
                    continue

                original = board[i][j]
                board[i][j] = key
                self.dfs(board, i, j, path, root, points, currentWord, skips - 1, True)
                board[i][j] = original


        root = root.children.get(char)
        if root is None:
            return


        letterValues = {'A': 1,'E': 1,'I': 1,'O': 1,'N': 2,'R': 2,'S': 2,'T': 2,'D': 3,'G': 3,'L': 3,'B': 4,'H': 4,'P': 4,'M': 4,'U': 4,'Y': 4,'C': 5,'F': 5,'V': 5,'W': 5,'K': 6,'J': 7,'X': 7,'Q': 8,'Z': 8} 

        # Update path and mark visited
        path = path + [(i, j)]
        points += letterValues[char]
        currentWord = currentWord + char
        board[i][j] = letterValues[char]

        # Add to solution if node is marked as a word in trie
        if root.word:
            longWordBonus = 0
            doubleLetterBonus = 0
            tripleLetterBonus = 0
            doublePointBonus = 1

            if len(currentWord) >= 6:
                longWordBonus = 10

            if self.doubleLetter in path:
                doubleLetterBonus = board[self.doubleLetter[0]][self.doubleLetter[1]]
            if self.tripleLetter in path:
                tripleLetterBonus = board[self.tripleLetter[0]][self.tripleLetter[1]] * 2
            if self.doublePoint in path:
                doublePointBonus = 2

            wordTotalScore = (points + doubleLetterBonus + tripleLetterBonus) * doublePointBonus + longWordBonus
            if wordTotalScore > self.resultPoints:
                self.result = currentWord
                self.resultPath = path
                self.resultPoints = wordTotalScore


        # Right
        if j + 1 < self.cols and board[i][j+1] and type(board[i][j+1]) != int:
            self.dfs(board, i, j+1, path, root, points, currentWord, skips)
        
        #Left
        if j - 1 >= 0 and board[i][j-1] and type(board[i][j-1]) != int:
            self.dfs(board, i, j-1, path, root, points, currentWord, skips)

        # Down
        if i + 1 < self.rows and board[i+1][j] and type(board[i+1][j]) != int:
            self.dfs(board, i+1, j, path, root, points, currentWord, skips)

        # Up
        if i - 1 >= 0 and board[i-1][j] and type(board[i-1][j]) != int:
            self.dfs(board, i-1, j, path, root, points, currentWord, skips)

        #Diagonals

        if j + 1 < self.cols and i + 1 < self.rows and type(board[i+1][j+1]) != int:
            self.dfs(board, i + 1, j + 1, path, root, points, currentWord, skips)
        
        if j + 1 < self.cols and i - 1 >= 0 and type(board[i-1][j+1]) != int:
            self.dfs(board, i - 1, j + 1, path, root, points, currentWord, skips)

        if j - 1 >= 0 and i + 1 < self.rows and type(board[i+1][j-1]) != int:
            self.dfs(board, i + 1, j - 1, path, root, points, currentWord, skips)

        if j - 1 >= 0 and i - 1 >= 0 and type(board[i-1][j-1]) != int:
            self.dfs(board, i - 1, j - 1, path, root, points, currentWord, skips)
        
        board[i][j] = char

    def resetData(self):
        self.result = ''
        self.resultPath = []
        self.resultPoints = 0
        self.doubleLetter = None
        self.doublePoint = None
        self.tripleLetter = None

    def solve(self, board, doubleLetter, tripleLetter, doublePoint, skips):
        result = self.findWords(board, doubleLetter, doublePoint, tripleLetter, skips)
        self.resetData()    

        swappedLetters = []
        for i in range(len(result[0])):
            letter, coords = result[0][i], result[1][i]
            if letter != board[coords[0]][coords[1]]:
                swappedLetters.append([coords[0], coords[1], letter, board[coords[0]][coords[1]]])

        result.append(swappedLetters)
        return result

