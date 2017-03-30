import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation

class Nasa_AcePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthenticator)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITranslation)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'nasa_ace')

    # IAuthenticator
    # This requires that I define identify, login, and abort even if I don't use them.
    def identify(self):
        pass

    def login(self):
        pass

    def abort(self):
        pass

    # Set CC_DATA to 0 to logout the current user in CometChat.
    def logout(self):
        toolkit.response.set_cookie('cc_data', '0')

    #IRoutes
    def before_map(self, m):
        """redirect index to dataset """
        m.redirect('/', '/dataset')
        return m
