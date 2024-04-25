# usr/bin/env python3
# -*- coding: utf-8 -*-
# Dekomori by soreikomori
# Futsuwu ni nagareteku nichijou ni - muri shite najimaseta
# Shizunjimatta koseitachi wo kande nonde haite warau
version = "1.2.2"
################# IMPORTS #################

import logging.handlers
import discord
from discord import app_commands
from discord.ext import commands
import toml
import asyncio
import random
from typing import Literal, Optional
import logging
import datetime

################# INITIAL SETUP #################

# Help Command Class - from soheab_ on the discord.py discord server. Kudos!
class InteractionHelpCommand(commands.DefaultHelpCommand):
    async def send_pages(self) -> None:
        if interaction := self.context.interaction:
          await interaction.response.defer()
          for page in self.paginator.pages:
              await interaction.followup.send(page)
          return
        destination = self.get_destination()
        for page in self.paginator.pages:
            await destination.send(page)
# Client and Intent Definition
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix='d!', intents=intents, help_command=InteractionHelpCommand())
# Configuration Files
try:
    globalConfig = toml.load("./config/config.toml")
except FileNotFoundError:
    print("No config.toml found! Please make sure you have a config.toml in the config folder.")
    exit()
except toml.TomlDecodeError:
    print("config.toml is not a valid TOML file! Please make sure it's properly formatted, and that it is populated with values.")
    exit()
try:
    guildsDB = toml.load("./config/guilds_db.toml")
except FileNotFoundError:
    print("No guilds_db.toml found! Please make sure you have a guilds_db.toml in the config folder.")
    exit()
except toml.TomlDecodeError:
    print("guilds_db.toml is not a valid TOML file! Please make sure it's properly formatted, and that it is populated with values.")
    exit()
# Logging Setup
def setup_logger(logger, guild):
    """
    Sets up the logger object.

    Parameters
    ----------
    logger : logging.Logger
        The logger object to be set up.
    guild : discord.Guild
        The guild object to be used to set up the logger.
    """
    if guild == "global":
        logger.setLevel(logging.DEBUG if globalConfig["debug_logging"] else logging.INFO)
        logHandler = logging.handlers.RotatingFileHandler("./config/logs/dekomori.log", maxBytes=125000, backupCount=1, encoding='utf-8')
    else:
        guildId = str(guild.id)
        logger.setLevel(logging.DEBUG if guildsDB[guildId]["debug_logging"] else logging.INFO)
        logHandler = logging.handlers.RotatingFileHandler(f"./config/logs/{guildId}.log", maxBytes=125000, backupCount=1, encoding='utf-8')
    logFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logHandler.setFormatter(logFormatter)
    logger.addHandler(logHandler)
globalLogger = logging.getLogger("dekologger")
setup_logger(globalLogger, "global")

################# AUXILIARY FUNCTIONS #################

def evaluateBaitRoles(guildId, member):
    """
    Evaluates if a member has any of the bait roles. Returns True if the member has a bait role, False otherwise.

    Parameters
    ----------
    guildId : int
        The ID of the guild to be used.
    member : discord.Member
        The member object to be evaluated.
    """
    guildLogger = logging.getLogger(str(guildId))
    guildLogger.info(f"Evaluating bait roles for {member.name}.")
    guildId = str(guildId)
    memRoles = member.roles
    baitRoles = guildsDB[guildId]["bait_roles"]
    hasBaitRoles = any(role.id in baitRoles for role in memRoles)
    if hasBaitRoles:
        guildLogger.info(f"Found a bait role in {member.name}.")
        guildLogger.info(f"Evaluation complete for {member.name}.")
        return True
    guildLogger.info(f"No bait roles found in {member.name}.")
    guildLogger.info(f"Evaluation complete for {member.name}.")
    return False

def roleEdit(guildId, role, action):
    """
    Edits the bait roles list. Returns a list of roleIds added, 1 if the role is not a valid id, 2 if the role to be removed is not in the list or if the role to be added is already on the list.

    Parameters
    ----------
    guildId : int
        The ID of the guild to be used.
    role : str
        The role to be added or removed.
    action : Literal["add", "remove"]
        The action to be performed. Can be either "add" or "remove".
    """
    guildLogger = logging.getLogger(str(guildId))
    guildId = str(guildId)
    if role == "all":
        rawList = "all"
    elif "," in role:
        rawList = role.split(",")
    else:
        rawList = [role]
    roleList = []
    for role in rawList:
        guildLogger.debug(f"Attempting to add role: {role}")
        if rawList == "all":
            roleList = "all"
            guildLogger.debug("Role is all, exiting loop.")
            break
        role = role.strip()
        if role.startswith("<@&") and role.endswith(">") and role[3:-1].isdigit():
            guildLogger.debug("Role is a mention.")
            roleId = int(role[3:-1])
        elif role.isdigit():
            guildLogger.debug("Role is an ID.")
            roleId = int(role)
        else:
            guildLogger.debug("Invalid Role.")
            roleId = None
        roleList.append(roleId)
    modifList = []
    if action == "add":
        for indRole in roleList:
            if indRole not in guildsDB[guildId]["bait_roles"] and indRole is not None:
                modifList.append(indRole)
                guildsDB[guildId]["bait_roles"].append(indRole)
                guildLogger.info(f"Added {indRole} to bait roles.")
        if len(modifList) == 0:
            if any(isinstance(role, int) for role in roleList):
                return 2
            else:
                return 1
        return modifList
    elif action == "remove" and roleList != "all":
        for indRole in roleList:
            if indRole in guildsDB[guildId]["bait_roles"] and indRole is not None:
                modifList.append(indRole)
                guildsDB[guildId]["bait_roles"].remove(indRole)
                guildLogger.info(f"Removed {indRole} from bait roles.")
        if len(modifList) == 0:
            if any(isinstance(role, int) for role in roleList):
                return 2
            else:
                return 1
        return modifList
    elif action == "remove" and roleList == "all":
        guildsDB[guildId]["bait_roles"] = []
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")

def execRejoinChecker(guild, member):
    """
    Executes the rejoin checker. Returns True if the rejoin checker has reached the max join count, False otherwise.

    Parameters
    ----------
    guild : discord.Guild
        The guild object to be used.
    member : discord.Member
        The member object to be checked.
    """
    guildId = str(guild.id)
    guildLogger = logging.getLogger(guildId)
    if guildsDB[guildId]["rejoin_checker"]["enabled"]:
        if guildsDB[guildId]["rejoin_checker"]["userId"] == member.id:
            if guildsDB[guildId]["rejoin_checker"]["joinCount"] == guildsDB[guildId]["rejoin_checker"]["maxJoinCount"]-1:
                guildLogger.info(f"Max rejoin checker reached for {member.name}.")
                guildsDB[guildId]["rejoin_checker"]["joinCount"] = 0
                with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
                    toml.dump(guildsDB, f)
                globalLogger.debug(f"Wrote to guilds_db.toml.")
                guildLogger.info(f"Reset {member.name}'s Join Count to 0.")
                return True
            else:
                guildsDB[guildId]["rejoin_checker"]["joinCount"] += 1
                with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
                    toml.dump(guildsDB, f)
                globalLogger.debug(f"Wrote to guilds_db.toml.")
                guildLogger.info(f"Added 1 to Join Count for {member.name}.")
                return False
        else:
            guildsDB[guildId]["rejoin_checker"]["userId"] = member.id
            guildsDB[guildId]["rejoin_checker"]["joinCount"] = 1
            with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
                toml.dump(guildsDB, f)
            globalLogger.debug(f"Wrote to guilds_db.toml.")
            guildLogger.info(f"Added 1 to Join Count for {member.name}.")
        return False
    return False

def parseDuration(seconds):
    """
    Parses a duration in seconds to a human-readable format. Returns a string with the duration in days, hours, and minutes.
     
    Parameters
    ----------
    seconds : int
        The duration in seconds to be parsed.
    """
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return ' '.join(f"{int(value)}{unit[0]}" for value, unit in zip([days, hours, minutes], ['days', 'hours', 'minutes']) if value)

################# EVENTS #################

