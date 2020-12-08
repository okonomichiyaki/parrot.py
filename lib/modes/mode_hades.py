from lib.modes.base_mode import *
from pressdirectxkey import PressKey, ReleaseKey
from directinput_scancodes import ScanCodes

class HadesMode(BaseMode):
    logging = True
    attacking = False
    moving = False
    held_keys = {}

    patterns = [
        {
            'name': 'attack',
            'sounds': ['hiss'],
            'strategy': 'frequency_threshold',
            'threshold': {
                'percentage': 99,
                'power': 20000,
                'frequency': 150,
            }
        },
        {
            'name': 'dash',
            'sounds': ['motorlips'],
            'strategy': 'frequency_threshold',
            'threshold': {
                'percentage': 95,
                'power': 15000,
                'below_frequency': 40,
            },
            'throttle': {
                'dash': 0.3
            }
        },
        {
            'name': 'cast',
            'sounds': ['tch'],
            'strategy': 'frequency_threshold',
            'threshold': {
                'percentage': 90,
                'power': 50000,
                'frequency': 120,
            },
            'throttle': {
                'cast': 0.3,
                'move': 0.3
            }
        },
        {
            'name': 'special',
            'sounds': ['pop'],
            'strategy': 'frequency_threshold',
            'threshold': {
                'percentage': 95,
                'power': 20000,
                'frequency': 55,
                'below_frequency': 65,
            },
            'throttle': {
                'move': 0.3
            }
        },
        {
            'name': 'interact',
            'sounds': ['whistle'],
            'strategy': 'frequency_threshold',
            'threshold': {
                'percentage': 99,
                'power': 10000,
                'frequency': 70,
                'below_frequency': 100,
            },
            'throttle': {
                'interact': 0.3
            }
        },
        {
            'name': 'move',
            'sounds': ['cluck'],
            'strategy': 'frequency_threshold',
            'threshold': {
                'percentage': 99,
                'power': 10000,
                'frequency': 55,
                'below_frequency': 70,
            },
            'throttle': {
                'move': 0.3,
                'special': 0.3,
                'attack': 0.1
            }
        },
    ]

    def log( self, action ):
        if (self.logging):
            print('........................................................................... ' + action)

    def short_press_key( self, scan_code ):
        if ( not self.inputManager.is_testing ):
            PressKey(scan_code)
            time.sleep(0.1)
            ReleaseKey(scan_code)

    def hold_key( self, scan_code ):
        if ( not self.inputManager.is_testing ):
            PressKey(scan_code)

    def press_key(self,scan_code):
        if ( not self.inputManager.is_testing ):
            PressKey(scan_code)

    def release_key( self, scan_code ):
        if ( not self.inputManager.is_testing ):
            ReleaseKey(scan_code)

    def interact( self ):
        self.log('interact')
        quadrant = self.detector.detect_mouse_quadrant( 2, 2 )
        # If we are moving, this is a "call"
        # otherwise it's summon, interact, codex, or gift depending on mouse
        if ( self.moving ):
            self.short_press_key(ScanCodes.KEY_F)
        elif ( quadrant == 1 ): 
            self.short_press_key(ScanCodes.KEY_1)
        elif ( quadrant == 2 ): 
            self.short_press_key(ScanCodes.KEY_E)
        elif ( quadrant == 3 ): 
            self.short_press_key(ScanCodes.KEY_C)
        elif ( quadrant == 4 ): 
            self.short_press_key(ScanCodes.KEY_G)

    def get_wasd( self ):
        keys = { ScanCodes.KEY_W: False, ScanCodes.KEY_A: False, ScanCodes.KEY_S: False, ScanCodes.KEY_D: False }
        if( self.quadrant3x3 == TOPLEFT or self.quadrant3x3 == TOPMIDDLE or self.quadrant3x3 == TOPRIGHT ):
            keys[ScanCodes.KEY_W]=True
        if( self.quadrant3x3 == TOPLEFT or self.quadrant3x3 == CENTERLEFT or self.quadrant3x3 == BOTTOMLEFT ):
            keys[ScanCodes.KEY_A]=True
        if( self.quadrant3x3 == BOTTOMLEFT or self.quadrant3x3 == BOTTOMMIDDLE or self.quadrant3x3 == BOTTOMRIGHT ):
            keys[ScanCodes.KEY_S]=True
        if( self.quadrant3x3 == CENTERRIGHT or self.quadrant3x3 == TOPRIGHT or self.quadrant3x3 == BOTTOMRIGHT ):
            keys[ScanCodes.KEY_D]=True
        return keys

    def handle_sounds( self, dataDicts ):
        # If we get input for `attack`, enable attack, otherwise if silence disable
        if ( self.detect('attack') ):
            self.attacking = True
        elif ( self.detect_silence() ):
            self.attacking = False

        elif ( self.detect('dash') ):
            self.log('dash')
            self.short_press_key(ScanCodes.KEY_SPACE)

        # cast is RMB single click, for now?
        elif ( self.detect('cast') ):
            self.log('cast')
            self.drag_mouse(button='right')
            time.sleep(0.1)
            self.stop_drag_mouse(button='right')

        elif ( self.detect('special') ):
            self.log('special')
            self.short_press_key(ScanCodes.KEY_Q)

        elif ( self.detect('interact') ):
            self.interact()

        # If we get input for `move`, toggle moving
        elif ( self.detect('move') ):
            self.log('move')
            self.moving = not self.moving

        # If we are moving now, hold keys and maybe release some
        keys = self.get_wasd()
        if ( self.moving ):
            for key, held in keys.items():
                if ( held ):
                    self.press_key(key)
                else:
                    self.release_key(key)
        # If not moving release all keys
        else:
            for key in keys:
                self.release_key(key)

        # If we are attacking, hold LMB
        if ( self.attacking ):
            self.drag_mouse()
        else:
            self.stop_drag_mouse()
