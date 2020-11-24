from lib.modes.base_mode import *
from pressdirectxkey import PressKey, ReleaseKey, ScanCodes

class PyreMode(BaseMode):

    holding_shift = False

    patterns = [
        {
            'name': 'walk',
            'sounds': ['cluck'],
            'threshold': {
                'percentage': 70,
                'intensity': 1000
            }
        },
        {
            'name': 'pass switch',
            'sounds': ['whistle','pop'],
            'threshold': {
                'percentage': 60,
                'intensity': 1000
            },
            'throttle': {
                'pass switch': 0.3
            }
        },
        {
            'name': 'jump evade',
            'sounds': ['ff','motorlips'],
            'strategy': 'continuous',
            'threshold': {
                'percentage': 70,
                'lowest_percentage': 30,
                'intensity': 1000,
                'lowest_intensity': 300,
            }
        },
        {
            'name': 'sprint',
            'strategy': 'continuous',
            'sounds': ['hiss'],
            'threshold': {
                'percentage': 70,
                'lowest_percentage': 30,
                'intensity': 1000,
                'lowest_intensity': 300,
            }
        },
        {
            'name': 'cast',
            'strategy': 'continuous',
            'sounds': ['zzh'],
            'threshold': {
                'percentage': 70,
                'lowest_percentage': 30,
                'intensity': 1000,
                'lowest_intensity': 300,
            },
        },
    ]

    def short_press_key( self, scan_code ):
        PressKey(scan_code)
        time.sleep(0.1)
        ReleaseKey(scan_code)

    def handle_sounds( self, dataDicts ):
        if ( self.detect('walk') ):
            self.drag_mouse()
            time.sleep(0.1)
            self.stop_drag_mouse()

        elif ( self.detect('pass switch')):
            self.short_press_key(ScanCodes.SPACE)

        elif ( self.detect('jump evade')):
            self.short_press_key(ScanCodes.KEY_W)

        elif ( not self.holding_shift and self.detect('sprint')):
            PressKey(ScanCodes.LEFT_SHIFT)
            self.holding_shift = True
            self.drag_mouse()

        elif ( self.holding_shift and self.detect_silence() ):
            self.holding_shift = False
            ReleaseKey(ScanCodes.LEFT_SHIFT)

        elif ( self.detect('cast') ):
            self.drag_mouse(button='right')
