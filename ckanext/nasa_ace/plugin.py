import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckan.lib.plugins import DefaultTranslation
import routes.mapper
import ckan.lib.base as base


class Nasa_AcePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITranslation)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'nasa_ace')


    #IRoutes
    def before_map(self, route_map):
        with routes.mapper.SubMapper(route_map, controller='ckanext.nasa_ace.plugin:NASAACEController') as m:
                m.connect('chat', '/chat', action='chat')
        route_map.redirect('/', '/dataset')
        return route_map

class NASAACEController(base.BaseController):
        def chat(self):
                return base.render('snippets/cometchat-embedded.html')
