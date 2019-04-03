import sys
import csv
import os
from GitHub.element_github.issue_comments import IssueComments


class Issues:
    def __init__(self, name_repository, user_login, html_url, url, title, body, state, pull_request, created_at,
                 updated_at):
        self.__name_repository = name_repository
        self.__id = id
        self.__user_login = user_login
        self.__html_url = html_url
        self.__url = url
        self.__title = title
        self.__body = body
        self.__state = state
        self.__pull_request = pull_request
        self.__created_at = created_at
        self.__updated_at = updated_at
        self.__list_comments: list = list()

    def get_name_repository(self):
        return self.__name_repository

    def get_creator(self):
        return self.__user_login

    def get_html_url(self):
        return self.__html_url

    def get_url(self):
        return self.__url

    def get_title(self):
        return self.__title

    def get_body(self):
        return self.__body

    def get_state(self):
        return self.__state

    def is_pull_request(self):
        return self.__pull_request is not None

    def get_pull_request(self):
        return self.__pull_request

    def get_created_at(self):
        return self.__created_at

    def get_updated_at(self):
        return self.__updated_at

    def add_comment(self, comment: IssueComments):
        self.__list_comments.append(comment)

    def len_comments(self):
        return len(self.__list_comments)

    def get_comment_index(self, index):
        return self.__list_comments[index]

    @classmethod
    def load_issues_without_comments(cls, name_file_issue, url):
        file = open(name_file_issue, "rt")
        try:
            csv.field_size_limit(sys.maxsize)
            reader_issue: csv.DictReader = csv.reader(x.replace('\0', '') for x in file)
            index_issue = 0
            for row_issue in reader_issue:
                if index_issue == 0:
                    index_issue = 1
                else:
                    issue = Issues(row_issue[0], row_issue[1], row_issue[2], row_issue[3], row_issue[4],
                                   row_issue[5], row_issue[6], row_issue[7], row_issue[8], row_issue[9])
                    if issue.get_html_url() == url:
                        return issue
        finally:
            file.close()
        return None

    @classmethod
    def load_issues(cls, name_file_issue, name_file_comments_issue, url):
        file = open(name_file_issue, "rt")
        try:
            csv.field_size_limit(sys.maxsize)
            reader_issue: csv.DictReader = csv.reader(x.replace('\0', '') for x in file)
            index_issue = 0
            for row_issue in reader_issue:
                if index_issue == 0:
                    index_issue = 1
                else:
                    issue = Issues(row_issue[0], row_issue[1], row_issue[2], row_issue[3], row_issue[4],
                                   row_issue[5], row_issue[6], row_issue[7], row_issue[8], row_issue[9])
                    if issue.get_html_url() == url:
                        issue = IssueComments.read_comment(name_file_comments_issue, issue)
                        return issue
        finally:
            file.close()
        return None

    @classmethod
    def load_issue_of_repository(cls, repo_name,name_file_issue, name_file_comments_issue):
        list_issue: list = list()
        file = open(name_file_issue, "rt")
        try:
            csv.field_size_limit(sys.maxsize)
            reader_issue: csv.DictReader = csv.reader(x.replace('\0', '') for x in file)
            index_issue = 0
            for row_issue in reader_issue:
                if index_issue == 0:
                    index_issue = 1
                else:
                    issue = Issues(row_issue[0], row_issue[1], row_issue[2], row_issue[3], row_issue[4],
                                   row_issue[5], row_issue[6], row_issue[7], row_issue[8], row_issue[9])
                    if issue.get_name_repository() == repo_name:
                        #issue = IssueComments.read_comment(name_file_comments_issue, issue)
                        list_issue.append(issue)
        finally:
            file.close()
        return list_issue

    def write_issue(self, name_file_issue, name_file_comment):
        if not (os.path.exists(name_file_issue)):
            file = open(name_file_issue, 'w')
            try:
                write_csv: csv.DictWriter = csv.writer(file)
                write_csv.writerow(
                    ('name repository', 'creator user', 'url_html issue', 'url_api issue', 'title', 'body',
                     'state', 'pull request', 'data open', 'updated at'))
            finally:
                file.close()
        file = open(name_file_issue, 'a')
        try:
            csv.field_size_limit(sys.maxsize)
            csv.writer(file)
            write_csv: csv.DictWriter = csv.writer(file)
            write_csv.writerow((
                self.get_name_repository(), self.get_creator(), self.get_html_url(), self.get_url(),
                self.get_title(), self.get_body(), self.get_state(), self.is_pull_request(),
                self.get_created_at(), self.get_updated_at()))
        finally:
            file.close()
        index = 0
        while index < self.len_comments():
            comment: IssueComments = self.get_comment_index(index)
            comment.write_comment_issue(self.__url, name_file_comment)
            index = index + 1
