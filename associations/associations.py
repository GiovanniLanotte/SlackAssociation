
class Associations:

    def __init__(self, repository, channel, name_organization, name_file_issue, name_file_comments_issue, name_file_pull_request,
                 name_file_comments_pull_request):
        self._repository = repository
        self._channel = channel
        self._name_organization = name_organization
        self._name_file_issue = name_file_issue
        self._name_file_comments_issue = name_file_comments_issue
        self._name_file_pull_request = name_file_pull_request
        self._name_file_comments_pull_request = name_file_comments_pull_request

    def get_repository(self):
        return self._repository

    def get_channel(self):
        return self._channel

    def get_name_organization(self):
        return self._name_organization

    def get_name_file_issue(self):
        return self._name_file_issue

    def get_name_file_comments_issue(self):
        return self._name_file_comments_issue

    def get_name_file_pull_request(self):
        return self._name_file_pull_request

    def get_name_file_comments_pull_request(self):
        return self._name_file_comments_pull_request
