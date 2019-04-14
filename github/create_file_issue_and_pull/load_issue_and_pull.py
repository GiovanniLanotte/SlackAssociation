from multiprocessing import Lock


class LoadIssueAndPull:
    __t_pause: Lock = Lock()

    def __init__(self, repo: str, organization, token_access, name_file_issue, name_file_comments_issue, name_file_pull_request,
                 name_file_comments_pull_request):
        self._repo: str = repo
        self._token_access = token_access
        index = 0
        self.__t_pause.acquire()
        index = token_access.get_index(index)
        self.__t_pause.release()
        self._name_file_issue = name_file_issue
        self._name_file_pull_request = name_file_pull_request
        self._name_file_comments_issue = name_file_comments_issue
        self._name_file_comments_pull_request = name_file_comments_pull_request
        token_access.get_issues_and_commits(index, repo, organization, self._name_file_issue, self._name_file_comments_issue)
        print('finish loading {} issues'.format(self._repo))
        self._list_pull_request: dict = dict()
        self._list_pull_request = token_access.get_pull_request(index, repo, organization, self._name_file_pull_request,
                                                                self._name_file_comments_pull_request)
        print('finish loading {} pull request'.format(self._repo))
        self._token_access.unlock_token(index)
