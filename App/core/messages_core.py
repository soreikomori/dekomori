# usr/bin/env python3
# -*- coding: utf-8 -*-

def nokos_stall(memberMention, memberName, parsedDuration):
    #TODO refactor this, no longer used, check baitrole.py/baitrole for appropriate code 
    return f"**Stall Kick:** {memberMention} ({memberName}) joined earlier, but didn't complete onboarding in {parsedDuration}. They have _NOT_ been kicked, okay!?"

from App.dekomori import client
from App.utils.constants import get_commands_list
from App.utils.constants import get_cog_ids
from App.utils import formatting as fmt

commandList = get_commands_list(client)
cogIds = get_cog_ids(client)

def cog_id(cogName):
    """Returns the cog ID for a given cog name.

    Parameters
    ----------
    cogName : str
        The name of the cog.

    Returns
    -------
    int
        The cog ID for the given cog name.
    """
    return cogIds.get(cogName, None)

def slash(commandName):
    """Returns the slash command for a given command name.

    Parameters
    ----------
    commandName : str
        The name of the command.

    Returns
    -------
    str
        The slash command for the given command name.
    """
    if " " in commandName:
        cogName = commandName.split(" ")[0]
        commandName = commandName.split(" ")[1]
        return f"</{cogName} {commandName}:{cog_id(cogName)}>"
    else:
        return f"</{commandName}:{cog_id(commandName)}>"

class commands:
    baitrole = {
        "no_args": lambda: f"Hey, what exactly do you want me to do? There's {fmt.format_command_list(commandList['baitrole'])}!",
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
    },
    toggle = {
        "no_args": lambda: f"Hey, what exactly do you want me to toggle? There's {fmt.format_command_list(commandList['toggle'])}!",
        "dm": {
            "kick": {
                "on": lambda: "**DM On Kick Turned __On__:** I'll have some _deathly_ mercy on my enemies and DM them before I kick them!",
                "off": lambda: "**DM On Kick Turned __Off__:** No more DMs for anyone! I'll kick them till **DEATH**!",
            },
            "ban": {
                "on": lambda: "**DM On Ban Turned __On__:** I'll spare some _deathly_ words for my enemies before they face **DEATH**!",
                "off": lambda: "**DM On Ban Turned __Off__:** I have no words to spare, only **DEATH**!",
            },
            "kos": {
                "on": lambda: "**DM On Stall Kick Turned __On__:** I'll have some _deathly_ mercy on those who stall and DM them before I kick them!",
                "off": lambda: "**DM On Kick Turned __Off__:** No more DMs for stallers! They'll be _deathly_ kicked without warning!",
            },
        },
        "delwm": {
            "on": lambda: "**Delete Welcome Messages Turned __On__:** I'll delete the welcome messages for users who took the bait!",
            "off": lambda: "**Delete Welcome Messages Turned __Off__:** I'll let the welcome messages be!",
        },
        "action": {
            "ban": lambda: "**Action Set To __Banning__:** They shall be banned and face **DEATH** itself!",
            "kick": lambda: "**Action Set To __Kicking__:** I'll spare them from **DEATH** and just kick them away!",
            "rjc_off": lambda: "**Rejoin Checker Turned __Off__:** I've also turned off the Rejoin Checker, as it only works when kicking!"
        },
        "kos": {
            "on": lambda: "**Kick on Stall Turned __On__:** I'll kick users who stall in the onboarding process!",
            "off": lambda: "**Kick on Stall Turned __Off__:** I'll just leave users who stall be, then!"
        },
        "kick_spf": {
            "on": lambda: "**Flagged Spammer Kick Turned __On__:** Got it! I'll keep an eye out for _deathly_ spammers!",
            "off": lambda: "**Flagged Spammer Kick Turned __Off__:** Okay, no more _deathly_ spammer checks!",
        },
        "rjc": {
            "on": lambda: "**Rejoin Checker Turned __On__:** I'll notify the role when someone tries to rejoin the server multiple times in a row!",
            "off": lambda: "**Rejoin Checker Turned __Off__:** No more notifications, only **DEATH**!",
            "no_ping_role": lambda: f"You need to set a role to ping first! Use `d!rejoinchecker pingrole` or {slash('rejoinchecker pingrole')}.",
            "no_max_join_count": lambda: f"You need to set the maximum number of joins first! Use `d!rejoinchecker setmax` or {slash('rejoinchecker setmax')}.",
            "action_is_ban": lambda: f"The Rejoin Checker only works if I'm kicking users, not banning them! Use `d!toggle action` or {slash('toggle action')} to change it!",
        },
        "rjc_kick": {
            "on": lambda: "**Rejoin Checker Kick Turned __On__:** I'll kick users who try to rejoin the server multiple times in a row!",
            "off": lambda: "**Rejoin Checker Kick Turned __Off__:** I'll spare some _deathly_ mercy and just ping the role, but the user will stay!",
            "rjc_was_off": lambda: f"**NOTE**: The Rejoin Checker is still disabled even if you turn this on! Use `d!toggle rjc` or {slash('toggle rjc')} to enable it!",
        },
    }