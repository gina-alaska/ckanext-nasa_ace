import ckan.plugins.toolkit as toolkit

import smtplib
from email.mime.text import MIMEText




def workspace_msg (action, msg):
    """will send a message to the NASA ACE workspace thingy
    """
    pass 
    # message suff should go here 
    


def user_create(context, data_dict=None, original_action=None):
    """extra create user actions for connecting workspace
    """
    if original_action is None:
        raise toolkit.ValidationError, "Original action not provideded"
    
    workspace_info = {
        'id': original_action['id'],
        'username': original_action['name'],
        'email': original_action['email'],
        'apikey':original_action['apikey'],
    }
    workspace_msg('create',  workspace_info)
    
def user_update(context, data_dict=None, original_action=None):
    """extra user update actions for connecting workspace
    """
    if original_action is None:
        raise toolkit.ValidationError, "Original action not provideded"
        
    workspace_info = {
        'id': original_action['id'],
        'username': original_action['name'],
        'email': original_action['email'],
        'apikey':original_action['apikey'],
    }
    workspace_msg('update',  workspace_info)
    
def user_delete(context, data_dict=None, original_action=None):
    """extra user update actions for connecting workspace
    """
    #~ workspace_info = {
        #~ 'id': data_dict['id'],
        #~ 'username': data_dict['name'],
        #~ 'email': data_dict['email'],
        #~ }
        
    workspace_msg('delete',  data_dict)
