import ckan.plugins.toolkit as toolkit
import ckan.logic.action as action
#~ import ckanext.loopback.plugin as loopback
#~ from config import chat_connect
import time
from sqlalchemy import *


## USER actions
def user_show(context, data_dict=None):
    """extra user show actions for connecting chat
    """
    mysql_engine = create_engine(chat_connect(), pool_recycle=3600)
    mysql_engine.connect()
    result = mysql_engine.execute(
        "select userid from users where name='" + str(context['user']) + "'")
    for row in result:
        toolkit.response.set_cookie('cc_data', str(row['userid']))
    #~ return action.get.user_show(context, data_dict)

def user_create(context, data_dict=None, original_action=None):
    """extra create user actions for connecting chat
    """
    #~ original_action = loopback.user_create(context,data_dict)
    if original_action is None:
        raise toolkit.ValidationError, "Original action not provideded"
    mysql_engine = create_engine(chat_connect(), pool_recycle=3600)
    connection = mysql_engine.connect()
    metadata = MetaData()
    users = Table('users',
                  metadata,
                  Column('userid', Integer),
                  Column('name', String),)
    metadata.create_all(mysql_engine)
    userobj = context['user_obj']
    insert = users.insert().values(name=str(userobj.name))
    result = connection.execute(insert)
    #~ return original_action

def user_update(context, data_dict=None, original_action=None):
    """extra user update actions for connecting chat
    """
    if original_action is None:
        raise toolkit.ValidationError, "Original action not provideded"
    original_username = context['user']
    mysql_engine = create_engine(chat_connect(), pool_recycle=3600)
    connection = mysql_engine.connect()
    metadata = MetaData()
    users = Table('users',
                  metadata,
                  Column('userid', Integer),
                  Column('name', String),)
    metadata.create_all(mysql_engine)
    update = users.update().where(users.c.name == str(original_username)).\
        values(name=str(context['user_obj'].name))
    connection.execute(update)
    #~ return original_action

def user_delete(context, data_dict=None):
    """extra user delete actions for connecting chat
    """
    model = context['model']
    user_id = toolkit.get_or_bust(data_dict, 'id')
    delete_user = model.User.get(user_id)
    mysql_engine = create_engine(chat_connect(), pool_recycle=3600)
    connection = mysql_engine.connect()
    metadata = MetaData()
    users = Table('users',
                  metadata,
                  Column('userid', Integer),
                  Column('name', String),)
    metadata.create_all(mysql_engine)
    delete = users.delete().where(users.c.name == str(delete_user.name))
    connection.execute(delete)


## ORGANIZATION ations
def organization_create(context, data_dict=None, original_action=None):
    """extra organization_create for connection chat
    """
    if original_action is None:
        raise toolkit.ValidationError, "Original action not provideded"
    mysql_engine = create_engine(chat_connect(), pool_recycle=3600)
    connection = mysql_engine.connect()
    metadata = MetaData()
    chatrooms = Table('cometchat_chatrooms',
                      metadata,
                      Column('id', Integer),
                      Column('name', String),
                      Column('lastactivity', Integer),
                      Column('createdby', Integer),
                      Column('password', String),
                      Column('type', Integer),
                      Column('vidsession', String),
                      Column('invitedusers', String),)
    chatroom_users = Table('cometchat_chatrooms_users',
                           metadata,
                           Column('userid', Integer),
                           Column('chatroomid', Integer),
                           Column('isbanned', Integer),)
    metadata.create_all(mysql_engine)
    result = mysql_engine.execute(\
        "select userid from users where name='" + \
        str(context['auth_user_obj'].name) + "'")
    for userid in result:
        insert_chatroom = chatrooms.insert().values(
            name="Org: " + str(context['group'].display_name),
            lastactivity=int(time.time()),
            createdby=int(userid['userid']),
            type=2)
        insert_result = connection.execute(insert_chatroom)
        insert_user = chatroom_users.insert().values(
                                        userid=int(userid['userid']),
                                        chatroomid=int(insert_result.lastrowid))
        connection.execute(insert_user)

