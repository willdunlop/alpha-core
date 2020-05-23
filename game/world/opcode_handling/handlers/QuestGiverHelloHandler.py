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
            questgiver_npc = GridManager.get_surrounding_unit_by_guid(world_session.player_mgr, guid)
            if not questgiver_npc:
                Logger.error("Error with OpCode CMSG_QUESTGIVER_HELLO, could not find questgiver with guid of: %s"%(guid))
                return 0

            print("QGiver: %s"%(questgiver_npc.entry))
            print("QGiver.faction: %s"%(questgiver_npc.faction))

            # TODO: Cancel feign death, if it even exists at this point

            # TODO: Stop the npc if they are moving

        return 0

