#  Copyright 2020 Nicole Borrelli
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

from collections import namedtuple, KeysView

PlacementDetails = namedtuple("Placement",
                              ['source', 'type', 'sprite', 'movable', 'map_id', 'index', 'sprite_index', 'ship',
                               'airship', 'reward', 'plot_flag', 'plot_item', 'extra'])
VehiclePlacement = namedtuple("VehiclePlacement", ["x", "y"])


class Placements(object):
    def __init__(self, key_item_locations: tuple):
        self._by_source = {}
        self._by_reward = {}

        # Create two lookup tables so we can lookup the data we need to build the shuffled placement.
        by_source = {}
        by_reward = {}
        for vanilla_placement in PLACEMENT_DATA:
            by_source[vanilla_placement.source] = vanilla_placement
            by_reward[vanilla_placement.reward] = vanilla_placement

        for key_item_location in key_item_locations:
            # Caravan isn't shuffled, and we don't record it, so skip it
            if key_item_location.location == "caravan":
                continue

            source = by_source[key_item_location.location]
            reward = by_reward[key_item_location.item]
            print(f"{reward.reward} -> {source.source}")

    def from_source(self, source: str) -> PlacementDetails:
        return self._by_source[source]

    def from_reward(self, reward: str) -> PlacementDetails:
        return self._by_reward[reward]

    def all_sources(self) -> KeysView:
        return self._by_source.keys()

    def all_rewards(self) -> KeysView:
        return self._by_reward.keys()