def organization_delete(context, data_dict=None, original_action=None):
    """extra organization_delete actions for chat
    """
    mysql_engine = create_engine(chat_connect(), pool_recycle=3600)
    connection = mysql_engine.connect()
    metadata = MetaData()
    chatrooms = Table('cometchat_chatrooms',
                      metadata,
                      Column('id', Integer),
                      Column('name', String),
                      Column('lastactivity', Integer),
                      Column('createdby', Integer),
                      Column('password', String),
                      Column('type', Integer),
                      Column('vidsession', String),
                      Column('invitedusers', String),)
    chatroom_users = Table('cometchat_chatrooms_users',
                           metadata,
                           Column('userid', Integer),
                           Column('chatroomid', Integer),
                           Column('isbanned', Integer),)
    metadata.create_all(mysql_engine)
    result = connection.execute(
        'select id from cometchat_chatrooms where name="Org: ' +\
         str(context['group'].display_name) + '"')
    for chatroom in result:
        delete_chatroom = \
            chatrooms.delete().where(chatrooms.c.id == str(chatroom['id']))
        delete_chatroom_users = chatroom_users.delete().where(
                            chatroom_users.c.chatroomid == str(chatroom['id']))
        connection.execute(delete_chatroom)
        connection.execute(delete_chatroom_users)

def organization_member_create(context, data_dict=None, original_action=None):
    """extra organization_member_create actions for chat
    """
    if original_action is None:
        raise toolkit.ValidationError, "Original action not provideded"
    mysql_engine = create_engine(chat_connect(), pool_recycle=3600)
    connection = mysql_engine.connect()
    metadata = MetaData()
    chatrooms = Table('cometchat_chatrooms',
                      metadata,
                      Column('id', Integer),
                      Column('name', String),
                      Column('lastactivity', Integer),
                      Column('createdby', Integer),
                      Column('password', String),
                      Column('type', Integer),
                      Column('vidsession', String),
                      Column('invitedusers', String),)
    chatroom_users = Table('cometchat_chatrooms_users',
                           metadata,
                           Column('userid', Integer),
                           Column('chatroomid', Integer),
                           Column('isbanned', Integer),)
    metadata.create_all(mysql_engine)
    userid_result = connection.execute(
        "select userid from users where name='" +\
        str(data_dict['username']) + "'")
    for userid in userid_result:
        for chatroom in connection.execute(\
            select([chatrooms.c.id, chatrooms.c.invitedusers]).\
            where(chatrooms.c.name == "Org: " + str(context['group'].title))):
            ## start loop
            chatroom_user_result = connection.execute(
                ('select userid from cometchat_chatrooms_users'
                ' where chatroomid=') + str(chatroom[chatrooms.c.id]))
            for user in chatroom_user_result:
                if (user['userid'] == userid['userid']):
                    return
            insert_user = chatroom_users.insert().values(
                                    userid=int(userid['userid']),
                                    chatroomid=int(chatroom[chatrooms.c.id]))
            if (chatroom[chatrooms.c.invitedusers] != None):
                update_chatroom = chatrooms.update().where(
                    chatrooms.c.id==chatroom[chatrooms.c.id]).\
                    values(invitedusers=str(chatroom[chatrooms.c.invitedusers])\
                    + "," + str(userid['userid']))
            else:
                update_chatroom = chatrooms.update().\
                    where(chatrooms.c.id==chatroom[chatrooms.c.id]).\
                    values(invitedusers=str(userid['userid']))
            connection.execute(update_chatroom)
            connection.execute(insert_user)


