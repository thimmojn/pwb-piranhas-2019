import lxml.etree
from move import Move, MoveDirection


def test_move_repr():
    aMove = Move(0, 0, MoveDirection.UpLeft)
    assert repr(aMove) == '(0,0) -> UpLeft'

def test_move_xml():
    aMove = Move(0, 0, MoveDirection.Up)
    expectedXML = lxml.etree.XML('<data class="move" x="0" y="0" direction="UP" />')
    assert lxml.etree.tostring(aMove.toXML()) == lxml.etree.tostring(expectedXML)

# -*- encoding: utf-8-unix -*-
