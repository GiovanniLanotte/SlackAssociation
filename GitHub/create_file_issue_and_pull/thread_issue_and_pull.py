from GitHub.create_file_issue_and_pull.load_issue_and_pull import LoadIssueAndPull
from threading import Thread


class ThreadIssueAndPull(Thread):
    def __init__(self, repo, token_access, index, name_file_issue, name_file_comments_issue,
                 name_file_pull_request, name_file_comments_pull_request):
        Thread.__init__(self)
        self._repo = repo
        self._token_access = token_access
        self._return = None
        self.index = index
        self._name_file_issue = name_file_issue
        self._name_file_comments_issue = name_file_comments_issue
        self._name_file_pull_request = name_file_pull_request
        self._name_file_comments_pull_request = name_file_comments_pull_request

    def run(self):
        self._return = LoadIssueAndPull(self._repo, self._token_access, self._name_file_issue,
                                        self._name_file_comments_issue, self._name_file_pull_request,
                                        self._name_file_comments_pull_request)

    def join(self, timeout=None):
        Thread.join(self)
        return self._return