@client.event
async def on_ready():
    print(f"Dekomori Sanae, koko ni suisu!")
    print(f"Logged in succesfully as {client.user}.")
    globalLogger.info(f" - - - DEKOMORI {version} STARTED - - - ")
    globalLogger.info(f"Setting up logger for guilds.")
    for guild in client.guilds:
        globalLogger.info(f"Setting up logger for {guild.name}.")
        guildLogger = logging.getLogger(str(guild.id))
        setup_logger(guildLogger, guild)
        globalLogger.info(f"Logger set up for {guild.name}.")
        guildLogger.info(f" - - -  RECONNECTED DEKOMORI {version} - - - ")
    globalLogger.info(f"Beggining Stall Loop.")
    # STALL LOOP
    while True:
        for guildId in guildsDB:
            if guildsDB[guildId]["currenteval"] != []:
                guild = discord.utils.get(client.guilds, id=int(guildId))
                guildLogger = logging.getLogger(guildId)
                logChanObj = discord.utils.get(guild.text_channels, id=guildsDB[guildId]["log_channel_id"])
            for memberdict in guildsDB[guildId]["currenteval"]:
                # Timeout Checker
                timeElapsed = (datetime.datetime.now() - memberdict["joined"])
                if timeElapsed >= datetime.timedelta(seconds=memberdict["timeout"]):
                    member = discord.utils.get(guild.members, id=memberdict["memberid"])
                    guildLogger.warning(f"{member.name} has reached the stall timeout.")
                    # - - - - - - TIMEOUT ACTIONS - - - - - -
                    # - - - - - Kick on Stall - - - - -
                    parsedDuration = parseDuration(timeElapsed.seconds)
                    if guildsDB[guildId]["kick_on_stall"]:
                        # - - - - Kick Action - - - -
                        guildLogger.info(f"Attempting to kick {member.name}.")
                        # Permissions Check
                        if not guild.me.guild_permissions.kick_members:
                            guildLogger.critical(f"Missing permissions to kick {member.name}.")
                            await logChanObj.send(f"I don't have the necessary permissions to kick {member.mention} ({member.name})! Please check my permissions and try again! I'll leave them be for now.")
                        # DM Check
                        if guildsDB[guildId]["dm_on_stallkick"]:
                            guildLogger.info(f"Sending Stall Kick DM to {member.name}.")
                            dmChan = await member.create_dm()
                            await dmChan.send(content=guildsDB[guildId]["stall_dm_message"])
                        # Kick Loop
                        while True:
                            try:
                                await member.kick(reason="User didn't complete onboarding in time.")
                            except discord.errors.HTTPException:
                                guildLogger.error(f"Got an HTTPException while trying to kick {member.name}. Retrying...")
                            else:
                                guildLogger.info(f"Kicked {member.name}.")
                                await logChanObj.send(f"{member.mention} ({member.name}) joined earlier, but didn't complete onboarding in {parsedDuration}, so I've _deathly_ kicked them away!")
                                guildsDB[guildId]["kick_counter"] += 1
                                guildLogger.debug(f"Added 1 to Kick Counter.")
                                with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
                                    toml.dump(guildsDB, f)
                                globalLogger.debug(f"Wrote to guilds_db.toml.")
                                break
                    # - - - - - No Action - - - - -
                    else:
                        await logChanObj.send(f"{member.mention} ({member.name}) joined earlier, but didn't complete onboarding in {parsedDuration}. They're still here, so you might want to check on them!")
                    # - - - - - Rejoin Check - - - - - -
                    # The timeout rejoin check does not check for the rejoinchecker kick user setting.
                    if execRejoinChecker(guild, member):
                        maxJoinCount = guildsDB[guildId]["rejoin_checker"]["maxJoinCount"]
                        pingRole = discord.utils.get(guild.roles, id=guildsDB[guildId]["rejoin_checker"]["pingRoleId"])
                        await logChanObj.send(f"Oh? It looks like {member.mention} ({member.name}) has attempted to rejoin {maxJoinCount} times in a row now...! You should take a look, {pingRole.mention}, this could mean **DEATH**!")
        await asyncio.sleep(1)

@client.event
async def on_guild_join(guild):
    globalLogger.info(f"Joined {guild.name}.")
    guildId = str(guild.id)
    globalLogger.info(f"Adding {guild.name} with ID {guildId} to guildsDB file.")
    guildLogger = logging.getLogger(guildId)
    guildsDB[guildId] = {"paused": True,
                         "bait_roles": [],
                         "currenteval": [],
                         "dm_on_kick": False,
                         "dm_on_ban": False,
                         "dm_on_stallkick": False,
                         "rejoin_checker": {"enabled": False, "userId": 0, "joinCount": 0, "maxJoinCount": 0, "pingRoleId": 0, "kickuser": True},
                         "ban": False,
                         "log_channel_id": 0,
                         "kick_on_stall": False,
                         "stall_timer": 300,
                         "kick_dm_message": f"You have been kicked from {guild.name} for suspicious activity.",
                         "ban_dm_message": f"You have been banned from {guild.name} for suspicious activity.",
                         "stall_dm_message": f"You have been kicked from {guild.name} because you didn't complete onboarding in a while. If you join back, please complete onboarding.",
                         "ban_counter": 0,
                         "kick_counter": 0,
                         "delete_welcome_message": False,
                         "welcome_channel_id": 0,
                         "logger": guildLogger,
                         "debug_logging": False}
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    globalLogger.info(f"Added {guild.name} to guildsDB file.")
    setup_logger(guildLogger, guild)
    guildLogger.info(f" - - - Dekomori has joined {guild.name}! - - - ")
    guildLogger.info(f"First Setup - Dekomori {version}")

@client.event
async def on_guild_remove(guild):
    globalLogger.info(f"Left {guild.name}.")
    guildId = str(guild.id)
    guildLogger = logging.getLogger(guildId)
    globalLogger.info(f"Removing {guild.name} with ID {guildId} from guildsDB file.")
    guildsDB.pop(guildId)
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    globalLogger.info(f"Removed {guild.name} from guildsDB file.")
    guildLogger.info(f" - - - Dekomori has left {guild.name}. Goodbye! - - - ")
    guildLogger.info(f"Dekomori {version}")

@client.event
async def on_member_remove(member):
    guild = member.guild
    guildId = str(guild.id)
    guildLogger = logging.getLogger(guildId)
    guildLogger.debug(f"Member {member.name} has left.")
    for memberdict in guildsDB[guildId]["currenteval"]:
        if member.id == memberdict["memberid"] and not member.flags.completed_onboarding:
            guildsDB[guildId]["currenteval"].remove(memberdict)
            guildLogger.info(f"{member.name} (on evaluation) has left while onboarding.")
            guildLogger.debug(f"Removed {member.name} from currentEval.")
            with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
                toml.dump(guildsDB, f)
            globalLogger.debug(f"Wrote to guilds_db.toml.")
            return

@client.event
async def on_member_update(before, after):
    guild = after.guild
    guildId = str(guild.id)
    guildLogger = logging.getLogger(guildId)
    # First check: Member is currently being evaluated (hasn't stalled out or left while onboarding).
    # Second check: Member has completed onboarding.
    for memberdict in guildsDB[guildId]["currenteval"]:
        if after.id == memberdict["memberid"] and after.flags.completed_onboarding:
            logChanObj = discord.utils.get(after.guild.text_channels, id=guildsDB[guildId]["log_channel_id"])
            if not logChanObj.permissions_for(guild.me).send_messages:
                guildLogger.critical(f"Can't send messages in {logChanObj.name}! Skipping check of {member.name}...")
                return
            member = after
            guildLogger.info(f"{member.name} has completed onboarding.")
            guildLogger.info(f"Evaluation beginning for {member.name}.")
            # ON SUCCESS
            if evaluateBaitRoles(guildId, member):
                # If ban
                if guildsDB[guildId]["ban"]:
                    guildLogger.info(f"Attempting to ban {member.name}.")
                    # Permissions Checker
                    if not guild.me.guild_permissions.ban_members:
                        guildLogger.critical(f"Missing permissions to ban {member.name}.")
                        await logChanObj.send(f"I don't have the necessary permissions to ban {member.mention} ({member.name})! Please check my permissions and try again. I'll pause my actions until then.")
                        guildsDB[guildId]["paused"] = True
                        guildLogger.info(f"Pausing Dekomori ")
                        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
                            toml.dump(guildsDB, f)
                        globalLogger.debug(f"Wrote to guilds_db.toml.")
                        return
                    # DM Checker
                    if guildsDB[guildId]["dm_on_ban"]:
                        guildLogger.info(f"Sending Ban DM to {member.name}")
                        dmChan = await member.create_dm()
                        await dmChan.send(content=guildsDB[guildId]["ban_dm_message"])
                    # Ban Loop
                    while True:
                        try:
                            await member.ban(reason="User had a bait role.")
                        except discord.errors.HTTPException:
                            guildLogger.error(f"Got an HTTPException while trying to ban {member.name}. Retrying...")
                        else:
                            guildLogger.info(f"Banned {member.name}.")
                            await logChanObj.send(f"Mjolnir Striker! {member.mention} ({member.name}) had a bait role and has been banned to **DEATH**!")
                            guildsDB[guildId]["ban_counter"] += 1
                            guildLogger.debug(f"Added 1 to Ban Counter.")
                            with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
                                toml.dump(guildsDB, f)
                            globalLogger.debug(f"Wrote to guilds_db.toml.")
                            break
                # If kick
                else:
                    # Rejoin Checker
                    if execRejoinChecker(guild, member):
                        maxJoinCount = guildsDB[guildId]["rejoin_checker"]["maxJoinCount"]
                        pingRole = discord.utils.get(guild.roles, id=guildsDB[guildId]["rejoin_checker"]["pingRoleId"])
                        await logChanObj.send(f"Oh? It looks like {member.mention} ({member.name}) has attempted to rejoin {maxJoinCount} times in a row now...! You should take a look, {pingRole.mention}, this could mean **DEATH**!")
                        if not guildsDB[guildId]["rejoin_checker"]["kickuser"]:
                            await logChanObj.send(f"I won't kick them because they have rejoined many times in a row, though!")
                            return
                    guildLogger.info(f"Attempting to kick {member.name}.")
                    # Permissions Checker
                    if not guild.me.guild_permissions.kick_members:
                        guildLogger.critical(f"Missing permissions to kick {member.name}.")
                        await logChanObj.send(f"I don't have the necessary permissions to kick {member.mention} ({member.name})! Please check my permissions and try again. I'll pause my actions until then.")
                        guildsDB[guildId]["paused"] = True
                        guildLogger.info(f"Pausing Dekomori ")
                        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
                            toml.dump(guildsDB, f)
                        globalLogger.debug(f"Wrote to guilds_db.toml.")
                        return
                    # DM Checker
                    if guildsDB[guildId]["dm_on_kick"]:
                        guildLogger.info(f"Sending Kick DM to {member.name}.")
                        dmChan = await member.create_dm()
                        await dmChan.send(content=guildsDB[guildId]["kick_dm_message"])
                    # Kick Loop
                    while True:
                        try:
                            await member.kick(reason="User had a bait role.")
                        except discord.errors.HTTPException:
                            guildLogger.error(f"Got an HTTPException while trying to kick {member.name}. Retrying...")
                        else:
                            guildLogger.info(f"Kicked {member.name}.")
                            await logChanObj.send(f"Mjolnir Tornado! {member.mention} ({member.name}) had a bait role and was _deathly_ kicked away!")
                            guildsDB[guildId]["kick_counter"] += 1
                            guildLogger.debug(f"Added 1 to Kick Counter.")
                            with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
                                toml.dump(guildsDB, f)
                            globalLogger.debug(f"Wrote to guilds_db.toml.")
                            break
                # Welcome Message Deletion
                if guildsDB[guildId]["delete_welcome_message"]:
                    guildLogger.info(f"Deleting {member.name}'s welcome message - Expect a confirmation.")
                    welcomeChan = guild.system_channel
                    wmCount = 0
                    async for message in welcomeChan.history(limit=10):
                        if message.author == member:
                            try:
                                await message.delete()
                            except discord.errors.Forbidden:
                                guildLogger.error(f"Missing permissions to delete {member.name}'s welcome message.")
                                await logChanObj.send(f"I don't have the necessary permissions to delete their welcome message! Please check my permissions and try again.")
                                break
                            else:
                                wmCount += 1
                    wmS = "s" if wmCount > 1 else ""
                    if wmCount > 0:
                        guildLogger.info(f"Deleted {member.name}'s welcome message{wmS}.")
                        await logChanObj.send(f"I also deleted {wmCount} welcome message{wmS}, they're not _deathly_ welcome here!")
            guildsDB[guildId]["currenteval"].remove(memberdict)
            guildLogger.debug(f"Removed {after.name} from currentEval.")
            with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
                toml.dump(guildsDB, f)
            globalLogger.debug(f"Wrote to guilds_db.toml.")
            return

