
class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        output = '({}, {})'.format(self.x, self.y)
        return output
