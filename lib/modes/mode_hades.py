from lib.modes.base_mode import *
from pressdirectxkey import PressKey, ReleaseKey, ScanCodes

class HadesMode(BaseMode):
    attacking = False
    moving = False
    held_keys = {}

    patterns = [
        {
            'name': 'attack',
            'sounds': ['hiss'],
            'threshold': {
                'percentage': 85,
                'intensity': 1000
            }
        },
        {
            'name': 'attack2',
            'sounds': ['zzh'],
            'threshold': {
                'percentage': 90,
                'intensity': 1000
            },
            'throttle': {
                'attack2': 0.3
            }
        },
        {
            'name': 'special',
            'sounds': ['ii'],
            'threshold': {
                'percentage': 50,
                'intensity': 1000
            },
            'throttle': {
                'special': 0.3
            }
        },
        {
            'name': 'interact call',
            'sounds': ['whistle'],
            'threshold': {
                'percentage': 90,
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
                'percentage': 85,
                'intensity': 1000,
            },  
            'throttle': {
                'dash': 0.3
            }
        },
        {
            'name': 'move',
            'sounds': ['cluck'],
            'threshold': {
                'percentage': 85,
                'intensity': 1000,
            },
            'throttle': {
                'move': 0.3
            }

        },
    ]

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

    def interact_call( self ):
        side = 'left' if self.detector.detect_mouse_quadrant( 2, 1 ) == 1 else 'right'
        # If we are moving, this is a "call"
        # otherwise it's interact or gift depending on mouse
        if ( self.moving ):
            self.short_press_key(ScanCodes.KEY_F)
        elif ( side == 'left' ): 
            self.short_press_key(ScanCodes.KEY_E)
        elif ( side == 'right' ):
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
        # If we get input for `move`, toggle moving
        if ( self.detect('move') ):
            self.moving = not self.moving

        elif ( self.detect('dash') ):
            self.short_press_key(ScanCodes.SPACE)

        # If we get input for `attack`, enable attack, otherwise if silence disable
        elif ( self.detect('attack') ):
            self.attacking = True
        elif ( self.detect_silence() ):
            self.attacking = False

        # Attack2 is RMB single click, for now?
        elif ( self.detect('attack2') ):
            self.drag_mouse(button='right')
            time.sleep(0.1)
            self.stop_drag_mouse(button='right')

        elif ( self.detect('special') ):
            self.short_press_key(ScanCodes.KEY_Q)

        elif ( self.detect('interact call') ):
            self.interact_call()

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
