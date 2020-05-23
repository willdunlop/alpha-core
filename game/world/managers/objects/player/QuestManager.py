from struct import pack

from database.world.WorldDatabaseManager import WorldDatabaseManager
from network.packet.PacketWriter import PacketWriter, OpCode
from utils.constants.ObjectCodes import QuestGiverStatuses, QuestStatuses


class QuestManager(object):
    def __init__(self, owner):
        self.owner = owner
        # self.menu = {}

    # class QuestMenu:
    #     pass

    def get_dialog_status(self, world_obj):
        dialog_status = QuestGiverStatuses.QUEST_GIVER_NONE
        relations_list = WorldDatabaseManager.creature_quest_get_by_entry(world_obj.entry)               #   relations bounds, the quest giver
        involved_relations_list = WorldDatabaseManager.creature_involved_quest_get_by_entry(world_obj.entry)     #   involved relations bounds, the quest completer

        #   TODO: If unit is hostile to player, do not display status

        #   TODO: Quest finish, Loop through all the completion quests offered by this quest giver
        for involved_relation in involved_relations_list:
            if len(involved_relation) == 0: continue
            quest_entry = involved_relation[1]
            quest = WorldDatabaseManager.quest_get_by_entry(quest_entry)
            # TODO: put in a check for quest status when you have quests that are already accepted by player

        # Quest start, Loop through all the acceptable quests offered by this quest giver
        for relation in relations_list:
            new_dialog_status = QuestGiverStatuses.QUEST_GIVER_NONE
            quest_entry = relation[1]
            quest = WorldDatabaseManager.quest_get_by_entry(quest_entry)
            if (quest.Method == 0):
                new_dialog_status = QuestGiverStatuses.QUEST_GIVER_REWARD
            elif self.owner.level < quest.MinLevel & self.owner.level >= quest.MinLevel - 4:
                new_dialog_status = QuestGiverStatuses.QUEST_GIVER_FUTURE                   # Silver !
            elif self.owner.level >= quest.MinLevel & self.owner.level < quest.QuestLevel + 7:
                new_dialog_status = QuestGiverStatuses.QUEST_GIVER_QUEST                    # Yellow !
            elif self.owner.level > quest.QuestLevel + 7:
                new_dialog_status = QuestGiverStatuses.QUEST_GIVER_TRIVIAL                  # Trivial, no exclamation mark will be displayed
            #   Update the status if it appears to be a "higher" code then any of the previous
            if new_dialog_status > dialog_status:
                dialog_status = new_dialog_status

        return dialog_status

    def prepare_quest_menu(self, questgiver):
        status = QuestStatuses.QUEST_STATUS_NONE
        menu = {}
        relations_list = WorldDatabaseManager.creature_quest_get_by_entry(questgiver.entry)               #   realtions bounds, the quest giver
        involved_relations_list = WorldDatabaseManager.creature_involved_quest_get_by_entry(questgiver.entry)     #   involved relations bounds, the quest completer

    def send_quest_status(self, questgiver_guid, quest_status):
        data = pack(
            '<2Q',
            questgiver_guid if questgiver_guid > 0 else self.owner.guid,
            quest_status
        )
        self.owner.session.request.sendall(PacketWriter.get_packet(OpCode.SMSG_QUESTGIVER_STATUS, data))