import math

class Distance:
    '''
        Class for Distance between Nodes

        @author: Marco Marrelli
        @date: 06/12/2024
    '''

    def __init__(self, cost: float = math.inf) -> None:
        ''' Constructor for Distance Class '''

        self.cost = cost

    def __add__(self, other: 'Distance') -> 'Distance':
        ''' Add Operator for Distance Class '''

        return Distance(self.cost + other.cost)

    def __lt__(self, other: 'Distance') -> bool:
        ''' Less Than Operator for Distance Class '''

        return self.cost < other.cost