PLACEMENT_DATA = [
    PlacementDetails(source="king", type="npc", sprite=0x22, movable=True, map_id=0x39, index=0x2, sprite_index=-0x1,
                     ship=VehiclePlacement(x=2328, y=2600), airship=VehiclePlacement(x=2328, y=2456), reward="bridge",
                     plot_flag="Obtained Bridge", plot_item=None, extra=None),
    PlacementDetails(source="sara", type="npc", sprite=0x0, movable=True, map_id=0x39, index=0x3, sprite_index=-0x1,
                     ship=VehiclePlacement(x=2328, y=2600), airship=VehiclePlacement(x=2328, y=2456), reward="lute",
                     plot_flag="Obtained Lute", plot_item="Lute", extra=None),
    PlacementDetails(source="bikke", type="npc", sprite=0x45, movable=True, map_id=0x62, index=0x2, sprite_index=-0x1,
                     ship=VehiclePlacement(x=3256, y=2344), airship=VehiclePlacement(x=3256, y=2296), reward="ship",
                     plot_flag="Obtained Ship", plot_item=None, extra=None),
    PlacementDetails(source="marsh", type="chest", sprite=0x94, movable=True, map_id=0x5b, index=0x5, sprite_index=0x0,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=1528, y=3656), reward="crown",
                     plot_flag="Obtained Crown", plot_item="Crown", extra=None),
    PlacementDetails(source="astos", type="npc", sprite=0x47, movable=True, map_id=0x58, index=0x0, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=1528, y=2104), reward="crystal",
                     plot_flag="Obtained Crystal Eye", plot_item="Crystal Eye", extra=None),
    PlacementDetails(source="matoya", type="npc", sprite=0x37, movable=True, map_id=0x61, index=0x4, sprite_index=-0x1,
                     ship=VehiclePlacement(x=2440, y=2136), airship=VehiclePlacement(x=2584, y=1784),
                     reward="jolt_tonic",
                     plot_flag="Obtained Jolt Tonic", plot_item="Jolt Tonic", extra=None),
    PlacementDetails(source="elf", type="npc", sprite=0x31, movable=False, map_id=0x6, index=0x7, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=2072, y=3448), reward="mystic_key",
                     plot_flag="Obtained Mystic Key", plot_item="Mystic Key", extra="remove_all 0x1f4a"),
    PlacementDetails(source="locked_cornelia", type="chest", sprite=0xd, movable=True, map_id=0x38, index=0x2,
                     sprite_index=0x2,
                     ship=VehiclePlacement(x=2328, y=2600), airship=VehiclePlacement(x=2328, y=2456),
                     reward="nitro_powder", plot_flag="Obtained Nitro Powder", plot_item="Nitro Powder", extra=None),
    PlacementDetails(source="nerrick", type="npc", sprite=0x3b, movable=True, map_id=0x57, index=0xb, sprite_index=-0x1,
                     ship=VehiclePlacement(x=1848, y=2104), airship=VehiclePlacement(x=1496, y=2392), reward="canal",
                     plot_flag="Obtained Canal", plot_item=None, extra=None),
    PlacementDetails(source="vampire", type="chest", sprite=0x58, movable=False, map_id=0x3, index=0x1,
                     sprite_index=0x0,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=936, y=2888), reward="star_ruby",
                     plot_flag="Obtained Star Ruby", plot_item="Star Ruby", extra=None),
    PlacementDetails(source="sarda", type="npc", sprite=0x39, movable=True, map_id=0x37, index=0x0, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=376, y=2952), reward="rod",
                     plot_flag="Obtained Earth Rod", plot_item="Earth Rod", extra=None),
    PlacementDetails(source="lukahn", type="npc", sprite=0x38, movable=True, map_id=0x2f, index=0xd, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=3384, y=3384), reward="canoe",
                     plot_flag="Obtained Canoe", plot_item="Canoe", extra=None),
    PlacementDetails(source="ice", type="npc", sprite=0x57, movable=False, map_id=0x44, index=0x0, sprite_index=-0x1,
                     ship=VehiclePlacement(x=3256, y=2344), airship=VehiclePlacement(x=3080, y=2840),
                     reward="levistone",
                     plot_flag="Obtained Levistone", plot_item="Levistone", extra=None),
    PlacementDetails(source="citadel_of_trials", type="chest", sprite=0x25, movable=True, map_id=0x4f, index=0x8,
                     sprite_index=0x0,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=1960, y=632), reward="rats_tail",
                     plot_flag="Obtained Rat's Tail", plot_item="Rat's Tail", extra=None),
    PlacementDetails(source="bahamut", type="npc", sprite=0x64, movable=False, map_id=0x54, index=0x2,
                     sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1), reward="promotion",
                     plot_flag="Obtained Class Change", plot_item=None, extra="promote_pcs"),
    PlacementDetails(source="waterfall", type="npc", sprite=0x2b, movable=True, map_id=0x53, index=0x0,
                     sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1), reward="warp_cube",
                     plot_flag="Obtained Warp Cube", plot_item="Warp Cube", extra=None),
    PlacementDetails(source="fairy", type="npc", sprite=0x29, movable=True, map_id=0x47, index=0xb, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1), reward="oxyale",
                     plot_flag="Obtained Oxyale", plot_item="Oxyale", extra=None),
    PlacementDetails(source="mermaids", type="chest", sprite=0x1b, movable=True, map_id=0x1e, index=0xc,
                     sprite_index=0x0,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1), reward="rosetta_stone",
                     plot_flag="Obtained Rosetta Stone", plot_item="Rosetta Stone", extra=None),
    PlacementDetails(source="dr_unne", type="npc", sprite=0x3a, movable=True, map_id=0x6a, index=0x0, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=1192, y=2456), reward="lufienish",
                     plot_flag="Learned Lufienian", plot_item=None, extra=None),
    PlacementDetails(source="lefien", type="npc", sprite=0x21, movable=True, map_id=0x70, index=0xb, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1), reward="chime",
                     plot_flag="Obtained Chime", plot_item="Chime", extra=None),
    PlacementDetails(source="sky2", type="npc", sprite=0x59, movable=False, map_id=0x5d, index=0x0, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1), reward="adamantite",
                     plot_flag="Obtained Adamantite", plot_item="Adamantite", extra=None),
    PlacementDetails(source="smyth", type="npc", sprite=0x3c, movable=True, map_id=0x57, index=0x4, sprite_index=-0x1,
                     ship=VehiclePlacement(x=1848, y=2104), airship=VehiclePlacement(x=1496, y=2392),
                     reward="excalibur",
                     plot_flag="Obtained Excalibur", plot_item="Excalibur", extra=None),
    PlacementDetails(source="desert", type="chest", sprite=0xac, movable=False, map_id=0x0, index=0xc, sprite_index=0x0,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=3432, y=3688), reward="airship",
                     plot_flag="Obtained Airship", plot_item=None, extra=None),
    PlacementDetails(source="lich", type="npc", sprite=0x51, movable=False, map_id=0x5, index=0xa, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=936, y=2888), reward="earth",
                     plot_flag="Lit Earth Crystal", plot_item=None, extra=None),
    PlacementDetails(source="kary", type="npc", sprite=0x52, movable=False, map_id=0x2e, index=0x0, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=2920, y=3176), reward="fire",
                     plot_flag="Lit Fire Crystal", plot_item=None, extra=None),
    PlacementDetails(source="kraken", type="npc", sprite=0x50, movable=False, map_id=0x17, index=0x0, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1), reward="water",
                     plot_flag="Lit Water Crystal", plot_item=None, extra=None),
    PlacementDetails(source="tiamat", type="npc", sprite=0x4f, movable=False, map_id=0x60, index=0x0, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1), reward="air",
                     plot_flag="Lit Air Crystal", plot_item=None, extra=None),
    PlacementDetails(source="none", type="npc", sprite=0xc7, movable=False, map_id=0x0, index=0x0, sprite_index=-0x1,
                     ship=VehiclePlacement(x=-1, y=-1), airship=VehiclePlacement(x=-1, y=-1), reward="gear",
                     plot_flag="Obtained Gear", plot_item=None, extra=None),
]
