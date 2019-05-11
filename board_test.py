import lxml.etree
from board import Board, FieldState
from player import Player


def createSimpleBoard():
    boardString = """
_BB_
R_OR
R__R
_BB_
""".strip()
    return Board.fromString(boardString), boardString

def test_basic():
    b = Board(4, 4)
    b.set(1, 0, FieldState.Blue)
    b.set(2, 0, FieldState.Blue)
    b.set(1, 3, FieldState.Blue)
    b.set(2, 3, FieldState.Blue)
    b.set(0, 1, FieldState.Red)
    b.set(0, 2, FieldState.Red)
    b.set(3, 1, FieldState.Red)
    b.set(3, 2, FieldState.Red)
    b.set(2, 2, FieldState.Obstructed)

    expected = """
_BB_
R_OR
R__R
_BB_
""".strip()

    assert repr(b) == expected

def test_from_string():
    b, boardString = createSimpleBoard()
    assert repr(b) == boardString

def test_xml():
    boardXML = lxml.etree.XML("""<board>
  <fields>
    <field x="0" y="0" state="EMPTY" />
    <field x="0" y="1" state="RED" />
    <field x="0" y="2" state="RED" />
    <field x="0" y="3" state="EMPTY" />
  </fields>
  <fields>
    <field x="1" y="0" state="BLUE" />
    <field x="1" y="1" state="EMPTY" />
    <field x="1" y="2" state="EMPTY" />
    <field x="1" y="3" state="BLUE" />
  </fields>
  <fields>
    <field x="2" y="0" state="BLUE" />
    <field x="2" y="1" state="EMPTY" />
    <field x="2" y="2" state="OBSTRUCTED" />
    <field x="2" y="3" state="BLUE" />
  </fields>
  <fields>
    <field x="3" y="0" state="EMPTY" />
    <field x="3" y="1" state="RED" />
    <field x="3" y="2" state="RED" />
    <field x="3" y="3" state="EMPTY" />
  </fields>
</board>""")
    b = Board.fromXML(boardXML)

    expected = """
_BB_
R_OR
R__R
_BB_
""".strip()

    assert repr(b) == expected

def test_valid_coordinate():
    b, _ = createSimpleBoard()
    assert b.isValidCoordinate(1, 2)
    assert b.isValidCoordinate(0, 0)
    assert b.isValidCoordinate(3, 3)
    assert b.isValidCoordinate(0, 3)
    assert b.isValidCoordinate(3, 0)

def test_invalid_coordinate():
    b, _ = createSimpleBoard()
    assert not b.isValidCoordinate(-1, 2)
    assert not b.isValidCoordinate(1, -2)
    assert not b.isValidCoordinate(4, 2)
    assert not b.isValidCoordinate(1, 5)
    assert not b.isValidCoordinate(-2, -1)
    assert not b.isValidCoordinate(6, 4)

def test_fish_count_all():
    b, _ = createSimpleBoard()
    assert b.fishCount() == 8

def test_fish_count_red():
    b, _ = createSimpleBoard()
    assert b.fishCount(Player.Red) == 4

def test_fish_count_blue():
    b, _ = createSimpleBoard()
    assert b.fishCount(Player.Blue) == 4

# -*- encoding: utf-8-unix -*-
