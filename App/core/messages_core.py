# usr/bin/env python3
# -*- coding: utf-8 -*-

def nokos_stall(memberMention, memberName, parsedDuration):
    return f"**Stall Kick:** {memberMention} ({memberName}) joined earlier, but didn't complete onboarding in {parsedDuration}. They have _NOT_ been kicked, okay!?"