def organization_member_delete(context, data_dict=None, original_action=None):
    """extra organization_member_delete actions for chat
    """
    model = context['model']
    mysql_engine = create_engine(chat_connect(), pool_recycle=3600)
    connection = mysql_engine.connect()
    metadata = MetaData()
    chatrooms = Table('cometchat_chatrooms',
                       metadata,
                       Column('id', Integer),
                       Column('name', String),
                       Column('lastactivity', Integer),
                       Column('createdby', Integer),
                       Column('password', String),
                       Column('type', Integer),
                       Column('vidsession', String),
                       Column('invitedusers', String),)
    chatroom_users = Table('cometchat_chatrooms_users',
                        metadata,
                        Column('userid', Integer),
                        Column('chatroomid', Integer),
                        Column('isbanned', Integer),)
    metadata.create_all(mysql_engine)
    user = model.User.get(data_dict['user_id'])
    group = model.Group.get(data_dict['id'])
    member = mysql_engine.execute(
        "select userid from users where name='" + str(user.name) + "'")
    for userid in member:
        for chatroomid in connection.execute(\
            select([chatrooms.c.id, chatrooms.c.invitedusers]).\
            where(chatrooms.c.name == "Org: " + str(group.title))):
            ## start loop
            delete_chatroom_user = \
                chatroom_users.delete().where(and_(
                chatroom_users.c.userid == str(userid['userid']),
                chatroom_users.c.chatroomid == str(chatroomid[chatrooms.c.id])))
            new_invitedusers = chatroomid[chatrooms.c.invitedusers].split(',')
            try:
                new_invitedusers.remove(str(userid['userid']))
            except:
                pass
            new_invitedusers = ','.join(new_invitedusers)
            update_chatroom = chatrooms.update().\
                where(chatrooms.c.id==chatroomid[chatrooms.c.id]).\
                values(invitedusers=str(new_invitedusers))
            connection.execute(delete_chatroom_user)
            connection.execute(update_chatroom)




## GROUP ACTIONS
def group_create(context, data_dict=None, original_action = None):
    """extra group create actions for nasa ace
    """
    mysql_engine = create_engine(chat_connect(), pool_recycle=3600)
    connection = mysql_engine.connect()
    metadata = MetaData()
    chatrooms = Table('cometchat_chatrooms',
                      metadata,
                      Column('id', Integer),
                      Column('name', String),
                      Column('lastactivity', Integer),
                      Column('createdby', Integer),
                      Column('password', String),
                      Column('type', Integer),
                      Column('vidsession', String),
                      Column('invitedusers', String),)
    chatroom_users = Table('cometchat_chatrooms_users',
                            metadata,
                            Column('userid', Integer),
                            Column('chatroomid', Integer),
                            Column('isbanned', Integer),)
    metadata.create_all(mysql_engine)
    result = mysql_engine.execute(\
        "select userid from users where name='" + \
        str(context['auth_user_obj'].name) + "'")
    for userid in result:
        insert_chatroom = chatrooms.insert().values(\
            name="Group: " + str(context['group'].display_name),
            lastactivity=int(time.time()),
            createdby=int(userid['userid']),
            type=2)
        insert_result = connection.execute(insert_chatroom)
        insert_user = chatroom_users.insert().values(\
            userid=int(userid['userid']),
            chatroomid=int(insert_result.lastrowid))
        connection.execute(insert_user)

def group_delete(context, data_dict=None, original_action = None):
    """extra delete create actions for nasa ace
    """
    mysql_engine = create_engine(chat_connect(), pool_recycle=3600)
    connection = mysql_engine.connect()
    metadata = MetaData()
    chatrooms = Table('cometchat_chatrooms',
                      metadata,
                      Column('id', Integer),
                      Column('name', String),
                      Column('lastactivity', Integer),
                      Column('createdby', Integer),
                      Column('password', String),
                      Column('type', Integer),
                      Column('vidsession', String),
                       Column('invitedusers', String),)
    chatroom_users = Table('cometchat_chatrooms_users',
                           metadata,
                           Column('userid', Integer),
                           Column('chatroomid', Integer),
                           Column('isbanned', Integer),)
    metadata.create_all(mysql_engine)
    result = connection.execute(\
        'select id from cometchat_chatrooms where name="Group: ' +\
         str(context['group'].display_name) + '"')
    for chatroom in result:
        delete_chatroom = \
            chatrooms.delete().where(chatrooms.c.id == str(chatroom['id']))
        delete_chatroom_users = \
            chatroom_users.delete().\
            where(chatroom_users.c.chatroomid == str(chatroom['id']))
        connection.execute(delete_chatroom)
        connection.execute(delete_chatroom_users)


