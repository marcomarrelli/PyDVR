from typing import Dict, List

from node import Node
from distance import Distance
from routing_table import RouteTable

class Router:
    '''
        Class for the Router

        @author: Marco Marrelli
        @date: 06/12/2024
    '''

    def __init__(self, node: Node) -> None:
        ''' Constructor for the Router '''

        self.node = node
        self.neighbors: Dict[Node, Distance] = {}
        self.route_table = RouteTable()

    def add_neighbor(self, neighbor: Node, distance: Distance) -> None:
        ''' Add Neighbor to the Router '''

        self.neighbors[neighbor] = distance
        self.route_table.add_route(self.node, neighbor, distance, neighbor)
    
    def update_routes(self, route_tables: List[RouteTable]) -> bool:
        ''' Update Routes in the Router '''

        changed: bool = False # Flag to track if any Routes were Updated

        # Iterate over Each Neighbor and its Distance
        # then Get the Current Distance to the Neighbor from the Route Table
        for neighbor, distance_from_neighbor in self.neighbors.items():
            current_distance, _ = self.route_table.get_route(self.node, neighbor)

            # If the new distance is Shorter, update the Route
            if distance_from_neighbor < current_distance:
                self.route_table.add_route(self.node, neighbor, distance_from_neighbor, neighbor)
                changed = True

            # Iterate over Each Route Table from other Routers
            for route_table in route_tables:
                if neighbor not in route_table.routes: # Skip if the Neighbor is not in the Current Route Table
                    continue

                # Iterate over each destination and its distance from the neighbor
                for dest, (dest_distance, _) in route_table.routes[neighbor].items():
                    if dest == self.node: # Skip if the Destination is the Current Node
                        continue

                    # Calculate The New Distance To The Destination Through The Neighbor
                    new_distance = distance_from_neighbor + dest_distance
                    # Get The Current Distance To The Destination From The Route Table
                    current_distance, _ = self.route_table.get_route(self.node, dest)
                    
                    # If The New Distance Is Shorter, Update The Route
                    if new_distance < current_distance:
                        self.route_table.add_route(self.node, dest, new_distance, neighbor)
                        changed = True

        return changed # Return if there were and update to the Routes