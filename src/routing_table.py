from typing import Dict
from node import Node
from distance import Distance

class RouteTable:
    def __init__(self):
        self.routes: Dict[Node, Dict[Node, tuple[Distance, Node]]] = {}
    
    def add_route(self, source: Node, dest: Node, distance: Distance, next_hop: Node):
        if source not in self.routes:
            self.routes[source] = {}
        self.routes[source][dest] = (distance, next_hop)
    
    def get_route(self, source: Node, dest: Node) -> tuple[Distance, Node]:
        return self.routes[source].get(dest, (Distance(), None))