from typing import Dict, List

from node import Node
from distance import Distance
from routing_table import RouteTable

class Router:
    def __init__(self, node: Node):
        self.node = node
        self.neighbors: Dict[Node, Distance] = {}
        self.route_table = RouteTable()
    
    def add_neighbor(self, neighbor: Node, distance: Distance):
        self.neighbors[neighbor] = distance
        self.route_table.add_route(self.node, neighbor, distance, neighbor)
    
    def update_routes(self, route_tables: List[RouteTable]):
        changed = False

        for route_table in route_tables:
            for source in route_table.routes:
                for dest, (distance, next_hop) in route_table.routes[source].items():
                    if source in self.neighbors:
                        new_distance = self.neighbors[source] + distance
                        current_distance, _ = self.route_table.get_route(self.node, dest)
                        
                        if new_distance < current_distance:
                            self.route_table.add_route(self.node, dest, new_distance, source)
                            changed = True
        return changed