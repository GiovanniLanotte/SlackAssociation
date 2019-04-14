from slack.element_slack.messages import Messages
from slack.element_slack.users import Users
import abc
from slack.messagesusers import MessagesUsers


class Channels(abc.ABC):

    def __init__(self, name):
        self.__name_channel = name
        self._users: dict = dict()

    def get_name_channel(self):
        return self.__name_channel

    def get_key_users(self, id_user):
        for key in self._users:
            user = self._users.get(key)
            if user.get_id_user() == id_user:
                return user
        return None

    def get_users(self):
        return self._users

    def get_message_for_users(self, name_users):
        user: Users = self._users.get(name_users)
        if user is not None:
            messages = user.show_messages()
            return messages
        return None

    def is_member(self, id_user):
        return id_user in self._users

    def add_message_user(self, message: Messages):
        username = message.get_sender()
        user: Users = self._users.get(username)
        if user is None:
            user = Users(username, message.get_id())
            user.add_message(message)
            self._users[username] = user
        else:
            user.add_message(message)

    @abc.abstractmethod
    def search_for_users_mentioned(self):
        pass

    def get_messages_github(self, name_file_issue, name_file_comments_issue, name_file_pull_request,
                            name_file_comments_pull_request):
        thread_list: list = list()
        messages_list: set = set()
        for key in self._users:
            user_message: Users = self._users.get(key)
            text_set: set = set()
            for message in user_message.show_messages():
                text: str = message.get_message()
                index_text = 0
                while index_text < len(text):
                    if text.find('https://github.com', index_text) != -1 and (
                            text.find('/issues/', index_text) != -1):
                        index: int = text.find('https://github.com', index_text)
                        url = ''
                        num_slash = 0
                        while index < len(text) and num_slash < 7 and text[index] != ' ' and text[index] != '>' and \
                                text[index] != '<' and text[index] != '\'':
                            if text[index] == '/':
                                num_slash = num_slash + 1
                            if num_slash == 6:
                                url = url + text[index]
                                index = index + 1
                                while index < len(text) and (
                                        text[index] == '0' or text[index] == '1' or text[index] == '2' or
                                        text[index] == '3' or text[index] == '4' or text[index] == '5' or
                                        text[index] == '6' or text[index] == '7' or text[index] == '8' or
                                        text[index] == '9' or text[index] == '#' or text[index] == 'i' or
                                        text[index] == 's' or text[index] == 'u' or text[index] == 'e' or
                                        text[index] == 'c' or text[index] == 'o' or text[index] == 'm' or
                                        text[index] == 'e' or text[index] == 'n' or text[index] == 't' or
                                        text[index] == '-'):
                                    url = url + text[index]
                                    index = index + 1
                                break
                            else:
                                url = url + text[index]
                                index = index + 1
                        if num_slash == 6 and (url.find('/issues/') != -1):
                            message_user = MessagesUsers(self._users, text, message, url, name_file_issue,
                                                         name_file_comments_issue, name_file_pull_request,
                                                         name_file_comments_pull_request)
                            text_set.add(text)
                            thread_list.append(message_user)
                        index_text = index
                    else:
                        index_text = index_text + 1
                text: str = message.get_message()
                index_text = 0
                while index_text < len(text):
                    if text.find('https://github.com', index_text) != -1 and (
                            text.find('/pull/', index_text) != -1):
                        index: int = text.find('https://github.com', index_text)
                        url = ''
                        num_slash = 0
                        while index < len(text) and num_slash < 7 and text[index] != ' ' and text[index] != '>' and \
                                text[index] != '<' and text[index] != '\'':
                            if text[index] == '/':
                                num_slash = num_slash + 1
                            if num_slash == 6:
                                url = url + text[index]
                                index = index + 1
                                # discussion_r124452764
                                while index < len(text) and (
                                        text[index] == '0' or text[index] == '1' or text[index] == '2' or
                                        text[index] == '3' or text[index] == '4' or text[index] == '5' or
                                        text[index] == '6' or text[index] == '7' or text[index] == '8' or
                                        text[index] == '9' or text[index] == '#' or text[index] == 'd' or
                                        text[index] == 'i' or text[index] == 's' or text[index] == 'c' or
                                        text[index] == 'u' or text[index] == 'o' or text[index] == 'n' or
                                        text[index] == '_' or text[index] == 'r' or
                                        text[index] == '#' or text[index] == 'i' or text[index] == 's' or
                                        text[index] == 'u' or text[index] == 'e' or text[index] == 'c' or
                                        text[index] == 'o' or text[index] == 'm' or text[index] == 'e' or
                                        text[index] == 'n' or text[index] == 't' or text[index] == '-'):
                                    url = url + text[index]
                                    index = index + 1
                                break
                            else:
                                url = url + text[index]
                                index = index + 1
                        if num_slash == 6 and url.find('/pull/') != -1:
                            index_files = index + len('/files')
                            index_commits = index + len('/commits')
                            sub_text_files = text[index_text:index_files]
                            sub_text_commits = text[index_text:index_commits]
                            if sub_text_files.find('/files') == -1 and sub_text_commits.find('/commits') == -1:
                                message_user = MessagesUsers(self._users, text, message, url, name_file_issue,
                                                             name_file_comments_issue, name_file_pull_request,
                                                             name_file_comments_pull_request)
                                text_set.add(text)
                                thread_list.append(message_user)
                        index_text = index
                    else:
                        index_text = index_text + 1
        index = 0
        index_show = 0
        threads = list()
        for thread in thread_list:
            index = index + 1
            if index != 10:
                thread.start()
                threads.append(thread)
            else:
                for thread_join in threads:
                    ris = thread_join.join()
                    messages_list.add(ris)
                threads = list()
                thread.start()
                threads.append(thread)
                index = 0
            index_show = index_show + 1
        for thread_join in threads:
            ris = thread_join.join()
            messages_list.add(ris)
        return messages_list
