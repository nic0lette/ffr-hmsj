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

# All pairings are of the form "pair(item,location)" - need to parse the info
import json
from collections import namedtuple
from subprocess import PIPE, run

Placement = namedtuple("Placement", ["item", "location"])


def vanilla_placement() -> tuple:
    return (
        Placement("bridge", "king"),
        Placement("lute", "sara"),
        Placement("ship", "bikke"),
        Placement("crown", "marsh"),
        Placement("crystal", "astos"),
        Placement("jolt_tonic", "matoya"),
        Placement("mystic_key", "elf"),
        Placement("nitro_powder", "locked_cornelia"),
        Placement("canal", "nerrick"),
        Placement("star_ruby", "vampire"),
        Placement("rod", "sarda"),
        Placement("canoe", "lukahn"),
        Placement("levistone", "ice"),
        Placement("airship", "desert"),
        Placement("rats_tail", "citadel_of_trials"),
        Placement("promotion", "bahamut"),
        Placement("bottle", "caravan"),
        Placement("oxyale", "fairy"),
        Placement("rosetta_stone", "mermaids"),
        Placement("lufienish", "dr_unne"),
        Placement("chime", "lefien"),
        Placement("warp_cube", "waterfall"),
        Placement("adamantite", "sky2"),
        Placement("excalibur", "smyth"),
        Placement("earth", "lich"),
        Placement("fire", "kary"),
        Placement("water", "kraken"),
        Placement("air", "tiamat"),
    )


def solve_placement(seed: int) -> tuple:
    """Create a random distribution for key items (KI).

    Note: this requires an installation of Clingo 4.5 or better

    :param seed: The random number seed to use for the solver.
    :return: A list of tuples that contain item+location for each KI.
    """

    command = [
        "clingo", "asp/KeyItemSolvingShip.lp", "asp/KeyItemDataShip.lp",
        "--sign-def=rnd",
        "--seed=" + str(seed),
        "--outf=2"
    ]

    clingo_out = json.loads(run(command, stdout=PIPE).stdout)
    pairings = clingo_out['Call'][0]['Witnesses'][0]['Value']

    ki_placement = []
    for pairing in pairings:
        pairing = Placement(*pairing[5:len(pairing) - 1].split(","))
        ki_placement.append(pairing)

    return tuple(ki_placement)