@client.event
async def on_member_join(member):
    guild = member.guild
    guildId = str(guild.id)
    guildLogger = logging.getLogger(guildId)
    guildLogger.info(f"{member.name} has joined.")
    # - - - - CHECKS - - - - #
    # Pause Check
    resumeId = globalConfig["command_ids"]["resume"]
    failPauseMsg = (f"\nFor now, I'll pause my actions indefinitely. When you've set this up, type `d!resume` or do </resume:{resumeId}> and I'll get back to _deathly_ work!")
    if guildsDB[guildId]["paused"]:
        guildLogger.error(f"Dekomori is paused. Skipping check of {member.name}...")
        return
    # Log Channel Check
    logChanObj = discord.utils.get(member.guild.text_channels, id=guildsDB[guildId]["log_channel_id"])
    if not logChanObj.permissions_for(guild.me).send_messages:
        guildLogger.critical(f"Can't send messages in {logChanObj.name}! Skipping check of {member.name}...")
        return
    # Bait Roles Check
    if guildsDB[guildId]["bait_roles"] == []:
        brCmdId = globalConfig['command_ids']["baitrole"]
        guildLogger.error(f"No bait roles set. Skipping check of {member.name}...")
        await logChanObj.send(f"{member.mention} just joined, but no bait roles are set, so I can't really do anything...\nPlease set bait roles using `d!baitrole add [roles]`, or </baitrole:{brCmdId}>."+failPauseMsg)
        guildsDB[guildId]["paused"] = True
        guildLogger.info(f"Pausing Dekomori ")
        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
            toml.dump(guildsDB, f)
        guildLogger.debug(f"Wrote to guilds_db.toml.")
        return
    # Genuine Bot/Application Check
    if member.bot:
        guildLogger.info(f"{member.name} is a Discord genuine bot. Skipping check.")
        return
    # Onboarding Enabled Check
    if not member.flags.started_onboarding:
        guildLogger.error(f"User {member.name} joined but no onboarding was detected. Skipping check of {member.name}...")
        await logChanObj.send(f"{member.mention} just joined, but no onboarding was detected! This means that onboarding is not set up on the server.\nIf onboarding is not set up (and users don't get prompted to get roles) then there's no point in me checking for bait roles...\nPlease enable onboarding in the server settings so I can get to _deathly_ work!."+failPauseMsg)
        guildsDB[guildId]["paused"] = True
        guildLogger.info(f"Pausing Dekomori.")
        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
            toml.dump(guildsDB, f)
        globalLogger.debug(f"Wrote to guilds_db.toml.")
        return
    # - - - - PASS - - - - #
    guildLogger.info(f"All pre-checks passed for {member.name}.")
    memberEvalDict = {"memberid": member.id, "joined": datetime.datetime.now(), "timeout": guildsDB[guildId]["stall_timer"]}
    guildsDB[guildId]["currenteval"].append(memberEvalDict)
    guildLogger.debug(f"Added {member.name} to currentEval.")
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")

################# COMMANDS #################

### Command Checks ###
@client.check
def botCheck(ctx):
    globalLogger.debug(f"Bot Check - {ctx.author.name}.")
    return not ctx.author.bot

@client.check
def guildCheck(ctx):
    globalLogger.debug(f"Guild Check - {ctx.author.name} in {ctx.guild.name if ctx.guild.name is not None else ctx.author.name}.")
    return ctx.guild is not None
### Error Handling ###

@client.event
async def on_command_error(ctx, error):
    guildLogger = logging.getLogger(str(ctx.guild.id))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Who are you, a fake?! You don't have the necessary permissions to try that command!")
        guildLogger.error(f"{ctx.author.name} tried to use a command without the necessary permissions.")
        guildLogger.debug(f"{type(error)}: {error}")
    elif isinstance(error, commands.MissingRequiredArgument):
        # Groups
        if ctx.command.root_parent is not None:
            if ctx.command.root_parent.name == "baitrole":
                if ctx.command.name == "add":
                    await ctx.send("You need to specify a role to add!")
                    guildLogger.error(f"Failure was a Missing Required Argument in baitrole add.")
                elif ctx.command.name == "remove":
                    await ctx.send("You need to specify a role to remove!")
                    guildLogger.error(f"Failure was a Missing Required Argument in baitrole remove.")
            elif ctx.command.root_parent.name == "toggle":
                if ctx.command.name == "dm":
                    await ctx.send("You need to specify if you want to toggle DMs for `kick`, `ban`, or `stall`!")
                    guildLogger.error(f"Failure was a Missing Required Argument in toggle dm.")
            elif ctx.command.root_parent.name == "set":
                if ctx.command.name == "dmmsg":
                    await ctx.send("You need to specify if you want to message for `kick`, `ban`, or `stall`, and the message!")
                    guildLogger.error(f"Failure was a Missing Required Argument in dmmsg- action None.")
                elif ctx.command.name == "logchannel":
                    await ctx.send("You need to specify a channel to set as the log channel!")
                    guildLogger.error(f"Failure was a Missing Required Argument in set logchannel.")
                elif ctx.command.name == "stalltimer":
                    await ctx.send("You need to specify a number of minutes for the stall timer!")
                    guildLogger.error(f"Failure was a Missing Required Argument in set stalltimer.")
            elif ctx.command.root_parent.name == "rejoinchecker":
                if ctx.command.name == "pingrole":
                    await ctx.send("You need to specify a role to ping when the rejoin checker is triggered!")
                    guildLogger.error(f"Failure was a Missing Required Argument in rejoinchecker pingrole.")
                elif ctx.command.name == "setmax":
                    await ctx.send("You need to specify the maximum number of joins before the rejoin checker triggers!")
                    guildLogger.error(f"Failure was a Missing Required Argument in rejoinchecker setmax.")
        # Commands
        else:
            if ctx.command.name == "logchannel":
                await ctx.send("Hey! You need to specify a channel!")
                guildLogger.error(f"Failure was a Missing Required Argument in logchannel.")
            if ctx.command.name == "resetcounter":
                await ctx.send("For what? You need to specify if you want to reset the `kick` or `ban` counter!")
                guildLogger.error(f"Failure was a Missing Required Argument in resetcounter.")
            if ctx.command.name == "fight":
                await ctx.send("Fight who? I'll need a name and I'll see it _deathly_ done!!")
                guildLogger.error(f"Failure was a Missing Required Argument in fight.")
            if ctx.command.name == "config":
                await ctx.send("You need to specify if you want a `brief` or `complete` configuration!")
                guildLogger.error(f"Failure was a Missing Required Argument in config.")
            if ctx.command.name == "togglevblog":
                await ctx.send("Master, do you want to toggle `global`, `here`, or an ID?")	
                guildLogger.error(f"Owner Failure was a Missing Required Argument in togglevblog.")
            if ctx.command.name == "addline":
                await ctx.send("Master, do you want to add a line to `fight` or `chuuni`?")
                guildLogger.error(f"Owner Failure was a Missing Required Argument in addline.")
        guildLogger.error(f"{ctx.author.name} tried to use a command without the necessary arguments.")
        guildLogger.debug(f"{type(error)}: {error}")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("The command went to **DEATH**! Please try again.")
        guildLogger.error(f"{ctx.author.name} got an Invoke Error.")
        guildLogger.debug(f"{type(error)}: {error}")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"That's too fast even for Mjolnir Accel! Try again in {error.retry_after:.2f} seconds!")
        guildLogger.error(f"{ctx.author.name} tried to use a command on cooldown.")
        guildLogger.debug(f"{type(error)}: {error}")
    elif isinstance(error, commands.CheckFailure):
        if ctx.guild is None:
            await ctx.send("Hey, you can't use this command in DMs!")
            guildLogger.error(f"{ctx.author.name} tried to use a command in DMs.")
            guildLogger.debug(f"{type(error)}: {error}")
        else:
            await ctx.send("Who are you, a fake?! You don't have the necessary permissions to try that command!")
            guildLogger.error(f"{ctx.author.name} failed a check.")
            guildLogger.debug(f"{type(error)}: {error}")
    elif isinstance(error, commands.CommandNotFound):
        #await ctx.send("What the **DEATH** are you trying to do? That command doesn't exist!")
        guildLogger.error(f"{ctx.author.name} tried to use a non-existent command.")
        guildLogger.debug(f"{type(error)}: {error}")
    elif isinstance(error, commands.BadLiteralArgument):
        # Groups
        if ctx.command.root_parent is not None:
            if ctx.command.root_parent.name == "set":
                if ctx.command.name == "dmmsg":
                    await ctx.send("That's not a valid argument! Try `kick`, `ban`, or `stall`!")
                    guildLogger.error(f"Failure was a Bad Literal Argument in set dmmsg.")
                    return
            elif ctx.command.root_parent.name == "toggle":
                if ctx.command.name == "dm":
                    await ctx.send("That's not a valid argument! Try `kick`, `ban`, or `stall`!")
                    guildLogger.error(f"Failure was a Bad Literal Argument in toggle dm.")
                    return
        # Commands
        if ctx.command.name == "config":
            await ctx.send("That's not a valid argument! Try `brief` or `complete`!")
            guildLogger.error(f"{ctx.author.name} got a Bad Argument.")
            guildLogger.debug(f"{type(error)}: {error}")
            return
        await ctx.send("I don't think that's a valid argument... Try again!")
        guildLogger.error(f"{ctx.author.name} got a Bad Argument.")
        guildLogger.debug(f"{type(error)}: {error}")
    elif isinstance(error, commands.MemberNotFound) and ctx.command.name == "fight":
        await ctx.send("Who the **DEATH** is that? I can't find them anywhere!")
        guildLogger.error(f"{ctx.author.name} tried to fight an invalid user.")
        guildLogger.debug(f"{type(error)}: {error}")
    elif isinstance(error, commands.ChannelNotFound) and ctx.command.name == "logchannel":
        await ctx.send("That's not a valid channel... Try again!")
        guildLogger.error(f"{ctx.author.name} tried to set an invalid channel.")
        guildLogger.debug(f"{type(error)}: {error}")
    elif isinstance(error, commands.RoleNotFound) and ctx.command.root_parent.name == "rejoinchecker":
        await ctx.send("That's not a valid role... Try again!")
        guildLogger.error(f"{ctx.author.name} tried to set an invalid role.")
        guildLogger.debug(f"{type(error)}: {error}")
    elif isinstance(error, commands.BadArgument) and (ctx.command.root_parent.name == "rejoinchecker" or ctx.command.root_parent.name == "set"):
        await ctx.send("That's not a valid number... Try again with a whole number!")
        guildLogger.error(f"{ctx.author.name} tried to set an invalid number.")
        guildLogger.debug(f"{type(error)}: {error}")
    else:
        if str(ctx.guild.id) not in guildsDB:
            await ctx.send("There is no configuration for this server yet! This happens when I join a server while being offline.\nTo make a configuration for this server, the owner must do `d!remakeguildconfig [Server ID]`.")
        await ctx.send("I, uh, don't know what happened, actually... Try again!")
        guildLogger.error(f"{ctx.author.name} got an unknown error.")
        guildLogger.debug(f"{type(error)}: {error}")

