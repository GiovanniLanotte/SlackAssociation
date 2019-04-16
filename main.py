import csv
import sys
from containers import Containers


def read_token_file(file_name):
    file = open(file_name, 'rt')
    token: list = list()
    try:
        reader_token: csv.DictReader = csv.reader(file)
        for row in reader_token:
            token.append(row[0])
    finally:
        file.close()
        return token


def main():
    tokens = read_token_file(sys.argv[3])
    containers: Containers = Containers()
    containers.add_association(sys.argv[1], sys.argv[2], tokens)
    containers.correspondence_channel_to_archive(sys.argv[1])
    containers.get_len_message_for_channel(sys.argv[1])
    containers.messages_for_channel()
    containers.messages_slack_url_github()
    containers.pull_request_on_message_slack()
    containers.messages_for_channel()


if __name__ == '__main__':
    main()
