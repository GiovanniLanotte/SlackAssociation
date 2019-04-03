#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 13:51:07 2018
@author: giovanni
"""


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
