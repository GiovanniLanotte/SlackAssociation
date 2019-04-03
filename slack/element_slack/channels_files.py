from slack.element_slack.channels import Channels
from slack.element_slack.users import Users


class ChannelsFiles(Channels):

    def __init__(self, name_channel):
        super().__init__(name_channel)

    def search_for_users_mentioned(self):
        self.all_messages = 0
        for key in self._users:
            user: Users = self._users.get(key)
            self.all_messages = self.all_messages + user.len_messages()
            for message in user.show_messages():
                mentions: list = message.get_mentions()
                for mention in mentions:
                    if self.get_key_users(mention) is None:
                        n = -1
                        index_a = 0
                        index_b = index_a + 1
                        user_name_mention: list = list()
                        while index_b < len(mention):
                            name_mention = mention[index_a: index_b + 1]
                            index_b = index_b + 1
                            if self.get_key_users(name_mention) is not None:
                                user_name_mention.append(name_mention)
                                n = n + 1
                        if len(user_name_mention) != 0:
                            user_mention = self.get_key_users(user_name_mention[n])
                            user_mention.add_mention(message)

                    else:
                        user_mention = self._users.get(mention)
                        user_mention.add_mention(message)

