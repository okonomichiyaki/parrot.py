from lib.modes.base_mode import *

from dragonfly import Grammar
from dragonfly.actions.action_mouse import Mouse
from lib.grammar.simple_grammar import SimpleSpeechCommand
from lib.grammar.action_grammar import ActionSpeechCommand
import pythoncom
from lib.system_toggles import toggle_speechrec

class SimpleSpeechMode(BaseMode):
    patterns = [
        {
            'name': 'loud',
            'sounds': ['noise'],
            'threshold': {
                'percentage': 90,
                'power': 100
            },
            'throttle': {
                'loud': 1.0,
            }
        }
    ]

    speech_commands = {
        'alpha': ['a'],
        'beta': ['b'],
    }

    speech_actions = {
        'click': Mouse("left"),
    }

    def __init__(self, modeSwitcher, is_testing=False, repeat_delay=REPEAT_DELAY, repeat_rate=REPEAT_RATE):
        BaseMode.__init__(self, modeSwitcher, is_testing=is_testing, repeat_delay=repeat_delay, repeat_rate=repeat_rate)
        self.actionCommandRule = ActionSpeechCommand(self.speech_actions)
        self.grammar.add_rule( self.actionCommandRule )

    def handle_sounds( self, dataDicts ):
        if( self.detect('loud') ):
            self.toggle_speech()

    def handle_speech( self, dataDicts ):
        return
