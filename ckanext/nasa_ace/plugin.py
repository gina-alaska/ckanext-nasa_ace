import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import actions

class Nasa_AcePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'nasa_ace')

    # IActions
    def get_actions(self):
        return {'user_show': actions.user_show, 
                'user_create': actions.user_create }
