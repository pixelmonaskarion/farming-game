class Grid:
    def __init__(self,rows,cols):
        self.numRows = rows
        self.numCols = cols
        self.create(self.numRows, self.numCols)
    def create(self,numR,numC, set=0):
        self.list = []
        for _ in range(numR*numC):
            self.list.append(set)
    def get(self,R,C):
        #print("getting {}, {} with lenth {}".format(R, C, len(self.list)))
        return self.list[(((round(C))*self.numCols))+(round(R))]
    def change(self,R,C, new):
        self.list[((round(C)*self.numCols))+(round(R))] = new

if __name__ == "__main__":
    TheGrid = Grid(10,10)
    print(TheGrid.get(1,1))
        

    
    
