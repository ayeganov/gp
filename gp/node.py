import abc
import enum
import functools
import operator
import random


class Method(enum.Enum):
    GROW = 1,
    FULL = 2


class Node:
    '''
    Interface that each node in the GP program must conform to.
    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def call(self, context, children_values):
        '''
        Each node is callable - most of the time they will need to perform some
        function.

        @param context - possible arguments to the node evaluation.
        @param children_values - values from children of this node calculated
                                 based on the provided context
        @returns based on the implementation.
        '''

    @abc.abstractproperty
    def name(self):
        '''
        Returns the name of the node.
        '''

class BaseNode(Node):
    '''
    Base node that fills in arity and name properties used by every node.
    '''
    ARITY = 0
    def __init__(self, name):
        self._name = name
        self._children = []

    @property
    def name(self):
        return self._name

    def __call__(self, context=None):
        '''
        Base implementation of node evaluation. Values to be used for
        calculations are contained within `context`. Entries in context can be
        accessed by specifying ParamNode with appropriate index. Context is
        equivalent to a stack growing upwards. A useful representation of
        context would be as follows:

            3) w
            2) x
            1) y
            0) z

        A parameter node given to an operation node would access one of these
        variables by appropriate index. ParamNode(2) would use value of `x` in
        calculations.

        @param context - a stack of external variables to be used as part of
                         expression calcuation.

        @returns a list of values calculated from the children nodes of this
                 node.
        '''
        context = [] if not context else context
        results = [node(context) for node in self._children]
        return self.call(context, results)

    def display(self, indent=0):
        '''
        Prints out the textual representation of the expression tree.

        @param indent = how far to indent this node.
        '''
        whitespace = '\t' * indent
        print(whitespace + "(" + self.name)
        for node in self._children:
            node.display(indent+1)



class TerminalNode(BaseNode):
    '''
    Node that represents a constant value.
    '''
    def __init__(self, value):
        super(TerminalNode, self).__init__("Term" + str(value))
        self._value = value

    def call(self, context, children_values):
        '''
        Return the node's value. Parameters context is only specified to conform
        to the interface of node.
        '''
        return self._value

    def __repr__(self):
        '''
        Simply print the value of the terminal.
        '''
        return str(self._value)


class ParamNode(BaseNode):
    '''
    Node for extracting a specific value from the context list.
    '''
    def __init__(self, index):
        '''
        Initializes the param node

        @parma index - index into the context list
        '''
        name = 'Param' + '[' + str(index) + ']'
        super(ParamNode, self).__init__(name=name)
        self._index = index

    def call(self, context, children_values):
        '''
        Returns the specific value from the context.

        @param context - variables outside of the expression tree
        @param children_values - values calculated from children nodes of this
                                 node.
        '''
        return context[self._index]

    def __repr__(self):
        return self.name


class AdditionNode(BaseNode):
    '''
    Node for adding multiple values.
    '''
    ARITY = float('inf')
    def __init__(self, children):
        super(AdditionNode, self).__init__("+")
        self._children = children

    def call(self, context, children_values):
        return sum(children_values)


class MultiplicationNode(BaseNode):
    '''
    Node for multiplying multiple values.
    '''
    ARITY = float('inf')
    def __init__(self, children):
        super(MultiplicationNode, self).__init__("*")
        self._children = children

    def call(self, context, children_values):
        return functools.reduce(operator.mul, children_values, 1)

    def __repr__(self):
        return self.name


class DivisionNode(BaseNode):
    '''
    Node for dividing multiple values.
    '''
    ARITY = float('inf')
    def __init__(self, children):
        super(DivisionNode, self).__init__("/")
        self._children = children

    def call(self, context, children_values):
        if not context or self._children is None:
            return 1

        if len(self._children) == 1:
            return 1.0 / float(children_values[0])
        else:
            numerator = children_values[0]
            denominator = functools.reduce(operator.mul, children_values[1:], 1)
            return float(numerator) / denominator


class SubtractionNode(BaseNode):
    '''
    Node for subtracting multiple values.
    '''
    ARITY = float('inf')
    def __init__(self, children):
        super(SubtractionNode, self).__init__("-")
        self._children = children

    def call(self, context, children_values):
        if len(self._children) > 1:
            return functools.reduce(operator.sub, children_values)
        else:
            return -children_values[0]


TERMINAL_SET = list([])
FUNCTION_SET = list([AdditionNode, MultiplicationNode, DivisionNode, SubtractionNode])

def generate_random_tree(num_params, func_set, term_set, max_depth, method):
    '''
    This function generates a random expression of provided maximum depth using
    the given method: full, or grow.

    @param num_params - number of parameters to be accepted by generated tree.
    '''
    if num_params < 0:
        raise ValueError("Number of parameters must be specified as value >= 0")

    param_set = [ParamNode(i) for i in range(num_params)]

    return _generate_random_tree(num_params, func_set, param_set, term_set, max_depth, method)


def _generate_random_tree(num_params, func_set, param_set, term_set, max_depth, method, choose_param=0.8):
    '''
    This function generates a random expression of provided maximum depth using
    the given method: full, or grow.

    @param num_params - number of parameters to be accepted by generated tree.
    @param func_set - set of functions that could be used in the expression.
    @param term_set - set of terminal nodes to be used in the expression.
    @param max_depth - maximum depth of generated expression.
    @param method - method to be used for expression generation.
    @param choose_param - percentage of time the parameter nodes should be chosen
                          as terminal
    @returns an executable expression tree
    '''
    terms_to_funcs = float(len(term_set) + len(param_set))\
                     / (len(term_set) + len(param_set) + len(func_set))

    if max_depth == 0 or (method == Method.GROW and random.random() < terms_to_funcs):
        expr = random.choice(param_set)\
               if random.random() <= choose_param\
               else random.choice(term_set)
    else:
        func = random.choice(func_set)
        num_args = random.randint(1, num_params) if func.ARITY == float('inf') else func.ARITY
        print("Function %s will have %s children" % (func, num_args))
        args = [_generate_random_tree(num_params, func_set, param_set, term_set, max_depth-1, method)
                for _ in range(num_args)]
        expr = func(args)
    return expr


