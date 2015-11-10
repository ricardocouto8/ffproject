import random
import Line

def normalize(value, minimum, maximum):
    value = min(max(value, minimum), maximum)
    return (value - minimum) / float(maximum - minimum)

def denormalize(value, minimum, maximum):
    x1 = 0
    y1 = minimum
    x2 = 1
    y2 = maximum
    return ysolver((x1, y1), (x2, y2), value)

def normalize_list(li):
    norm = [float(i)/sum(li) for i in li]
    return norm

def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w > r:
            return c
        upto += w
    assert False, "Shouldn't get here"

def ysolver(point1, point2, x):
    return Line.Line((point1, point2)).solve_for_y(x)

def num2str(number):
    # sign = int(number/abs(number))
    # number = int(round(abs(number),1))
    return str(int(number))
    # ktest = number/1000
    # if ktest >= 1:
    #     if ktest >= 10:
    #         if ktest >= 1000:
    #             if ktest >= 10000:
    #                 return str(int(round(ktest/1000.0, 1))) + 'M'
    #             else:
    #                 return str(round(sign * ktest/1000.0, 1)) + 'M'
    #         else:
    #             return str(int(round(sign * ktest, 1))) + 'k'
    #     else:
    #         return str(round(sign * number/1000.0, 1)) + 'k'
    # else:
    #     return str(int(round(sign * number, 1)))
