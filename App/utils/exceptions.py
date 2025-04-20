# usr/bin/env python3
# -*- coding: utf-8 -*-

import discord
from App.dekomori import client
from App.utils.startup import globalLogger
from App.utils.constants import VERSION

class BaitRoleError(Exception):
    """Base class for bait role-related exceptions."""
    pass

class RoleAlreadyInListError(BaitRoleError):
    """Raised when trying to add a role that's already in the bait role list."""
    pass

class AddAllRolesError(BaitRoleError):
    """Raised when an attempt is made to add all roles to the bait roles list."""
    pass

class InvalidRoleError(BaitRoleError):
    """Raised when a role is invalid or doesn't exist."""
    pass
