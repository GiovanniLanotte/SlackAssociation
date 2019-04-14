import csv
from organization_github.element_github.issues_comments import IssuesComments
from organization_github.element_github.pull_request import PullRequest
from organization_github.element_github.pull_request_comments import PullRequestComments
from organization_github.element_github.issues import Issues
from slack.element_slack.channels import Channels
from slack.element_slack.messages import Messages
from associations.associations import Associations
import time
import datetime


class UrlMessagesSlack:

    def __init__(self, association: Associations):
        self._channel: Channels = association.get_channel()
        self._repository = association.get_repository()
        self._organization = association.get_name_organization()
        self._name_file_issue = association.get_name_file_issue()
        self._name_file_comments_issue = association.get_name_file_comments_issue()
        self._name_file_pull_request = association.get_name_file_pull_request()
        self._name_file_comments_pull_request = association.get_name_file_comments_pull_request()
        self._path = 'message url ' + association.get_name_organization()
        self._messages_github = self._channel.get_messages_github(self._name_file_issue, self._name_file_comments_issue,
                                                                  self._name_file_pull_request,
                                                                  self._name_file_comments_pull_request)

    def generic_url_github(self):
        name_file = self._path + '/messages url github ' + self._channel.get_name_channel() + ' ' + self._organization \
                    + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('Sender', 'channel', 'text', 'url_html', 'is issue', 'is comment\'s issue',
                             'is pull request', 'is comment\'s pull request', 'issue or pull another repository',
                             'is other issue or pull of another organization', 'url not found'))
            for message_github in self._messages_github:
                message: Messages = message_github[0]
                github = message_github[1]

                if github is not None:
                    url: str = ''
                    if isinstance(github, Issues):
                        url = github.get_html_url()
                    elif isinstance(github, PullRequest):
                        url = github.get_html_url()
                    elif isinstance(github, IssuesComments):
                        url = github.get_html_url()
                    elif isinstance(github, PullRequestComments):
                        url = github.get_html_url()
                    elif isinstance(github, str):
                        url = github
                    if url.find(
                            'https://github.com/' + self._organization + '/' + self._repository.get_repository_name()
                            + '/') != -1:
                        writer.writerow(
                            (message.get_sender(), message.get_channel_name(), message.get_message(), url,
                             isinstance(github, Issues), isinstance(github, IssuesComments),
                             isinstance(github, PullRequest), isinstance(github, PullRequestComments),
                             False, False, isinstance(github, str)))
                    elif url.find('https://github.com/' + self._organization + '/') != -1:
                        writer.writerow(
                            (message.get_sender(), message.get_channel_name(), message.get_message(), url,
                             False, False, False, False, True, False, False))
                    else:
                        writer.writerow((message.get_sender(), message.get_channel_name(), message.get_message(), url,
                                         isinstance(github, Issues), isinstance(github, IssuesComments),
                                         isinstance(github, PullRequest), isinstance(github, PullRequestComments),
                                         False, True, False))
        finally:
            file.close()

    def issue_open_in_this_repository(self):
        name_file = self._path + '/messages url issues open in this repository ' + self._channel.get_name_channel() + \
                    ' ' + self._repository.get_repository_name() + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('Sender', 'channel', 'text', 'url_html'))
            for message_github in self._messages_github:
                message: Messages = message_github[0]
                github = message_github[1]
                if github is not None:
                    if isinstance(github, Issues):
                        url = github.get_html_url()
                        if github.get_state() == 'open' and url.find(
                                'https://github.com/' + self._organization + '/' +
                                self._repository.get_repository_name() + '/') != -1:
                            writer.writerow(
                                (message.get_sender(), message.get_channel_name(), message.get_message(), url))

        finally:
            file.close()

    def issue_open_not_in_this_repository(self):
        name_file = self._path + '/messages url issues open not in this repository ' + \
                    self._channel.get_name_channel() + ' ' + self._repository.get_repository_name() + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('Sender', 'channel', 'repository', 'url_html'))
            for message_github in self._messages_github:
                message: Messages = message_github[0]
                github = message_github[1]
                if github is not None:
                    if isinstance(github, Issues):
                        url = github.get_html_url()
                        if github.get_state() == 'open' and url.find(
                                'https://github.com/' + self._organization + '/'
                                + self._repository.get_repository_name() + '/') == -1:
                            writer.writerow(
                                (message.get_sender(), message.get_channel_name(), github.get_name_repository(), url))

        finally:
            file.close()

    def issue_closed_in_this_repository(self):
        name_file = self._path + '/messages url issues closed in this repository ' + self._channel.get_name_channel() \
                    + ' ' + self._repository.get_repository_name() + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('Sender', 'channel', 'text', 'url_html'))
            for message_github in self._messages_github:
                message: Messages = message_github[0]
                github = message_github[1]
                if github is not None:
                    if isinstance(github, Issues):
                        url = github.get_html_url()
                        if github.get_state() == 'closed' and url.find(
                                'https://github.com/' + self._organization + '/'
                                + self._repository.get_repository_name() + '/') != -1:
                            writer.writerow(
                                (message.get_sender(), message.get_channel_name(), message.get_message(), url))
        finally:
            file.close()

    def issue_closed_not_in_this_repository(self):
        name_file = self._path + '/messages url issues closed not in this repository ' \
                    + self._channel.get_name_channel() + ' ' + self._repository.get_repository_name() + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('Sender', 'channel', 'repository', 'url_html'))
            for message_github in self._messages_github:
                message: Messages = message_github[0]
                github = message_github[1]
                if github is not None:
                    if isinstance(github, Issues):
                        url = github.get_html_url()
                        if github.get_state() == 'closed' and url.find(
                                'https://github.com/' + self._organization + '/' +
                                self._repository.get_repository_name() + '/') == -1:
                            writer.writerow(
                                (message.get_sender(), message.get_channel_name(), github.get_name_repository(), url))
        finally:
            file.close()

    def pull_open_in_this_repository(self):
        name_file = self._path + '/messages url pull request open in this repository ' \
                    + self._channel.get_name_channel() + ' ' + self._repository.get_repository_name() + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('Sender', 'channel', 'text', 'date', 'url_html', 'is merged'))
            for message_github in self._messages_github:
                message: Messages = message_github[0]
                github = message_github[1]
                if github is not None:
                    if isinstance(github, PullRequest):
                        url = github.get_html_url()
                        if github.get_state() == 'open' and url.find(
                                'https://github.com/' + self._organization + '/' +
                                self._repository.get_repository_name() + '/') != -1:
                            writer.writerow((message.get_sender(), message.get_channel_name(), message.get_message(),
                                             message.get_time(),
                                             url, github.is_merged()))
        finally:
            file.close()

    def pull_open_not_in_this_repository(self):
        name_file = self._path + '/messages url pull request open not in this repository ' \
                    + self._channel.get_name_channel() + ' ' + self._repository.get_repository_name() + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('Sender', 'channel', 'repository', 'url_html'))
            for message_github in self._messages_github:
                message: Messages = message_github[0]
                github = message_github[1]
                if github is not None:
                    if isinstance(github, PullRequest):
                        url = github.get_html_url()
                        if github.get_state() == 'open' and url.find(
                                'https://github.com/' + self._organization + '/' +
                                self._repository.get_repository_name() + '/') == -1:
                            writer.writerow(
                                (message.get_sender(), message.get_channel_name(), github.get_name_repository(), url))
        finally:
            file.close()

    def pull_closed_in_this_repository(self):
        name_file = self._path + '/messages url pull request closed in this repository ' + \
                    self._channel.get_name_channel() + ' ' + self._repository.get_repository_name() + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('Sender', 'channel', 'text', 'date', 'url_html', 'is merged'))
            for message_github in self._messages_github:
                message: Messages = message_github[0]
                github = message_github[1]
                if github is not None:
                    if isinstance(github, PullRequest):
                        url = github.get_html_url()
                        if github.get_state() == 'closed' and url.find(
                                'https://github.com/' + self._organization + '/' +
                                self._repository.get_repository_name() + '/') != -1:
                            writer.writerow((message.get_sender(), message.get_channel_name(), message.get_message(),
                                             message.get_time(),
                                             url, github.is_merged()))
        finally:
            file.close()

    def pull_closed_not_in_this_repository(self):
        name_file = self._path + '/messages url pull request closed not in this repository ' +\
                    self._channel.get_name_channel() + ' ' + self._repository.get_repository_name() + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('Sender', 'channel', 'repository', 'url_html', 'is merged'))
            for message_github in self._messages_github:
                message: Messages = message_github[0]
                github = message_github[1]
                if github is not None:
                    if isinstance(github, PullRequest):
                        url = github.get_html_url()
                        if github.get_state() == 'closed' and url.find(
                                'https://github.com/' + self._organization + '/' +
                                self._repository.get_repository_name() + '/') == -1:
                            writer.writerow((message.get_sender(), message.get_channel_name(),
                                             github.get_name_repository(), url, github.is_merged()))
        finally:
            file.close()

    def dif_message_date(self):
        name_file = self._path + '/date difference pull request closed in this repository ' + \
                    self._channel.get_name_channel() + ' ' + self._repository.get_repository_name() + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('Sender', 'channel', 'text', 'url_html', 'is merged', 'date message', 'date pull request',
                             'date closed pull request', 'date merged',
                             'difference date massage and pull request closed',
                             'difference date open pull request and pull request closed'))
            for message_github in self._messages_github:
                message: Messages = message_github[0]
                github = message_github[1]
                if github is not None:
                    if isinstance(github, PullRequest):
                        github: PullRequest
                        url = github.get_html_url()
                        if github.get_state() == 'closed' and url.find(
                                'https://github.com/' + self._organization + '/'
                                + self._repository.get_repository_name() + '/') != -1:
                            ris1 = self.dif_data(github.get_closed_at(), message.get_time())
                            ris2 = self.dif_data(github.get_closed_at(), github.get_created_at())
                            writer.writerow((message.get_sender(), message.get_channel_name(), message.get_message(),
                                             url, github.is_merged(), message.get_time(), github.get_created_at(),
                                             github.get_closed_at(), github.get_merged_at(), ris1, ris2))
        finally:
            file.close()

    @staticmethod
    def dif_data(date1, date2):
        aa = time.strptime(date1, '%Y-%m-%d %H:%M:%S')
        aaa = datetime.datetime.fromtimestamp(time.mktime(aa))
        bb = time.strptime(date2, '%Y-%m-%d %H:%M:%S')
        bbb = datetime.datetime.fromtimestamp(time.mktime(bb))
        return aaa - bbb
