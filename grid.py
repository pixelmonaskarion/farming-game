class Grid:
    def __init__(self,rows,cols, set=0):
        self.numRows = rows
        self.numCols = cols
        self.create(self.numRows, self.numCols, set)
    def create(self,numR,numC, set):
        self.list = []
        for _ in range(numR*numC):
            self.list.append(set)
    def get(self,R,C):
        return self.list[self.index(R, C)]
    def change(self,R,C, new):
        self.list[self.index(R, C)] = new
    def add(self, R, C, add):
        self.change(R, C, self.get(R,C)+add)
    def index(self, R, C):
        index = R*self.numCols + (C)
        #print(index)
        return index

if __name__ == "__main__":
    TheGrid = Grid(30,20)
    i = 0
    for x in range(TheGrid.numRows):
        for y in range(TheGrid.numCols):
            TheGrid.change(x,y,i)
            i+=1
    i = 0
    for x in range(TheGrid.numRows):
        for y in range(TheGrid.numCols):
            g = TheGrid.get(x,y)
            if (i !=g ):
                print("x:",x, "y:", y, "i:", i, "from the list:", g, "nc", TheGrid.numCols)
                0/0
            i+=1
