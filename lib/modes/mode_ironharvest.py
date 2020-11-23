from lib.modes.base_mode import *

class IronHarvestMode(BaseMode):

    patterns = [
        {
            'name': 'left',
            'sounds': ['hiss'],
            'strategy': 'continuous',
            'threshold': {
                'percentage': 70,
                'lowest_percentage': 30,
                'intensity': 1000,
                'lowest_intensity': 300,
            }
        },
        {
            'name': 'right',
            'sounds': ['cluck'],
            'threshold': {
                'percentage': 70,
                'intensity': 1000,
            }
        },
        {
            'name': 'wasd',
            'sounds': ['hum'],
            'strategy': 'continuous',
            'threshold': {
                'percentage': 70,
                'lowest_percentage': 30,
                'intensity': 1000,
                'lowest_intensity': 300,
            }
        },
    ]

    def handle_sounds( self, dataDicts ):
        if (self.detect('left')):
            self.toggle_drag_mouse(True)
        elif (self.detect('right')):
            self.rightclick()
        elif (self.detect('wasd')):
            if( self.quadrant3x3 == TOPMIDDLE ):
                press('w')
            if( self.quadrant3x3 == TOPRIGHT ):
                press('e')
            if( self.quadrant3x3 == TOPLEFT ):
                press('q')
            elif( self.quadrant3x3 == CENTERLEFT ):
                press('a')
            elif( self.quadrant3x3 == CENTERRIGHT ):
                press('d')
            elif( self.quadrant3x3 == BOTTOMMIDDLE ):
                press('s')

