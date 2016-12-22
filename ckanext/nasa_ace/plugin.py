import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import actions

class Nasa_AcePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthenticator)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'nasa_ace')

    # IActions
    def get_actions(self):
        return {'user_show': actions.user_show,
                'user_create': actions.user_create,
                'user_update': actions.user_update,
                'user_delete': actions.user_delete,
                'organization_create': actions.organization_create }

    # IAuthenticator
    # This requires that I define identify and login even if I don't use them.
    def identify(self):
        pass

    def login(self):
        pass

    def abort(self):
        pass

    # Set CC_DATA to 0 to logout the current user in CometChat.
    def logout(self):
        toolkit.response.set_cookie('cc_data', '0')
