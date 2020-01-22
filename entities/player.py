class Player:
    def __init__(self, id, db):
        self.id = id
        self.db = db

    def get_info(self):
        return self.db.get_player_info(self.id)

