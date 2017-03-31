import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
import nasa_ace_actions as naa

from sqlalchemy.util import OrderedDict

def create_dataset_types():
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'dataset_types'}
        toolkit.get_action('vocabulary_show')(context, data)
    except toolkit.ObjectNotFound:
        data = {'name': 'dataset_types'}
        vocab = toolkit.get_action('vocabulary_create')(context, data)
        for tag in (u'Weather', u'Oceans', u'Sea Ice', u'Snow', u'Terrestial', u'Hydrology', u'Hazards', u'Infrastructure'):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)


def dataset_types():
    create_dataset_types()
    try:
        tag_list = toolkit.get_action('tag_list')
        dataset_types = tag_list(data_dict={'vocabulary_id': 'dataset_types'})
        return dataset_types
    except toolkit.ObjectNotFound:
        return None

class Nasa_AcePlugin(plugins.SingletonPlugin, DefaultTranslation, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthenticator)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IActions, inherit = True)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets, inherit = True)

    def get_actions(self):
        """defines actions to extend
        """
        return {
            'user_show': naa.nasa_ace_user_show,
            'user_create': naa.nasa_ace_user_create,
            'user_update': naa.nasa_ace_user_update,
            'user_delete': naa.nasa_ace_user_delete,
            'organization_create': naa.nasa_ace_organization_create,
            'organization_delete': naa.nasa_ace_organization_delete,
            'organization_member_create':
                naa.nasa_ace_organization_member_create,
            'organization_member_delete':
                naa.nasa_ace_organization_member_delete,
            'group_create': naa.nasa_ace_group_create,
            'group_delete': naa.nasa_ace_group_delete,
            'group_member_create': naa.nasa_ace_group_member_create,
            'group_member_delete': naa.nasa_ace_group_member_delete,}

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

    ## IDatasetform

    # modify schema
    def _modify_package_schema(self, schema):
        #~ schema.update({
            #~ 'custom_text': [toolkit.get_validator('ignore_missing'),
                            #~ toolkit.get_converter('convert_to_extras')]
        #~ })
        schema.update({
            'dataset_type': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_tags')('dataset_types')
            ]
        })
        return schema

    def create_package_schema(self):
        schema = super(Nasa_AceDatasetPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(Nasa_AceDatasetPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(Nasa_AceDatasetPlugin, self).show_package_schema()
        #~ schema.update({
            #~ 'custom_text': [toolkit.get_converter('convert_from_extras'),
                            #~ toolkit.get_validator('ignore_missing')]
        #~ })
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        schema.update({
            'dataset_type': [
                toolkit.get_converter('convert_from_tags')('dataset_types'),
                toolkit.get_validator('ignore_missing')]
            })
        return schema
    # end modify schema

    ## these next two functions are default dataset types
    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []


    def get_helpers(self):
        return {'dataset_types': dataset_types}


    def dataset_facets(self, facets_dict, package_type):
        if package_type != 'dataset':
            return facets_dict


        new_facets = OrderedDict()
        new_facets['vocab_dataset_types'] = toolkit._('Dataset Types')
        for f in facets_dict:
            new_facets[f] = facets_dict[f]
        return new_facets