### Main Hybrid Commands ###

# Baitrole Hybrid Group -----------------------------------------------------
@client.hybrid_group(aliases=["br","baitroles"], brief="Add or remove bait roles.")
@app_commands.default_permissions(manage_roles = True)
@commands.has_permissions(manage_roles=True)
async def baitrole(ctx):
    """Add or remove a role from the bait roles list.
    You can also operate multiple roles by separating them with commas inside quotes, for example d!baitrole add "@role1, @role2". You can also remove all roles by typing d!baitrole remove all.

    Parameters
    ----------
    action : str
        The action to be performed. Can be either "add" or "remove".
    role : str
        The role to be added or removed. Can be a mention or an ID. For multiple roles, they must be separated by commas inside quotes.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    await ctx.send("Hey, what exactly do you want me to do? There's `add` and `remove`!")
    guildLogger.error(f"{ctx.author.name} didn't specify any arguments for baitrole.")

@baitrole.command(aliases=["a"], brief="Add a role to the bait roles list.")
@commands.has_permissions(manage_roles=True)
async def add(ctx, role):
    """Add a role to the bait roles list. You can also operate multiple roles by separating them with commas inside quotes, for example d!baitrole add "@role1, @role2".

    Parameters
    ----------
    role : str
        The role(s) to be added. Can be a mention or an ID.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    guildLogger.info(f"{ctx.author.name} requested to add roles.")
    guildLogger.info(f"Roles: {role}")
    guildLogger.info(f"Attempting to edit roles...")
    edit = roleEdit(guildId, role, "add")
    # Error Handling
    # 1: Invalid Role(s)
    if edit == 1:
        if "," in role:
            await ctx.send("None of those roles are valid...")
        else:
            await ctx.send("That's not a valid role...")
        guildLogger.error(f"{ctx.author.name} tried to add an invalid role.")
        return
    # 2: Role(s) Already in List
    elif edit == 2:
        if "," in role:
            await ctx.send("All of those roles are already in the bait roles list!")
        else:
            await ctx.send("That role is already in the bait roles list!")
        guildLogger.error(f"{ctx.author.name} tried to add roles already in the bait roles list.")
        return
    # Success
    if isinstance(edit, list):
        roleList = [f"<@&{role}>" for role in edit]
        await ctx.send(f"I added {', '.join(roleList)} to the bait roles!")
        guildLogger.info(f"{ctx.author.name} added {', '.join(roleList)} to the bait roles.")
    else:
        await ctx.send(f"I added <@&{edit}> to the bait roles!")
        guildLogger.info(f"{ctx.author.name} added <@&{role.name}> to the bait roles.")

@baitrole.command(aliases=["r"], brief="Remove a role from the bait roles list.")
@commands.has_permissions(manage_roles=True)
async def remove(ctx, role):
    """Remove a role from the bait roles list. You can also operate multiple roles by separating them with commas inside quotes, for example d!baitrole add "@role1, @role2". You can also remove all roles by typing d!baitrole remove all.

    Parameters
    ----------
    role : str
        The role(s) to be removed. Can be a mention, an ID, or "all".
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    guildLogger.info(f"{ctx.author.name} requested to remove roles.")
    guildLogger.info(f"Roles: {role}")
    guildLogger.info(f"Attempting to edit roles...")
    edit = roleEdit(guildId, role, "remove")
    # Error Handling
    # 1: Invalid Role(s)
    if edit == 1:
        if "," in role:
            await ctx.send("None of those roles are valid...")
        else:
            await ctx.send("That's not a valid role...")
        guildLogger.error(f"{ctx.author.name} tried to remove an invalid role.")
        return
    # 2: Role(s) Not in List
    elif edit == 2:
        if "," in role:
            await ctx.send("None of those roles are in the bait roles list!")
        else:
            await ctx.send("That role is not in the bait roles list!")
        guildLogger.error(f"{ctx.author.name} tried to remove a role not in the bait roles list.")
        return
    # Success
    if role == "all":
        await ctx.send("I removed all bait roles!")
        guildLogger.info(f"{ctx.author.name} removed all bait roles.")
        return
    if isinstance(edit, list):
        roleList = [f"<@&{role}>" for role in edit]
        await ctx.send(f"I removed {', '.join(roleList)} from the bait roles!")
        guildLogger.info(f"{ctx.author.name} removed {', '.join(roleList)} from the bait roles.")
    else:
        await ctx.send(f"I removed <@&{edit}> from the bait roles!")
        guildLogger.info(f"{ctx.author.name} removed <@&{role.name}> from the bait roles.")

# Toggle Hybrid Group -----------------------------------------------------
@client.hybrid_group(brief="Toggle various settings for Dekomori.")
@app_commands.default_permissions(manage_roles = True)
@commands.has_permissions(manage_roles=True)
async def toggle(ctx):
    """Toggle various settings for Dekomori. You can check their status with d!config."""
    guildLogger = logging.getLogger(str(ctx.guild.id))
    await ctx.send("Hey, what exactly do you want me to toggle? There's `dm`, `delwm`, `ban`, `rejoinchecker`, and `kickonstall`!")
    guildLogger.error(f"{ctx.author.name} didn't specify any arguments for toggle.")

@toggle.command(aliases=["dmuser"], brief="Toggle DMs on detection of bait roles.")
@commands.has_permissions(manage_roles=True)
async def dm(ctx, action:Literal["kick", "ban", "stall"]):
    """Toggle DMs on detection of bait roles. If enabled, Dekomori will DM the user before taking action. You can check its status with d!config.

    Parameters
    ----------
    action : str
        The action to be performed. Can be either "kick", "ban", or "stall".
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    if action == "kick":
        guildsDB[guildId]["dm_on_kick"] = not guildsDB[guildId]["dm_on_kick"]
        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
            toml.dump(guildsDB, f)
        globalLogger.debug(f"Wrote to guilds_db.toml.")
        if guildsDB[guildId]["dm_on_kick"]:
            await ctx.send("I'll have some _deathly_ mercy on my enemies and DM them before I kick them!")
            guildLogger.info(f"{ctx.author.name} turned on DM on Kick.")
        else:
            await ctx.send("No more DMs for anyone! I'll kick them to **DEATH**!")
            guildLogger.info(f"{ctx.author.name} turned off DM on Kick.")
    elif action == "ban":
        guildsDB[guildId]["dm_on_ban"] = not guildsDB[guildId]["dm_on_ban"]
        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
            toml.dump(guildsDB, f)
        globalLogger.debug(f"Wrote to guilds_db.toml.")
        if guildsDB[guildId]["dm_on_ban"]:
            await ctx.send("I'll spare some _deathly_ words for my enemies before they face **DEATH**!")
            guildLogger.info(f"{ctx.author.name} turned on DM on Ban.")
        else:
            await ctx.send("I have no words to spare, only **DEATH**!")
            guildLogger.info(f"{ctx.author.name} turned off DM on Ban.")
    elif action == "stall":
        guildsDB[guildId]["dm_on_stallkick"] = not guildsDB[guildId]["dm_on_stallkick"]
        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
            toml.dump(guildsDB, f)
        globalLogger.debug(f"Wrote to guilds_db.toml.")
        if guildsDB[guildId]["dm_on_stallkick"]:
            await ctx.send("I'll have some _deathly_ mercy on those who stall and DM them before I kick them!")
            guildLogger.info(f"{ctx.author.name} turned on DM on Stall Kick.")
        else:
            await ctx.send("No more DMs for stallers! I'll kick them to **DEATH**!")
            guildLogger.info(f"{ctx.author.name} turned off DM on Stall Kick.")

