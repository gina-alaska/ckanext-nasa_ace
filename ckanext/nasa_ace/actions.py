import ckan.plugins.toolkit as toolkit
import ckan.logic.action as action

def user_show(context, data_dict=None):
    # This will be modified by the Chef run to match the AWS infrastructure
    # It will simply return the user_show action if not modified by Chef.
    return action.get.user_show(context, data_dict)

def user_create(context, data_dict=None):
    return action.get.user_create(context, data_dict)
