import lxml.etree
from move import Move, MoveDirection


def test_direction_inverse():
    assert all(d.inverse.inverse == d for d in MoveDirection)

def test_move_repr():
    aMove = Move(0, 0, MoveDirection.UpLeft)
    assert repr(aMove) == '(0,0) -> UpLeft'

def test_hint():
    aMove = Move(1, 3, MoveDirection.Down)
    aMove.addHint('special move')
    assert aMove.hints == ['special move']

def test_move_xml():
    aMove = Move(0, 0, MoveDirection.Up)
    expectedXML = lxml.etree.XML('<data class="move" x="0" y="0" direction="UP" />')
    assert lxml.etree.tostring(aMove.toXML()) == lxml.etree.tostring(expectedXML)

def test_move_with_hints_xml():
    aMove = Move(5, 3, MoveDirection.DownRight)
    aMove.addHint('some debug').addHint('more debug')
    expectedXML = lxml.etree.XML("""<data class="move" x="5" y="3" direction="DOWN_RIGHT">
  <hint content="some debug" />
  <hint content="more debug" />
</data>""")
    assert lxml.etree.tostring(aMove.toXML(), pretty_print=True) \
        == lxml.etree.tostring(expectedXML, pretty_print=True)

# -*- encoding: utf-8-unix -*-
