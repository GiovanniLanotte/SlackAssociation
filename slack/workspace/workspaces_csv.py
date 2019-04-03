""""
Created on Wed Sep 19 13:51:07 2018
@author: giovanni
"""
from slack.element_slack.channels import Channels
from slack.element_slack.channels_csv import ChannelsCSV
from slack.element_slack.messages import Messages
import csv

from slack.workspace.workspaces import Workspaces


class WorkspacesCSV(Workspaces):

    def __init__(self, name_file):
        f = open(name_file, 'rt')
        name_workspace = str()
        try:
            reader = csv.reader(f)
            i = 0
            for row in reader:
                if i == 0:
                    i = 1
                else:
                    name_workspace = row[1]
                    break
        finally:
            f.close()
        super().__init__(name_workspace)
        self.__initialization_users(name_file)
        for key in self._channels:
            channel: Channels = self._channels.get(key)
            channel.search_for_users_mentioned()

    def __initialization_users(self, name_file: str):
        f = open(name_file, 'rt')
        try:
            reader = csv.reader(f)
            i = 0
            for row in reader:
                if i == 0:
                    i = 1
                else:
                    message = Messages(row[0], row[1], row[2], row[3], row[4], row[5])
                    channel_name = message.get_channel_name()
                    if self._channels.get(channel_name) is None:
                        channel = ChannelsCSV(channel_name)
                        channel.add_message_user(message)
                        self._channels[channel_name] = channel
                    else:
                        self._channels.get(channel_name).add_message_user(message)
        finally:
            f.close()
