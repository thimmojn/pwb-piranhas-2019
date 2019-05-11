import lxml.etree
from memento import Memento, Player


def test_memento_from_official_doc():
    mementoXML = lxml.etree.XML("""<data class="memento">
  <state class="state" turn="0" startPlayer="RED" currentPlayer="RED">
    <red displayName="Unknown" color="RED" />
    <blue displayName="Unknown" color="BLUE" />
    <board>
      <fields>
        <field x="0" y="0" state="EMPTY" />
        <field x="0" y="9" state="EMPTY" />
      </fields>
      <fields>
        <field x="9" y="0" state="EMPTY" />
        <field x="9" y="9" state="EMPTY" />
      </fields>
    </board>
  </state>
</data>""")
    memento = Memento.fromXML(mementoXML)

    assert memento.turn == 0
    assert memento.startPlayer is Player.Red
    assert memento.currentPlayer is Player.Red
    assert memento.playerNames[Player.Red] == 'Unknown'
    assert memento.playerNames[Player.Blue] == 'Unknown'
    assert repr(memento.board) == '\n'.join(''.join(10 * ['_']) for _ in range(10))
    assert memento.lastMove is None

# -*- encoding: utf-8-unix -*-
