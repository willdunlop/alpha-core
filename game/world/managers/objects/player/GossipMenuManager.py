
# TODO: Expand on this menu so that it can handle all gossip types and things like emotes
# Currently it only handles quests
class GossipMenuManager:
    def __init__(self, owner):
        self.owner = owner
        self.items = {}

    @staticmethod
    def add_menu_item(self, entry, status):
        self.items[entry] = status

    @staticmethod
    def clear_menu(self):
        self.items = {}