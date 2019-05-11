import lxml.etree
from board import PiranhasBoard, FieldState


def test_basic():
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
    b = PiranhasBoard.fromXML(boardXML)

    expected = """  B B  
R   O R
R     R
  B B  """

    assert repr(b) == expected

# -*- encoding: utf-8-unix -*-
