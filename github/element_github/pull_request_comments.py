import csv
import os
import sys


class PullRequestComments:
    def __init__(self, body, commit_id, created_at, id, diff_hunk, position, updated_at, url, html_url, user):
        self.__body = body
        self.__commit_id = commit_id
        self.__created_at = created_at
        self.__id = id
        self.__diff_hunk = diff_hunk
        self.__position = position
        self.__updated_at = updated_at
        self.__url = url
        self.__html_url = html_url
        self.__user = user

    def get_body(self):
        return self.__body

    def get_commit_id(self):
        return self.__commit_id

    def get_created_at(self):
        return self.__created_at

    def get_id(self):
        return self.__id

    def get_diff_hunk(self):
        return self.__diff_hunk

    def get_position(self):
        return self.__position

    def get_updated_at(self):
        return self.__updated_at

    def get_url(self):
        return self.__url

    def get_html_url(self):
        return self.__html_url

    def get_user(self):
        return self.__user

    @classmethod
    def read_comment_pull_request(cls, name_file_comments_pull_request, pull_request):
        if os.path.isfile(name_file_comments_pull_request):
            file = open(name_file_comments_pull_request, 'rt')
            eq = False
            try:
                reader_comments_pull_request: csv.DictReader = csv.reader(x.replace('\0', '') for x in file)
                index_comments_pull_request = 0
                for row_comments_pull_request in reader_comments_pull_request:
                    if index_comments_pull_request == 0:
                        index_comments_pull_request = 1
                    else:
                        if row_comments_pull_request[0] == pull_request.get_html_url():
                            pull_request_comment = PullRequestComments(row_comments_pull_request[2],
                                                                       row_comments_pull_request[3],
                                                                       row_comments_pull_request[4],
                                                                       row_comments_pull_request[5],
                                                                       row_comments_pull_request[6],
                                                                       row_comments_pull_request[7],
                                                                       row_comments_pull_request[8],
                                                                       row_comments_pull_request[9],
                                                                       row_comments_pull_request[10],
                                                                       row_comments_pull_request[11])
                            pull_request.add_comment(pull_request_comment)
                            eq = True
                        elif eq:
                            return pull_request
            finally:
                file.close()
            return pull_request
        else:
            return pull_request

    @classmethod
    def read_comment_of_url(cls, name_file_comments_pull_request, url):
        if os.path.isfile(name_file_comments_pull_request):
            file = open(name_file_comments_pull_request, 'rt')
            try:
                reader_comments_pull_request: csv.DictReader = csv.reader(x.replace('\0', '') for x in file)
                index_comments_pull_request = 0
                for row_comments_pull_request in reader_comments_pull_request:
                    if index_comments_pull_request == 0:
                        index_comments_pull_request = 1
                    else:
                        pull_request_comment = PullRequestComments(row_comments_pull_request[2],
                                                                   row_comments_pull_request[3],
                                                                   row_comments_pull_request[4],
                                                                   row_comments_pull_request[5],
                                                                   row_comments_pull_request[6],
                                                                   row_comments_pull_request[7],
                                                                   row_comments_pull_request[8],
                                                                   row_comments_pull_request[9],
                                                                   row_comments_pull_request[10],
                                                                   row_comments_pull_request[11])
                        if pull_request_comment.get_html_url() == url:
                            return pull_request_comment
            finally:
                file.close()
            return None
        else:
            return None

    def write_comment_pull_request(self, pull_request, name_file):
        if not (os.path.exists(name_file)):
            file = open(name_file, 'wt')
            try:
                write_csv: csv.DictWriter = csv.writer(file)
                write_csv.writerow(('pull request url html', 'pull request url', 'body', 'commit_id', 'create at', 'id',
                                    'diff_hunk', 'position', 'update at', 'url', 'html url', 'user'))
            finally:
                file.close()
        file = open(name_file, 'a')
        try:
            csv.field_size_limit(sys.maxsize)
            csv.writer(file)
            write_csv: csv.DictWriter = csv.writer(file)
            write_csv.writerow((pull_request.get_html_url(), pull_request.get_html_url(),
                                self.get_body(), self.get_commit_id(), self.get_created_at(),
                                self.get_id(), self.get_diff_hunk(), self.get_position(),
                                self.get_updated_at(), self.get_url(), self.get_html_url(),
                                self.get_user()))
        finally:
            file.close()
