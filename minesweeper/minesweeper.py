import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"    

    def known_mines(self):
        if len(self.cells) == self.count:
            return self.cells
        return set()
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        #raise NotImplementedError

    def known_safes(self):
        if self.count == 0:
            return self.cells
        return set()
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #raise NotImplementedError

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #raise NotImplementedError

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
       #raise NotImplementedError

    # def check(self,cell,count):
    #     if count==0:
    #         for c in self.cells.remove(cell):
    #             self.mark_safe(c) 
    #     if count==len((self.cells-1)):
    #         for c in self.cells.remove(cell):
    #             self.mark_mine(c)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
        self.knowledge.append(Sentence(set(cell),1))

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        self.knowledge.append(Sentence(set(cell),0))
        


    # def add_knowledge(self, cell, count):
    #     (i,j)=cell

    #     self.moves_made.add(cell)
    #     self.mark_safe(cell)
        

    #     neighbors = set()
    #     for k in range(i-1,i+2):
    #         for l in range(j-1,j+2):
    #             if 0<=k<=self.width and 0<=l<=self.height:
    #                 if k!=i or l!=j:
    #                     neighbors.add((k,l))

    #     self.knowledge.append(Sentence(neighbors-self.safes, count))
    #     ms=0
    #     for i in neighbors-self.safes:
    #         if i in self.mines:
    #             ms+=1
    #     self.knowledge.append(Sentence(neighbors-self.safes-self.mines, count-ms))
    #     #sent.check(cell,count)
        
       
    #         for sentence1 in self.knowledge:
    #             for sentence2 in self.knowledge:
    #                 if sentence1.cells.issubset(sentence2.cells) and sentence1.cells != sentence2.cells:
    #                     newSentence=Sentence(cells=sentence2.cells-sentence1.cells-self.safes, count=sentence2.count-sentence1.count)
    #                     self.knowledge.append(newSentence)
    #                     ms=0
                        
    #                     for i in sentence2.cells-sentence1.cells-self.safes:
    #                         if i in self.mines:
    #                             ms+=1
    #                     self.knowledge.append(Sentence(sentence2.cells-sentence1.cells-self.safes-self.mines, sentence2.count-sentence1.count-ms))
                       

    #     for sentence in self.knowledge:
    #         if sentence.count==0:
    #             for cell in sentence.cells:
    #                 self.safes.add(cell)
                
    #         if sentence.count==len(sentence.cells):
    #             for cell in sentence.cells:
    #                 self.mines.add(cell)
                    
        # if len(self.safes)>len(self.moves_made):
        #     return self.make_safe_move
        # return self.make_random_move
    
    #update self.mines, self.safes, self.moves_made, self.knowledge
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        #"""
    

                    


    def add_knowledge(self,cell,count):
        #raise NotImplementedError
        self.mark_safe(cell)
        self.moves_made.add(cell) #updates self.knowledge
        (i,j)=cell
        print(i,j)
        
        #add a new sentence to the AI's knowledge base based on the value of 'cell' and 'count'
        neighbors=set()
        for k in range(i-1,i+2):
            for l in range(j-1,j+2):
                if 0<=k and k<=self.height and 0<=l and l<=self.width:
                    neighbors.add((k,l))
        neighbors=neighbors-{(i,j)}-self.safes
        newSent=Sentence(neighbors, count)
        self.knowledge.append(newSent)
        for sent1 in self.knowledge:
            for sent2 in self.knowledge:
                if sent1.cells.issubset(sent2.cells) and len(sent1.cells)<len(sent2.cells):
                    print('d')
                    nwS=Sentence(sent2.cells-sent1.cells, sent2.count-sent1.count)
                    nwS.cells = nwS.cells-self.safes 
                    # x=True
                    for mine in self.mines:
                        print(mine)
                        if mine in nwS.cells:
                            nwS.cells= nwS.cells-set(mine)
                            nwS.count= nwS.count-1
                    self.knowledge.append(nwS)
                    self.knowledge.remove(sent2)
                    print(nwS)
        
        for sent in self.knowledge:
            if sent.count==0:
                for cel in sent.cells:
                    print(cel)
                self.safes.union(sent.cells)
            elif sent.count==len(sent.cells):
                #for cello in sent.cells:
                self.mines.union(sent.cells)
        
        
    


        







    def make_safe_move(self):
        print('d')
        for move in self.safes:
            if move not in self.moves_made:
                return move
        
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        #raise NotImplementedError

    def make_random_move(self):
        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            if (i,j) not in self.moves_made:
                if (i,j) not in self.mines:
                    return (i,j)
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        #raise NotImplementedError

test = MinesweeperAI()
test.safes={(1,1),(1,2)}
test.moves_made={(1,1)}
test.mines=set((3,3))

test.knowledge=[Sentence({(1,1),(1,2)}, 0), Sentence({(1,3),(3,3)},1), Sentence({(3,3)},1)]
test.mark_safe((2,3))
#print(test.knowledge, test.safes)
test.add_knowledge((1,0),0)
#print(test.safes)
#print(test.mines)

