from lib.modes.base_mode import *

class SimpleClickMode(BaseMode):

    patterns = [
        {
            'name': 'hold',
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
            'name': 'right',
            'sounds': ['pop'],
            'threshold': {
                'percentage': 70,
                'intensity': 1000,
            },
            'throttle': {
                'right': 0.3
            }
        },
    ]

    def handle_sounds( self, dataDicts ):
        if (self.detect('hold')):
            self.toggle_drag_mouse(True)
        elif (self.detect('right')):
            self.rightclick()
