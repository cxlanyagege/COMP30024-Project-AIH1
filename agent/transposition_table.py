# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent
# Team: AIH1
# Author: He Shen, Lanruo Su

import hashlib

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def store(self, board_hash, depth, value):
        self.table[board_hash] = (depth, value)

    def lookup(self, board_hash, depth):
        if board_hash in self.table:
            stored_depth, stored_value = self.table[board_hash]
            if stored_depth >= depth:
                return stored_value
        return None

    def generate_hash(self, board):
        return hashlib.sha256(str(board).encode()).hexdigest()
