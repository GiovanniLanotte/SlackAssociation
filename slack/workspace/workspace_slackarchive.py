import time
from slack.element_slack.messages import Messages
from slack.workspace.workspaces import Workspaces
from slack.element_slack.channels_files import ChannelsFiles
from slack.element_slack.users import Users
import json


class WorkspacesSlackArchive(Workspaces):

    def __init__(self, path_dir, name_workspace):
        super().__init__(name_workspace)
        self._users: dict = dict()
        self._channel_list = list()
        path = path_dir + '/team.json'
        open(path).read()
        self._name_workspace = name_workspace
        path = path_dir + '/channels.json'
        json_file = open(path).read()
        json_channels = json.loads(json_file)
        index = 0
        while index < len(json_channels):
            self._create_users(path_dir, json_channels[index]['name'])
            index = index + 1
        for key in self._channels:
            channel = self._channels.get(key)
            channel.search_for_users_mentioned()

    def _create_users(self, path_dir, channel_name):
        path = path_dir + '/users/' + channel_name + '.json'
        json_file = open(path).read()
        members: list = list()
        users_json = json.loads(json_file)
        users_id = users_json.keys()
        users: dict = dict()
        for key in users_id:
            name = users_json[key]['name']
            user_id = users_json[key]['user_id']
            members.append(user_id)
            if self._users.get(user_id) is None:
                user = Users(name, user_id)
                users[user_id] = user
        name_file = path_dir + '/messages/' + channel_name + '.json'
        json_file = open(name_file).read()
        messages_json = json.loads(json_file)
        index = 0
        users_channel = users
        channel = ChannelsFiles(channel_name)
        while index < len(messages_json):
            user_id = messages_json[index]['user']
            if users_channel.get(user_id) is not None:
                user: Users = users_channel[user_id]
                text_json = messages_json[index]['text']
                second = float(messages_json[index]['ts'])
                date = time.gmtime(second)
                str_date = time.strftime('%Y-%m-%d %H:%M:%S', date)
                m: Messages = Messages(user.get_id_user(), self._name_workspace, channel_name, user.get_name_user(),
                                       text_json, str_date)
                channel.add_message_user(m)
            index = index + 1
        self._channels[channel_name] = channel