@toggle.command(aliases=["wm", "wmdel", "welcomemessage", "deletewelcomemessage"], brief="Toggle deletion of welcome messages.")
@commands.has_permissions(manage_guild=True)
async def delwm(ctx):
    """Toggle deletion of welcome messages. If enabled, Dekomori will delete the default welcome message for new users. You can check its status with d!config.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    guildsDB[guildId]["delete_welcome_message"] = not guildsDB[guildId]["delete_welcome_message"]
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    if guildsDB[guildId]["delete_welcome_message"]:
        guildLogger.info(f"{ctx.author.name} turned on Welcome Message Deletion.")
        await ctx.send("I'll delete the welcome messages for users who took the bait!")
    else:
        guildLogger.info(f"{ctx.author.name} turned off Welcome Message Deletion.")
        await ctx.send("I'll let the welcome messages be!")

@toggle.command(aliases=["ban", "kick"], brief="Toggle between banning and kicking users with bait roles.")
@commands.has_permissions(manage_roles=True)
async def action(ctx):
    """Toggle between banning and kicking users with bait roles. By default, Dekomori will kick users with bait roles. You can check its status with d!config.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    guildsDB[guildId]["ban"] = not guildsDB[guildId]["ban"]
    if guildsDB[guildId]["ban"]:
        await ctx.send("They shall be banned by **DEATH** itself!")
        guildLogger.info(f"{ctx.author.name} turned on Banning.")
        if guildsDB[guildId]["rejoin_checker"]["enabled"]:
            guildsDB[guildId]["rejoin_checker"]["enabled"] = False
            guildLogger.warning(f"As banning has been turned on, the rejoin checker has been disabled.")
            await ctx.send("I've also turned off the Rejoin Checker, as it only works with kicks!")
    else:
        guildLogger.info(f"{ctx.author.name} turned off Banning.")
        await ctx.send("I'll spare them from **DEATH** and just kick them away!")
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")

@toggle.command(aliases=["kos", "stallkick"], brief="Toggle kicking on stall.")
@commands.has_permissions(manage_roles=True)
async def kickonstall(ctx):
    """Toggle kicking on stall. If enabled, Dekomori will kick users who stall in the onboarding process. You can check its status with d!config.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    guildsDB[guildId]["kick_on_stall"] = not guildsDB[guildId]["kick_on_stall"]
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    if guildsDB[guildId]["kick_on_stall"]:
        guildLogger.info(f"{ctx.author.name} turned on Kick on Stall.")
        await ctx.send("I'll kick users who stall in the onboarding process!")
    else:
        guildLogger.info(f"{ctx.author.name} turned off Kick on Stall.")
        await ctx.send("I'll just leave users who stall be, then!")

@toggle.command(aliases=["rc", "rejoin", "rjc"], brief="Toggle the rejoin checker.")
@commands.has_permissions(manage_roles=True)
async def rejoinchecker(ctx):
    """Toggle the rejoin checker. This feature will notify a role when a user repeatedly rejoins the server.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    rjcCmdId = globalConfig["command_ids"]["rejoinchecker"]
    if guildsDB[guildId]["rejoin_checker"]["pingRoleId"] == 0:
        await ctx.send(f"You need to set a role to ping first! Use `d!rejoinchecker pingrole` or </rejoinchecker pingrole:{rjcCmdId}>.")
        return
    if guildsDB[guildId]["rejoin_checker"]["maxJoinCount"] == 0:
        await ctx.send(f"You need to set the maximum number of joins first! Use `d!rejoinchecker setmax` or </rejoinchecker setmax:{rjcCmdId}>.")
        return
    if guildsDB[guildId]["ban"]:
        toggleCmdId = globalConfig["command_ids"]["toggle"]
        await ctx.send(f"The Rejoin Checker only works if I'm kicking users, not banning them! Use `d!toggle action` or </toggle action:{toggleCmdId}> to switch to kicking.")
        return
    guildsDB[guildId]["rejoin_checker"]["enabled"] = not guildsDB[guildId]["rejoin_checker"]["enabled"]
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    if guildsDB[guildId]["rejoin_checker"]["enabled"]:
        guildLogger.info(f"{ctx.author.name} turned on Rejoin Checker.")
        await ctx.send("I'll notify the role when someone tries to rejoin the server multiple times in a row!")
    else:
        guildLogger.info(f"{ctx.author.name} turned off Rejoin Checker.")
        await ctx.send("No more notifications, only **DEATH**!")

@toggle.command(aliases=["rjckick", "rjck"], brief="Toggle the rejoin checker kicking users.")
@commands.has_permissions(manage_roles=True)
async def rejoincheckerkick(ctx):
    """Toggle the rejoin checker kicking users. If enabled, Dekomori will kick users who repeatedly rejoin the server. You can check its status with d!config.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    guildsDB[guildId]["rejoin_checker"]["kickuser"] = not guildsDB[guildId]["rejoin_checker"]["kickuser"]
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    if guildsDB[guildId]["rejoin_checker"]["kickuser"]:
        guildLogger.info(f"{ctx.author.name} turned on Rejoin Checker Kick.")
        await ctx.send("I'll kick users who try to rejoin the server multiple times in a row!")
    else:
        guildLogger.info(f"{ctx.author.name} turned off Rejoin Checker Kick.")
        await ctx.send("I'll spare some _deathly_ mercy and just ping the role, but the user will stay!")

# Set Hybrid Group -----------------------------------------------------
@client.hybrid_group(brief="Set various configurations for Dekomori.")
@app_commands.default_permissions(manage_roles = True)
@commands.has_permissions(manage_roles=True)
async def set(ctx):
    """Set various configurations for Dekomori. You can check their current configuration with d!config.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    await ctx.send("What do you want to set? You can set a `logchannel`, a `stalltimer`, or a `dmmsg`.")
    guildLogger.error(f"{ctx.author.name} didn't specify any arguments for set.")

@set.command(aliases=["logchan", "setlogchannel", "setlogchan"], brief="Set the log channel for Dekomori.")
@commands.has_permissions(manage_roles=True)
async def logchannel(ctx, channel: discord.TextChannel):
    """Set the channel where Dekomori will log the actions taken. You can check the current one with d!config.
    
    Parameters
    ----------
    channel : str
        The channel to be set as the log channel. Can be a mention or an ID.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    guildsDB[guildId]["log_channel_id"] = channel.id
    if not channel.permissions_for(ctx.guild.me).send_messages:
        await ctx.send("I can't send messages in that channel! Please make sure I have the necessary permissions.")
        guildLogger.error(f"{ctx.author.name} tried to set a log channel without send messages permission for Dekomori.")
        return
    guildLogger.info(f"{ctx.author.name} set log channel to {channel.name} ({str(channel.id)}).")
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    await ctx.send(f"I'll write the names of slain enemies in {channel.mention}!")

@set.command(aliases=["st", "stalltimeout", "jointimer", "jointimeout"], brief="Set the stall timer for Dekomori.")
@commands.has_permissions(manage_roles=True)
async def stalltimer(ctx, time: int):
    """Set the stall timer for Dekomori. This is the time in seconds a user has to complete the onboarding process before being kicked.
    
    Parameters
    ----------
    time : int
        The time in seconds a user has to complete the onboarding process.
    """
    if time < 60:
        await ctx.send("Hey, I can't set a stall timer for less than a minute!")
        return
    elif time > 604800:
        await ctx.send("A week is the maximum time I can give users to complete the onboarding process!")
        return
    parsedDuration = parseDuration(time)
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    guildsDB[guildId]["stall_timer"] = time
    guildLogger.info(f"{ctx.author.name} set stall timer to {parsedDuration}.")
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    await ctx.send(f"I'll give users {parsedDuration} to complete the onboarding process before kicking them!")

@set.command(aliases=["setdmmsg", "dmmessage"], brief="Set the DM message for Dekomori's actions.")
@commands.has_permissions(manage_roles=True)
async def dmmsg(ctx, action:Literal["kick", "ban", "stall"], *, message: str):
    """Set the message to be sent to users before taking action. You can check the current one with d!config.
    
    Parameters
    ----------
    action : str
        The action to be performed. Can be either "kick", "ban", or "stall".
    message : str
        The message to be sent to the user.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    if action == "kick":    
        guildsDB[guildId]["kick_dm_message"] = message
        guildLogger.info(f"{ctx.author.name} set kick dm msg to \"{message}\".")
        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
            toml.dump(guildsDB, f)
        globalLogger.debug(f"Wrote to guilds_db.toml.")
        await ctx.send("Roger! I'll tell this to those I _deathly_ kick away!")
    elif action == "ban":
        guildsDB[guildId]["ban_dm_message"] = message
        guildLogger.info(f"{ctx.author.name} set ban dm msg to \"{message}\".")
        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
            toml.dump(guildsDB, f)
        globalLogger.debug(f"Wrote to guilds_db.toml.")
        await ctx.send("Roger! I'll tell this to the victims of my Mjolnir Hammer!!")
    elif action == "stall":
        guildsDB[guildId]["stall_dm_message"] = message
        guildLogger.info(f"{ctx.author.name} set stall dm msg to \"{message}\".")
        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
            toml.dump(guildsDB, f)
        globalLogger.debug(f"Wrote to guilds_db.toml.")
        await ctx.send("Roger! I'll tell this to those who get kicked for stalling in the onboarding process!")

