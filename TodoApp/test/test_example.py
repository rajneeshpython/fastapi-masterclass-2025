import pytest


def test_greater_or_less_equal():
    assert 3 >= 2
    assert 3 >= 3


def test_is_instance():
    assert isinstance(3, int)
    assert isinstance(3.0, float)
    assert isinstance("Hello", str)


def test_boolean():
    validate = True
    assert validate
    assert ("Hello" == "Hello")
    assert ("Hello" == "World") is False


def test_type():
    assert type("Hello") == str
    assert type(3) == int
    assert type(3.0) == float
    assert type(True is bool)


def test_list():
    numbers = [1, 2, 3]
    any_list = [False, False]

    assert 1 in numbers
    assert 4 not in numbers
    assert not any(any_list)
    assert all(numbers)


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_student():
    return Student("Rajneesh", "Kumar", "Computer Science", 3)


def test_student_initialization(default_student):
    assert default_student.first_name == "Rajneesh", "First name should be Rajneesh"
    assert default_student.last_name == "Kumar", "Last name should be Kumar"
    assert default_student.major == "Computer Science"
    assert default_student.years == 3

