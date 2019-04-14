import csv
import sys
import os


class IssueComments:

    def __init__(self, url, html_url, user_login, body, created_at, updated_at):
        self.__url = url
        self.__html_url = html_url
        self.__user_login = user_login
        self.__body = body
        self.__created_at = created_at
        self.__updated_at = updated_at

    def get_url(self):
        return self.__url

    def get_html_url(self):
        return self.__html_url

    def get_user_login(self):
        return self.__user_login

    def get_body(self):
        return self.__body

    def get_created_at(self):
        return self.__created_at

    def get_updated_at(self):
        return self.__updated_at

    @classmethod
    def read_comment_of_issue(cls, name_file_comments_issue, issue):
        if os.path.isfile(name_file_comments_issue):
            file = open(name_file_comments_issue, 'rt')
            eq = False
            try:
                csv.field_size_limit(sys.maxsize)
                reader_comments: csv.DictReader = csv.reader(x.replace('\0', '') for x in file)
                for row_comment in reader_comments:

                    if issue.get_url() == row_comment[0]:
                        comment_issue = IssueComments(row_comment[1], row_comment[2], row_comment[3], row_comment[4],
                                                      row_comment[5], row_comment[6])
                        issue.add_comment(comment_issue)
                        eq = True
                    elif eq:
                        return issue
            finally:
                file.close()
            return issue
        else:
            return issue

    @classmethod
    def read_comment_of_url(cls, name_file_comments_issue, url):
        if os.path.isfile(name_file_comments_issue):
            file = open(name_file_comments_issue, 'rt')
            try:
                csv.field_size_limit(sys.maxsize)
                reader_comments: csv.DictReader = csv.reader(x.replace('\0', '') for x in file)
                for row_comment in reader_comments:
                    comment_issue = IssueComments(row_comment[1], row_comment[2], row_comment[3], row_comment[4],
                                                  row_comment[5], row_comment[6])
                    if url == comment_issue.get_html_url():
                        return comment_issue
            finally:
                file.close()
            return None
        else:
            return None

    def write_comment_issue(self, url_issue, name_file_comment):
        if not (os.path.exists(name_file_comment)):
            file = open(name_file_comment, 'w')
            try:
                write_csv: csv.DictWriter = csv.writer(file)
                write_csv.writerow(('url issues', 'url_api comment', 'url_html comment', 'user create comment', 'body',
                                    'created_at', 'updated_at'))
            finally:
                file.close()
        file = open(name_file_comment, 'a')
        try:
            csv.field_size_limit(sys.maxsize)
            csv.writer(file)
            write_csv: csv.DictWriter = csv.writer(file)
            write_csv.writerow((
                url_issue, self.get_url(), self.get_html_url(), self.get_user_login(),
                self.get_body(), self.get_created_at(), self.get_updated_at()))
        finally:
            file.close()
