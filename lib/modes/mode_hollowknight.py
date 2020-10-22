from config.config import *
from lib.modes.visual_mode import *
from lib.overlay_manipulation import update_overlay_image
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.0

class HollowknightMode(VisualMode):

    patterns = [
        {
            'name': 'map',
            'sounds': ['sound_whistle'],
            'threshold': {
                'percentage': 80,
                'power': 10000
            },            
            'throttle': {
                'map': 0.5
            }
        },
        {
            'name': 'movement_modes',
            'sounds': ['vowel_iy', 'vowel_y'],
            'threshold': {
                'percentage': 80,
                'power': 10000
            },            
            'throttle': {
                'movement_modes': 0.2
            }
        },
        {
            'name': 'press_arrowkeys',
            'sounds': ['vowel_aa', 'vowel_ah'],
            'threshold': {
                'percentage': 90,
                'power': 10000
            },
            'throttle': {
                'press_arrowkeys': 0.2
            }
        },
        {
            'name': 'hold_arrowkeys',
            'sounds': ['nasal_m', 'nasal_n'],
            'threshold': {
                'percentage': 90,
                'power': 40000
            },
            'continual_threshold': {
                'percentage': 40,
                'power': 10000
            }
        },        
        {
            'name': 'slash',
            'sounds': ['click_alveolar'],
            'threshold': {
                'percentage': 82,
                'power': 12000
            },
            'throttle': {
                'slash': 0.1
            }
        },
        {
            'name': 'up_slash',
            'sounds': ['click_dental'],
            'threshold': {
                'percentage': 90,
                'power': 12000
            },
            'throttle': {
                'jump': 0.1,
                'up_slash': 0.15,
                'down_slash': 0.15,
                'menu': 0.5                
            }
        },
        {
            'name': 'down_slash',
            'sounds': ['click_lateral'],
            'threshold': {
                'percentage': 90,
                'power': 12000
            },
            'throttle': {
                'jump': 0.1,            
                'down_slash': 0.15,
                'up_slash': 0.15,
                'menu': 0.5
            }
        },
        {
            'name': 'charge',
            'sounds': ['approximant_r'],
            'threshold': {
                'percentage': 90,
                'power': 12000
            },
            'continual_threshold': {
                'percentage': 30,
                'power': 3000                
            },
            'throttle': {
                'slash': 0.1
            }
        },
        {
            'name': 'jump',
            'sounds': ['sibilant_s', 'sibilant_z'],
            'threshold': {
                'percentage': 90,
                'power': 4000
            },
            'continual_threshold': {
                'percentage': 30,
                'power': 2000
            }
        },
        {
            'name': 'menu',
            'sounds': ['sound_finger_snap'],
            'threshold': {
                'percentage': 99 ,
                'power': 80000
            },
            'throttle': {
                'menu': 0.5
            }
        }
    ]
    
    def start(self):
        super().start()
        self.enable('single-press-grid')
        update_overlay_image('coords-overlay')
        
    
    hold_arrow_keys = []
        
    def handle_sounds( self, dataDicts ):
        if (self.detect('slash')):
            self.press('x')
        elif (self.detect('up_slash')):
            self.hold('up')
            self.press('x')
            self.release('up')
        elif (self.detect('down_slash')):
            self.hold('down')
            self.press('x')
            self.release('down')
        elif (self.detect('menu')):
            self.press('esc')
            self.toggle_singlepress()
        elif (self.detect('movement_modes')):
            self.toggle_singlepress()
            
        # Toggle the map open
        elif (self.detect('map')):
            self.toggle('tab')
                
            if (self.detect('tab')):
                self.inputManager.keyDown('tab')
            else:
                self.inputManager.keyUp('tab')
    
        # Make it possible to jump for various lengths of time
        if (self.detect('jump')):
            if (self.detect('space-held') == False):
                self.inputManager.keyDown('space')
                self.enable('space-held')
                self.detector.pointerController.update_origin_coords()
            
        elif (self.detect('space-held')):
            self.inputManager.keyUp('space')
            self.disable('space-held')
            
        # Make it possible to charge A
        if (self.detect('charge')):
            if (self.detect('charge-held') == False):
                self.inputManager.keyDown('a')
                self.enable('charge-held')
        elif (self.detect('charge-held')):
            self.inputManager.keyUp('a')
            self.disable('charge-held')
            
        # Movement types
        if (self.detect('precision_movement') and not self.detect('space-held')):
            if (self.detect('press_arrowkeys')):
                self.press_arrowkeys(dataDicts)
            elif (self.detect('hold_arrowkeys')):
                self.handle_arrowkeys(dataDicts)
            else:
                if ( len(self.hold_arrow_keys) > 0 ):
                    for key in self.hold_arrow_keys:
                        self.release( key )
                self.hold_arrow_keys = []
                
        # Arial movement
        elif(self.detect('space-held')):
            self.handle_arrowkeys(dataDicts, "relative")
            
        # Fast movement
        else:
            self.handle_arrowkeys(dataDicts)    
                
    def toggle_singlepress( self ):
        print( 'Toggling arrowkey mode' ) 
        self.toggle('precision_movement')
        if ( len(self.hold_arrow_keys) > 0 ):
            for key in self.hold_arrow_keys:
                self.release( key )
                
    def handle_arrowkeys( self, dataDicts, mode = "edges"):
        edges = self.handle_grid(mode)                   
        if ( len(self.hold_arrow_keys) > 0 ):
            for key in self.hold_arrow_keys:
                if ( key not in edges ):
                    self.release( key )

        if ( len(edges) > 0 ):
            for key in edges:
                if ( key not in self.hold_arrow_keys ):
                    self.hold( key )
        self.hold_arrow_keys = edges

    def press_arrowkeys( self, dataDicts):
        edges = self.handle_grid()
        if ( len(edges) > 0 ):
            for key in edges:
                self.press( key )

    def handle_grid( self, mode = "edges" ):
        if (mode == "edges" ):
            hold_arrowkeys = self.detector.detect_mouse_screen_edge( 200 )
                
            if ('left' not in hold_arrowkeys and ( self.quadrant3x3 == 1 or self.quadrant3x3 == 4 or self.quadrant3x3 == 7 ) ):
                hold_arrowkeys.append( 'left' )
            elif ('right' not in hold_arrowkeys and ( self.quadrant3x3 == 3 or self.quadrant3x3 == 6 or self.quadrant3x3 == 9 ) ):
                hold_arrowkeys.append( 'right' )            
        elif (mode == "relative"):
            hold_arrowkeys = self.detector.pointerController.detect_origin_directions( 100 )
            
        return hold_arrowkeys