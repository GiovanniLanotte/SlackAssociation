from GitHub.organizations import Organizations
from GitHub.repositories import Repositories
from slack.workspace.workspace_slackarchive import WorkspacesSlackArchive
from slack.workspace.workspaces_raw import WorkspacesRaw
from containers import Containers


def main():
    tokens = list((
        "89d20a3738fab785ac969762b24825cf29655662", "3fef2701e4e3c1e9c7e9bde1a79dc35ae9b7105e",
        "a66b6e28a0facc3d7dd72e42ceff0a3ebb292b01", "2909303039a854ba34f28cbea893521a1d91f5b7",
        "b670034b9206d2a313c05365708c40faa9aef163", "9da3ce90b285e7f11f488ccf2c4b3581e2452244",
        "0ad2645c59787be7cd465206afd4b2ee4f511461", "d61111dbbb6ccde9e996183d594f3b0c14ae4afa",
        "cc1a6fd94a3838ce2565e6f91d50f3fb3bba2109"))
    org = Organizations('kubernetes', tokens)


    containers: Containers = Containers()
    containers.add_association('hyperledger', 'workspace_Hyperledge', tokens)
    print("inizio")
    containers.correspondence_channel_to_archive()
    #containers.print_organization()
    #containers.get_len_message_for_channel()
    #containers.messages_for_channel()
    #containers.messages_slack_url_github()
    #containers.pull_request_on_message_slack()
    #containers.messages_for_channel()
    print("fine")



if __name__ == '__main__':
    main()
