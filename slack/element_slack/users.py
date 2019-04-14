from slack.element_slack.messages import Messages


class Users:
    def __init__(self, name, id_user):
        self._sender = name
        self._messages = set()
        self._id_user = id_user
        self._mention_messages = set()

    def get_name_user(self):
        return self._sender

    def add_message(self, message: Messages):
        self._messages.add(message)

    def add_mention(self, message: Messages):
        self._mention_messages.add(message)

    def show_messages(self):
        return self._messages

    def mention_user(self, name_login):
        if name_login in self._mention_messages:
            cont = 0
            for message in self._messages:
                for mention in message.get_mentions():
                    if mention == name_login:
                        cont = cont + 1
            return cont
        else:
            return 0

    def show_mention_messages(self):
        return self._mention_messages

    def len_messages(self):
        return len(self._messages)

    def len_all_mentions(self):
        return len(self._mention_messages)

    def len_mentions(self):
        len_element = 0
        for message in self._mention_messages:
            if len(message.get_mentions()) != 0:
                len_element = len_element + 1
        return len_element

    def get_channels(self):
        channels = []
        for message in self._messages:
            channels.append(message.get_channel_name())
        return set(channels)

    def get_team_name(self):
        teamName = []
        for message in self._messages:
            teamName.append(message.get_team_name())
        return set(teamName)

    def get_id_user(self):
        return self._id_user

    def __eq__(self, other):
        if type(other) is Users:
            return self._sender == other.sender
        else:
            return False
