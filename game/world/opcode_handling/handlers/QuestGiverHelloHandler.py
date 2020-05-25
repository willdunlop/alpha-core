from struct import unpack, pack

from database.world.WorldDatabaseManager import WorldDatabaseManager
from game.world.managers.GridManager import GridManager
from utils.Logger import Logger
from utils.constants import ObjectCodes

from network.packet.PacketWriter import PacketWriter, OpCode


class QuestGiverHelloHandler(object):

    @staticmethod
    def handle(world_session, socket, reader):
        if len(reader.data) >= 8:
            guid = unpack('<Q', reader.data[:8])[0]
            quest_giver = GridManager.get_surrounding_unit_by_guid(world_session.player_mgr, guid)
            if not quest_giver:
                Logger.error("Error with OpCode CMSG_QUESTGIVER_HELLO, could not find quest giver with guid of: %s"%(guid))
                return 0

            print("QGiver: %s"%(quest_giver.entry))
            print("QGiver.faction: %s"%(quest_giver.faction))

            # print("Testing is_friendly_to: %s"%(world_session.player_mgr.is_friendly_to(quest_giver)))            
            world_session.player_mgr.quests.prepare_quest_giver_gossip_menu(quest_giver)

            # TODO: Cancel feign death, if it even exists at this point

            # TODO: Stop the npc if they are moving

        return 0

