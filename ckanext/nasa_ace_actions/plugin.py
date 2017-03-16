import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

#~ import ckan.logic.action as actions


import smtplib
from email.mime.text import MIMEText



original_user_create = toolkit.get_action('user_create')
original_user_update = toolkit.get_action('user_upadte')
original_user_delete = toolkit.get_action('user_delete')



def workspace_msg (action, msg):
    """will send a message to the NASA ACE workspace thingy
    """
    
    msg = MIMEText(action + '/n' + msg)
    msg['Subject'] = 'test user create 1'
    msg["From"] = 'rwspicer@alaska.edu'
    msg["To"] = 'rwspicer@alaska.edu'
    
    #send messege
    server = smtplib.SMTP('smtp.uaf.edu')
    server.sendmail('rwspicer@alaska.edu','rwspicer@alaska.edu',msg.as_string())
    server.quit()

    

def nasa_ace_user_create(context, data_dict=None):
    original_action= original_user_create(context, data_dict)
    
    
    loopback_info = {
        'id': original_action['id'],
        'username': original_action['name'],
        'email': original_action['email'],
        'password': toolkit.get_or_bust(data_dict,'password1'),
    }
    workspace_info = {
        'id': original_action['id'],
        'username': original_action['name'],
        'email': original_action['email'],
        'apikey':original_action['apikey'],
    }
    
    
    
    
    loopback.loopback_user_create(loopback_info)
    chatconnect.user_create(original_action)
    workspace_msg('create',  workspace_info)
    
    
    return original_action
    
def nasa_ace_user_update(context, data_dict=None):
    original_action= original_user_update(context, data_dict)
    
    
    loopback_info = {
        'id': original_action['id'],
        'username': original_action['name'],
        'email': original_action['email'],
        'password': toolkit.get_or_bust(data_dict,'password1'),
    }
    workspace_info = {
        'id': original_action['id'],
        'username': original_action['name'],
        'email': original_action['email'],
        'apikey':original_action['apikey'],
    }
    
    
    
    
    loopback.loopback_user_update(TBD ARGS)
    chatconnect.user_update(original_action)
    workspace_msg('update',  workspace_info)
    
    
    return original_action
    
    
    
def nasa_ace_user_delete(context, data_dict=None):
    
    
    workspace_info = {
        'id': toolkit.get_or_bust(data_dict,'id'),
    }
    
    workspace_msg('delete',  workspace_info)
    chatconnect.user_delete(context, data_dict)
    return original_user_delete(context, data_dict)
    



class Nasa_AceActions(plugins.SingletonPlugin, DefaultTranslation):

    #~ plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions, inherit = True)
    #~ plugins.implements(plugins.IAuthFunctions)
    
    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'nasa_ace')
        

    #IRoutes
    def before_map(self, m):
        """redirect index to dataset """
        m.redirect('/', '/dataset')
        return m

    def get_actions(self):
        return {
            'user_show': ,
            'user_create': nasa_ace_user_create,
            'user_update': nasa_ace_user_update,
            'user_create': nasa_ace_user_delete,
            'organization_create': ,
            'organization_delete': ,
            'organization_member_create': ,
            'organization_member_delete': ,
            'group_create': ,
            'group_delete': ,
            'group_member_create': ,
            'group_member_delete':  }

    #~ # IAuthenticator
    #~ # This requires that I define identify, login, and abort even if I don't use them.
    #~ def identify(self):
        #~ pass

    #~ def login(self):
        #~ pass

    #~ def abort(self):
        #~ pass

    #~ # Set CC_DATA to 0 to logout the current user in CometChat.
    #~ def logout(self):
        #~ toolkit.response.set_cookie('cc_data', '0')

