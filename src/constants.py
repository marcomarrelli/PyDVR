from typing import Final

'''
    Constants for the Application
    
    @author: Marco Marrelli
    @date: 06/12/2024
'''

class Network(object):
    MIN_NODES: Final[int] = int(3)
    ''' Minimum number of nodes in the network '''

    MAX_NODES: Final[int] = int(7)
    ''' Maximum Number of Nodes in the Network '''

    MIN_DISTANCE: Final[float] = float(1)
    ''' Minimum Distance Cost between Nodes '''

    MAX_DISTANCE: Final[float] = float(10)
    ''' Maximum Distance Cost between Nodes '''

class GUI(object):
    APPLICATION_WIDTH: Final[float] = 1000
    ''' Window Width '''

    APPLICATION_HEIGHT: Final[float] = 500
    ''' Window Height '''

    APPLICATION_TITLE: Final[str] = str("Distance Vector Routing Simulator")
    ''' Application Title '''

    APPLICATION_BACKGROUND_COLOR: Final[str] = str("#171717")
    ''' Background Color for the Main Window '''

    GRAPH_BACKGROUND_COLOR: Final[str] = str("#373737")
    ''' Background Color for the Graph '''

    APPLICATION_TEXT_COLOR: Final[str] = str("#F1F1F1")
    ''' Text Color '''

    ADD_BUTTON_TEXT: Final[str] = str("Add Router")
    ''' Add Router Button Text '''

    REMOVE_BUTTON_TEXT: Final[str] = str("Remove Router")
    ''' Remove Router Button Text '''

    RANDOMIZE_BUTTON_TEXT: Final[str] = str("Randomize")
    ''' Randomize Button Text '''

    START_BUTTON_TEXT: Final[str] = str("Start Simulation")
    ''' Start Simulation Button Text '''

    INITIAL_ROUTER_TABLE_TEXT: Final[str] = str("Press 'Start Simulation' to see routes")
    ''' Initial Router Table Text - Before 'Start Simulation' '''

    ROUTER_COLOR: Final[str] = str("#FFD700")
    ''' Router Color (in the Graph) '''