# Rejoin Checker Hybrid Group -----------------------------------------------------
@client.hybrid_group(aliases=["rc", "rjck", "rjc"], brief="Configure the rejoin checker.")
@app_commands.default_permissions(manage_roles = True)
@commands.has_permissions(manage_roles=True)
async def rejoinchecker(ctx):
    """Configure the rejoin checker. This feature will notify a role when a user repeatedly rejoins the server.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    toggleRcId = globalConfig["command_ids"]["toggle"]
    await ctx.send(f"What do you want to configure for the rejoin checker? You can `setpingrole` or `setmax`.\nIf you're looking to enable or disable it, use `d!toggle rejoinchecker` or </toggle rejoinchecker:{toggleRcId}>!")
    guildLogger.error(f"{ctx.author.name} didn't specify any arguments for rejoinchecker.")

@rejoinchecker.command(aliases=["spr", "setping", "pr", "ping"], brief="Set the role to be pinged by the rejoin checker.")
@commands.has_permissions(manage_roles=True)
async def pingrole(ctx, role: discord.Role):
    """Set the role to be pinged by the rejoin checker. This role will be pinged when a user repeatedly rejoins the server.
    
    Parameters
    ----------
    role : str
        The role to be pinged. Can be a mention or an ID.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    guildsDB[guildId]["rejoin_checker"]["pingRoleId"] = role.id
    guildLogger.info(f"{ctx.author.name} set rejoin checker ping role to {role.name} ({str(role.id)}).")
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    await ctx.send(f"Roger! I'll ping {role.name} when someone tries to rejoin too many times!")

@rejoinchecker.command(aliases=["sm", "setmaxcount", "max"], brief="Set the maximum number of times a user can rejoin before a role is alerted.")
@commands.has_permissions(manage_roles=True)
async def setmax(ctx, count: int):
    """Set the maximum number of times a user can rejoin the server before the rejoin checker takes action.
    
    Parameters
    ----------
    count : int
        The maximum number of times a user can rejoin the server.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    guildsDB[guildId]["rejoin_checker"]["maxJoinCount"] = count
    guildLogger.info(f"{ctx.author.name} set rejoin checker max join count to {count}.")
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    await ctx.send(f"Got it! I'll take action after {count} rejoins!")

# Non-grouped Hybrid Commands -----------------------------------------------------
@client.hybrid_command(aliases=["configure","cfg"], brief="Show the current configuration.")
@app_commands.default_permissions(manage_roles = True)
@commands.has_permissions(manage_roles=True)
async def config(ctx, mode:Literal["brief", "complete"]):
    """Shows the current configuration for the server. Use `brief` for a summary, or `complete` for a detailed view.

    Parameters:
    ------------
    mode: str
        The mode to show the configuration in. Use `brief` for a summary, or `complete` for a detailed view.
    """
    guildId = str(ctx.guild.id)
    guildLogger = logging.getLogger(guildId)
    complete = True if mode == "complete" else False
    guildLogger.info(f"{ctx.author.name} requested configuration."+(" (Complete)" if complete else ""))
    # Values
    pauseValue = "⏸️ No" if guildsDB[guildId]["paused"] else "▶️ Yes"
    setCmdId = globalConfig["command_ids"]["set"]
    logchannel = discord.utils.get(ctx.guild.channels, id=guildsDB[guildId]['log_channel_id']).mention if guildsDB[guildId]["log_channel_id"] != 0 else f"⚠️ **__NOT SET - NO ACTION WILL BE TAKEN! USE `d!logchannel [channel]` OR </set logchannel:{setCmdId}>!__** ⚠️"
    roleList = []
    for role in guildsDB[guildId]["bait_roles"]:
        roleList.append(f"<@&{role}>")
    brCmdId = globalConfig["command_ids"]["baitrole"]
    roleValue = f"⚠️ **__NOT SET - NO ACTION WILL BE TAKEN! USE `d!baitrole add [roles]` OR </baitrole add:{brCmdId}>!__** ⚠️" if roleList == [] else "\n".join(roleList)
    actionValue = "🔨 Ban" if guildsDB[guildId]["ban"] else "🚷 Kick"
    dmValue = "**On Ban:** "+("Yes" if guildsDB[guildId]['dm_on_ban'] else "No")+"\n**On Kick:** "+("Yes" if guildsDB[guildId]['dm_on_kick'] else "No")+"\n**On Stall Kick:** "+ ('Yes' if guildsDB[guildId]['dm_on_stallkick'] else 'No')
    kickDmMessage = ">>> "+guildsDB[guildId]["kick_dm_message"]
    banDmMessage = ">>> "+guildsDB[guildId]["ban_dm_message"]
    stallDmMessage = ">>> "+guildsDB[guildId]["stall_dm_message"]
    
    counters = f"**Bans**: {guildsDB[guildId]['ban_counter']}\n**Kicks**: {guildsDB[guildId]['kick_counter']}"
    delWelcome = "🚮 Yes" if guildsDB[guildId]["delete_welcome_message"] else "💬 No"
    stallTimer = parseDuration(guildsDB[guildId]["stall_timer"])
    kickOnStall = f"Yes - {stallTimer} Timeout" if guildsDB[guildId]["kick_on_stall"] else f"No - {stallTimer} Timeout"
    rjcRole = discord.utils.get(ctx.guild.roles, id=guildsDB[guildId]['rejoin_checker']['pingRoleId']).mention if guildsDB[guildId]['rejoin_checker']['pingRoleId'] != 0 else "Not set"
    rjcMaxJoins = guildsDB[guildId]['rejoin_checker']['maxJoinCount'] if guildsDB[guildId]['rejoin_checker']['maxJoinCount'] != 0 else "Not set"
    rjcEnabled = "Yes" if guildsDB[guildId]['rejoin_checker']['enabled'] else "No"
    rjcKick = "Yes" if guildsDB[guildId]['rejoin_checker']['kickuser'] else "No"
    rejoinChecker = f"**Enabled**: {rjcEnabled}\n**Max Joins**: {rjcMaxJoins}\n**Role to Ping**: {rjcRole}\n**Kick After Max Rejoins**: {rjcKick}"
    
    # Embed
    helpCmdId = globalConfig["command_ids"]["help"]
    incompleteMsg = f"\nIf you want to show the complete configuration, use `d!config complete` or pass the complete argument in the slash command." if not complete else ""
    embed = discord.Embed(title=f"Dekomori Configuration - {ctx.guild.name}", description=f"I'll show you what I'm _deathly_ capable of! You can run `d!help` or </help:{helpCmdId}> to see how to edit these.\nRemember you need to have Onboarding enabled so I can check for bait roles!{incompleteMsg}", color=discord.Color.yellow())
    embed.add_field(name="Active", value=pauseValue, inline=False)
    embed.add_field(name="Log Channel", value=logchannel, inline=False)
    embed.add_field(name="Bait Roles", value=roleValue, inline=False)
    embed.add_field(name="Action To Take", value=actionValue, inline=False)
    if not complete:
        dmValue = "**On Ban:** "+("Yes" if guildsDB[guildId]['dm_on_ban'] else "No") if guildsDB[guildId]['ban'] else "**On Kick:** "+("Yes" if guildsDB[guildId]['dm_on_kick'] else "No")
        if guildsDB[guildId]['kick_on_stall']:
            dmValue += "\n**On Stall Kick:** "+ ('Yes' if guildsDB[guildId]['dm_on_stallkick'] else 'No')
    embed.add_field(name="DM After Action", value=dmValue, inline=False)
    if (guildsDB[guildId]["dm_on_kick"] and not guildsDB[guildId]["ban"]) or complete:
        embed.add_field(name="Kick DM Message", value=kickDmMessage, inline=False)
    if (guildsDB[guildId]["dm_on_ban"] and guildsDB[guildId]["ban"]) or complete:
        embed.add_field(name="Ban DM Message", value=banDmMessage, inline=False)
    if (guildsDB[guildId]["dm_on_stallkick"] and guildsDB[guildId]["kick_on_stall"]) or complete:
        embed.add_field(name="Stall Kick DM Message", value=stallDmMessage, inline=False)
    embed.add_field(name="Delete Default Welcome Message", value=delWelcome, inline=False)
    if not complete:
        kickOnStall = f"Yes - {stallTimer} Timeout" if guildsDB[guildId]["kick_on_stall"] else "No"
    embed.add_field(name="Kick on Stall", value=kickOnStall, inline=False)
    if not complete and not guildsDB[guildId]["rejoin_checker"]["enabled"]:
        rejoinChecker = f"**Enabled**: {rjcEnabled}"
    embed.add_field(name="Rejoin Checker", value=rejoinChecker, inline=False)
    embed.add_field(name="Counters", value=counters, inline=False)
    embed.set_author(name=f"Dekomori {version}", icon_url=client.user.avatar.url)
    embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

@client.hybrid_command(aliases=["stop"], brief="Pause Dekomori's actions.")
@app_commands.default_permissions(manage_roles = True)
@commands.has_permissions(manage_roles=True)
async def pause(ctx):
    """
    Pause Dekomori's actions for the server. She will not take any action until you resume her.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    guildLogger.info(f"{ctx.author.name} attempting to pause Dekomori.")
    if guildsDB[guildId]["paused"]:
        guildLogger.warning(f"Dekomori was already paused.")
        await ctx.send("I'm already paused, you know?")
        return
    guildsDB[guildId]["paused"] = True
    guildLogger.info(f"Dekomori has been paused.")
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    resumeId = globalConfig["command_ids"]["resume"]
    await ctx.send(f"Oh? Okay, I'll stop for now...\nWhen you need me again, type `d!resume` or do </resume:{resumeId}>!")

