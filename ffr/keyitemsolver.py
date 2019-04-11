#  Copyright 2019 Nicole Borrelli
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import copy
import json
from collections import namedtuple
from random import seed, randint
from subprocess import run, PIPE

from doslib.event import EventTable, EventTextBlock, Event
from doslib.eventbuilder import EventBuilder
from doslib.maps import Maps
from doslib.rom import Rom
from ffr.eventrewrite import EventRewriter, Reward
from stream.output import Output


# TODO: Remove this once the class based one works
def solve_key_item_placement(seed: int):
    """Create a random distribution for key items (KI).
    Note: this requires an installation of Clingo 4.5 or better
    :param seed: The random number seed to use for the solver.
    :return: A list of tuples that contain item+location for each KI.
    """
    command = [
        "clingo", "asp/KeyItemSolving.lp", "asp/KeyItemData.lp",
        "--sign-def=3",
        "--seed=" + str(seed),
        "--outf=2"
    ]

    clingo_out = json.loads(run(command, stdout=PIPE).stdout)
    pairings = clingo_out['Call'][0]['Witnesses'][0]['Value']

    # All pairings are of the form "pair(item,location)" - need to parse the info
    Placement = namedtuple("Placement", ["item", "location"])

    ki_placement = []
    for pairing in pairings:
        pairing = Placement(*pairing[5:len(pairing) - 1].split(","))
        ki_placement.append(pairing)

    return tuple(ki_placement)


class KeyItemPlacement(object):
    def __init__(self, rom: Rom, rom_seed):
        self.rom = rom
        self.maps = Maps(rom)
        self.events = EventTable(rom, 0x7788, 0xbb7, base_event_id=0x1388)
        self.event_text_block = EventTextBlock(rom)

        # Reset the seed before placement begins.
        seed(rom_seed)
        self._do_placement()

    def _solve_placement(self, seed: int) -> tuple:
        """Create a random distribution for key items (KI).

        Note: this requires an installation of Clingo 4.5 or better

        :param seed: The random number seed to use for the solver.
        :return: A list of tuples that contain item+location for each KI.
        """
        command = [
            "clingo", "asp/KeyItemSolving.lp", "asp/KeyItemData.lp",
            "--sign-def=3",
            "--seed=" + str(seed),
            "--outf=2"
        ]

        clingo_out = json.loads(run(command, stdout=PIPE).stdout)
        pairings = clingo_out['Call'][0]['Witnesses'][0]['Value']

        # All pairings are of the form "pair(item,location)" - need to parse the info
        Placement = namedtuple("Placement", ["item", "location"])

        ki_placement = []
        for pairing in pairings:
            pairing = Placement(*pairing[5:len(pairing) - 1].split(","))
            ki_placement.append(pairing)

        return tuple(ki_placement)

    def _do_placement(self):
        key_item_locations = self._solve_placement(randint(0, 0xffffffff))

        # The Key items returned work like this. Suppose a Placement returned was
        # `Placement(item='oxyale', location='king')` this means that the "Oxyale" key item
        # should be found in the King of Cornelia location.
        #
        # This does *NOT* mean the King of Cornelia will give you Oxyale, rather, it means the NPC
        # that gives Oxyale (the Fairy) should be placed in the King's spot.
        #
        # Further, the Fairy in the King of Cornelia's spot, will be there at the start of the game, and
        # won't need to be rescued from the Bottle. It *does* mean that the Fairy won't provide Oxyale
        # until Garland is defeated and that NPC (or treasure) is itself rescued.

        for placement in key_item_locations:
            print(f"Placement: {placement}")

        self.rom = self._placement_king(0x94, 0x64)

    def _placement_king(self, king_sprite_id: int, kidnapped_sprite_id: int) -> Rom:
        garland_event_offset = Rom.pointer_to_offset(self.events.get_addr(0x138B))

        king_event = Event(self.rom.get_event(garland_event_offset))
        replacement = EventRewriter(king_event)
        replacement.include_dialogs(0x131)
        replacement.rewrite_dialog(0x127, 0x10b)

        # NPC indecies are:
        # - 6: Princess Sara's slot
        # - 2: The King of Cornelia
        # - 3: Pricess Sara in the throne room.
        replacement.visiting_npc(6, 2, 3)

        replacement.replace_reward(Reward(flag=0x2, mask=0x0), Reward(item=0x1))

        event_output = Output()
        replacement.rewrite().write(event_output)

        # Princess Sara has a unique sprite pose of her lying down, which is
        # set by the map init routine for the Chaos Shrine (map ID 0x1f).
        # The easy way around this is to change the command to just say "face down/south".
        make_npc_face_south = EventBuilder().set_npc_pose(6, 0).get_event()

        # There are two maps that Princess Sara appears on, and so our replacement
        # has to be placed in both places.
        maps = self.maps
        chaos_shrine = maps.get_map(0x1F)
        cornelia_castle_2f = maps.get_map(0x39)

        # In the Chaos Shrine, Sara is NPC #6
        chaos_shrine.npcs[6].sprite_id = kidnapped_sprite_id
        chaos_shrine_out = Output()
        chaos_shrine.write(chaos_shrine_out)

        # And in Cornelia Castle, she's NPC #3
        cornelia_castle_2f.npcs[3].sprite_id = kidnapped_sprite_id
        # And the King is #2
        cornelia_castle_2f.npcs[2].sprite_id = king_sprite_id
        cornelia_castle_2f_out = Output()
        cornelia_castle_2f.write(cornelia_castle_2f_out)

        patches = {
            0x813c: make_npc_face_south,
            garland_event_offset: event_output.get_buffer(),
            maps.get_map_offset(0x1f): chaos_shrine_out.get_buffer(),
            maps.get_map_offset(0x39): cornelia_castle_2f_out.get_buffer()
        }
        return self.rom.apply_patches(patches)
