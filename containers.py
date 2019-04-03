from GitHub.organizations import Organizations
from pathlib import Path
from GitHub.element_github.pull_request import PullRequest
from GitHub.repositories import Repositories
from associations.associations import Associations
from slack.element_slack.channels import Channels
from slack.element_slack.messages import Messages
from slack.element_slack.users import Users
from slack.urlmessagesslack import UrlMessagesSlack
from slack.workspace.workspace_slackarchive import WorkspacesSlackArchive
from slack.workspace.workspaces_csv import WorkspacesCSV
from slack.workspace.workspaces_raw import WorkspacesRaw
import csv
import threading
import os


class Containers:

    def __init__(self, ):
        self._associations: list = list()

    def add_association(self, name_organization, path, tokens):
        print('creazione classe Organization')
        organization: Organizations = Organizations(name_organization, tokens)
        print('creazione dei file repository')
        organization.get_scv_repositories()
        organization.get_average_percentage_file_programming()
        organization.get_average_percentage_file_programming_and_repositories_merged()
        organization.get_average_percentage_file_programming_and_repositories_merged_and_use_tracking_issue()
        organization.get_average_percentage_file_programming_and_repositories_merged_and_use_tracking_issue_and_more_average_contributors()
        organization.get_average_percentage_file_programming_and_repositories_merged_and_use_tracking_issue_and_more_average_contributors_and_more_average_commits()
        organization.get_average_percentage_file_programming_and_repositories_merged_and_use_tracking_issue_and_more_average_contributors_and_more_average_commits_and_last_update_in_2018()
        print('conclusa la creazione dei file repository')
        p = Path(path)
        workspace = None
        if p.is_file() and p.suffix == ".csv":
            workspace = WorkspacesCSV(path)
        else:
            try:
                workspace = WorkspacesSlackArchive(path, name_organization)
            except FileNotFoundError:
                print("sono qui.........")
                workspace = WorkspacesRaw(path, name_organization)
        if workspace is not None:
            for name_channel in workspace.get_names_channel():
                if organization.contain_association(name_channel):
                    repositories = organization.get_association(name_channel)
                    workspace.get_channel(name_channel)
                    for repository in repositories:
                        association: Associations = Associations(repository, workspace.get_channel(name_channel),
                                                                 name_organization, organization.get_name_file_issue(),
                                                                 organization.get_name_file_comments_issue(),
                                                                 organization.get_name_file_pull_request(),
                                                                 organization.get_name_file_comments_pull_request())
                        self._associations.append(association)

    def messages_for_channel(self):
        for association in self._associations:
            association: Associations
            channel: Channels = association.get_channel()
            file = open(
                "messages for channel " + channel.get_name_channel() + " of " + association.get_name_organization() + ".csv",
                "wt")
            try:
                writer: csv.DictWriter = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter='|')
                writer.writerow(("Workspace", "Channel", "Id", "Sender", "text", "time", "mention"))
                name_workspace = association.get_name_organization()
                senders = channel.get_users()
                for key in senders:
                    sender: Users = senders.get(key)
                    messages = sender.show_messages()
                    if messages is not None and len(messages) != 0:
                        for message in messages:
                            mentions: str = ""
                            for mention in message.get_mentions():
                                mentions = mentions + ", " + str(mention)
                            writer.writerow((name_workspace, channel.get_name_channel(), sender.get_id_user(),
                                             sender.get_name_user(), message.get_message(),
                                             message.get_time(), mentions))
            finally:
                file.close()

    def print_organization(self):
        for association in self._associations:
            association: Associations
            repository: Repositories = association.get_repository()
            channel: Channels = association.get_channel()
            print('channel: {} repository: {}'.format(channel.get_name_channel(), repository.get_repository_name()))

    def pull_request_on_message_slack(self):
        list_thread = list()
        for association in self._associations:
            channel: Channels = association.get_channel()
            repository: Repositories = association.get_repository()
            print('channel: {} repository: {}'.format(channel.get_name_channel(), repository.get_repository_name()))
            thread = threading.Thread(target=self._create_file_pull, args=(channel, repository))
            thread.start()
            list_thread.append(thread)
            print("sto eseguendo")
        for thread in list_thread:
            thread.join()

    def _create_file_pull(self, channel, repository):
        channel: Channels
        repository: Repositories
        file = open(
            'pull request url in message in ' + channel.get_name_channel() + ' ' +
            repository.get_repository_name() + '.csv', 'w')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('pr url', 'merged', 'count'))
            pulls = repository.get_pulls()
            for pull in pulls:
                count_pr_url = 0
                pull: PullRequest
                if pull.get_state() == 'closed':
                    users = channel.get_users()
                    for user_key in users:
                        user = users.get(user_key)
                        for message in user.show_messages():
                            message: Messages
                            text = message.get_message()
                            if text.find(pull.get_html_url()) != -1:
                                length = len(pull.get_html_url()) + text.find(pull.get_html_url())
                                if len(text) > length and (
                                        text[length] == '>' or text[length] == ' '):
                                    count_pr_url = count_pr_url + 1
                                elif len(text) == length:
                                    count_pr_url = count_pr_url + 1
                    writer.writerow((pull.get_html_url(), pull.is_merged(), count_pr_url))
        finally:
            file.close()

    def get_len_message_for_channel(self):
        file = open(
            'number of messages of channel.csv', 'w')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('organization', 'channel slack', '# messages'))
            for association in self._associations:
                channel: Channels = association.get_channel()
                len_message_channel = 0
                users = channel.get_users()
                for user_key in users:
                    user: Users = users.get(user_key)
                    len_message_channel = len_message_channel + user.len_messages()
                writer.writerow((association.get_name_organization(), channel.get_name_channel(), len_message_channel))
        finally:
            file.close()

    def messages_slack_url_github(self):
        for association in self._associations:
            association: Associations
            channel: Channels = association.get_channel()
            repository: Repositories = association.get_repository()
            if repository.get_repository_name() == 'kubernetes' and channel.get_name_channel() == 'kubernetes-users':
                channel: Channels = association.get_channel()
                path = 'message url ' + association.get_name_organization()
                if os.path.isdir(path) is not True:
                    os.makedirs(path)
                print('channel: {} repository: {}'.format(channel.get_name_channel(), repository.get_repository_name()))
                url_message_slack = UrlMessagesSlack(association)
                url_message_slack.generic_url_github()
                url_message_slack.issue_open_in_this_repository()
                url_message_slack.issue_open_not_in_this_repository()
                url_message_slack.issue_closed_in_this_repository()
                url_message_slack.issue_closed_not_in_this_repository()
                url_message_slack.pull_open_in_this_repository()
                url_message_slack.pull_open_not_in_this_repository()
                url_message_slack.pull_closed_in_this_repository()
                url_message_slack.pull_closed_not_in_this_repository()
                url_message_slack.dif_message_date()

    def correspondence_channel_to_archive(self):
        name_file = 'correspondence channel to archive in the workspace.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(
                ('Name Channel', 'Name Repository', 'url html', 'percentage programming file',
                 'has pull request merged',
                 'use issue for tracking',
                 '# contributors', '# commits', 'last update at least in 2018'))
            for association in self._associations:
                channel: Channels = association.get_channel()
                repository: Repositories = association.get_repository()
                writer.writerow((channel.get_name_channel(),
                                 repository.get_repository_name(), repository.get_url_html(),
                                 repository.get_percentage_programming_files(),
                                 repository.has_pull_request_merged(), repository.use_issue_for_tracking(),
                                 len(repository.get_contributors()), repository.get_number_of_commits(),
                                 repository.last_update_at_least_in_2018()))
        finally:
            file.close()