@client.hybrid_command(aliases=["start", "awaken"], brief="Resume Dekomori's actions.")
@app_commands.default_permissions(manage_roles = True)
@commands.has_permissions(manage_roles=True)
async def resume(ctx):
    """Resume Dekomori's actions for the server. She will start taking action again."""
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    guildLogger.info(f"{ctx.author.name} attempting to resume Dekomori.")
    if not guildsDB[guildId]["paused"]:
        await ctx.send("I'm already here!")
        guildLogger.warning(f"Dekomori was already resumed.")
        return
    if guildsDB[guildId]["log_channel_id"] == 0:
        setCmdId = globalConfig["command_ids"]["set"]
        await ctx.send(f"You need to set a log channel first! Use `d!logchannel [channel]` or </set logchannel:{setCmdId}> to set one!")
        guildLogger.error(f"{ctx.author.name} tried to resume Dekomori without setting a log channel.")
        return
    if guildsDB[guildId]["bait_roles"] == []:
        brCmdId = globalConfig["command_ids"]["baitrole"]
        await ctx.send(f"You need to set bait roles first! Use `d!baitrole add [roles]` or </baitrole add:{brCmdId}> to set them!")
        guildLogger.error(f"{ctx.author.name} tried to resume Dekomori without setting bait roles.")
        return
    guildsDB[guildId]["paused"] = False
    guildLogger.info(f"Dekomori has been resumed.")
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    await ctx.send("I'm _deathly_ ready to serve!")

