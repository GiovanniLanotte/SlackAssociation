#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 13:22:38 2018

@author: giovanni
"""


class Messages:
    """definire il costruttore"""

    def __init__(self, index, teamName: str, channelName: str, sender: str, message: str, time: str):
        self.id: str = index
        self.teamName: str = teamName
        self.channelName: str = channelName
        self.sender: str = sender
        self.message: str = message
        self.time: str = time
        self.mentions: list = list()
        self.__search_mentions()

    """serve per stampare gli elementi"""

    def __repr__(self):
        return "ID:{} teamName:{} channelName:{} sender:{} message:{} time:{}".format(self.id, self.teamName,
                                                                                      self.channelName, self.sender,
                                                                                      self.message, self.time)

    def __str__(self):
        return "ID:" + self.id + " teamName:" + self.teamName + " channelName:" + self.channelName + " sender:" + \
               self.sender + " messagge:" + self.message + " time:" + self.time

    def get_id(self):
        return self.id

    def get_team_name(self):
        return self.teamName

    def get_channel_name(self):
        return self.channelName

    def get_sender(self):
        return self.sender

    def get_message(self):
        return self.message

    def get_time(self):
        return self.time

    def get_mentions(self):
        return self.mentions

    def __eq__(self, other):
        if isinstance(other, Messages):
            return self.id == other.id and self.teamName == other.teamName and self.channelName == other.channelName and \
                   self.sender == other.sender and self.message == other.message and self.time == other.time
        else:
            return False
    def __hash__(self):
        return self.time.__hash__() + self.message.__hash__() + self.get_channel_name().__hash__()

    def __search_mentions(self):
        message_index = 0
        while message_index < self.message.__len__():
            char = self.message[message_index]
            if char == '@':
                element_index = message_index + 2
                sub_string: str = str()
                while element_index < self.message.__len__() and self.message[element_index] != ' ' \
                        and self.message[element_index] != '\"':
                    sub_string: str = self.message[message_index + 1:element_index + 1]
                    element_index = element_index + 1
                if sub_string != "":
                    self.mentions.append(sub_string)
            message_index = message_index + 1


def main():
    mex = Messages("", "kubernetes", "kubernetes-users", "roffe", """and a login app i wrote""", "Oct 25, 2017 05:41")
    print(mex)


if __name__ == "__main__":
    main()