def group_member_create(context, data_dict=None, original_action = None):
    """extra group member create functions
    """
    mysql_engine = create_engine(chat_connect(), pool_recycle=3600)
    connection = mysql_engine.connect()
    metadata = MetaData()
    chatrooms = Table('cometchat_chatrooms',
                      metadata,
                      Column('id', Integer),
                      Column('name', String),
                      Column('lastactivity', Integer),
                      Column('createdby', Integer),
                      Column('password', String),
                      Column('type', Integer),
                      Column('vidsession', String),
                      Column('invitedusers', String),)
    chatroom_users = Table('cometchat_chatrooms_users',
                            metadata,
                            Column('userid', Integer),
                            Column('chatroomid', Integer),
                            Column('isbanned', Integer),)
    metadata.create_all(mysql_engine)
    userid_result = mysql_engine.execute(\
        "select userid from users where name='" +\
        str(data_dict['username']) + "'")
    for userid in userid_result:
        for chatroom in connection.execute(
            select([chatrooms.c.id, chatrooms.c.invitedusers]).\
            where(chatrooms.c.name == "Group: " + str(context['group'].title))):
            ## start loop
            chatroom_user_result = connection.execute(\
                ('select userid from cometchat_chatrooms_users'
                ' where chatroomid=') + str(chatroom[chatrooms.c.id]))
            for user in chatroom_user_result:
                if (user['userid'] == userid['userid']):
                    return
            insert_user = chatroom_users.insert().values(\
                                    userid=int(userid['userid']),
                                    chatroomid=int(chatroom[chatrooms.c.id]))
            if (chatroom[chatrooms.c.invitedusers] != None):
                update_chatroom = chatrooms.update().where(\
                    chatrooms.c.id==chatroom[chatrooms.c.id]).values(\
                    invitedusers=str(chatroom[chatrooms.c.invitedusers])\
                    +"," + str(userid['userid']))
            else:
                update_chatroom = chatrooms.update().where(\
                    chatrooms.c.id==chatroom[chatrooms.c.id]).\
                    values(invitedusers=str(userid['userid']))
            connection.execute(update_chatroom)
            connection.execute(insert_user)

def group_member_delete(context, data_dict=None, original_action = None):
    """extra group member delete functions
    """
    model = context['model']
    mysql_engine = create_engine(chat_connect(), pool_recycle=3600)
    connection = mysql_engine.connect()
    metadata = MetaData()
    chatrooms = Table('cometchat_chatrooms',
                    metadata,
                    Column('id', Integer),
                    Column('name', String),
                    Column('lastactivity', Integer),
                    Column('createdby', Integer), Column('password', String),
                    Column('type', Integer), Column('vidsession', String),
                    Column('invitedusers', String),)
    chatroom_users = Table('cometchat_chatrooms_users',
                            metadata, Column('userid', Integer),
                            Column('chatroomid', Integer),
                            Column('isbanned', Integer),)
    metadata.create_all(mysql_engine)
    user = model.User.get(data_dict['user_id'])
    group = model.Group.get(data_dict['id'])
    member = mysql_engine.execute(\
        "select userid from users where name='" + str(user.name) + "'")
    for userid in member:
        for chatroomid in connection.execute(\
            select([chatrooms.c.id, chatrooms.c.invitedusers]).\
            where(chatrooms.c.name == "Org: " + str(group.title))):
            ## start loop
            delete_chatroom_user = chatroom_users.delete().\
                where(and_(chatroom_users.c.userid == str(userid['userid']),
                chatroom_users.c.chatroomid == str(chatroomid[chatrooms.c.id])))
            new_invitedusers = chatroomid[chatrooms.c.invitedusers].split(',')
            try:
                new_invitedusers.remove(str(userid['userid']))
            except:
                pass
            new_invitedusers = ','.join(new_invitedusers)
            update_chatroom = chatrooms.update().where(\
                chatrooms.c.id==chatroomid[chatrooms.c.id]).\
                values(invitedusers=str(new_invitedusers))
            connection.execute(delete_chatroom_user)
            connection.execute(update_chatroom)


