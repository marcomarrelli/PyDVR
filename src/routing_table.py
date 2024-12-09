from typing import Dict
from node import Node
from distance import Distance

class RouteTable:
    '''
        Class for the Routing Table

        @author: Marco Marrelli
        @date: 06/12/2024
    '''

    def __init__(self) -> None:
        ''' Constructor for the Routing Table '''

        self.routes: Dict[Node, Dict[Node, tuple[Distance, Node]]] = {}

    def add_route(self, source: Node, dest: Node, distance: Distance, next_hop: Node) -> None:
        ''' Add Route to the Routing Table '''

        if source not in self.routes:
            self.routes[source] = {}
        self.routes[source][dest] = (distance, next_hop)
    
    def get_route(self, source: Node, dest: Node) -> tuple[Distance, Node]:
        ''' Get Route from the Routing Table '''

        return self.routes[source].get(dest, (Distance(), None))