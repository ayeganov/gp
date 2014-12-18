import abc
import operator


class Node:
    '''
    Base class representing a single node in the GP program.
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, *args):
        '''
        Each node is callable - most of the time they will need to perform some
        function.

        @param args - possible arguments to the node evaluation.
        @returns based on the implementation.
        '''

    @abc.abstractproperty
    def arity(self):
        '''
        Specifies number of arguments this node accepts when evaluated.
        '''

    @abc.abstractproperty
    def name(self):
        '''
        Returns the name of the node.
        '''


class TerminalNode(Node):
    '''
    Node that represents a constant value.
    '''
    def __init__(self, value):
        self._value = value

    def __call__(self, *args):
        '''
        Return the node's value. Parameters args is only specified to conform
        to the interface of node.
        '''
        return self._value

    def arity(self):
        '''
        This is a terminal node, so arity is 0.
        '''
        return 0

    def name(self):
        '''
        Name of this node.
        '''
        return "Terminal"

    def __str__(self):
        '''
        Simply print the value of the terminal.
        '''
        return str(self._value)


class ParamNode(Node):
    '''
    Node for specifying a specific parameter from the input list.
    '''
    def __init__(self, index):
        '''
        Initializes the param node

        @parma index - index into the input list
        '''
        self._index = index

    def __call__(self, input_list):
        '''
        Returns the specific value from the input_list.
        '''
        return input_list[self._index]

    def arity(self):
        '''
        Arity of parameter node is equal to the index in the list it accesses.
        '''
        return self._index + 1

    def name(self):
        '''
        Paramter node's name
        '''
        return "Param"

    def __str__(self):
        return self.name + str(self._index)


class AdditionNode(Node):
    '''
    Node for adding multiple values.
    '''
    def __init__(self, left, right):
        self._left = left
        self._right = right
        self._arity = 2

    def arity(self):
        return self._arity

    def name(self):
        return "Add"

    def __call__(self, *args):
        return sum(args)





