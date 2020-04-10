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

import os
from collections import namedtuple

from doslib.event import EventTextBlock, EventTables
from doslib.gen.map import Npc
from doslib.maps import Maps, TreasureChest
from doslib.rom import Rom
from doslib.textblock import TextBlock
from event import easm
from event.epp import pparse
from randomizer.flags import Flags
from randomizer.keyitemrewards import *
from randomizer.placements import Placements
from stream.outputstream import AddressableOutputStream, OutputStream

KeyItem = namedtuple("KeyItem", ["sprite", "movable", "key_item", "reward"])
NpcSource = namedtuple("NpcSource", ["map_id", "npc_index", "ship", "airship"])
ChestSource = namedtuple("ChestSource", ["map_id", "chest_id", "sprite_id", "ship", "airship"])
VehiclePlacement = namedtuple("VehiclePlacement", ["x", "y"])

EVENT_SOURCE_MAP = {}

NEW_REWARD_SOURCE = {
    "king": NpcSource(map_id=0x39, npc_index=2,
                      ship=VehiclePlacement(x=2328, y=2600), airship=VehiclePlacement(x=2328, y=2456)),
    "sara": NpcSource(map_id=0x39, npc_index=3,
                      ship=VehiclePlacement(x=2328, y=2600), airship=VehiclePlacement(x=2328, y=2456)),
    "bikke": NpcSource(map_id=0x62, npc_index=2,
                       ship=VehiclePlacement(x=3256, y=2344), airship=VehiclePlacement(x=3256, y=2296)),
    "marsh": ChestSource(map_id=0x5B, chest_id=5, sprite_id=0,
                         ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=1528, y=3656)),
    "astos": NpcSource(map_id=0x58, npc_index=0,
                       ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=1528, y=2104)),
    "matoya": NpcSource(map_id=0x61, npc_index=4,
                        ship=VehiclePlacement(x=2440, y=2136), airship=VehiclePlacement(x=2584, y=1784)),
    "elf": NpcSource(map_id=0x06, npc_index=7,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=2072, y=3448)),
    "locked_cornelia": ChestSource(map_id=0x38, chest_id=2, sprite_id=2,
                                   ship=VehiclePlacement(x=2328, y=2600), airship=VehiclePlacement(x=2328, y=2456)),
    "nerrick": NpcSource(map_id=0x57, npc_index=11,
                         ship=VehiclePlacement(x=1848, y=2104), airship=VehiclePlacement(x=1496, y=2392)),
    "vampire": ChestSource(map_id=0x03, chest_id=1, sprite_id=0,
                           ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=936, y=2888)),
    "sarda": NpcSource(map_id=0x37, npc_index=0,
                       ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=376, y=2952)),
    "lukahn": NpcSource(map_id=0x2F, npc_index=13,
                        ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=3384, y=3384)),
    "ice": NpcSource(map_id=0x44, npc_index=0,
                     ship=VehiclePlacement(x=3256, y=2344), airship=VehiclePlacement(x=3080, y=2840)),
    "citadel_of_trials": ChestSource(map_id=0x4F, chest_id=8, sprite_id=0,
                                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=1960, y=632)),
    "bahamut": NpcSource(map_id=0x54, npc_index=2,
                         ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1)),
    "waterfall": NpcSource(map_id=0x53, npc_index=0,
                           ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1)),
    "fairy": NpcSource(map_id=0x47, npc_index=11,
                       ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1)),
    "mermaids": ChestSource(map_id=0x1E, chest_id=12, sprite_id=0,
                            ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1)),
    "dr_unne": NpcSource(map_id=0x6A, npc_index=0,
                         ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=1192, y=2456)),
    "lefien": NpcSource(map_id=0x70, npc_index=11,
                        ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1)),
    "sky2": NpcSource(map_id=0x5D, npc_index=0,
                      ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1)),
    "smyth": NpcSource(map_id=0x57, npc_index=4,
                       ship=VehiclePlacement(x=1848, y=2104), airship=VehiclePlacement(x=1496, y=2392)),
    "desert": ChestSource(map_id=None, chest_id=12, sprite_id=0,
                          ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=3432, y=3688)),
    "lich": NpcSource(map_id=0x05, npc_index=10,
                      ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=936, y=2888)),
    "kary": NpcSource(map_id=0x2E, npc_index=0,
                      ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=2920, y=3176)),
    "kraken": NpcSource(map_id=0x17, npc_index=0,
                        ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1)),
    "tiamat": NpcSource(map_id=0x60, npc_index=0,
                        ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1)),
}

