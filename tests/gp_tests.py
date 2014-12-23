#!/usr/bin/env python

import nose
import gp

def setup():
    print("SETUP!")

def teardown():
    print("TEAR DOWN!")


def test_terminal_node():
    for i in range(10):
        term = gp.node.TerminalNode(i)
        assert term([]) == i, "Terminal node error"


def test_param_node():
    vals = range(10)
    for i in range(len(vals)):
        param = gp.node.ParamNode(i)
        assert param(vals) == i,\
               "Parameter node returned wrong value exp={exp}, actual={actual}".\
               format(exp=i, actual=param(vals))


def test_param_node_index_error():
    param = gp.node.ParamNode(2)
    nose.tools.assert_raises(IndexError, param, [1])


def test_addition_node_single_term():
    term5 = gp.node.TerminalNode(5)
    add = gp.node.AdditionNode([term5])
    assert add([]) == 5, "Addition node error: exp={exp}, actual={act}".\
                         format(exp=5, act=add([]))


def test_addition_node_multiple_terms():
    term5 = gp.node.TerminalNode(5)
    term3 = gp.node.TerminalNode(3)
    add = gp.node.AdditionNode([term5, term3])

    expected = term5([]) + term3([])
    assert add([]) == expected, "Addition error: exp={exp}, actual={act}".\
           format(exp=expected, act=add([]))


def test_addition_node_with_param_nodes():
    param0 = gp.node.ParamNode(0)
    param1 = gp.node.ParamNode(1)
    add = gp.node.AdditionNode([param0, param1])

    vals = [2, 3]
    expected = sum(vals)
    result = add(vals)

    assert result == expected, "Addition error: exp={exp}, actual={act}".\
           format(exp=expected, act=result)

def test_addition_node_mixed():
    param0 = gp.node.ParamNode(0)
    term5 = gp.node.TerminalNode(5)
    add = gp.node.AdditionNode([param0, term5])

    vals = [5]
    expected = vals[0] + term5([])
    result = add(vals)

    assert result == expected, "Addition error: exp={exp}, actual={act}".\
           format(exp=expected, act=result)

def test_multiplication_node():
    param = gp.node.ParamNode(0)
    term5 = gp.node.TerminalNode(5)

    mul = gp.node.MultiplicationNode([param, term5])
    vals = [5]
    expected = vals[0] * term5([])
    result = mul(vals)

    assert result == expected, "Multiplication error: exp={exp}, actual={act}".\
           format(exp=expected, act=result)

def test_division_node():
    param0 = gp.node.ParamNode(0)
    param1 = gp.node.ParamNode(1)
    param2 = gp.node.ParamNode(2)

    div = gp.node.DivisionNode([param0])
    vals = [5]
    expected = 1/5.0
    result = div(vals)

    assert result == expected, "Division error: exp={exp}, actual={act}".\
           format(exp=expected, act=result)

    div = gp.node.DivisionNode([param0, param1])
    vals = [5, 5, 10]
    expected = 1.0
    result = div(vals)

    assert result == expected, "Division error: exp={exp}, actual={act}".\
           format(exp=expected, act=result)

    div = gp.node.DivisionNode([param0, param1, param2])
    vals = [5, 5, 10]
    expected = 1 / 10.0
    result = div(vals)

    assert result == expected, "Division error: exp={exp}, actual={act}".\
           format(exp=expected, act=result)


def test_subtraction_node():
    term3 = gp.node.TerminalNode(-3)

    sub = gp.node.SubtractionNode([term3])
    expected = 3
    result = sub([])

    assert result == expected, "Subtraction error: exp={exp}, actual={act}".\
           format(exp=expected, act=result)

    term3 = gp.node.TerminalNode(3)
    term4 = gp.node.TerminalNode(4)
    sub = gp.node.SubtractionNode([term4, term3])
    expected = 1
    result = sub([])

    assert result == expected, "Subtraction error: exp={exp}, actual={act}".\
           format(exp=expected, act=result)



if __name__ == "__main__":
    nose.main()

