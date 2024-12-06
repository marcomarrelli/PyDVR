import math

class Distance:
    def __init__(self, cost: float = math.inf) -> None:
        self.cost = cost

    def __add__(self, other: 'Distance') -> 'Distance':
        return Distance(self.cost + other.cost)

    def __lt__(self, other: 'Distance') -> bool:
        return self.cost < other.cost