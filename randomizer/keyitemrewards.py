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

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#
# Key Item Reward snippets
#
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

bridge_reward = """
%text_id 0x127
%reward_flag 0x03

#define GIVE_REWARD set_flag %reward_flag
"""

lute_reward = """
%text_id 0x10a
%reward_flag 0x04

#define GIVE_REWARD \\
    give_item 0x0 \\
    set_flag %reward_flag
"""

ship_reward = """
%text_id 0x224
%reward_flag 0x05

#define GIVE_REWARD set_flag %reward_flag
"""

crown_reward = """
%text_id 0x10b
%reward_flag 0x06

#define GIVE_REWARD \\
    give_item 0x01 \\
    set_flag %reward_flag
"""

crystal_reward = """
%text_id 0x1f3
%reward_flag 0x07

#define GIVE_REWARD \\
    give_item 0x02 \\
    set_flag %reward_flag
"""

jolt_tonic_reward = """
%text_id 0x216
%reward_flag 0x08

#define GIVE_REWARD \\
    give_item 0x03 \\
    set_flag %reward_flag
"""

mystic_key_reward = """
%text_id 0x154
%reward_flag 0x09

#define GIVE_REWARD \\
    give_item 0x04 \\
    set_flag %reward_flag \\
    remove_all 0x1f4a               ; Unlock all Mystic Key locked doors on the map
"""

nitro_powder_reward = """
%text_id 0x128
%reward_flag 0x0A

#define GIVE_REWARD \\
    give_item 0x05 \\
    set_flag %reward_flag
"""

canal_reward = """
%text_id 0x1e8
%reward_flag 0x0B

#define GIVE_REWARD set_flag %reward_flag
"""

star_ruby_reward = """
%text_id 0x142
%reward_flag 0x0D

#define GIVE_REWARD \\
    give_item 0x08 \\
    set_flag %reward_flag
"""

rod_reward = """
%text_id 0x21a
%reward_flag 0x0F

#define GIVE_REWARD \\
    give_item 0x09 \\
    set_flag %reward_flag
"""

canoe_reward = """
%text_id 0x1b1
%reward_flag 0x12

#define GIVE_REWARD \\
    give_item 0x10 \\
    set_flag %reward_flag
"""

levistone_reward = """
%text_id 0x10c
%reward_flag 0x14

#define GIVE_REWARD \\
    give_item 0x0a \\
    set_flag %reward_flag
"""

rats_tail_reward = """
%text_id 0x10d
%reward_flag 0x17

#define GIVE_REWARD \\
    give_item 0x0c \\
    set_flag %reward_flag
"""

promotion_reward = """
%text_id 0x1d2
%reward_flag 0x18

#define GIVE_REWARD \\
    set_flag %reward_flag \\
    promote_pcs 
"""

bottle_reward = """
%text_id 0x1bf
%reward_flag 0x19

#define GIVE_REWARD \\
    give_item 0x0e \\
    set_flag %reward_flag
"""

oxyale_reward = """
%text_id 0x1c0
%reward_flag 0x1a

#define GIVE_REWARD \\
    give_item 0x0f \\
    set_flag %reward_flag
"""

rosetta_stone_reward = """
%text_id 0x10e
%reward_flag 0x1c

#define GIVE_REWARD \\
    give_item 0x07 \\
    set_flag %reward_flag
"""

lufienish_reward = """
%text_id 0x235
%reward_flag 0x1e

#define GIVE_REWARD set_flag %reward_flag 
"""

chime_reward = """
%text_id 0x240
%reward_flag 0x1f

#define GIVE_REWARD \\
    give_item 0x0b \\
    set_flag %reward_flag
"""

warp_cube_reward = """
%text_id 0x241
%reward_flag 0x20

#define GIVE_REWARD \\
    give_item 0x0d \\
    set_flag %reward_flag
"""

adamantite_reward = """
%text_id 0x10f
%reward_flag 0x21

#define GIVE_REWARD \\
    give_item 0x06 \\
    set_flag %reward_flag
"""

excalibur_reward = """
%text_id 0x1ed
%reward_flag 0x23

#define GIVE_REWARD \\
    give_item 0x11 \\
    set_flag %reward_flag
"""

airship_reward = """
%text_id 0x270
%reward_flag 0x15

#define GIVE_REWARD set_flag %reward_flag 
"""

gear_reward = """
%text_id 0x47c
%reward_flag 0x28

#define GIVE_REWARD \\
    give_item_ex 0x1 0x8 \\
    set_flag %reward_flag
"""

earth_reward = """
%text_id 0x47d
%reward_flag 0x11

#define GIVE_REWARD set_flag %reward_flag
"""

fire_reward = """
%text_id 0x47e
%reward_flag 0x13

#define GIVE_REWARD set_flag %reward_flag
"""

water_reward = """
%text_id 0x47f
%reward_flag 0x1d

#define GIVE_REWARD set_flag %reward_flag
"""

air_reward = """
%text_id 0x480
%reward_flag 0x22

#define GIVE_REWARD set_flag %reward_flag
"""
