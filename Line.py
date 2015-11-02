class Line(object):

    def __init__(self, data):
            self.first, self.second = data

    def slope(self):
            '''Get the slope of a line segment'''
            (x1, y1), (x2, y2) = self.first, self.second
            try:
                return (float(y2)-y1)/(float(x2)-x1)
            except ZeroDivisionError:
                # line is vertical
                return None

    def yintercept(self):
            '''Get the y intercept of a line segment'''
            if self.slope() != None:
                x, y = self.first
                return y - self.slope() * x
            else:
                return None

    def solve_for_y(self, x):
            '''Solve for Y cord using line equation'''
            if self.slope() != None and self.yintercept() != None:
                return float(self.slope()) * x + float(self.yintercept())
            else:
                raise Exception('Can not solve on a vertical line')

    def solve_for_x(self, y):
            '''Solve for X cord using line equation'''
            if self.slope() != 0 and self.slope():
                return float((y - float(self.yintercept()))) / float(self.slope())
            else:
                raise Exception('Can not solve on a horizontal line')