NEW_KEY_ITEMS = {
    "bridge": KeyItem(sprite=0x22, movable=True, key_item=None, reward=bridge_reward),
    "lute": KeyItem(sprite=0x00, movable=True, key_item=0x00, reward=lute_reward),
    "ship": KeyItem(sprite=0x45, movable=True, key_item=None, reward=ship_reward),
    "crown": KeyItem(sprite=0x94, movable=True, key_item=0x01, reward=crown_reward),
    "crystal": KeyItem(sprite=0x47, movable=True, key_item=0x02, reward=crystal_reward),
    "jolt_tonic": KeyItem(sprite=0x37, movable=True, key_item=0x03, reward=jolt_tonic_reward),
    "mystic_key": KeyItem(sprite=0x31, movable=False, key_item=0x04, reward=mystic_key_reward),
    "nitro_powder": KeyItem(sprite=0x0D, movable=True, key_item=0x05, reward=nitro_powder_reward),
    "canal": KeyItem(sprite=0x3B, movable=True, key_item=None, reward=canal_reward),
    "star_ruby": KeyItem(sprite=0x58, movable=False, key_item=0x08, reward=star_ruby_reward),
    "rod": KeyItem(sprite=0x39, movable=True, key_item=0x09, reward=rod_reward),
    "canoe": KeyItem(sprite=0x38, movable=True, key_item=0x10, reward=canoe_reward),
    "levistone": KeyItem(sprite=0x57, movable=False, key_item=0x0a, reward=levistone_reward),
    "rats_tail": KeyItem(sprite=0x25, movable=True, key_item=0x0c, reward=rats_tail_reward),
    "promotion": KeyItem(sprite=0x64, movable=False, key_item=None, reward=promotion_reward),
    "bottle": KeyItem(sprite=0x44, movable=True, key_item=0x0e, reward=bottle_reward),
    "oxyale": KeyItem(sprite=0x29, movable=True, key_item=0x0f, reward=oxyale_reward),
    "rosetta_stone": KeyItem(sprite=0x1B, movable=True, key_item=0x07, reward=rosetta_stone_reward),
    "lufienish": KeyItem(sprite=0x3A, movable=True, key_item=None, reward=lufienish_reward),
    "chime": KeyItem(sprite=0x21, movable=True, key_item=0x0b, reward=chime_reward),
    "warp_cube": KeyItem(sprite=0x2B, movable=True, key_item=0x0d, reward=warp_cube_reward),
    "adamantite": KeyItem(sprite=0x59, movable=False, key_item=0x06, reward=adamantite_reward),
    "excalibur": KeyItem(sprite=0x3C, movable=True, key_item=0x11, reward=excalibur_reward),
    "airship": KeyItem(sprite=0xac, movable=False, key_item=None, reward=airship_reward),
    "gear": KeyItem(sprite=0xc7, movable=False, key_item=None, reward=gear_reward),
    "earth": KeyItem(sprite=0x51, movable=False, key_item=None, reward=earth_reward),
    "fire": KeyItem(sprite=0x52, movable=False, key_item=None, reward=fire_reward),
    "water": KeyItem(sprite=0x50, movable=False, key_item=None, reward=water_reward),
    "air": KeyItem(sprite=0x4F, movable=False, key_item=None, reward=air_reward),
}


