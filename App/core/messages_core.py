# usr/bin/env python3
# -*- coding: utf-8 -*-

def nokos_stall(memberMention, memberName, parsedDuration):
    #TODO refactor this, no longer used, check baitrole.py/baitrole for appropriate code 
    return f"**Stall Kick:** {memberMention} ({memberName}) joined earlier, but didn't complete onboarding in {parsedDuration}. They have _NOT_ been kicked, okay!?"

class commands:
    baitrole = {
        "no_args": lambda: "Hey, what exactly do you want me to do? There's `add` and `remove`!"
    }