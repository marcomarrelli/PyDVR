'''
    GUI for the Distance Vector Routing Simulator

    @author: Marco Marrelli
    @date: 05/12/2024
'''

from typing import List
import math
import tkinter as tk
import random

from node import Node
from router import Router
from distance import Distance
import constants as Constants
from scripts.utils import Utils

class NetworkGUI:
    ''' GUI for the DVR Simulator '''

    def __init__(self) -> None:
        ''' Initializer for the GUI '''

        self.root: tk.Tk = tk.Tk()
        ''' Main Window '''

        self.routers: int = Constants.Network.MIN_NODES
        ''' Number of Routers in the Network '''

        self.router_list: List[Router] = []
        ''' List of Routers in the Network '''

        self.node_positions: List = []
        ''' List of Node Positions '''

        self.window: tk.Frame = tk.Frame(self.root, width = Constants.GUI.APPLICATION_WIDTH, height = Constants.GUI.APPLICATION_HEIGHT, background = Constants.GUI.APPLICATION_BACKGROUND_COLOR)
        ''' Main Frame '''

        self.control_frame: tk.Frame = tk.Frame(self.window, background = Constants.GUI.APPLICATION_BACKGROUND_COLOR)
        ''' Frame Used for Controls (Buttons) '''

        self.canvas: tk.Canvas = tk.Canvas(self.window, width = Utils.perc(Constants.GUI.APPLICATION_WIDTH, 65), height = Constants.GUI.APPLICATION_HEIGHT, background = Constants.GUI.GRAPH_BACKGROUND_COLOR)
        ''' Canva Used for Drawing the Network '''

        self.table_container: tk.Frame = tk.Frame(self.window, width = Utils.perc(Constants.GUI.APPLICATION_WIDTH, 35), height = Constants.GUI.APPLICATION_HEIGHT)
        ''' Frame Used for the RouteTable '''

        self.scrollbar: tk.Scrollbar = tk.Scrollbar(self.table_container)
        ''' Scrollbar for the RouteTable '''

        self.table_canvas: tk.Canvas = tk.Canvas(self.table_container, yscrollcommand = self.scrollbar.set)
        ''' Canva for the RouteTable '''

        self.table_frame: tk.Frame = tk.Frame(self.table_canvas)
        ''' Frame for the RouteTable '''

        self.addButton: tk.Button = tk.Button(self.control_frame, text = Constants.GUI.ADD_BUTTON_TEXT, command = self.add_node).pack(side = tk.LEFT, padx = 5)
        ''' Button Used to Add a Node '''

        self.removeButton: tk.Button = tk.Button(self.control_frame, text = Constants.GUI.REMOVE_BUTTON_TEXT, command = self.remove_node).pack(side = tk.LEFT, padx = 5)
        ''' Button Used to Remove a Node '''

        self.randomButton: tk.Button = tk.Button(self.control_frame, text = Constants.GUI.RANDOMIZE_BUTTON_TEXT, command = self.create_network_connections).pack(side = tk.LEFT, padx = 5)
        ''' Button Used to Randomize the Network Layout '''

        self.startButton: tk.Button = tk.Button(self.control_frame, text = Constants.GUI.START_BUTTON_TEXT, command = self.run_algorithm).pack(side = tk.LEFT, padx = 5)
        ''' Button Used to Start the Simulation '''

        # Setup the Application
        # Set the Title, Make it Not Resizable and Add Colors to Backgrounds
        self.root.title(string = Constants.GUI.APPLICATION_TITLE)
        self.root.resizable(width = False, height = False)
        self.root.configure(background = Constants.GUI.APPLICATION_BACKGROUND_COLOR)

        # Setup the Scrollbar
        self.table_container.pack_propagate(False)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)        
        self.table_canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.scrollbar.config(command = self.table_canvas.yview)
        self.table_frame.bind("<Configure>", lambda e: self.table_canvas.configure(
            scrollregion = self.table_canvas.bbox("all")
        ))

        # Packs the Window and the Frames
        self.table_canvas.create_window((0, 0), window = self.table_frame, anchor = "nw")
        self.window.pack(fill = tk.BOTH, expand = True, padx = 10, pady = 10)
        self.control_frame.pack(side = tk.TOP, fill = tk.X, pady = 5)
        self.canvas.pack(side = tk.LEFT, padx = 5, pady = 5)
        self.table_container.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True, padx = 5)

        # Initialize the Network and Clear the RouteTable
        self.initialize_network()
        self.clear_table()

        # AUTO Run the GUI
        self.root.mainloop()

    def initialize_network(self):
        ''' Initialize the Network Creating Routers and Their Connections '''
        
        # Clear Canvas, Router List
        self.router_list.clear()
        self.canvas.delete("all")
        self.node_positions = []
        ''' List of Node Positions '''

        center_x = Utils.perc(Constants.GUI.APPLICATION_WIDTH, 32.5)
        center_y = Utils.perc(Constants.GUI.APPLICATION_HEIGHT, 50)
        radius = min(Utils.perc(Constants.GUI.APPLICATION_WIDTH, 25), Utils.perc(Constants.GUI.APPLICATION_HEIGHT, 40))

        # Crea tutti i router e disegna i nodi
        for i in range(self.routers):
            angle = (2*math.pi*i)/self.routers - math.pi/2
            x = center_x + radius*math.cos(angle)
            y = center_y + radius*math.sin(angle)
            
            node = Node(chr(65 + i))
            router = Router(node)
            self.router_list.append(router)
            self.node_positions.append((x, y))

            # Disegna il nodo
            self.canvas.create_oval(x-20, y-20, x+20, y+20, 
                                fill=Constants.GUI.ROUTER_COLOR, tags="node")
            self.canvas.create_text(x, y, text=node.id, tags="node_label")
        
        # Dopo aver creato i nodi, crea le connessioni
        self.clear_table()

    def create_network_connections(self):
        """Create and draw connections between nodes ensuring all nodes are connected"""

        self.clear_table()
        self.canvas.delete("line", "cost", "cost_bg")

        adjacency_matrix = [[False] * self.routers for _ in range(self.routers)]

        connected_nodes = set()
        unconnected_nodes = set(range(self.routers))

        current_node = 0
        connected_nodes.add(current_node)
        unconnected_nodes.remove(current_node)

        while unconnected_nodes:
            min_distance = float('inf')
            next_node = None
            connecting_node = None

            for connected in connected_nodes:
                for unconnected in unconnected_nodes:
                    x1, y1 = self.node_positions[connected]
                    x2, y2 = self.node_positions[unconnected]
                    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)

                    if distance < min_distance:
                        min_distance = distance
                        next_node = unconnected
                        connecting_node = connected

            self.create_single_connection(connecting_node, next_node)
            adjacency_matrix[connecting_node][next_node] = True
            adjacency_matrix[next_node][connecting_node] = True

            connected_nodes.add(next_node)
            unconnected_nodes.remove(next_node)

        for i in range(self.routers):
            for j in range(i + 1, self.routers):
                if not adjacency_matrix[i][j] and random.random() < 0.3:
                    self.create_single_connection(i, j)
                    adjacency_matrix[i][j] = True
                    adjacency_matrix[j][i] = True

    def create_single_connection(self, i: int, j: int):
        """Helper method to create and draw a connection between two nodes"""

        # Prima controlla se la connessione già esiste
        if self.router_list[i].node in self.router_list[j].route_table.routes:
            return  # Se esiste già, non fare nulla

        # Crea la connessione logica
        distance = Distance(random.randint(1, 5))
        self.router_list[i].add_neighbor(self.router_list[j].node, distance)
        self.router_list[j].add_neighbor(self.router_list[i].node, distance)

        # Recupera le coordinate dei nodi
        x1, y1 = self.node_positions[i]
        x2, y2 = self.node_positions[j]

        # Disegna la linea sotto tutto
        self.canvas.create_line(x1, y1, x2, y2, tags = "line")

        # Calcola il punto medio per il costo
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        # Crea lo sfondo per il costo
        self.canvas.create_rectangle(
            mx-10, my-10, mx+10, my+10,
            fill = "white",
            outline = "white",
            tags = "cost_bg"
        )

        # Crea il testo del costo
        self.canvas.create_text(mx, my, text=str(distance.cost), fill="red", tags="cost")

        self.canvas.tag_raise("cost_bg", "line")
        self.canvas.tag_raise("cost", "cost_bg")
        self.canvas.tag_raise("node", "cost")
        self.canvas.tag_raise("node_label", "node")

    def add_node(self):
        if self.routers < 7:
            self.routers += 1
            self.initialize_network()
    
    def remove_node(self):
        if self.routers > 3:
            self.routers -= 1
            self.initialize_network()
    
    def run_algorithm(self):
        # Esegui l'algoritmo di routing

        while True:
            changes = False
            tables = [router.route_table for router in self.router_list]
            
            for router in self.router_list:
                changes |= router.update_routes(tables)
            
            if not changes:
                break
        
        self.update_route_table()

    def clear_table(self):
        '''Clear the route table'''
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        tk.Label(self.table_frame, text="Press 'Start Simulation' to see routes", 
                font=('Arial', 12)).pack(pady=5)

    def update_route_table(self):
        '''Update the route table after simulation'''
        # Pulisci la vecchia tabella
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Crea l'intestazione
        tk.Label(self.table_frame, text="Route Table", font=('Arial', 12, 'bold')).pack(pady=5)

        # Crea una tabella per ogni router
        for router in self.router_list:
            tk.Label(self.table_frame, 
                    text=f"Router {router.node.id}", 
                    font=('Arial', 10, 'bold')).pack(pady=2)

            # Crea una stringa formattata per le route
            routes_text = ""
            for dest in router.route_table.routes[router.node]:
                distance, next_hop = router.route_table.get_route(router.node, dest)
                if next_hop:
                    routes_text += f"To {dest.id} via {next_hop.id}: {distance.cost}\n"
            
            tk.Label(self.table_frame, text=routes_text).pack(pady=2)

        # Aggiorna la scrollregion
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
