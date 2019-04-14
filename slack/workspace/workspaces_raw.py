import os
from slack.element_slack.channels_files import ChannelsFiles
from slack.element_slack.users import Users
from slack.element_slack.messages import Messages
from slack.workspace.workspaces import Workspaces
import json
import time


class WorkspacesRaw(Workspaces):

    def __init__(self, path_dir, name_workspace):
        super().__init__(name_workspace)
        users: dict = dict()
        self._name_workspace = name_workspace
        path = path_dir + '/users.json'
        json_file = open(path).read()
        json_users = json.loads(json_file)
        index = 0
        while index < len(json_users):
            if json_users[index]['is_bot'] is False:
                user: Users = Users(json_users[index]['name'], json_users[index]['id'])
                user_id = json_users[index]['id']
                users[user_id] = user
            index = index + 1
        index = 0
        path = path_dir + '/channels.json'
        json_file = open(path).read()
        json_channel = json.loads(json_file)
        while index < len(json_channel):
            channel = ChannelsFiles(json_channel[index]['name'])
            self._channels[channel.get_name_channel()]=channel
            users_channel = users
            self._create_users(path_dir, channel.get_name_channel(), users_channel)
            index = index + 1
        for key in self._channels:
            channel : ChannelsFiles = self._channels.get(key)
            channel.search_for_users_mentioned()

    def _create_users(self, path_dir, channel_name, users_channel):
        path = path_dir + '/' + channel_name
        files = os.listdir(path)
        for file in files:
            name_file = path_dir + '/' + channel_name + '/' + file
            json_file = open(name_file).read()
            json_file: dict = json.loads(json_file)
            index = 0
            while index < len(json_file):
                if 'text' in json_file[index]:
                    text: str = json_file[index]['text']
                    if 'user' in json_file[index]:
                        id_user = json_file[index]['user']
                        user: Users = users_channel.get(id_user)
                        if user is not None:
                            second = float(json_file[index]['ts'])
                            date = time.gmtime(second)
                            str_date = time.strftime('%Y-%m-%d %H:%M:%S', date)
                            message: Messages = Messages(id_user, self._name_workspace, channel_name,
                                                         user.get_name_user(), text, str_date)
                            channel: ChannelsFiles = self._channels.get(channel_name)
                            channel.add_message_user(message)
                index = index + 1
