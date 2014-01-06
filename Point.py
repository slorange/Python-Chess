class Point(object):

    def __init__(self):
        self.X = 0
        self.Y = 0
        
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __repr__(self):
        return "(%s,%s)"%(self.X, self.Y) 

    def getX(self):
        return self.X
        
    def getY(self):
        return self.Y
        
    def __mul__(self, other):
        return Point(self.X*other, self.Y*other);
        
    def __add__(self, other):
        return Point(self.X+other.X, self.Y+other.Y);
        
    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y