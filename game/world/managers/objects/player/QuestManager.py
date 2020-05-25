from struct import pack

from database.world.WorldDatabaseManager import WorldDatabaseManager
from network.packet.PacketWriter import PacketWriter, OpCode
from utils.constants.ObjectCodes import QuestGiverStatuses, QuestStatuses


class QuestManager(object):
    def __init__(self, owner):
        self.owner = owner

    def get_dialog_status(self, world_obj):
        dialog_status = QuestGiverStatuses.QUEST_GIVER_NONE
        relations_list = WorldDatabaseManager.creature_quest_get_by_entry(world_obj.entry)               #   relations bounds, the quest giver
        involved_relations_list = WorldDatabaseManager.creature_involved_quest_get_by_entry(world_obj.entry)     #   involved relations bounds, the quest completer
        if self.owner.is_enemy_to(world_obj): return QuestGiverStatuses.QUEST_GIVER_NONE

        #   TODO: Quest finish
        for involved_relation in involved_relations_list:
            if len(involved_relation) == 0: continue
            quest_entry = involved_relation[1]
            quest = WorldDatabaseManager.quest_get_by_entry(quest_entry)
            # TODO: put in a check for quest status when you have quests that are already accepted by player

        # Quest start
        for relation in relations_list:
            new_dialog_status = QuestGiverStatuses.QUEST_GIVER_NONE
            quest_entry = relation[1]
            quest = WorldDatabaseManager.quest_get_by_entry(quest_entry)
            if (quest.Method == 0):
                new_dialog_status = QuestGiverStatuses.QUEST_GIVER_REWARD
            elif self.owner.level < quest.MinLevel and self.owner.level >= quest.MinLevel - 4:
                new_dialog_status = QuestGiverStatuses.QUEST_GIVER_FUTURE                   # Silver !
            elif self.owner.level >= quest.MinLevel and self.owner.level < quest.QuestLevel + 7:
                new_dialog_status = QuestGiverStatuses.QUEST_GIVER_QUEST                    # Yellow !
            elif self.owner.level > quest.QuestLevel + 7:
                new_dialog_status = QuestGiverStatuses.QUEST_GIVER_TRIVIAL                  # Trivial, no exclamation mark will be displayed
            #   Update the status if it appears to be a "higher" code then any of the previous
            if new_dialog_status > dialog_status:
                dialog_status = new_dialog_status

        return dialog_status

    def prepare_quest_giver_gossip_menu(self, quest_giver):
        # TODO: A gossip menu is the menu that (generally) appears when interacting with an NPC
        # It usually contains text and some options for things such as training, binding HS, buying, quests
        # This menu would be more appropriatley placed in the Player manager and could in fact be controlled by its own manager
        
        relations_list = WorldDatabaseManager.creature_quest_get_by_entry(quest_giver.entry)               #   realtions bounds, the quest giver
        involved_relations_list = WorldDatabaseManager.creature_involved_quest_get_by_entry(quest_giver.entry)     #   involved relations bounds, the quest completer
        #   Finish quests

        #   Starting quests
        for relation in relations_list:
            if len(relation) == 0: continue
            quest_entry = relation[1]
            quest = WorldDatabaseManager.quest_get_by_entry(quest_entry)
            self.check_quest_requirements(quest)

    def check_quest_requirements(self, quest):
        print("RequiredRaces: %s"%(quest.RequiredRaces))
        print("Race: %s"%(self.owner.player.race))
        print("Race mask: %s"%(self.owner.race_mask))
        print("Is required race: %s"%(quest.RequiredRaces & self.owner.race_mask == self.owner.race_mask))
        # Is the player character the required race
        race_is_required = quest.RequiredRaces > 0
        is_not_required_race = quest.RequiredRaces & self.owner.race_mask != self.owner.race_mask
        print("Is not required race: %s"%(is_not_required_race))
        print("The final condition: %s"%(quest.RequiredRaces > 0 & is_not_required_race))
        if race_is_required & is_not_required_race:
            print("The character is the incorrect race")
        #   Does the character have the required source item
        #   Is the character the required class
        #   Has the character already started the next quest in the chain
        #   Does the character have the previous quest
        #   Does the character have the required skill
        
        #   if one of the previous conditions failed, quest is failed

    def send_quest_status(self, quest_giver_guid, quest_status):
        data = pack(
            '<2Q',
            quest_giver_guid if quest_giver_guid > 0 else self.owner.guid,
            quest_status
        )
        self.owner.session.request.sendall(PacketWriter.get_packet(OpCode.SMSG_QUESTGIVER_STATUS, data))