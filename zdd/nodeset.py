from . import node
import weakref

class NodeSet:
    def __init__(self, variables):
        self.variables=variables
        # True and false never fetched from cache but need unique counters still
        self.trueNode=node.TrueNode(self, 0)
        self.falseNode=node.FalseNode(self, 1)
        self.nodes=weakref.WeakValueDictionary()
        self.nextCounter=2

    def getNode(self, variable, t, f):
        key = (variable, t.counter, f.counter)
        if key in self.nodes:
            return self.nodes[key]

        if t.isFalse():
            return f
        
        newNode = node.Node(variable, self, t, f, self.nextCounter)
        self.nextCounter+=1
        self.nodes[key] = newNode
        return newNode

    def assertVariable(self, variable):
        diagram=self.trueNode
        for i in reversed(range(len(self.variables))):
            if self.variables[i]!=variable:
                diagram=self.getNode(i, diagram, diagram)
            else:
                diagram=self.getNode(i, diagram, self.falseNode)

        return diagram

    def assertAll(self):
        diagram=self.trueNode
        for i in reversed(range(len(self.variables))):
            diagram=self.getNode(i, diagram, self.falseNode)
        
        return diagram

    def assertNone(self):
        return self.trueNode

    def tautology(self):
        diagram=self.trueNode
        for i in reversed(range(len(self.variables))):
            diagram=self.getNode(i,diagram,diagram)

        return diagram

    def contradiction(self):
        return self.falseNode

    def visualiseDiagram(self, root, filename):
        toProcess=[root]
        toDraw=set()

        while toProcess:
            current=toProcess.pop()
            if current and current not in toDraw:
                toDraw.add(current)
                toProcess.append(current.t)
                toProcess.append(current.f)
        output = """digraph zdd{\n"""
        output += '"%s"\n' % str(root) # Necessary if there's only a single node
        for node in toDraw:
            if node.t: output+='"%s" -> "%s"\n' % (str(node), str(node.t))
            if node.f: output+='"%s" -> "%s" [style=dotted]\n' % (str(node), str(node.f))
        
        output+= """}"""
        f = open(filename, "w")
        f.write(output)
        f.close()