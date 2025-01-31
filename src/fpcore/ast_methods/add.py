from fpcore.ast import ASTNode, Atom, FPCore, Number, Operation
from utils import add_method


def typecast_and_add(a, b):
    # Extract body expressions of FPCores
    if type(a) == FPCore:
        a = a.body
    if type(b) == FPCore:
        b = b.body

    # Force number types into AST nodes
    if type(a) in {int, float}:
        a = Number(str(a))
    if type(b) in {int, float}:
        b = Number(str(b))

    # Error if no AST Nodes
    if not issubclass(type(a), ASTNode):
        msg = "FPCore does not support addition by type '{}' (value = {})"
        raise TypeError(msg.format(type(a), a))
    if not issubclass(type(b), ASTNode):
        msg = "FPCore does not support addition by type '{}' (value = {})"
        raise TypeError(msg.format(type(b), a))

    # Make the new node
    return Operation("+", a, b)


@add_method(ASTNode)
def __add__(self, *args, **kwargs):
    # Make sure calling __add__ leads to an error if not overridden
    class_name = type(self).__name__
    msg = f"__add__ not implemented for class '{class_name}'"
    raise NotImplementedError(msg)


@add_method(Atom)
def __add__(self, other):
    return typecast_and_add(self, other)


@add_method(Operation)
def __add__(self, other):
    return typecast_and_add(self, other)


@add_method(FPCore)
def __add__(self, other):
    return FPCore(self.name,
                  self.arguments,
                  self.properties,
                  typecast_and_add(self, other))
