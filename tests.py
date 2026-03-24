import pytest
from model import Question


@pytest.fixture
def question_with_two_choices():
    question = Question(title="q1")
    question.add_choice("a", False)
    question.add_choice("b", False)

    return question


def test_create_question():
    question = Question(title="q1")
    assert question.id != None


def test_create_multiple_questions():
    question1 = Question(title="q1")
    question2 = Question(title="q2")
    assert question1.id != question2.id


def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title="")
    with pytest.raises(Exception):
        Question(title="a" * 201)
    with pytest.raises(Exception):
        Question(title="a" * 500)


def test_create_question_with_valid_points():
    question = Question(title="q1", points=1)
    assert question.points == 1
    question = Question(title="q1", points=100)
    assert question.points == 100


def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title="q1", points=0)
    with pytest.raises(Exception):
        Question(title="q2", points=101)


def test_create_choice():
    question = Question(title="q1")

    question.add_choice("a", False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == "a"
    assert not choice.is_correct


def test_remove_choice_by_id():
    question = Question(title="q1")

    question.add_choice("a", False)

    choice = question.choices[0]
    assert len(question.choices) == 1

    question.remove_choice_by_id(choice.id)

    assert len(question.choices) == 0


def test_remove_unexisted_choice():
    question = Question(title="q1")

    with pytest.raises(Exception):
        question.remove_choice_by_id(1231230)


def test_remove_all_choices():
    question = Question(title="q1")

    question.add_choice("a", False)
    question.add_choice("b", False)
    question.add_choice("c", False)
    question.add_choice("d", False)

    assert len(question.choices) == 4

    question.remove_all_choices()

    assert len(question.choices) == 0


def test_remove_all_choices_with_empty_question():
    question = Question(title="q1")

    assert len(question.choices) == 0

    question.remove_all_choices()

    assert len(question.choices) == 0


def test_set_correct_choice():
    question = Question(title="q1")

    question.add_choice("a", False)
    question.add_choice("b", False)
    question.add_choice("c", False)
    question.add_choice("d", False)

    question.set_correct_choices([question.choices[0].id])

    assert question.choices[0].is_correct
    assert not question.choices[1].is_correct
    assert not question.choices[2].is_correct
    assert not question.choices[3].is_correct


def test_set_correct_multiple_choices():
    question = Question(title="q1")

    choice1 = question.add_choice("a", False)
    choice2 = question.add_choice("b", False)
    question.add_choice("c", False)
    question.add_choice("d", False)

    question.set_correct_choices([choice1.id, choice2.id])

    assert question.choices[0].is_correct
    assert question.choices[1].is_correct
    assert not question.choices[2].is_correct
    assert not question.choices[3].is_correct


def test_set_correct_choice_that_dont_exist():
    question = Question(title="q1")

    question.add_choice("a", False)

    with pytest.raises(Exception):
        question.set_correct_choices([1231231])


def test_correct_selected_choices():
    question = Question(title="q1")

    choice1 = question.add_choice("a", False)
    question.add_choice("b", False)

    question.set_correct_choices([question.choices[0].id])

    correction = question.correct_selected_choices([choice1.id])

    assert correction[0]


def test_correct_selected_choices_invalid():
    question = Question(title="q1")

    choice1 = question.add_choice("a", False)
    choice2 = question.add_choice("b", False)

    question.set_correct_choices([choice1.id])

    with pytest.raises(Exception):
        question.correct_selected_choices([choice1.id, choice2.id])


def test_fixture_with_two_questions(question_with_two_choices):
    assert len(question_with_two_choices.choices) == 2


def test_fixture_with_two_questions_removing(question_with_two_choices):
    assert len(question_with_two_choices.choices) == 2

    question_with_two_choices.remove_all_choices()

    assert len(question_with_two_choices.choices) == 0
