from organization_github.element_github.issues import Issues
from threading import Thread
from organization_github.element_github.pull_request import PullRequest
from organization_github.element_github.issues_comments import IssuesComments
from organization_github.element_github.pull_request_comments import PullRequestComments


class MessagesUsers(Thread):

    def __init__(self, users, text, massage, url, name_file_issue, name_file_comments_issue, name_file_pull_request,
                 name_file_comments_pull_request):
        Thread.__init__(self)
        self._users = users
        self.text = text
        self._massage = massage
        self._return = None
        self._url = url
        self._name_file_issue = name_file_issue
        self._name_file_comments_issue = name_file_comments_issue
        self._name_file_pull_request = name_file_pull_request
        self._name_file_comments_pull_request = name_file_comments_pull_request

    def run(self):
        self._return = self.get_massage_list()

    def join(self, timeout=None):
        Thread.join(self)
        return self._return

    def get_massage(self):
        return self._massage

    def get_massage_list(self):
        if self._url.find('/issues/') != -1:
            index_comment = self._url.find('#issuecomment-')
            if index_comment != -1:
                url = self._url
                comment = IssuesComments.read_comment_of_url(self._name_file_comments_issue, url)
                if comment is not None:
                    tuple_value = (self._massage, comment)
                else:
                    tuple_value = (self._massage, url)
                return tuple_value
            else:
                url = self._url
                issue = Issues.load_issues_without_comments(self._name_file_issue, url)
                if issue is not None:
                    tuple_value = (self._massage, issue)
                else:
                    tuple_value = (self._massage, url)
                return tuple_value

        elif self._url.find('/pull/') != -1:
            index_comment = self._url.find('#discussion_r')
            if index_comment != -1:
                url = self._url
                comment = PullRequestComments.read_comment_of_url(self._name_file_comments_pull_request, url)
                if comment is not None:
                    tuple_value = (self._massage, comment)
                else:
                    tuple_value = (self._massage, url)
                return tuple_value
            else:
                url = self._url
                index_comment = self._url.find('#issuecomment-')
                if index_comment != -1:
                    comment = IssuesComments.read_comment_of_url(self._name_file_comments_issue, url)
                    if comment is not None:
                        tuple_value = (self._massage, comment)
                    else:
                        tuple_value = (self._massage, url)
                    return tuple_value
                else:
                    pull_request = PullRequest.load_pull_request_without_comments(
                        self._name_file_pull_request, url)
                    if pull_request is not None:
                        print("url: {} pull request: {}".format(url, pull_request.get_html_url()))
                        tuple_value = (self._massage, pull_request)
                        return tuple_value
                    else:
                        tuple_value = (self._massage, url)
                        return tuple_value
