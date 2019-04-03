class TokenAccess:

    def __init__(self, github_access):
        self._g = github_access
        self.__tokens: list = list()
        for token in github_access.get_tokens():
            t = (token, False)
            self.__tokens.append(t)

    def _is_token_free(self, index):
        elem = self.__tokens[index]
        return elem[1] is False

    def _lock_token(self, index):
        elem: tuple = self.__tokens[index]
        self.__tokens[index] = tuple((elem[0], True))

    def unlock_token(self, index):
        elem: tuple = self.__tokens[index]
        self.__tokens[index] = tuple((elem[0], False))

    def get_index(self, index):
        while not (self._is_token_free(index)):
            index = (index + 1) % self.len_tokens()
        self._lock_token(index)
        return index

    def len_tokens(self):
        return len(self.__tokens)

    def get_issues_and_commits(self, index, repo, name_file_issue, name_file_comment):
        
        return self._g.get_issues_and_commits(index, repo, name_file_issue, name_file_comment)

    def get_pull_request(self, repo, index, name_file_pull_request, name_file_comment_pull_request):
        return self._g.get_pull_request(repo, index, name_file_pull_request, name_file_comment_pull_request)
