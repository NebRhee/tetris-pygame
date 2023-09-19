class Position:

    def __init__(self, row, col):
        self.row = row
        self.col = col
    

    def is_equal(self, other_pos):
        if isinstance(other_pos, Position):
            return self.row == other_pos.row and self.col == other_pos.col
        return False
    
    # Debug function
    def print_pos(self, block):
        print(self.row, self.col, end=" ")
        print(block.row, block.col)