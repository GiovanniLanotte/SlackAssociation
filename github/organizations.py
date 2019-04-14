import csv

from github import Github, Commit, GitCommit, GitAuthor
from github import Organization
from github import Repository
from GitHub.create_file_issue_and_pull.thread_issue_and_pull import ThreadIssueAndPull
from GitHub.create_file_issue_and_pull.token_access import TokenAccess
from github import RateLimit
from github import Rate
from github import PullRequest
from github import GithubException
from github import PaginatedList
from requests import exceptions
import random
import datetime
import time
from math import ceil
from GitHub.control_files_repository import ControlFilesRepository
from GitHub.element_github.pull_request import PullRequest
import os
from log import Log
from GitHub.repositories import Repositories


class Organizations:

    def __init__(self,dir, organization, tokens):
        self._dir =dir
        self.__organization = organization
        self._rate_limit: list = list()
        self.__github: list = list()
        self.__tokens = tokens
        for token in self.__tokens:
            g = Github(token)
            self.__github.append(g)
            self._rate_limit.append(g.get_rate_limit())
        self._name_file_issue = "issue github access " + organization + ".csv"
        self._name_file_comments_issue = "comments of issue github access " + organization + ".csv"
        self._name_file_pull_request = "pull request github access " + organization + ".csv"
        self._name_file_comments_pull_request = "comments of pull request github access " + organization + ".csv"
        self.__pull_request_list: list = list()
        index = random.randint(0, len(self.__github) - 1)
        self.__question_max(index)
        g: Github = self.__github[index]
        org: Organization.Organization = g.get_organization(self.__organization)
        self.__repositories: dict = dict()
        thread_list = dict()
        self.average_commit = 0
        self.average_contributor = 0
        self.average_file_programming = 0
        print('controllo delle repository')
        for repo in org.get_repos():
            cfr = ControlFilesRepository(org.name, repo)
            cfr.start()
            thread_list[repo.name] = cfr
        for repo in org.get_repos():
            thread: ControlFilesRepository = thread_list.get(repo.name)
            ris_thread: tuple = thread.join()
            if ris_thread[0] != 0 and ris_thread[1] != 0:
                percentage = (ris_thread[0] / ris_thread[1]) * 100
            else:
                percentage = 0
            repository: Repositories = Repositories(repo.name, repo.html_url, self.members_repository(repo), repo.fork,
                                                    self.num_commits(repo.name),
                                                    self.has_committed_in_excess_of_the_year_2017(repo.name),
                                                    self.has_pull_request_merged(repo.name),
                                                    self.has_issue_for_tracking(repo.name),
                                                    percentage, self._dir, self._name_file_issue, self._name_file_comments_issue,
                                                    self._name_file_pull_request, self._name_file_comments_pull_request)
            self.average_commit = self.average_commit + repository.get_number_of_commits()
            self.average_contributor = self.average_contributor + len(repository.get_contributors())
            self.__repositories[repo.name] = repository
            self.average_file_programming = self.average_file_programming + percentage
        print('fine controllo')
        self.average_commit = self.average_commit / len(self.get_repositories())
        self.average_contributor = self.average_contributor / len(self.get_repositories())
        self.average_file_programming = self.average_file_programming / len(self.get_repositories())
        print('ricerca delle issue e pull request')
        self._search_issue_and_pull_request()

    def _search_issue_and_pull_request(self):
        multi_threading: dict = dict()
        num = 0
        keys: list = list()
        self._token_access = TokenAccess(self)
        file_finish = 'log/finish ' + self.__organization + '.log'
        if not (os.path.exists(file_finish)):
            if not os.path.isdir(self._dir):
                os.makedirs(self._dir)
            for repo in self.get_repositories():
                repo_name = repo.get_repository_name()
                print("start thread")
                create_contributor = ThreadIssueAndPull(self._dir, repo_name,self.__organization, self._token_access,
                                                        num % self._token_access.len_tokens(),
                                                        repo.get_name_file_issue(), repo.get_name_file_comments_issue(),
                                                        repo.get_name_file_pull_request(),
                                                        repo.get_name_file_comments_pull_request())
                create_contributor.setName(repo_name)
                create_contributor.start()
                multi_threading[repo_name] = create_contributor
                keys.append(repo_name)
                num = num + 1
            for key in keys:
                multi_threading[key].join()
            file = open(file_finish, 'w')
            file.close()

    def get_name_file_issue(self):
        return self._name_file_issue

    def get_name_file_comments_issue(self):
        return self._name_file_comments_issue

    def get_name_file_pull_request(self):
        return self._name_file_pull_request

    def get_name_file_comments_pull_request(self):
        return self._name_file_comments_pull_request

    def get_scv_repositories(self):
        name_file = 'repositories ' + self.__organization + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(
                ('name', 'url html', 'percentage programming file', 'has pull request merged',
                 'use issue for tracking',
                 '# contributors', '# commits', 'last update at least in 2018'))
            repositories = self.__repositories
            for key in repositories:
                repository = repositories.get(key)
                writer.writerow((
                    repository.get_repository_name(), repository.get_url_html(),
                    repository.get_percentage_programming_files(),
                    repository.has_pull_request_merged(), repository.use_issue_for_tracking(),
                    len(repository.get_contributors()), repository.get_number_of_commits(),
                    repository.last_update_at_least_in_2018()))

        finally:
            file.close()

    def get_average_percentage_file_programming(self):
        name_file = 'repositories percentage programming file ' + self.__organization + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(
                ('name', 'url html', 'percentage programming file', 'has pull request merged',
                 'use issue for tracking',
                 '# contributors', '# commits', 'last update at least in 2018'))
            repositories = self.__repositories
            for key in repositories:
                repository = repositories.get(key)
                if repository.get_percentage_programming_files() > \
                        self.average_file_programming:
                    writer.writerow((
                        repository.get_repository_name(), repository.get_url_html(),
                        repository.get_percentage_programming_files(),
                        repository.has_pull_request_merged(), repository.use_issue_for_tracking(),
                        len(repository.get_contributors()), repository.get_number_of_commits(),
                        repository.last_update_at_least_in_2018()))

        finally:
            file.close()

    def get_average_percentage_file_programming_and_repositories_merged(self):
            name_file = 'repositories percentage programming file and ' + \
                        'repositories merged ' + self.__organization + '.csv'
            file = open(name_file, 'wt')
            try:
                writer: csv.DictWriter = csv.writer(file)
                writer.writerow(
                    ('name', 'url html', 'percentage programming file', 'has pull request merged',
                     'use issue for tracking',
                     '# contributors', '# commits', 'last update at least in 2018'))
                repositories = self.__repositories

                for key in repositories:
                    repository = repositories.get(key)
                    if repository.get_percentage_programming_files() > \
                            self.average_file_programming and \
                            repository.has_pull_request_merged():
                        writer.writerow((
                            repository.get_repository_name(), repository.get_url_html(),
                            repository.get_percentage_programming_files(),
                            repository.has_pull_request_merged(), repository.use_issue_for_tracking(),
                            len(repository.get_contributors()), repository.get_number_of_commits(),
                            repository.last_update_at_least_in_2018()))

            finally:
                file.close()

    def get_average_percentage_file_programming_and_repositories_merged_and_use_tracking_issue(self):
            name_file = 'repositories percentage programming file and repositories merged and use tracking issue ' + self.__organization + '.csv'
            file = open(name_file, 'wt')
            try:
                writer: csv.DictWriter = csv.writer(file)
                writer.writerow(
                    ('name', 'url html', 'percentage programming file', 'has pull request merged',
                     'use issue for tracking',
                     '# contributors', '# commits', 'last update at least in 2018'))
                for key in self.__repositories:
                    repository = self.__repositories.get(key)
                    repository: Repositories
                    if repository.get_percentage_programming_files() > \
                            self.average_file_programming and \
                            repository.has_pull_request_merged() and repository.use_issue_for_tracking():
                        writer.writerow((
                            repository.get_repository_name(), repository.get_url_html(),
                            repository.get_percentage_programming_files(),
                            repository.has_pull_request_merged(), repository.use_issue_for_tracking(),
                            len(repository.get_contributors()), repository.get_number_of_commits(),
                            repository.last_update_at_least_in_2018()))

            finally:
                file.close()

    def get_average_percentage_file_programming_and_repositories_merged_and_use_tracking_issue_and_more_average_contributors(
            self):
            name_file = 'repositories percentage programming file and repositories merged and use tracking issue and contributors more average ' + self.__organization + '.csv'
            file = open(name_file, 'wt')
            try:
                writer: csv.DictWriter = csv.writer(file)
                writer.writerow(
                    ('name', 'url html', 'percentage programming file', 'has pull request merged',
                     'use issue for tracking',
                     '# contributors', '# commits', 'last update at least in 2018'))
                repositories = self.__repositories
                for key in repositories:
                    repository = repositories.get(key)
                    if repository.get_percentage_programming_files() > \
                            self.average_file_programming and \
                            repository.has_pull_request_merged() and repository.use_issue_for_tracking() and \
                            repository.len_contributors() > self.average_contributor:
                        writer.writerow((
                            repository.get_repository_name(), repository.get_url_html(),
                            repository.get_percentage_programming_files(),
                            repository.has_pull_request_merged(), repository.use_issue_for_tracking(),
                            len(repository.get_contributors()), repository.get_number_of_commits(),
                            repository.last_update_at_least_in_2018()))
            finally:
                file.close()

    def get_average_percentage_file_programming_and_repositories_merged_and_use_tracking_issue_and_more_average_contributors_and_more_average_commits(
            self):
        name_file = 'repositories percentage programming file and repositories merged and use tracking issue and contributors more average and more median average ' + self.__organization + '.csv'
        file = open(name_file, 'wt')
        try:
            writer: csv.DictWriter = csv.writer(file)
            writer.writerow(
                ('name', 'url html', 'percentage programming file', 'has pull request merged',
                 'use issue for tracking',
                 '# contributors', '# commits', 'last update at least in 2018'))
            repositories = self.__repositories
            for key in repositories:
                repository = repositories.get(key)
                if repository.get_percentage_programming_files() > \
                        self.average_file_programming and \
                        repository.has_pull_request_merged() and repository.use_issue_for_tracking() and \
                        repository.len_contributors() > self.average_contributor and \
                        repository.get_number_of_commits() > self.average_commit:
                    writer.writerow((
                        repository.get_repository_name(), repository.get_url_html(),
                        repository.get_percentage_programming_files(),
                        repository.has_pull_request_merged(), repository.use_issue_for_tracking(),
                        len(repository.get_contributors()), repository.get_number_of_commits(),
                        repository.last_update_at_least_in_2018()))
        finally:
            file.close()

    def get_average_percentage_file_programming_and_repositories_merged_and_use_tracking_issue_and_more_average_contributors_and_more_average_commits_and_last_update_in_2018(
            self):
            name_file = 'repositories percentage programming file and repositories merged and use tracking issue and contributors more average and more average commits and last update in 2018 ' + self.__organization + '.csv'
            file = open(name_file, 'wt')
            try:
                writer: csv.DictWriter = csv.writer(file)
                writer.writerow(
                    ('name', 'url html', 'percentage programming file', 'has pull request merged',
                     'use issue for tracking',
                     '# contributors', '# commits', 'last update at least in 2018'))
                repositories = self.__repositories
                for key in repositories:
                    repository = repositories.get(key)
                    if repository.get_percentage_programming_files() > \
                            self.average_file_programming and \
                            repository.has_pull_request_merged() and repository.use_issue_for_tracking() and \
                            repository.len_contributors() > self.average_contributor and \
                            repository.get_number_of_commits() > self.average_commit and \
                            repository.last_update_at_least_in_2018():
                        writer.writerow((
                            repository.get_repository_name(), repository.get_url_html(),
                            repository.get_percentage_programming_files(),
                            repository.has_pull_request_merged(), repository.use_issue_for_tracking(),
                            len(repository.get_contributors()), repository.get_number_of_commits(),
                            repository.last_update_at_least_in_2018()))
            finally:
                file.close()

    def get_repositories(self):
        list_repo = list()
        for repo_key in self.__repositories:
            list_repo.append(self.__repositories.get(repo_key))
        return list_repo

    def has_pull_request_merged(self, repo_name):
        index: int = random.randint(0, len(self.__github) - 1)
        remaining = self.get_remaining(index)
        g: Github = self.__github[index]
        org, remaining = self.get_organization(g, self.__organization, index, remaining)
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
        name_file_log = 'log/pull request is merged ' + repo.name + ' ' + self.__organization + '.log'
        num, value = Log.search_file_log(name_file_log)
        if value:
            return True
        else:
            try:
                while True:
                    request_exception = False
                    try:
                        remaining = self.__question_min(index, remaining, 1)
                        pull_request: PullRequest.PullRequest = pulls[num]
                        if pull_request.is_merged():
                            return True
                    except GithubException:
                        request_exception = True
                    except exceptions.RequestException:
                        request_exception = True
                    finally:
                        if request_exception is False:
                            num = num + 1
                        Log.control_write_log(name_file_log, num, False)
            except IndexError:
                return False

    def has_issue_for_tracking(self, repo_name):
        index: int = random.randint(0, len(self.__github) - 1)
        remaining = self.get_remaining(index)
        g: Github = self.__github[index]
        org, remaining = self.get_organization(g, self.__organization, index, remaining)
        repo, remaining = self._get_repository(repo_name, org, index, remaining)
        repo: Repository
        self.__question_min(index, remaining, 1)
        return repo.has_issues

    def contain_association(self, name_channel):
        if self.get_association(name_channel) == list():
            return False
        return True

    def get_association(self, name_channel):
        repository_list: list = list()
        for repository_name in self.__repositories:
            repository = self.__repositories.get(repository_name)
            pos = len(repository.get_repository_name())
            if repository.get_percentage_programming_files() > self.average_file_programming \
                    and repository.get_fork() is False \
                    and repository.len_contributors() > self.average_contributor \
                    and repository.last_update_at_least_in_2018() \
                    and repository.get_number_of_commits() > self.average_commit \
                    and repository.has_pull_request_merged() \
                    and repository.use_issue_for_tracking():
                if len(repository.get_repository_name()) < len(name_channel):
                    if name_channel.find(repository.get_repository_name()) == 0 and name_channel[pos] == '-':
                        repository_list.append(repository)
                if name_channel == repository.get_repository_name():
                    repository_list.append(repository)
        return repository_list

    def get_contributor_repository(self, repo_name):
        index: int = random.randint(0, len(self.__github) - 1)
        self.__question_max(index)
        g: Github = self.__github[index]
        contributors_login_list: set = set()
        org: Organization.Organization = g.get_organization(self.__organization)
        repo = org.get_repo(repo_name)
        member: PaginatedList.PaginatedList = repo.get_contributors()
        for person in member:
            contributors_login_list.add(person.login)
        return contributors_login_list

    def get_tokens(self):
        return self.__github

    def is_remaining_zero(self, index) -> bool:
        g: Github = self.__github[index]
        limit: RateLimit.RateLimit = g.get_rate_limit()
        core: Rate.Rate = limit.core
        remaining = core.remaining
        return remaining == 0

    def get_remaining(self, index) -> int:
        g: Github = self.__github[index]
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

    def __question_max(self, index):
        while self.get_remaining(index) <= 4000:
            self.__sleep(index)

    def __sleep(self, index):
        g: Github = self.__github[index]
        exception = False
        while exception is True:
            exception = False
            try:
                reset_time = datetime.datetime.fromtimestamp(g.rate_limiting_resettime)
                curr_time = datetime.datetime.now()
                time.sleep(abs(int(ceil((reset_time - curr_time).total_seconds())) + 1))
            except GithubException:
                exception = True
            except exceptions.RequestException:
                exception = True

    def __question_min(self, index, remaining, question_used):
        g: Github = self.__github[index]
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

    def get_contributors(self):
        while True:
            try:
                index: int = random.randint(0, len(self.__github) - 1)
                self.__question_max(index)
                g: Github = self.__github[index]
                contributors_login: dict = dict()
                org: Organization.Organization = g.get_organization(self.__organization)
                for repo in org.get_repos():
                    contributors: set = self.members_repository(repo)
                    contributors_login[repo.name] = contributors
                return contributors_login
            except GithubException:
                pass
            except exceptions.RequestException:
                pass

    @staticmethod
    def members_repository(repo: Repository.Repository):
        while True:
            try:
                contributors_login_list: set = set()
                member: PaginatedList.PaginatedList = repo.get_contributors()
                for person in member:
                    contributors_login_list.add(person)
                return contributors_login_list
            except TypeError:
                return set()
            except GithubException:
                pass
            except exceptions.RequestException:
                pass

    def has_committed_in_excess_of_the_year_2017(self, repo_name):
        index: int = random.randint(0, len(self.__github) - 1)
        remaining = self.get_remaining(index)
        g: Github = self.__github[index]
        org, remaining = self.get_organization(g, self.__organization, index, remaining)
        repo, remaining = self._get_repository(repo_name, org, index, remaining)
        num_tot = None
        commits = None
        while num_tot is None:
            try:
                remaining = self.__question_min(index, remaining, 1)
                commits: PaginatedList.PaginatedList = repo.get_commits()
                remaining = self.__question_min(index, remaining, 1)
                num_tot = commits.totalCount
            except GithubException as e:
                if e.status == 409:
                    num_tot = -1
                else:
                    num_tot = None
            except exceptions.RequestException:
                num_tot = None
        pos = 0
        if num_tot == -1:
            return False
        else:
            while True:
                try:
                    commit: Commit.Commit = commits[pos]
                    remaining = self.__question_min(index, remaining, 1)
                    git_commit: GitCommit.GitCommit = commit.commit
                    remaining = self.__question_min(index, remaining, 1)
                    committer: GitAuthor.GitAuthor = git_commit.committer
                    remaining = self.__question_min(index, remaining, 1)
                    date: datetime.datetime = committer.date
                    if date.year > 2017:
                        return True
                    pos = pos + 1
                except GithubException:
                    pos = pos
                except IndexError:
                    if pos >= num_tot:
                        return False

    def num_commits(self, repo_name):
        index: int = random.randint(0, len(self.__github) - 1)
        remaining = self.get_remaining(index)
        g: Github = self.__github[index]
        org, remaining = self.get_organization(g, self.__organization, index, remaining)
        repo, remaining = self._get_repository(repo_name, org, index, remaining)
        num_tot = None
        while num_tot is None:
            try:
                remaining = self.__question_min(index, remaining, 1)
                commits: PaginatedList.PaginatedList = repo.get_commits()
                remaining = self.__question_min(index, remaining, 1)
                num_tot = commits.totalCount
            except GithubException as e:
                if e.status == 409:
                    num_tot = 0
                else:
                    num_tot = None
            except exceptions.RequestException:
                num_tot = None
        return num_tot

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

    def __repr__(self):
        out = ""
        i = 0
        while i < len(self.__tokens):
            g: Github = self.__github[i]
            out = out + "num question:{} index:{} time:{}\n".format(self.get_remaining(i), i,
                                                                    datetime.datetime.fromtimestamp(
                                                                        g.rate_limiting_resettime))
            i = i + 1
        return out
