import ckan.plugins.toolkit as toolkit
import ckan.logic.action as action

# This will be modified by the Chef run to match the AWS infrastructure
# It will simply return the user_show action if not modified by Chef.
def user_show(context, data_dict=None):
    return action.get.user_show(context, data_dict)

def user_create(context, data_dict=None):
    return action.create.user_create(context, data_dict)

def user_update(context, data_dict=None):
    return action.update.user_update(context, data_dict)

def user_delete(context, data_dict=None):
    return action.delete.user_delete(context, data_dict)

def organization_create(context, data_dict=None):
    return action.create.organization_create(context, data_dict)
