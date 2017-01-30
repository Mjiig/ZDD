class Operations:

    @staticmethod
    def varMax(a,b):
        if Operations.varLessThan(a, b):
            return a
        else:
            return b

    @staticmethod
    def varLessThan(a, b):
        if a is None:
            return False
        elif b is None:
            return True
        else:
            return a<b

    
    @staticmethod
    def weaken(diagram, current_height, to_height):
        ns = diagram.owner

        tautology = ns.tautology()
        tautology_list = [tautology]
        tautology = tautology.t

        while not tautology_list[-1].isTrue():
            tautology_list.append(tautology)
            tautology = tautology.t

        if current_height is None: current_height = len(ns.variables)

        current_height -= 1

        while current_height > to_height:
            diagram = ns.getNode(current_height, tautology_list[current_height+1], diagram)
            current_height-=1

        return diagram

    @staticmethod
    def negation(diagram):
        cache = {}
        ns = diagram.owner
        
        def inner(node):
            # Base cases
            if node.isTrue():
                return ns.falseNode
            if node.isFalse():
                return ns.trueNode

            # Pre computed nodes
            if node.counter in cache:
                return cache[node.counter]

            # Inductive case
            left = inner(node.t)
            right = inner(node.f)

            left = Operations.weaken(left, node.t._variable, node._variable)
            right = Operations.weaken(right, node.f._variable, node._variable)

            ret = ns.getNode(node._variable, left, right)
            cache[node.counter] = ret
            return ret

        return Operations.weaken(inner(diagram), diagram._variable, -1)

    @staticmethod
    def disjunction(diagram1, diagram2):
        cache = {}
        ns = diagram1.owner

        def inner(node1, node2):
            if node1.isTrue() and node2.isTrue():
                return ns.trueNode
            if node1.isFalse():
                return node2
            if node2.isFalse():
                return node1

            if Operations.varLessThan(node2._variable, node1._variable):
                node1, node2 = node2, node1
            
            #node2 may be a TrueNode
            if Operations.varLessThan(node1._variable, node2._variable):
                ret = ns.getNode(node1._variable, node1.t, inner(node1.f, node2))
            else:
                # node1._variable is equal to node2._variable
                left = inner(node1.t, node2.t)
                right = inner(node1.f, node2.f)
                ret = ns.getNode(node1._variable, left, right)
            n1 = min(node1.counter, node2.counter)
            n2 = max(node1.counter, node2.counter)
            cache[(n1, n2)] = ret
            return ret

        return inner(diagram1, diagram2)

    @staticmethod
    def conjunction(diagram1, diagram2):
        cache = {}
        ns = diagram1.owner

        def inner(node1, node2):
            if node1.isTrue() and node2.isTrue():
                return ns.trueNode
            if node1.isFalse() or node2.isFalse():
                return ns.falseNode

            if Operations.varLessThan(node2._variable, node1._variable):
                node1, node2 = node2, node1

            if Operations.varLessThan(node1._variable, node2._variable):
                ret = inner(node1.f, node2)
            else:
                left = inner(node1.t, node2.t)
                right = inner(node1.f, node2.f)
                ret = ns.getNode(node1._variable, left, right)

            n1 = min(node1.counter, node2.counter)
            n2 = max(node1.counter, node2.counter)
            cache[(n1, n2)] = ret
            return ret

        return inner(diagram1, diagram2)

    @staticmethod
    def implication(diagram1, diagram2):
        #This is a potentially very inefficient implementation
        #return Operations.disjunction(Operations.negation(diagram1), diagram2)

        cache = {}
        ns = diagram1.owner

        def inner(node1, node2):
            if node1.isTrue():
                return node2
            if node1.isFalse():
                return ns.trueNode

            if Operations.varLessThan(node1._variable, node2._variable):
                left = inner(node1.t, ns.falseNode)
                right = inner(node1.f, node2)
                left = Operations.weaken(left, node1.t._variable, node1._variable)
                right = Operations.weaken(right, node1.f._variable, node1._variable)
               
                ret = ns.getNode(node1._variable, left, right)
            elif Operations.varLessThan(node2._variable, node1._variable):
                ret = inner(node1, node2.f)
            else:
                left = inner(node1.t, node2.t)
                right = inner(node1.f, node2.f)
                left = Operations.weaken(left, node1.t._variable, node1._variable)
                right = Operations.weaken(right, node1.f._variable, node1._variable)
                
                ret = ns.getNode(node1._variable, left, right)
            
            cache[(node1.counter, node2.counter)]=ret
            return ret
                
        return Operations.weaken(inner(diagram1, diagram2), diagram1._variable, -1)

    @staticmethod
    def bimplication(diagram1, diagram2):
        cache = {}
        ns = diagram1.owner

        def inner(node1, node2):
            if node1._variable is None and node2._variable is None:
                if (node1.isTrue() and node2.isTrue()) or (node1.isFalse() and node2.isFalse()):
                    return ns.trueNode
                else:
                    return ns.falseNode

            if Operations.varLessThan(node2._variable, node1._variable):
                node1, node2 = node2, node1

            if Operations.varLessThan(node1._variable, node2._variable):
                left = inner(node1.t, node2)
                right = inner(node1.f, node2)
                left = Operations.weaken(left, Operations.varMax(node1.t._variable, node2._variable), node1._variable)
                right = Operations.weaken(right, Operations.varMax(node1.f._variable, node2._variable), node1._variable)
            else:
                left = inner(node1.t, node2.t)
                right = inner(node1.f, node2.f)
                left = Operations.weaken(left, Operations.varMax(node1.t._variable, node2.t._variable), node1._variable)
                right = Operations.weaken(right, Operations.varMax(node1.f._variable, node2.f._variable), node1._variable)

            ret = ns.getNode(node1._variable, left, right)

            n1 = min(node1.counter, node2.counter)
            n2 = max(node1.counter, node2.counter)
            cache[(n1, n2)] = ret
            return ret

        return inner(diagram1, diagram2)