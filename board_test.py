# -*- encoding: utf-8-unix -*-

from board import PiranhasBoard, FieldState


def test_representation():
    b = PiranhasBoard(4, 4)
    b.set(1, 0, FieldState.Blue)
    b.set(2, 0, FieldState.Blue)
    b.set(1, 3, FieldState.Blue)
    b.set(2, 3, FieldState.Blue)
    b.set(0, 1, FieldState.Red)
    b.set(0, 2, FieldState.Red)
    b.set(3, 1, FieldState.Red)
    b.set(3, 2, FieldState.Red)
    b.set(2, 2, FieldState.Obstructed)

    expected = """  B B
R   O R
R     R
  B B  """

    assert repr(b) == expected
