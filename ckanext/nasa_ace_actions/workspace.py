import requests
import ckan.plugins.toolkit as toolkit


import smtplib
from email.mime.text import MIMEText

import pylons.config as config

def workspace_msg (action, msg):
    """will send a message to the NASA ACE workspace thingy
    """
    url = config.get('nasa_ace_actions.workspase_url')
    msg['action'] = action
    try:
        response = requests.post(url, data = msg)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        email = config.get('nasa_ace_actions.email')
        #~ print email
        msg = MIMEText("Error with user " + action + "for \n" + str(msg) )
        msg['Subject'] = "NASA ACE worspace sync error: " + action 
        msg["From"] = email
        msg["To"] = email
        
        #send messege
        server = smtplib.SMTP(config.get('nasa_ace_actions.mailserver'))
        server.sendmail(email,email,msg.as_string())
        server.quit()
    


def user_create(context, data_dict=None, original_action=None):
    """extra create user actions for connecting workspace
    """
    if original_action is None:
        raise toolkit.ValidationError, "Original action not provideded"
    
    workspace_info = {
        #~ 'id': original_action['id'],
        'username': original_action['name'],
        'name': original_action['display_name'],
        'email': original_action['email'],
        'apikey':original_action['apikey'],
    }
    workspace_msg('create',  workspace_info)
    
def user_update(context, data_dict=None, original_action=None):
    """extra user update actions for connecting workspace
    """
    if original_action is None:
        raise toolkit.ValidationError, "Original action not provideded"
    #~ print original_action 
    
    # if the api key not provided then this update does not need to be 
    # sent to the workspace as the apikey was not changed
    try:

        api_key = original_action['apikey']
    except KeyError:
        return 
        
    workspace_info = {
            #~ 'id': original_action['id'],
            'username': original_action['name'],
            'name': original_action['display_name'],
            'email': original_action['email'],
            'apikey': api_key,
        }
    workspace_msg('update',  workspace_info)
    
def user_delete(context, data_dict=None, original_action=None):
    """extra user update actions for connecting workspace
    """
    user_show = toolkit.get_action('user_show')
    user = user_show(context, data_dict)
    workspace_info = {
        #~ 'id': data_dict['id'],
        'username': user['name'],
        'name': user['display_name'],
        'email': user['email'],
        }
        
    workspace_msg('delete',  workspace_info)
