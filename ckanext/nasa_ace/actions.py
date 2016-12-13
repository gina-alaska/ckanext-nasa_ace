import ckan.plugins.toolkit as toolkit
import ckan.logic.action as action

def user_show(context, data_dict=None):
        user_dict = action.get.user_show(context, data_dict)
        toolkit.response.set_cookie('cc_data', user_dict.get('cc_id'), domain='*')
        return user_dict
