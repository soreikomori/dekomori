# usr/bin/env python3
# -*- coding: utf-8 -*-

def nokos_stall(memberMention, memberName, parsedDuration):
    #TODO refactor this, no longer used, check baitrole.py/baitrole for appropriate code 
    return f"**Stall Kick:** {memberMention} ({memberName}) joined earlier, but didn't complete onboarding in {parsedDuration}. They have _NOT_ been kicked, okay!?"

from App.dekomori import client
from App.utils.constants import get_commands_list as get_commands
from App.utils import formatting as fmt

commands = get_commands(client)

class commands:
    baitrole = {
        "no_args": lambda: "Hey, what exactly do you want me to do? There's `add` and `remove`!",
        "add": {
            "tried_adding_all": lambda: "Hey, you can't add all roles to the bait roles list!",
            "valid": lambda roles: f"I added {', '.join(roles)} to the bait roles list!",
            "existing": lambda roles, plural: f"{', '.join(roles)} {plural} already in the bait roles list...",
            "invalid": lambda roles, plural: f"{', '.join(roles)} {plural} _deathly_ invalid...",
        },
        "remove": {
            "all_roles_invalid": lambda: "None of those roles are valid...",
            "valid": lambda roles: f"I removed {', '.join(roles)} from the bait roles list!",
            "not_in_list": lambda roles, plural: f"{', '.join(roles)} {plural} not in the bait roles list...",
            "invalid": lambda roles, plural: f"{', '.join(roles)} {plural} _deathly_ invalid...",
        },
    }