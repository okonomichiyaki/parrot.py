from lib.modes.base_mode import *
from pressdirectxkey import PressKey, ReleaseKey, ScanCodes

class HadesMode(BaseMode):
    moving = False
    held_keys = {}

    patterns = [
        {
            'name': 'attack',
            'sounds': ['cluck'],
            'threshold': {
                'percentage': 70,
                'intensity': 1000
            }
        },
        {
            'name': 'attack2',
            'sounds': ['zzh'],
            'threshold': {
                'percentage': 70,
                'intensity': 1000
            },
            'throttle': {
                'attack2': 0.3
            }
        },
        {
            'name': 'interact',
            'sounds': ['whistle'],
            'threshold': {
                'percentage': 60,
                'intensity': 1000
            },
            'throttle': {
                'interact': 0.3
            }
        },
        {
            'name': 'dash',
            'sounds': ['motorlips'],
            'threshold': {
                'percentage': 70,
                'intensity': 1000,
            },
            'throttle': {
                'interact': 0.3
            }
        },
        {
            'name': 'move',
            'strategy': 'continuous',
            'sounds': ['hiss'],
            'threshold': {
                'percentage': 70,
                'lowest_percentage': 30,
                'intensity': 1000,
                'lowest_intensity': 300,
            }
        },
    ]

    def short_press_key( self, scan_code ):
        PressKey(scan_code)
        time.sleep(0.1)
        ReleaseKey(scan_code)

    def hold_key( self, scan_code ):
        PressKey(scan_code)
        self.held_keys[scan_code] = True

    def release_key( self, scan_code ):
        ReleaseKey(scan_code)
        self.held_keys[scan_code] = False

    def get_wasd( self ):
        keys = []
        letters = []
        if( self.quadrant3x3 == TOPLEFT or self.quadrant3x3 == TOPMIDDLE or self.quadrant3x3 == TOPRIGHT ):
            keys.append(ScanCodes.KEY_W)
            letters.append('w')
        if( self.quadrant3x3 == TOPLEFT or self.quadrant3x3 == CENTERLEFT or self.quadrant3x3 == BOTTOMLEFT ):
            keys.append(ScanCodes.KEY_A)
            letters.append('a')
        if( self.quadrant3x3 == CENTERRIGHT or self.quadrant3x3 == TOPRIGHT or self.quadrant3x3 == BOTTOMRIGHT ):
            keys.append(ScanCodes.KEY_D)
            letters.append('d')
        if( self.quadrant3x3 == BOTTOMLEFT or self.quadrant3x3 == BOTTOMMIDDLE or self.quadrant3x3 == BOTTOMRIGHT ):
            keys.append(ScanCodes.KEY_S)
            letters.append('s')
        print(letters)
        return keys

    def handle_sounds( self, dataDicts ):
        if ( self.detect_silence() ):
            for key in self.held_keys:
                if ( self.held_keys.get(key) ):
                    self.release_key(key)

        if ( self.detect('move') ):
            self.moving=True
            for key in self.get_wasd():
                self.hold_key(key)

        elif ( self.detect('dash') ):
            self.short_press_key(ScanCodes.SPACE)

        elif ( self.detect('attack') ):
            self.drag_mouse()
            time.sleep(0.1)
            self.stop_drag_mouse()

        elif ( self.detect('attack2') ):
            self.drag_mouse(button='right')
            time.sleep(0.1)
            self.stop_drag_mouse(button='right')

        elif ( self.detect('interact') ):
            self.short_press_key(ScanCodes.KEY_E)
