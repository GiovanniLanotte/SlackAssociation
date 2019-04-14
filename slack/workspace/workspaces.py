#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 13:51:07 2018
@author: giovanni
"""
import csv
from slack.element_slack.channels import Channels


class Workspaces:

    def __init__(self, workspace_name):
        self._name_workspace = workspace_name
        self._channels: dict = dict()

    def get_workspace(self):
        return self._name_workspace

    def get_channel(self, name_channel):
        return self._channels.get(name_channel)

    def get_names_channel(self):
        return self._channels.keys()

    def get_csv_channel_organization(self):
        name_file = 'channels ' + self._name_workspace + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(
                ('name', "# users"))
            for key in self._channels:
                channel:Channels = self._channels.get(key)
                writer.writerow((channel.get_name_channel(), len(channel.get_users())))
        finally:
            file.close()
