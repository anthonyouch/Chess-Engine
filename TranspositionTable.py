from collections import OrderedDict, namedtuple
class LRUCache:
    """Store items in the order the keys were last added"""
    def __init__(self, size):
        self.od = OrderedDict()
        self.size = size

    def get(self, key, default=None):
        try: self.od.move_to_end(key)
        except KeyError: return default
        return self.od[key]

    def __setitem__(self, key, value):
        try: del self.od[key]
        except KeyError:
            if len(self.od) == self.size:
                self.od.popitem(last=False)
        self.od[key] = value

class Entry(namedtuple('Entry',['depth','score','move','bound'])):
    BOUND_LOWER,BOUND_EXACT,BOUND_UPPER = 1,0,-1

    def narrowing(self,alpha,beta):
        if self.bound == self.BOUND_LOWER: # was entry.score >= beta
            alpha = max(alpha,self.score)
        elif self.bound == self.BOUND_UPPER: # was entry.score <= alpha
            beta = min(beta,self.score)
        return alpha,beta

    def isexact(self):
        return self.bound == self.BOUND_EXACT

