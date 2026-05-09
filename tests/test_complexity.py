
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

def get_compute_function():
    try:
        from complexity import compute_function_complexities
        return compute_function_complexities
    except ImportError:
        return None


def test_single_empty_function_has_complexity_1():
    compute = get_compute_function()
    assert compute is not None

    source = """
def foo():
    pass
"""
    assert compute(source) == [1]


def test_if_increases_complexity():
    compute = get_compute_function()
    assert compute is not None

    source = """
def foo(x):
    if x > 0:
        return x
    return -x
"""
    assert compute(source) == [2]


def test_loop_increases_complexity():
    compute = get_compute_function()
    assert compute is not None

    source = """
def foo(items):
    for i in items:
        print(i)
"""
    assert compute(source) == [2]


def test_boolean_and_or_increase_complexity():
    compute = get_compute_function()
    assert compute is not None

    source = """
def foo(a, b, c):
    if a and b or c:
        return True
    return False
"""
    assert compute(source) == [4]


def test_elif_counts_as_complexity():
    compute = get_compute_function()
    assert compute is not None

    source = """
def foo(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1
"""
    assert compute(source) == [3]


def test_except_increases_complexity():
    compute = get_compute_function()
    assert compute is not None

    source = """
def foo():
    try:
        int("abc")
    except ValueError:
        return None
"""
    assert compute(source) == [2]


def test_conditional_expression_counts():
    compute = get_compute_function()
    assert compute is not None

    source = """
def foo(x):
    return 1 if x > 0 else -1
"""
    assert compute(source) == [2]


def test_multiple_functions_return_multiple_values():
    compute = get_compute_function()
    assert compute is not None

    source = """
def foo():
    pass

def bar(x):
    if x:
        return x
"""
    assert sorted(compute(source)) == [1, 2]


def test_nested_functions_are_independent():
    compute = get_compute_function()
    assert compute is not None

    source = """
def outer(x):
    if x:
        def inner(y):
            return y if y > 0 else -y
        return inner(x)
"""
    assert sorted(compute(source)) == [2, 2]


def test_module_level_code_is_ignored():
    compute = get_compute_function()
    assert compute is not None

    source = """
if True:
    print("hello")

def foo():
    pass
"""
    assert compute(source) == [1]