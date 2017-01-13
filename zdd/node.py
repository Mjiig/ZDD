class Node:
    def __init__(self, variable, owner, t, f, counter):
        self._variable=variable
        self.owner=owner
        self.t=t
        self.f=f
        self.counter=counter

    def isLeaf(self):
        return False

    def isTrue(self):
        return False

    def isFalse(self):
        return False

    def id(self):
        return (self._variable, self.t.counter, self.f.counter)

    def getVariable(self):
        return self.owner.variables[self._variable]

    def __str__(self):
        return str(self.getVariable()) + ": " + str(self.counter)

class TrueNode:
    def __init__(self, owner, counter):
        self._variable=None
        self.t=None
        self.f=None
        self.owner=owner
        self.counter=counter

    def isLeaf(self):
        return True

    def isTrue(self):
        return True

    def isFalse(self):
        return False

    def __str__(self):
        return "True: " + str(self.counter)

class FalseNode:
    def __init__(self, owner, counter):
        self._variable=None
        self.t=None
        self.f=None
        self.owner=owner
        self.counter=counter

    def isLeaf(self):
        return True

    def isTrue(self):
        return False

    def isFalse(self):
        return True

    def __str__(self):
        return "False: " + str(self.counter)