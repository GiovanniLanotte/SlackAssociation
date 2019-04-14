from organization_github.element_github.issues import Issues
from organization_github.element_github.pull_request import PullRequest


class Repositories:

    def __init__(self, name, url, contributors, fork, number_commits, update_at_least_in_2018, use_pull_request_merged,
                 has_issue_for_tracking, percentage_programming_files, directory, name_file_issue,
                 name_file_comment_issue, name_file_pull_request, name_file_comment_pull_request):
        self._name = name
        self._url = url
        self._contributors = contributors
        self._fork = fork
        self._contributors: list = list()
        for member in contributors:
            self._contributors.append(member.login)
        self._number_commits = number_commits
        self._update_at_least_in_2018 = update_at_least_in_2018
        self._have_pull_request_merged = use_pull_request_merged
        self._use_issue_for_tracking = has_issue_for_tracking
        self._percentage_programming_files = percentage_programming_files
        self._name_file_issue = directory + '/' + self._name + '/' + name_file_issue
        self._name_file_comment_issue = directory + '/' + self._name + '/' + name_file_comment_issue
        self._name_file_pull_request = directory + '/' + self._name + '/' + name_file_pull_request
        self._name_file_comment_pull_request = directory + '/' + self._name + '/' + name_file_comment_pull_request

    def get_repository_name(self):
        return self._name

    def get_url_html(self):
        return self._url

    def get_contributors(self):
        return self._contributors

    def len_contributors(self):
        return len(self._contributors)

    def get_fork(self):
        return self._fork

    def get_number_of_commits(self):
        return self._number_commits

    def last_update_at_least_in_2018(self):
        return self._update_at_least_in_2018

    def get_issues(self):
        return set(Issues.load_issue_of_repository(self._name, self._name_file_issue, self._name_file_comment_issue))

    def get_pulls(self):
        return set(PullRequest.load_pull_request_of_repository(self._name, self._name_file_pull_request,
                                                               self._name_file_comment_pull_request))

    def has_pull_request_merged(self):
        return self._have_pull_request_merged

    def use_issue_for_tracking(self):
        return self._use_issue_for_tracking

    def get_percentage_programming_files(self):
        return self._percentage_programming_files

    def get_name_file_issue(self):
        return self._name_file_issue

    def get_name_file_comment_issue(self):
        return self._name_file_comment_issue

    def get_name_file_pull_request(self):
        return self._name_file_pull_request

    def get__name_file_comment_pull_request(self):
        return self._name_file_comment_pull_request
