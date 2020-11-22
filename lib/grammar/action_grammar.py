from dragonfly import Mouse, MappingRule

class ActionSpeechCommand(MappingRule):
    def __init__( self, mapping ):
        self.mapping = mapping
        MappingRule.__init__(self)
