from scatter import Machine, Node, Condition
import operator


class GateNode(Node):
    operator = 'and'
    a = False
    b = False

    def value(self):
        return getattr(operator, self.operator)(self.a, self.b)


class AndNode(GateNode):
    operator = '__and__'


class OrNode(GateNode):
    operator = 'or_'


class XorNode(GateNode):
    operator = 'xor'


class NotNode(GateNode):
    operator = 'not'


class InvertorNode(GateNode):

    def invert(self, v):
        return not v

    def value(self):
        v = super(InvertorNode, self).value()
        return self.invert(v)


class NandNode(AndNode, InvertorNode):
    pass


class NorNode(OrNode, InvertorNode):
    pass


class XnorNode(XorNode, InvertorNode):
    pass

def run():
    pass
