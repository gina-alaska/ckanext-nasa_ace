import logging
import requests
import pylons
import json
#~ import ckan.plugins as plugins
#~ import ckan.logic as logic
#~ import ckan.lib.navl.dictization_functions
#~ import ckan.lib.dictization.model_dictize as model_dictize
#~ import ckan.lib.dictization.model_save as model_save

log = logging.getLogger(__name__)
#~ _validate = ckan.lib.navl.dictization_functions.validate
#~ _get_action = logic.get_action
#~ _check_access = logic.check_access
#~ ValidationError = logic.ValidationError
#~ _get_or_bust = logic.get_or_bust
#~ _group_or_org_create = logic.action.create._group_or_org_create
#~ _group_or_org_member_create = logic.action.create._group_or_org_member_create
#~ _group_or_org_member_delete = logic.action.delete._group_or_org_member_delete


import ckan.plugins.toolkit as toolkit

def loopback_login():
    loopback_login_url = pylons.config.get('ckan.loopback.login_url')

    response = requests.post(loopback_login_url, data = {
        'username': pylons.config.get('ckan.loopback.username'),
        'password': pylons.config.get('ckan.loopback.password')
    })

    response.raise_for_status()

    pylons.config['loopback_token'] = json.loads(response.text)['id']
    log.debug('Logged into LoopBack with access token: {}'
        .format(pylons.config.get('loopback_token')))


def loopback_user_update(user_id, user_info):
    """update user actions for loopback
    """
    if pylons.config.get('loopback_token') is None:
        loopback_login()

    loopback_user_url = pylons.config.get('ckan.loopback.user_url')
    loopback_user_id_url = '{}/{}'.format(loopback_user_url, user_id)
    loopback_token = pylons.config.get('loopback_token')
    request_url = '{}?access_token={}'.format(loopback_user_id_url, loopback_token)
    response = requests.put(request_url, data = user_info)

    if response.status_code == 401:
        loopback_login()
    else:
        response.raise_for_status()

    log.debug('LoopBack user updated: {}'.format(user_id))

def loopback_group_create(group_info):
    """Create group actions for loopback
    """
    if pylons.config.get('loopback_token') is None:
        loopback_login()

    loopback_user_url = pylons.config.get('ckan.loopback.group_url')
    loopback_token = pylons.config.get('loopback_token')
    request_url = '{}?access_token={}'.format(loopback_user_url, loopback_token)
    response = requests.post(request_url, data = group_info)

    if response.status_code == 401:
        loopback_login()
    else:
        response.raise_for_status()

    log.debug('LoopBack group created: {}'.format(group_info['id']))


def user_create(context, data_dict=None, original_action=None):
    """prefrom extra user create actions for the loopback server
    """
    if original_action is None:
        raise toolkit.ValidationError, "Original action not provideded"
    user_info = {
        'id': original_action['id'],
        'username': original_action['name'],
        'email': original_action['email'],
        'apikey': original_action['id'],
        'password': toolkit.get_or_bust(data_dict,'password1'),
    }
    if pylons.config.get('loopback_token') is None:
        loopback_login()

    loopback_user_url = pylons.config.get('ckan.loopback.user_url')
    loopback_token = pylons.config.get('loopback_token')
    request_url = '{}?access_token={}'.format(loopback_user_url, loopback_token)
    response = requests.post(request_url, data = user_info)

    if response.status_code == 401:
        loopback_login()
    else:
        response.raise_for_status()

    log.debug('LoopBack user created: {}'.format(user_info['id']))

def user_update(context, data_dict=None, original_action=None):
    """prefrom extra user create actions for the loopback server
    """
    if original_action is None:
        raise toolkit.ValidationError, "Original action not provideded"

    user_id = original_action['id']
    user_info = {
        'username': original_action['name'],
        'email': original_action['email'],
    }
    loopback_user_update(user_id,user_info)


def organization_create(context, data_dict, original_action=None):
    """organization_create with extra actions for loopback
    """
    if original_action is None:
        raise toolkit.ValidationError, "Original action not provideded"

    loopback_group_create({
      'id': original_action['id'],
      'name': original_action['title']
    })


def organization_member_create(context, data_dict, original_action=None):
    """organization_member_create (add user to org) for loopback server
    """
    if original_action is None:
        raise toolkit.ValidationError, "Original action not provideded"

    loopback_user_update(original_action['table_id'], {
      'groupId': context['group'].id
    })


def organization_member_delete(context, data_dict=None, original_action=None):
    """organization_member_delete (remove user to org) for loopback server
    """
    loopback_user_info = {
        'groupId': ''
    }

    loopback_user_update(data_dict['user_id'], loopback_user_info)
