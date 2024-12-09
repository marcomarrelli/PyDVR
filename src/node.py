class Node:
    '''
        Node Class, used to Represent a Router in the Network Graph.

        @author: Marco Marrelli
        @date: 06/12/2024
    '''
    
    def __init__(self, id: str) -> None:
        ''' Constructor for the Node '''

        self.id = id

    def __eq__(self, other: 'Node') -> bool:
        ''' Equals Operator of the Node '''

        return self.id == other.id

    def __hash__(self) -> int:
        ''' Hash Operator of the Node '''

        return hash(self.id)