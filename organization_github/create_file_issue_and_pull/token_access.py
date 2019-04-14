import datetime
import time
from github import PullRequest, PullRequestComment, Repository
from github import Github, GithubException, Rate, PaginatedList
from github import RateLimit
from requests import exceptions
from organization_github.create_file_issue_and_pull.exit_exception import ExitException
from organization_github.element_github.issues_comments import IssuesComments
from organization_github.element_github.issues import Issues
from organization_github.element_github.pull_request import PullRequest
from math import ceil
from organization_github.element_github.pull_request_comments import PullRequestComments
from log import Log


class TokenAccess:

    def __init__(self, github_access):
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

    def get_remaining(self, index) -> int:
        g: Github = self.__tokens[index][0]
        remaining = None
        while remaining is None:
            try:
                limit: RateLimit.RateLimit = g.get_rate_limit()
                core: Rate.Rate = limit.core
                remaining = core.remaining
                return remaining
            except GithubException:
                remaining = None
            except exceptions.RequestException:
                remaining = None

    def __question_min(self, index, remaining, question_used):
        g: Github = self.__tokens[index][0]
        while True:
            try:
                if remaining < 100:
                    if self.get_remaining(index) < 1500:
                        reset_time = datetime.datetime.fromtimestamp(g.rate_limiting_resettime)
                        curr_time = datetime.datetime.now()
                        time.sleep(abs(int(ceil((reset_time - curr_time).total_seconds())) + 1))
                    remaining = self.get_remaining(index)
                return remaining - question_used
            except GithubException:
                pass
            except exceptions.RequestException:
                pass

    def get_organization(self, g, organization, index, remaining):
        org = None
        while org is None:
            try:
                remaining = self.__question_min(index, remaining, 1)
                org = g.get_organization(organization)
            except GithubException:
                org = None
        return org, remaining

    def _get_repository(self, repo_name, org, index, remaining):
        repo = None
        while repo is None:
            try:
                remaining = self.__question_min(index, remaining, 1)
                repo = org.get_repo(repo_name)
            except GithubException:
                repo = None
        return repo, remaining

    def get_issues_and_commits(self, index, repo, name_organization, name_file, name_file_comment):
        g: Github = self.__tokens[index][0]
        remaining = self.get_remaining(index)
        org, remaining = self.get_organization(g, name_organization, index, remaining)
        repository, remaining = self._get_repository(repo, org, index, remaining)
        num_tot = None
        issues = None
        while num_tot is None:
            try:
                remaining = self.__question_min(index, remaining, 1)
                issues = repository.get_issues(state='all')
                num_tot = issues.totalCount
            except GithubException:
                num_tot = None
            except exceptions.RequestException:
                num_tot = None
        remaining = self.__question_min(index, remaining, 1)
        name_file_log = 'log/issue ' + repository.name + ' ' + name_organization + '.log'
        num, state = Log.search_file_log(name_file_log)
        try:
            while True:
                request_exception = False
                issue_user = None
                issues: PaginatedList.PaginatedList
                repository: Repository
                try:
                    remaining = self.__question_min(index, remaining, 1)
                    issue = issues[num_tot - num]
                    remaining = self.__question_min(index, remaining, 1)
                    if issue.pull_request is not None:
                        remaining = self.__question_min(index, remaining, 2)
                        if type(issue.created_at) is not None:
                            issue_user: Issues = Issues(repository.name, issue.user.login, issue.html_url, issue.url,
                                                        issue.title,
                                                        issue.body, issue.state, issue.as_pull_request(),
                                                        issue.created_at,
                                                        issue.updated_at)
                        else:
                            issue_user: Issues = Issues(repository.name, issue.user.login, issue.html_url, issue.url,
                                                        issue.title,
                                                        issue.body, issue.state, issue.as_pull_request(), None,
                                                        None)
                    else:
                        remaining = self.__question_min(index, remaining, 2)
                        if type(issue.created_at) is not None:
                            issue_user: Issues = Issues(repository.name, issue.user.login, issue.html_url, issue.url,
                                                        issue.title,
                                                        issue.body, issue.state, None, issue.created_at,
                                                        issue.updated_at)
                        else:
                            issue_user: Issues = Issues(repository.name, issue.user.login, issue.html_url, issue.url,
                                                        issue.title,
                                                        issue.body, issue.state, None, None,
                                                        None)
                    remaining = self.__question_min(index, remaining, 1)
                    issue_user, remaining = self.comments_issue(issue, issue_user, index, remaining)
                except GithubException:
                    request_exception = True
                except ConnectionError:
                    request_exception = True
                except exceptions.RequestException:
                    request_exception = True
                except IndexError:
                    num = num + 1
                    request_exception = True
                finally:
                    if issue_user is not None and request_exception is False:
                        issue_user.write_issue(name_file, name_file_comment)
                        num = num + 1
                    if (num - num_tot) == -1:
                        raise ExitException
                    Log.control_write_log(name_file_log, num)
        except ExitException:
            pass

    def comments_issue(self, issue, issue_user, index, remaining):
        n_comments = None
        comments: PaginatedList.PaginatedList = None
        while n_comments is None:
            try:
                remaining = self.__question_min(index, remaining, 1)
                comments: PaginatedList.PaginatedList = issue.get_comments()
                remaining = self.__question_min(index, remaining, 1)
                n_comments = comments.totalCount
            except GithubException:
                n_comments = None
        index_comment = 0
        while True:
            except_github = False
            try:
                comment = comments[index_comment]
                remaining = self.__question_min(index, remaining, 1)
                comment_user: IssuesComments = IssuesComments(comment.url, comment.html_url,
                                                              comment.user.login, comment.body,
                                                              comment.created_at, comment.updated_at)
                issue_user.add_comment(comment_user)
            except GithubException:
                except_github = True
            except ConnectionError:
                except_github = True
            except IndexError:
                return issue_user, remaining
            finally:
                if except_github is False:
                    index_comment = index_comment + 1

    def get_pull_request(self, index, repo_name, name_organization, name_file_pull_request,
                         name_file_comment_pull_request):
        remaining = self.get_remaining(index)
        g: Github = self.__tokens[index][0]
        org, remaining = self.get_organization(g, name_organization, index, remaining)
        repo, remaining = self._get_repository(repo_name, org, index, remaining)
        num_tot = None
        pulls = None
        while num_tot is None:
            try:
                remaining = self.__question_min(index, remaining, 1)
                pulls: PaginatedList.PaginatedList = repo.get_pulls(state='all')
                remaining = self.__question_min(index, remaining, 1)
                num_tot = pulls.totalCount
            except GithubException:
                num_tot = None
            except exceptions.RequestException:
                num_tot = None
        name_file_log = 'log/pull ' + repo.name + ' ' + name_organization + '.log'
        num, state = Log.search_file_log(name_file_log)
        try:
            while True:
                request_exception = False
                pull_request_user = None
                try:
                    remaining = self.__question_min(index, remaining, 1)
                    pull_request = pulls[num_tot - num]
                    assignees: list = list()
                    for assignee in pull_request.assignees:
                        assignees.append(assignee.login)
                    labels: list = list()
                    for label in pull_request.labels:
                        labels.append(label.name)
                    if assignees is None:
                        remaining = self.__question_min(index, remaining, 1)
                        if pull_request.is_merged():
                            remaining = self.__question_min(index, remaining, 1)
                            if pull_request.merged_by is not None:
                                remaining = self.__question_min(index, remaining, 4)
                                pull_request_user = PullRequest(repo_name, pull_request.url,
                                                                pull_request.html_url,
                                                                pull_request.user.login, pull_request.title,
                                                                pull_request.body, list(pull_request.assignee.login),
                                                                pull_request.commits,
                                                                pull_request.created_at, pull_request.updated_at,
                                                                pull_request.closed_at,
                                                                pull_request.is_merged(), pull_request.merged_at,
                                                                pull_request.merged_by.login,
                                                                pull_request.mergeable_state,
                                                                pull_request.mergeable, pull_request.state)
                            else:
                                remaining = self.__question_min(index, remaining, 4)
                                pull_request_user = PullRequest(repo_name, pull_request.url,
                                                                pull_request.html_url,
                                                                pull_request.user.login, pull_request.title,
                                                                pull_request.body, list(pull_request.assignee.login),
                                                                pull_request.commits,
                                                                pull_request.created_at, pull_request.updated_at,
                                                                pull_request.closed_at,
                                                                '', pull_request.merged_at,
                                                                pull_request.merged_by.login,
                                                                pull_request.mergeable_state,
                                                                pull_request.mergeable, pull_request.state)
                        else:
                            remaining = self.__question_min(index, remaining, 3)
                            pull_request_user = PullRequest(repo_name, pull_request.url,
                                                            pull_request.html_url,
                                                            pull_request.user.login, pull_request.title,
                                                            pull_request.body, list(pull_request.assignee.login),
                                                            pull_request.commits,
                                                            pull_request.created_at, pull_request.updated_at,
                                                            pull_request.closed_at,
                                                            pull_request.is_merged(), '',
                                                            '', pull_request.mergeable_state,
                                                            pull_request.mergeable, pull_request.state)
                    else:
                        remaining = self.__question_min(index, remaining, 1)
                        if pull_request.is_merged():
                            remaining = self.__question_min(index, remaining, 1)
                            if pull_request.merged_by is not None:
                                remaining = self.__question_min(index, remaining, 3)
                                pull_request_user = PullRequest(repo_name, pull_request.url,
                                                                pull_request.html_url, pull_request.user.login,
                                                                pull_request.title,
                                                                pull_request.body, assignees, pull_request.commits,
                                                                pull_request.created_at, pull_request.updated_at,
                                                                pull_request.closed_at,
                                                                pull_request.is_merged(), pull_request.merged_at,
                                                                pull_request.merged_by.login,
                                                                pull_request.mergeable_state,
                                                                pull_request.mergeable, pull_request.state)
                            else:
                                pull_request_user = PullRequest(repo_name, pull_request.url,
                                                                pull_request.html_url, pull_request.user.login,
                                                                pull_request.title,
                                                                pull_request.body, assignees, pull_request.commits,
                                                                pull_request.created_at, pull_request.updated_at,
                                                                pull_request.closed_at,
                                                                pull_request.is_merged(), pull_request.merged_at,
                                                                '',
                                                                pull_request.mergeable_state,
                                                                pull_request.mergeable, pull_request.state)
                        else:
                            remaining = self.__question_min(index, remaining, 2)
                            pull_request_user = PullRequest(repo_name, pull_request.url,
                                                            pull_request.html_url, pull_request.user.login,
                                                            pull_request.title,
                                                            pull_request.body, assignees, pull_request.commits,
                                                            pull_request.created_at, pull_request.updated_at,
                                                            pull_request.closed_at,
                                                            pull_request.is_merged(), '',
                                                            '', pull_request.mergeable_state,
                                                            pull_request.mergeable, pull_request.state)
                    pull_request_user, remaining = self._comments_pull(pull_request, pull_request_user, index,
                                                                       remaining)
                except GithubException:
                    request_exception = True
                except exceptions.RequestException:
                    request_exception = True
                except ConnectionError:
                    request_exception = True
                except IndexError:
                    num = num + 1
                    request_exception = True
                finally:
                    if pull_request_user is not None and request_exception is False:
                        num = num + 1
                        pull_request_user.write_pull_request(name_file_pull_request, name_file_comment_pull_request)
                    if (num - num_tot) == -1:
                        raise ExitException
                    Log.control_write_log(name_file_log, num)
        except ExitException:
            pass

    def _comments_pull(self, pull_request, pull_request_users, index, remaining):
        n_comments = None
        comments: PaginatedList.PaginatedList = None
        while n_comments is None:
            try:
                remaining = self.__question_min(index, remaining, 1)
                comments = pull_request.get_comments()
                remaining = self.__question_min(index, remaining, 1)
                n_comments = comments.totalCount
            except GithubException:
                n_comments = None
        index_comment = 0
        while True:
            except_github = False
            try:
                remaining = self.__question_min(index, remaining, 1)
                comment: PullRequestComment = comments[index_comment]
                remaining = self.__question_min(index, remaining, 1)
                if comment.user is not None:
                    comment_pull_request = PullRequestComments(comment.body, comment.commit_id,
                                                               comment.created_at, comment.id,
                                                               comment.diff_hunk, comment.position,
                                                               comment.updated_at, comment.url,
                                                               comment.html_url, comment.user.login)
                    pull_request_users.add_comment(comment_pull_request)
            except GithubException:
                except_github = True
            except ConnectionError:
                except_github = True
            except IndexError:
                return pull_request_users, remaining
            finally:
                if except_github is False:
                    index_comment = index_comment + 1
