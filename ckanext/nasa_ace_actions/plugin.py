import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import nasa_ace_actions as naa

class Nasa_AceActions(plugins.SingletonPlugin):
    """Nasa Ace plugin for extending actions
    """
    plugins.implements(plugins.IActions, inherit = True)

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
