import csv
import os
import sys
from organization_github.element_github.pull_request_comments import PullRequestComments


class PullRequest:
    def __init__(self, name_repository, url, url_html, user_login, title, body, assignees, commits, created_at,
                 updated_at, closed_at, merged, merged_at, merged_by, mergeable_state, mergeable, state):
        self._name_repository = name_repository
        self._url = url
        self._url_html = url_html
        self._user_login = user_login
        self._title = title
        self._body = body
        self._assignees: list = assignees
        self._commits = commits
        self._creates_at = created_at
        self._updates_at = updated_at
        self._closed_at = closed_at
        self._merged = merged
        self.__merged_at = merged_at
        self.__merged_by = merged_by
        self.__mergeable_state = mergeable_state
        self.__mergeable = mergeable
        self.__state = state
        self.__list_comments: list = list()
        number = url_html
        len_url = len(self._url_html)
        index = 0
        while number.find('/') != -1:
            number = url_html[index:len_url]
            index = index + 1
        self.__number = int(number)

    def get_name_repository(self):
        return self._name_repository

    def get_url(self):
        return self._url

    def get_html_url(self):
        return self._url_html

    def get_user_created(self):
        return self._user_login

    def get_title(self):
        return self._title

    def get_body(self):
        return self._body

    def get_assignees(self):
        return self._assignees

    def get_commits(self):
        return self._commits

    def get_created_at(self):
        return self._creates_at

    def get_updated_at(self):
        return self._updates_at

    def is_merged(self):
        return self._merged

    def get_merged_at(self):
        return self.__merged_at

    def get_merged_by(self):
        return self.__merged_by

    def get_closed_at(self):
        return self._closed_at

    def get_mergeable_state(self):
        return self.__mergeable_state

    def get_mergeable(self):
        return self.__mergeable

    def get_state(self):
        return self.__state

    def add_comment(self, comment):
        self.__list_comments.append(comment)

    def len_comments(self):
        return len(self.__list_comments)

    def get_comment_index(self, index):
        return self.__list_comments[index]

    @classmethod
    def load_pull_request_without_comments(cls, name_file_pull_request, url):
        file_pull_request = open(name_file_pull_request, 'rt')
        try:
            csv.field_size_limit(sys.maxsize)
            reader_pull_request: csv.DictReader = csv.reader(x.replace('\0', '') for x in file_pull_request)
            index_pull_request = 0
            for row_pull_request in reader_pull_request:
                if index_pull_request == 0:
                    index_pull_request = 1
                else:
                    pull_request = PullRequest(row_pull_request[0], row_pull_request[1], row_pull_request[2],
                                               row_pull_request[3], row_pull_request[4], row_pull_request[5],
                                               row_pull_request[6], row_pull_request[7], row_pull_request[8],
                                               row_pull_request[9], row_pull_request[10], row_pull_request[11],
                                               row_pull_request[12], row_pull_request[13], row_pull_request[14],
                                               row_pull_request[15], row_pull_request[16])
                    if pull_request.get_html_url() == url:
                        return pull_request
        finally:
            file_pull_request.close()
        return None

    @classmethod
    def load_pull_request(cls, name_file_pull_request, name_file_comments_pull_request, url):
        file_pull_request = open(name_file_pull_request, 'rt')
        try:
            csv.field_size_limit(sys.maxsize)
            reader_pull_request: csv.DictReader = csv.reader(x.replace('\0', '') for x in file_pull_request)
            index_pull_request = 0
            for row_pull_request in reader_pull_request:
                if index_pull_request == 0:
                    index_pull_request = 1
                else:
                    pull_request = PullRequest(row_pull_request[0], row_pull_request[1], row_pull_request[2],
                                               row_pull_request[3], row_pull_request[4], row_pull_request[5],
                                               row_pull_request[6], row_pull_request[7], row_pull_request[8],
                                               row_pull_request[9], row_pull_request[10], row_pull_request[11],
                                               row_pull_request[12], row_pull_request[13], row_pull_request[14],
                                               row_pull_request[15], row_pull_request[16])
                    if pull_request.get_html_url() == url:
                        pull_request = PullRequestComments.read_comment_pull_request(name_file_comments_pull_request,
                                                                                     pull_request)
                        return pull_request
        finally:
            file_pull_request.close()
        return None

    @classmethod
    def load_pull_request_of_repository(cls, repo_name, name_file_pull_request, name_file_comments_pull_request):
        list_pull: list = list()
        file_pull_request = open(name_file_pull_request, 'rt')
        try:
            csv.field_size_limit(sys.maxsize)
            reader_pull_request: csv.DictReader = csv.reader(x.replace('\0', '') for x in file_pull_request)
            index_pull_request = 0
            for row_pull_request in reader_pull_request:
                if index_pull_request == 0:
                    index_pull_request = 1
                else:
                    pull_request = PullRequest(row_pull_request[0], row_pull_request[1], row_pull_request[2],
                                               row_pull_request[3], row_pull_request[4], row_pull_request[5],
                                               row_pull_request[6], row_pull_request[7], row_pull_request[8],
                                               row_pull_request[9], row_pull_request[10], row_pull_request[11],
                                               row_pull_request[12], row_pull_request[13], row_pull_request[14],
                                               row_pull_request[15], row_pull_request[16])
                    if pull_request.get_name_repository() == repo_name:
                        pull_request = PullRequestComments.read_comment_pull_request(name_file_comments_pull_request,
                                                                                     pull_request)
                        list_pull.append(pull_request)
        finally:
            file_pull_request.close()
        return list_pull

    def load_comment_pull_request(self, name_file_comments_pull_request):
        pull_request: PullRequest = PullRequestComments.read_comment_pull_request(name_file_comments_pull_request, self)
        index = 0
        while index < pull_request.len_comments():
            self.add_comment(pull_request.get_comment_index(index))

    def write_pull_request(self, name_pull_request, name_comment_pull_request):
        if not (os.path.exists(name_pull_request)):
            file = open(name_pull_request, 'w')
            try:
                write_csv: csv.DictWriter = csv.writer(file)
                write_csv.writerow(('name repository', 'url', 'url html', 'created by', 'title', 'body', 'assignees',
                                    '# commit', 'created at', 'updated at', 'closed at', 'is merged', 'merged at',
                                    'merged by', 'mergeable state', 'mergeable', 'state'))
            finally:
                file.close()
        file = open(name_pull_request, 'a')
        try:
            write_csv: csv.DictWriter = csv.writer(file)
            write_csv.writerow((self.get_name_repository(), self.get_url(), self.get_html_url(),
                                self.get_user_created(), self.get_title(), self.get_body(),
                                self.get_assignees(), self.get_commits(), self.get_created_at(), self.get_closed_at(),
                                self.get_updated_at(), self.is_merged(), self.get_merged_at(),
                                self.get_merged_by(), self.get_mergeable_state(), self.get_mergeable(),
                                self.get_state()))
        finally:
            file.close()
        index = 0
        while index < self.len_comments():
            comment: PullRequestComments = self.get_comment_index(index)
            comment.write_comment_pull_request(self, name_comment_pull_request)
            index = index + 1

    def __hash__(self):
        return self._url_html.__hash__()

    def get_num_pull(self):
        return self.__number
