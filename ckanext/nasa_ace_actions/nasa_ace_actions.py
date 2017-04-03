import ckan.plugins.toolkit as toolkit

import loopback
import chat
import workspace
import pylons

DEV = pylons.config.get('nasa_ace_actions.actions_dev')

## setup for original and extra actions
original_user_create = toolkit.get_action('user_create')
extra_user_create = [workspace] if DEV == "True" else [loopback, chat, workspace]

original_user_update = toolkit.get_action('user_update')
extra_user_update= [workspace] if DEV == "True" else [loopback, chat, workspace]

original_user_delete = toolkit.get_action('user_delete')
extra_user_delete = [workspace] if DEV == "True" else [chat, workspace]

original_user_show = toolkit.get_action('user_show')
extra_user_show = [] if DEV == "True" else [chat]

original_organization_create = toolkit.get_action('organization_create')
extra_organization_create = [] if DEV == "True" else [loopback, chat]

original_organization_delete = toolkit.get_action('organization_delete')
extra_organization_delete = [] if DEV == "True" else [loopback, chat]

original_organization_member_create = \
    toolkit.get_action('organization_member_create')
extra_organization_member_create = [] if DEV == "True" else [loopback, chat]

original_organization_member_delete= \
    toolkit.get_action('organization_member_delete')
extra_organization_member_delete = [] if DEV == "True" else [loopback, chat]

original_group_create = toolkit.get_action('group_create')
extra_group_create = [] if DEV == "True" else [chat]

original_group_delete = toolkit.get_action('group_delete')
extra_group_delete = [] if DEV == "True" else [chat]

original_group_member_create = \
    toolkit.get_action('group_member_create')
extra_group_member_create = [] if DEV == "True" else [chat]

original_group_member_delete= \
    toolkit.get_action('group_member_delete')
extra_group_member_delete = [] if DEV == "True" else [chat]

## USER_action
def nasa_ace_user_create(context, data_dict=None):
    """user create with extra actions for NASA ACE
    """
    original_action = original_user_create(context, data_dict)
    for extra_actions in extra_user_create:
        extra_actions.user_create(context, data_dict, original_action)
    return original_action

def nasa_ace_user_update(context, data_dict=None):
    """user update with extra actions for NASA ACE
    """
    original_action = original_user_update(context, data_dict)
    for extra_actions in extra_user_update:
        extra_actions.user_update(context, data_dict, original_action)
    return original_action

def nasa_ace_user_delete(context, data_dict=None):
    """user_delet with Extra actions for NASA ACE
    """
    for extra_actions in extra_user_delete:
        extra_actions.user_delete(context, data_dict)
    return original_user_delete(context, data_dict)

def nasa_ace_user_show(context, data_dict=None):
    """user_show with Extra actions for NASA ACE
    """
    for extra_actions in extra_user_show:
        extra_actions.user_show(context, data_dict)
    return original_user_show(context, data_dict)

## ORGANIZATION actions
def nasa_ace_organization_create(context, data_dict=None):
    """organization_create with extra actions for NASA ACE
    """
    original_action = original_organization_create(context, data_dict)
    for extra_actions in extra_organization_create:
        extra_actions.organization_create(context, data_dict, original_action)
    return original_action

def nasa_ace_organization_delete(context, data_dict=None):
    """organization_create with extra actions for NASA ACE
    """
    for extra_actions in extra_organization_delete:
        extra_actions.organization_delete(context, data_dict, original_action)
    return original_organization_delete(context, data_dict)


def nasa_ace_organization_member_create(context, data_dict=None):
    """organization_create with extra actions for NASA ACE
    """
    original_action = original_organization_member_create(context, data_dict)
    for extra_actions in extra_organization_member_create:
        extra_actions.organization_member_create(context,
                                                 data_dict,
                                                 original_action)
    return original_action

def nasa_ace_organization_member_delete(context, data_dict=None):
    """organization_create with extra actions for NASA ACE
    """
    for extra_actions in extra_organization_member_delete:
        extra_actions.organization_mamber_delete(context,
                                                 data_dict,
                                                 original_action)
    return original_organization_member_delete(context, data_dict)


## GROUP actions
def nasa_ace_group_create(context, data_dict=None):
    """group_create with extra actions for NASA ACE
    """
    original_action = original_group_create(context, data_dict)
    for extra_actions in extra_group_create:
        extra_actions.group_create(context, data_dict, original_action)
    return original_action

def nasa_ace_group_delete(context, data_dict=None):
    """group_create with extra actions for NASA ACE
    """
    for extra_actions in extra_group_delete:
        extra_actions.group_delete(context, data_dict, original_action)
    return original_group_delete(context, data_dict)


def nasa_ace_group_member_create(context, data_dict=None):
    """group_create with extra actions for NASA ACE
    """
    original_action = original_group_member_create(context, data_dict)
    for extra_actions in extra_group_member_create:
        extra_actions.group_member_create(context,
                                                 data_dict,
                                                 original_action)
    return original_action

def nasa_ace_group_member_delete(context, data_dict=None):
    """group_create with extra actions for NASA ACE
    """
    for extra_actions in extra_group_member_delete:
        extra_actions.group_mamber_delete(context,
                                                 data_dict,
                                                 original_action)
    return original_group_member_delete(context, data_dict)
