class Node:
    def __init__(self, id: str) -> None:
        self.id = id
    
    def __eq__(self, other: 'Node') -> bool:
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)