class KeyItemPlacement(object):

    def __init__(self, rom: Rom, flags: Flags, key_item_locations: tuple):
        self.rom = rom
        self.flags = flags
        self.maps = Maps(rom)
        self.events = EventTables(rom)
        self.event_text_block = EventTextBlock(rom)

        self.chests = self._load_chests()
        self.our_events = AddressableOutputStream(0x8223F4C, max_size=0x1860)

        for file in os.listdir("scripts/"):
            if file.endswith(".script"):
                add_events = KeyItemPlacement._parse_script(f"scripts/{file}")
                for event_id, source in add_events.items():
                    EVENT_SOURCE_MAP[event_id] = source

        by_source = {}
        for key_item in KeyItemPlacement._parse_data("data/KeyItemPlacement.tsv"):
            by_source[key_item["source"]] = key_item

        placements = Placements(key_item_locations)

        self._do_placement(key_item_locations, by_source)

    @staticmethod
    def _parse_data(data_file_path: str) -> list:
        data = []
        properties = None
        with open(data_file_path, "r") as data_file:
            first_line = True
            for line in data_file.readlines():
                if not first_line:
                    values = line.strip().split('\t')
                    row_data = {}
                    out = ""
                    for index, key in enumerate(properties):
                        if index < len(values):
                            if len(values[index]) == 0:
                                value = None
                                out += f"{key}={value},"
                            elif values[index].lower() in ["true", "false"]:
                                value = values[index].lower() == "true"
                                out += f"{key}={value},"
                            else:
                                try:
                                    value = int(values[index], 0)
                                    if key == "ship_x":
                                        out += f"ship=VehiclePlacement(x={value},"
                                    elif key == "ship_y":
                                        out += f"y={value}),"
                                    elif key == "airship_x":
                                        out += f"airship=VehiclePlacement(x={value},"
                                    elif key == "airship_y":
                                        out += f"y={value}),"
                                    else:
                                        out += f"{key}={hex(value)},"
                                except ValueError:
                                    value = values[index]
                                    out += f"{key}=\"{value}\","
                            row_data[key] = value
                        else:
                            out += f"{key}=None,"
                    data.append(row_data)
                    print(f"Placement({out}),")
                else:
                    properties = line.strip().split('\t')
                    print(f"{properties}")
                    first_line = False
        return data

    @staticmethod
    def _parse_script(script: str) -> dict:
        events = {}
        script_id = None
        script_code = ""
        with open(script, "r") as script_text:
            for line in script_text.readlines():
                if line.startswith("begin script="):
                    if script_id is not None:
                        events[script_id] = script_code
                        script_code = ""
                    script_id = int(line[line.find("=") + 1:], 0)
                elif script_id is not None:
                    script_code += line
        if script_id is not None:
            events[script_id] = script_code
        return events

    def _do_placement(self, key_item_locations: tuple, key_items: dict):
        source_headers = self._prepare_header(key_item_locations)

        event_sources = {}
        event_ids = sorted(EVENT_SOURCE_MAP.keys())
        patches = {}
        for event_id in event_ids:
            source = EVENT_SOURCE_MAP[event_id]
            event_source = pparse(f"{source_headers}\n\n{source}")

            event_sources[event_id] = source

            event_addr = self.events.get_addr(event_id)
            event_space = self.rom.get_event(Rom.pointer_to_offset(event_addr)).size()

            # See if the event fits into it's vanilla location.
            event = easm.parse(event_source, event_addr)
            if len(event) > event_space:
                # Didn't fit. Move it to our space.
                event_addr = self.our_events.current_addr()
                self.events.set_addr(event_id, event_addr)

                # We'll write all of our events together at the end
                event = easm.parse(event_source, event_addr)
                self.our_events.put_bytes(event)
            else:
                # Add the event to the vanilla patches.
                patches[Rom.pointer_to_offset(event_addr)] = event

        with open("sources.debug", "w") as debug:
            debug.write(f"Headers:\n{source_headers}\n\n")
            for event_id in sorted(event_sources.keys()):
                debug.write(f"Event: {hex(event_id)}\n{event_sources[event_id]}\n\n")

        self._update_npcs(key_item_locations)
        self._unite_mystic_key_doors()
        self._better_earth_plate()
        self._rewrite_give_texts()
        self._save_chests()

        # Append our new (relocated) events in the patch data.
        patches[0x223F4C] = self.our_events.get_buffer()

        # And then get all the patch data for the LUTs
        for offset, patch in self.events.get_patches().items():
            patches[offset] = patch
        self.rom = self.rom.apply_patches(patches)
        self.rom = self.maps.write(self.rom)

        # And, finally, update the vehicle start positions based on where they were
        ship_location = None
        airship_location = None

        for placement in key_item_locations:
            if placement.item == "ship":
                ship_location = NEW_REWARD_SOURCE[placement.location].ship
            elif placement.item == "airship":
                airship_location = NEW_REWARD_SOURCE[placement.location].airship

        if True or self.flags.start_item == "ship":
            print(f"Start with ship -> moved to Cornelia")
            ship_location = NEW_REWARD_SOURCE["king"].ship
        elif self.flags.start_item == "airship":
            print(f"Start with airship -> moved to Cornelia")
            airship_location = NEW_REWARD_SOURCE["king"].airship

        vehicle_starts = OutputStream()
        vehicle_starts.put_u32(ship_location.x)
        vehicle_starts.put_u32(ship_location.y)
        vehicle_starts.put_u32(airship_location.x)
        vehicle_starts.put_u32(airship_location.y)

        self.rom = self.rom.apply_patch(0x65278, vehicle_starts.get_buffer())

    def _prepare_header(self, key_item_locations: tuple) -> str:
        working_header = STD_HEADER

        if self.flags.start_item == "ship":
            print(f"Starting with the ship...")
            working_header += "\n#define FREE_START set_flag 0x05\n"
        elif self.flags.start_item == "airship":
            print(f"Starting with the airship...")
            working_header += "\n#define FREE_START set_flag 0x15\n"
        else:
            print(f"Starting with nothing...")
            working_header += "\n#define FREE_START nop\n"

        for placement in key_item_locations:
            if placement.location not in NEW_REWARD_SOURCE:
                continue
            if placement.item not in NEW_KEY_ITEMS:
                continue

            location = placement.location
            key_item = NEW_KEY_ITEMS[placement.item]

            base_reward_text = key_item.reward
            reward_text = base_reward_text.replace("GIVE_REWARD", f"GIVE_{location.upper()}_REWARD")
            reward_text = reward_text.replace("%text_id", f"%{location}_text_id")
            reward_text = reward_text.replace("%reward_flag", f"%{location}_reward_flag")

            if placement.location == "desert":
                reward_text += f"\n%desert_reward_sprite {hex(key_item.sprite)}"

            working_header += f";---\n; {placement.item} -> {location}\n;---\n{reward_text}\n\n"
        return working_header

    def _update_npcs(self, key_item_locations: tuple):

        print(f"Key Items: {key_item_locations}")

        for placement in key_item_locations:
            if placement.location not in NEW_REWARD_SOURCE:
                continue
            if placement.item not in NEW_KEY_ITEMS:
                continue

            source = NEW_REWARD_SOURCE[placement.location]
            key_item = NEW_KEY_ITEMS[placement.item]
            if isinstance(source, NpcSource):
                self._replace_map_npc(source.map_id, source.npc_index, key_item.sprite, key_item.movable)

                # Special case for "Sara" -- also update Chaos Shrine.
                if placement.location == "sara":
                    self._replace_map_npc(0x1f, 6, key_item.sprite, key_item.movable)
            elif isinstance(source, ChestSource):
                if source.map_id is not None:
                    self._replace_chest(source.map_id, source.chest_id, key_item.sprite)

    def _unite_mystic_key_doors(self):
        maps_with_doors = [
            0x06,  # Elven Castle
            0x38,  # Castle Cornelia 1F
        ]

        # There are two events (in vanilla) for mystic key locked doors.
        # - 0x1f4a: This door has been bound by the mystic key.
        # - 0x23cd: The treasure house has been bound by the mystic key.
        # In order to simplify some of the logic, change the 3 instances of the second to the first
        # since it's more generic.
        for map_id in maps_with_doors:
            map = self.maps.get_map(map_id)
            for sprite in map.sprites:
                if sprite.event == 0x23cd:
                    sprite.event = 0x1f4a

    def _better_earth_plate(self):
        self.maps.get_map(0x3).npcs[0xe].event = 0x139c

    def _rewrite_give_texts(self):
        with open("data/event_text.tsv", "r") as event_text:
            for line in event_text.readlines():
                string_num, text = line.strip().split('\t')
                string_num = int(string_num, 16)

                if not text.endswith('\x00'):
                    text += '\x00'

                self.event_text_block.strings[string_num] = TextBlock.encode_text(text)

        self.rom = self.event_text_block.pack(self.rom)

    def _replace_map_npc(self, map_id: int, npc_index: int, sprite: int, movable: bool):
        map = self.maps.get_map(map_id)
        map.npcs[npc_index].sprite_id = sprite

        # Some sprites weren't designed to move, so hold them still.
        if not movable:
            map.npcs[npc_index].move_speed = 0

    def _replace_chest(self, map_id: int, chest_id: int, sprite_id: int):
        map = self.maps.get_map(map_id)
        chest, sprite = map.get_event_chest(chest_id)
        map.chests.remove(chest)
        map.sprites.remove(sprite)

        chest_npc = Npc()
        chest_npc.identifier = 0x2
        chest_npc.in_room = 0x1
        chest_npc.x_pos = sprite.x_pos
        chest_npc.y_pos = sprite.y_pos
        chest_npc.move_speed = 0
        chest_npc.event = sprite.event

        if map_id in [0x38, 0x5b, 0x1e]:
            # Use a chest in Cornelia, Marsh, and the mermaid floor in Sea.
            chest_npc.sprite_id = 0xc7
        else:
            chest_npc.sprite_id = sprite_id
        map.npcs.append(chest_npc)

    def _load_chests(self) -> list:
        chest_stream = self.rom.open_bytestream(0x217FB4, 0x400)
        chests = []
        for index in range(256):
            chest = TreasureChest.read(chest_stream)
            chests.append(chest)
        return chests

    def _save_chests(self):
        # Save the chests (without key items in them).
        chest_data = OutputStream()
        for chest in self.chests:
            chest.write(chest_data)
        self.rom = self.rom.apply_patch(0x217FB4, chest_data.get_buffer())


STD_HEADER = """
#define WINDOW_TOP 0x0
#define WINDOW_BOTTOM 0x1
#define DIALOG_WAIT 0x1
#define DIALOG_AUTO_CLOSE 0x0
"""
