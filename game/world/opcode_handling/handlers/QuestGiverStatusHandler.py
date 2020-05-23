from struct import unpack, pack

from database.world.WorldDatabaseManager import WorldDatabaseManager
from game.world.managers.GridManager import GridManager
from utils.Logger import Logger
from utils.constants import ObjectCodes

from network.packet.PacketWriter import PacketWriter, OpCode


class QuestGiverStatusHandler(object):

    @staticmethod
    def handle(world_session, socket, reader):
        if len(reader.data) >= 8:  # Avoid handling empty set selection packet
            questgiver_guid = unpack('<Q', reader.data[:8])[0]
            questgiver_npc = GridManager.get_surrounding_unit_by_guid(world_session.player_mgr, questgiver_guid)
            # Terminate method if questgiver could not be found
            if not questgiver_npc:
                Logger.error("Error in OpCode CMSG_QUESTGIVER_STATUS_QUERY, could not find questgiver with guid of: %s"%(questgiver_guid))
                return 0

            if world_session.player_mgr:
                #   Get the status for this questgiver
                questgiver_status = world_session.player_mgr.quests.get_dialog_status(questgiver_npc)
                #   Construct the packet and send it off
                world_session.player_mgr.quests.send_quest_status(questgiver_guid, questgiver_status)

        return 0