@client.hybrid_command(aliases=["rescter", "resc"], brief="Reset the kick or ban counter.")
@app_commands.default_permissions(manage_roles = True)
@commands.has_permissions(manage_roles=True)
async def resetcounter(ctx, action:Literal["kick", "ban"]):
    """Reset the kick or ban counter for the server.
    
    Parameters
    ----------
    action : str
        The action to be performed. Can be either "kick" or "ban".
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildId = str(ctx.guild.id)
    if action == "kick":
        guildsDB[guildId]["kick_counter"] = 0
        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
            toml.dump(guildsDB, f)
        globalLogger.debug(f"Wrote to guilds_db.toml.")
        await ctx.send("I've reset the kick counter!")
    elif action == "ban":
        guildsDB[guildId]["ban_counter"] = 0
        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
            toml.dump(guildsDB, f)
        globalLogger.debug(f"Wrote to guilds_db.toml.")
        await ctx.send("I've reset the ban counter!")
    guildLogger.info(f"{ctx.author.name} reset {action} counter to 0.")

@client.hybrid_command(aliases=["pong"], brief="Show Dekomori's ping.")
async def ping(ctx):
    """Show Dekomori's ping.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildLogger.info(f"{ctx.author.name} requested Dekomori's ping.")
    embed = discord.Embed(title="Pong, DEATH!", description=f"There's a latency of **{round(client.latency*1000)}ms**!", color=discord.Color.yellow())
    embed.set_author(name=f"Dekomori {version}", icon_url=client.user.avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

# Help Slash Command
@app_commands.command(name="help")
async def help(interaction: discord.Interaction, command:Optional[str]):
    """Shows the help message for Dekomori.
    
    Parameters
    ----------
    command : str
        The command to show help for.
    """
    ctx = await client.get_context(interaction)
    guildLogger = logging.getLogger(str(ctx.guild.id))
    if command is not None:
        cmdList = [command.name for command in client.commands]
        if command in cmdList:
            await ctx.send_help(command)
            guildLogger.info(f"{ctx.author.name} requested help for {command}.")
        else:
            await ctx.send("That command doesn't exist!")
            guildLogger.error(f"{ctx.author.name} tried to get help for a non-existent command.")
    else:    
        await ctx.send_help()
        guildLogger.info(f"{ctx.author.name} requested help.")
    return ctx
client.tree.add_command(help, override=True)

### Fun Commands ###

def importfunTxt():
    """Imports the fun_mod.txt file and returns a dictionary with the keys as the sections and the values as the lines in the sections."""
    funMod = {}
    current_key = None
    with open("./config/fun_mod.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                current_key = line[1:-1]
                funMod[current_key] = []
            elif line:
                funMod[current_key].append(line)
    globalLogger.info(f"Loaded fun_mod.txt.")
    return funMod
funMod = importfunTxt()

@client.hybrid_command()
async def spin(ctx):
    """Spin!"""
    guildLogger = logging.getLogger(str(ctx.guild.id))
    await ctx.send("https://tenor.com/view/dekomori-%E3%81%A4%E3%81%84%E3%82%93%E3%81%A6%E3%83%BC%E3%82%8B-gif-5315029")
    guildLogger.info(f"{ctx.author.name} is spinning.")

@client.hybrid_command(brief="Fight someone!")
async def fight(ctx, user: discord.Member):
    """Unleash your fighting spirit! Dekomori will come up with a cool fight scene for you and your opponent.
    Dekomori never loses, though.
    
    Parameters
    ----------
    user : discord.Member
        The user to fight with."""
    guildLogger = logging.getLogger(str(ctx.guild.id))
    if user == ctx.author:
        await ctx.send("You can't fight yourself, silly!")
        guildLogger.error(f"{ctx.author.name} tried fighting themselves.")
    else:
        rngesus = random.randint(0, len(funMod["fight"])-1)
        string = funMod["fight"][rngesus]
        string = string.replace("<userA>", ctx.author.mention) if user != client.user else string.replace("<userB>", ctx.author.mention)
        string = string.replace("<userB>", user.mention) if user != client.user else string.replace("<userA>", "The Wielder of the Mjolnir Hammer, Dekomori Sanae")
        await ctx.send(string)
        guildLogger.info(f"{ctx.author.name} is fighting {user.name}.")

@client.hybrid_command(brief="It's cool!")
async def chuuni(ctx):
    """Dekomori will come up with a chuuni phrase for you."""
    guildLogger = logging.getLogger(str(ctx.guild.id))
    rngesus = random.randint(0, len(funMod["quotes"])-1)
    message = funMod["quotes"][rngesus]
    message = message.replace('\\n', '\n')
    await ctx.send(message)
    guildLogger.info(f"{ctx.author.name} asked Dekomori for some enlightening words.")

### Owner-Exclusive Debug Commands ###

@client.command(hidden=True)
@commands.is_owner()
async def ownerhelp(ctx):
    """Shows the help message for owner commands."""
    embed = discord.Embed(title="Owner Commands", description="Here's the stuff you can do, master!", color=discord.Color.blue())
    embed.set_author(name=f"Dekomori {version}", icon_url=client.user.avatar.url)
    embed.add_field(name="sync", value="Syncs the commands globally.", inline=False)
    embed.add_field(name="clearcommandtree", value="Clears the command tree.", inline=False)
    embed.add_field(name="updaterp", value="Updates the bot's Rich Presence. Takes a string as argument.", inline=False)
    embed.add_field(name="say", value="Sends a custom message.", inline=False)
    embed.add_field(name="reloadfile", value="Reloads a file. Takes `fun`, `config`, or `guilds` as arguments.", inline=False)
    embed.add_field(name="togglevblog", value="Toggles debug logging for the bot. Takes a guildID or `here` as argument.", inline=False)
    embed.add_field(name="remakeguildconfig", value="Remakes the guild config. Takes a guildID or `here` as argument.", inline=False)
    embed.add_field(name="addline", value="Adds a line to the fun_mod.txt file. Takes `fight` or `chuuni` then the line as argument.", inline=False)
    embed.add_field(name="globalannounce", value="Announces a message globally. Takes a string as argument.", inline=False)
    embed.set_footer(text=f"Dekomori - by soreikomori", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

@client.command(hidden=True)
@commands.is_owner()
async def sync(ctx):
    """Syncs the commands globally."""
    globalLogger.info(f"OWNER COMMAND - Syncing Commands Globally.")
    try:
        synced_commands = await client.tree.sync()
        globalLogger.debug("Synced commands:")
        for command in synced_commands:
            globalLogger.debug(command.name)
    except discord.HTTPException:
        globalLogger.error("Syncing commands failed because of an HTTP exception.")
    except discord.app_commands.CommandSyncFailure:
        globalLogger.error("Syncing commands failed because of a CommandSyncFailure.")
    except discord.Forbidden:
        globalLogger.error("Syncing commands failed because of a Forbidden error.")
    except discord.app_commands.MissingApplicationID:
        globalLogger.error("Syncing commands failed because of a MissingAppliationID.")
    except discord.app_commands.TranslationError:
        globalLogger.error("Syncing commands failed because of a Translating Error.")
    await ctx.send("Synced all servers, master!")
    globalLogger.info("Synced all commands.")

@client.command(aliases=["clcmdtree"], hidden=True)
@commands.is_owner()
async def clearcommandtree(ctx):
    """Clears the command tree. Dangerous! Use d!sync after this to resync the commands."""
    globalLogger.info("OWNER COMMAND - Clearing Command Tree...")
    client.tree.clear_commands(guild=None)
    globalLogger.info("Cleared Command Tree.")
    await ctx.send("Cleared command tree, master!")

@client.command(aliases=["setrp", "setrichpresence", "changerp", "changerichpresence", "updaterichpresence", "setstatus", "updatestatus"], hidden=True)
@commands.is_owner()
async def updaterp(ctx, status):
    """Updates the bot's Rich Presence/Status. Takes a string as argument.
    
    Parameters
    ----------
    status : str
        The status to be set.
    """
    await client.change_presence(activity=discord.CustomActivity(name=status))
    globalLogger.info(f"OWNER COMMAND - Updated RichPresence to {status}")
    await ctx.send("Updated, master!")

@client.command(hidden=True)
@commands.is_owner()
async def say(ctx, *, msg):
    """Sends a custom message.
    
    Parameters
    ----------
    msg : str
        The message to be sent.
    """
    guildLogger = logging.getLogger(str(ctx.guild.id))
    guildLogger.info(f"OWNER COMMAND - Sending custom message in {ctx.channel.name}.")
    await ctx.channel.send(msg)
    await asyncio.sleep(1)
    await ctx.message.delete()

@client.command(aliases=["reloadf", "rf"], hidden=True)
@commands.is_owner()
async def reloadfile(ctx, file:Literal["fun", "config", "guilds"]):
    """Reloads a file. Takes `fun`, `config`, or `guilds` as arguments.

    Parameters
    ----------
    file : str
        The file to be reloaded. Can be either `fun`, `config`, or `guilds`.
    """
    if file == "fun":
        global funMod
        funMod = importfunTxt()
        await ctx.send("Reloaded `fun_mod.txt`, master!")
    elif file == "config":
        global globalConfig
        globalConfig = toml.load("./config/config.toml")
        await ctx.send("Reloaded `config.toml`, master!")
    elif file == "guilds":
        global guildsDB
        guildsDB = toml.load("./config/guilds_db.toml")
        await ctx.send("Reloaded `guilds_db.toml`, master!")
    globalLogger.info(f"OWNER COMMAND - Reloaded {file}.")

@client.command(aliases=["setverboselog", "toggledebuglog", "tgdblog"], hidden=True)
@commands.is_owner()
async def togglevblog(ctx, guildId):
    """Toggles debug logging for the bot. Takes a guildID or `here` as arguments.

    Parameters
    ----------
    guildId : str
        The guild ID to toggle debug logging for. Can be either a guild ID or `here`.
    """
    if guildId == "global":
        globalConfig["debug_logging"] = not globalConfig["debug_logging"]
        with open('./config/config.toml', 'w') as f:
            toml.dump(globalConfig, f)
        if globalConfig["debug_logging"]:
            globalLogger.setLevel(logging.DEBUG)
            await ctx.send("I **enabled** config debug logging, master!")
        else:
            globalLogger.setLevel(logging.INFO)
            await ctx.send("I **disabled** config debug logging, master!")
    elif (guildId in guildsDB and guildId.isdigit()) or (guildId == "here" and str(ctx.guild.id) in guildsDB):
        guild = ctx.guild if guildId == "here" else discord.utils.get(client.guilds, id=int(guildId))
        guildId = str(guild.id)
        guildsDB[guildId]["debug_logging"] = not guildsDB[guildId]["debug_logging"]
        guildLogger = logging.getLogger(guildId)
        with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
            toml.dump(guildsDB, f)
        globalLogger.debug(f"Wrote to guilds_db.toml.")
        if guildsDB[guildId]["debug_logging"]:
            guildLogger.setLevel(logging.DEBUG)
            await ctx.send(f"I **enabled** debug logging for {guild.name}, master!")
        else:
            guildLogger.setLevel(logging.INFO)
            await ctx.send(f"I **disabled** debug logging for {guild.name}, master!")
    else:
        await ctx.send("That's not a valid guild ID, master!")

@client.command(aliases=["reloadguildconfig", "reloadguildcfg", "rlgcfg"], hidden=True)
@commands.is_owner()
async def remakeguildconfig(ctx, guildId):
    """Remakes the guild config. Takes a guildID or `here` as arguments.

    Parameters
    ----------
    guildId : str
        The guild ID to remake the config for. Can be either a guild ID or `here`.
    """
    guild = ctx.guild if guildId == "here" else discord.utils.get(client.guilds, id=int(guildId))
    guildId = str(guild.id)
    guildLogger = logging.getLogger(guildId)
    guildLogger.info(f"OWNER COMMAND - Remaking guild config.")
    guildsDB[guildId] = {"paused": True,
                         "bait_roles": [],
                         "currenteval": [],
                         "dm_on_kick": False,
                         "dm_on_ban": False,
                         "dm_on_stallkick": False,
                         "rejoin_checker": {"enabled": False, "userId": 0, "joinCount": 0, "maxJoinCount": 0, "pingRoleId": 0, "kickuser": True},
                         "ban": False,
                         "log_channel_id": 0,
                         "kick_on_stall": False,
                         "stall_timer": 300,
                         "kick_dm_message": f"You have been kicked from {guild.name} for suspicious activity.",
                         "ban_dm_message": f"You have been banned from {guild.name} for suspicious activity.",
                         "stall_dm_message": f"You have been kicked from {guild.name} because you didn't complete onboarding in a while. If you join back, please complete onboarding.",
                         "ban_counter": 0,
                         "kick_counter": 0,
                         "delete_welcome_message": False,
                         "welcome_channel_id": 0,
                         "logger": guildLogger,
                         "debug_logging": False}
    with open('./config/guilds_db.toml', 'w', encoding='utf-8') as f:
        toml.dump(guildsDB, f)
    globalLogger.debug(f"Wrote to guilds_db.toml.")
    await ctx.send(f"Remade guild config for {guild.name}, master!")

@client.command(hidden=True)
@commands.is_owner()
async def addline(ctx, category:Literal["fight", "chuuni"], *add):
    """Adds a line to the fun_mod.txt file. Takes `fight` or `chuuni` then the line as arguments.

    Parameters
    ----------
    category : str
        The category to add the line to. Can be either `fight` or `chuuni`.
    add : str
        The line to be added.
    """
    if isinstance(add, tuple):
        add = " ".join(add)
    if category == "fight":
        with open("./config/fun_mod.txt", "r+") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.strip() == "[fight]":
                    lines.insert(i + 1, add + "\n")
                    break
            file.seek(0)
            file.writelines(lines)
            file.truncate()
        globalLogger.info(f"OWNER COMMAND - Added a line to the fight category.")
        globalLogger.debug(f"Wrote to fun_mod.txt.")
        await ctx.send("Added a line to the fight category, master!")
    elif category == "chuuni":
        with open("./config/fun_mod.txt", "r+") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.strip() == "[quotes]":
                    lines.insert(i + 1, add + "\n")
                    break
            file.seek(0)
            file.writelines(lines)
            file.truncate()
        globalLogger.info(f"OWNER COMMAND - Added a line to the chuuni category.")
        globalLogger.debug(f"Wrote to fun_mod.txt.")
        await ctx.send("Added a line to the chuuni category, master!")
    global funMod
    funMod = importfunTxt()
    await ctx.send("Reloaded `fun_mod.txt`, master!")

@client.command(aliases=["gbann", "globalanc"], hidden=True)
@commands.is_owner()
async def globalannounce(ctx, *, msg):
    """Announces a message globally, and sends it to all the log channels in every server Dekomori is in. Takes a string as argument.

    Parameters
    ----------
    msg : str
        The message to be announced.
    """
    globalLogger.info(f"OWNER COMMAND - Global Announcement: {msg}")
    for guild in client.guilds:
        if guildsDB[str(guild.id)]["log_channel_id"] != 0:
            guildId = str(guild.id)
            logChanObj = discord.utils.get(guild.text_channels, id=guildsDB[guildId]["log_channel_id"])
            globalLogger.debug(f"Sending announcement to {guild.name}.")
            try:
                await logChanObj.send(msg)
            except discord.Forbidden:
                globalLogger.error(f"Couldn't send announcement to {guild.name} because of a Forbidden error.")
    await ctx.send("Announcement sent to the following servers, master!\n" + "\n".join([guild.name for guild in client.guilds]))

################# EXECUTE! #################
client.run(globalConfig["token"])