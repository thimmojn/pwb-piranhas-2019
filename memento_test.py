import lxml.etree
from memento import Memento, Player


def test_memento_from_official_doc():
    # XML from official XML documentation
    # updates:
    #  * startPlayer -> startPlayerColor
    #  * currentPlayer -> currentPlayerColor
    mementoXML = lxml.etree.XML("""<data class="memento">
  <state class="sc.plugin2019.GameState" turn="0" startPlayerColor="RED" currentPlayerColor="RED">
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

def test_memento_real():
    mementoXML = lxml.etree.XML("""<data class="memento">\n      <state class="sc.plugin2019.GameState" startPlayerColor="RED" currentPlayerColor="RED" turn="0">\n        <red displayName="Unknown" color="RED"/>\n        <blue displayName="Unknown" color="BLUE"/>\n        <board>\n          <fields>\n            <field x="0" y="0" state="EMPTY"/>\n            <field x="0" y="1" state="RED"/>\n            <field x="0" y="2" state="RED"/>\n            <field x="0" y="3" state="RED"/>\n            <field x="0" y="4" state="RED"/>\n            <field x="0" y="5" state="RED"/>\n            <field x="0" y="6" state="RED"/>\n            <field x="0" y="7" state="RED"/>\n            <field x="0" y="8" state="RED"/>\n            <field x="0" y="9" state="EMPTY"/>\n          </fields>\n          <fields>\n            <field x="1" y="0" state="BLUE"/>\n            <field x="1" y="1" state="EMPTY"/>\n            <field x="1" y="2" state="EMPTY"/>\n            <field x="1" y="3" state="EMPTY"/>\n            <field x="1" y="4" state="EMPTY"/>\n            <field x="1" y="5" state="EMPTY"/>\n            <field x="1" y="6" state="EMPTY"/>\n            <field x="1" y="7" state="EMPTY"/>\n            <field x="1" y="8" state="EMPTY"/>\n            <field x="1" y="9" state="BLUE"/>\n          </fields>\n          <fields>\n            <field x="2" y="0" state="BLUE"/>\n            <field x="2" y="1" state="EMPTY"/>\n            <field x="2" y="2" state="EMPTY"/>\n            <field x="2" y="3" state="EMPTY"/>\n            <field x="2" y="4" state="EMPTY"/>\n            <field x="2" y="5" state="EMPTY"/>\n            <field x="2" y="6" state="EMPTY"/>\n            <field x="2" y="7" state="EMPTY"/>\n            <field x="2" y="8" state="EMPTY"/>\n            <field x="2" y="9" state="BLUE"/>\n          </fields>\n          <fields>\n            <field x="3" y="0" state="BLUE"/>\n            <field x="3" y="1" state="EMPTY"/>\n            <field x="3" y="2" state="EMPTY"/>\n            <field x="3" y="3" state="EMPTY"/>\n            <field x="3" y="4" state="EMPTY"/>\n            <field x="3" y="5" state="EMPTY"/>\n            <field x="3" y="6" state="EMPTY"/>\n            <field x="3" y="7" state="EMPTY"/>\n            <field x="3" y="8" state="EMPTY"/>\n            <field x="3" y="9" state="BLUE"/>\n          </fields>\n          <fields>\n            <field x="4" y="0" state="BLUE"/>\n            <field x="4" y="1" state="EMPTY"/>\n            <field x="4" y="2" state="EMPTY"/>\n            <field x="4" y="3" state="EMPTY"/>\n            <field x="4" y="4" state="EMPTY"/>\n            <field x="4" y="5" state="OBSTRUCTED"/>\n            <field x="4" y="6" state="EMPTY"/>\n            <field x="4" y="7" state="EMPTY"/>\n            <field x="4" y="8" state="EMPTY"/>\n            <field x="4" y="9" state="BLUE"/>\n          </fields>\n          <fields>\n            <field x="5" y="0" state="BLUE"/>\n            <field x="5" y="1" state="EMPTY"/>\n            <field x="5" y="2" state="EMPTY"/>\n            <field x="5" y="3" state="EMPTY"/>\n            <field x="5" y="4" state="EMPTY"/>\n            <field x="5" y="5" state="EMPTY"/>\n            <field x="5" y="6" state="EMPTY"/>\n            <field x="5" y="7" state="EMPTY"/>\n            <field x="5" y="8" state="EMPTY"/>\n            <field x="5" y="9" state="BLUE"/>\n          </fields>\n          <fields>\n            <field x="6" y="0" state="BLUE"/>\n            <field x="6" y="1" state="EMPTY"/>\n            <field x="6" y="2" state="OBSTRUCTED"/>\n            <field x="6" y="3" state="EMPTY"/>\n            <field x="6" y="4" state="EMPTY"/>\n            <field x="6" y="5" state="EMPTY"/>\n            <field x="6" y="6" state="EMPTY"/>\n            <field x="6" y="7" state="EMPTY"/>\n            <field x="6" y="8" state="EMPTY"/>\n            <field x="6" y="9" state="BLUE"/>\n          </fields>\n          <fields>\n            <field x="7" y="0" state="BLUE"/>\n            <field x="7" y="1" state="EMPTY"/>\n            <field x="7" y="2" state="EMPTY"/>\n            <field x="7" y="3" state="EMPTY"/>\n            <field x="7" y="4" state="EMPTY"/>\n            <field x="7" y="5" state="EMPTY"/>\n            <field x="7" y="6" state="EMPTY"/>\n            <field x="7" y="7" state="EMPTY"/>\n            <field x="7" y="8" state="EMPTY"/>\n            <field x="7" y="9" state="BLUE"/>\n          </fields>\n          <fields>\n            <field x="8" y="0" state="BLUE"/>\n            <field x="8" y="1" state="EMPTY"/>\n            <field x="8" y="2" state="EMPTY"/>\n            <field x="8" y="3" state="EMPTY"/>\n            <field x="8" y="4" state="EMPTY"/>\n            <field x="8" y="5" state="EMPTY"/>\n            <field x="8" y="6" state="EMPTY"/>\n            <field x="8" y="7" state="EMPTY"/>\n            <field x="8" y="8" state="EMPTY"/>\n            <field x="8" y="9" state="BLUE"/>\n          </fields>\n          <fields>\n            <field x="9" y="0" state="EMPTY"/>\n            <field x="9" y="1" state="RED"/>\n            <field x="9" y="2" state="RED"/>\n            <field x="9" y="3" state="RED"/>\n            <field x="9" y="4" state="RED"/>\n            <field x="9" y="5" state="RED"/>\n            <field x="9" y="6" state="RED"/>\n            <field x="9" y="7" state="RED"/>\n            <field x="9" y="8" state="RED"/>\n            <field x="9" y="9" state="EMPTY"/>\n          </fields>\n        </board>\n      </state>\n    </data>""")
    memento = Memento.fromXML(mementoXML)

    assert memento.turn == 0
    assert memento.startPlayer == Player.Red
    assert memento.currentPlayer == Player.Red
    assert memento.playerNames[Player.Red] == 'Unknown'
    assert memento.playerNames[Player.Blue] == 'Unknown'
    assert memento.lastMove is None

# -*- encoding: utf-8-unix -*-
