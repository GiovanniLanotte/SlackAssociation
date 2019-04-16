from organization_github.organizations import Organizations
from pathlib import Path
from organization_github.repositories import Repositories
from associations.associations import Associations
from slack.element_slack.channels import Channels
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
        directory = 'issue&pull ' + name_organization
        organization: Organizations = Organizations(directory, name_organization, tokens)
        organization.get_scv_repositories()
        organization.get_first_filter()
        organization.get_second_filter()
        organization.get_third_filter()
        organization.get_fourth_filter()
        organization.get_fifth_filter()
        organization.get_sixth_filter()
        p = Path(path)
        workspace = None
        if p.is_file() and p.suffix == ".csv":
            workspace = WorkspacesCSV(path)
        else:
            try:
                workspace = WorkspacesSlackArchive(path, name_organization)
            except FileNotFoundError:
                workspace = WorkspacesRaw(path, name_organization)
        if workspace is not None:
            workspace.get_csv_channel_organization()
            for name_channel in workspace.get_names_channel():
                if organization.contain_association(name_channel):
                    repositories = organization.get_association(name_channel)
                    workspace.get_channel(name_channel)
                    for repository in repositories:
                        association: Associations = Associations(directory, repository,
                                                                 workspace.get_channel(name_channel),
                                                                 name_organization, organization.get_name_file_issue(),
                                                                 organization.get_name_file_comments_issue(),
                                                                 organization.get_name_file_pull_request(),
                                                                 organization.get_name_file_comments_pull_request())
                        self._associations.append(association)

    def messages_for_channel(self):
        for association in self._associations:
            channel: Channels = association.get_channel()
            file = open(
                "messages for channel " + channel.get_name_channel() + " of " +
                association.get_name_organization() + ".csv",
                "wt")
            try:
                writer: csv.DictWriter = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
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

    def correspondence_channel_to_archive(self, organization):
        name_file = 'correspondence channel to archive in ' + organization + '.csv'
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

    def pull_request_on_message_slack(self):
        list_thread = list()
        for association in self._associations:
            channel: Channels = association.get_channel()
            repository: Repositories = association.get_repository()
            thread = threading.Thread(target=self._create_file_pull, args=(channel, repository))
            thread.start()
            list_thread.append(thread)
        for thread in list_thread:
            thread.join()

    @staticmethod
    def _create_file_pull(channel, repository):
        file = open(
            'pull request url in message in ' + channel.get_name_channel() + ' ' +
            repository.get_repository_name() + '.csv', 'w')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(('pr url', 'merged', 'count'))
            pulls = repository.get_pulls()
            for pull in pulls:
                count_pr_url = 0
                if pull.get_state() == 'closed':
                    users = channel.get_users()
                    for user_key in users:
                        user = users.get(user_key)
                        for message in user.show_messages():
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

    def get_len_message_for_channel(self, organization):
        file = open(
            'number of messages ' + organization + '.csv', 'w')
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
            path = 'message url ' + association.get_name_organization()
            if os.path.isdir(path) is not True:
                os.makedirs(path)
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


