from pathlib import Path

import click
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build


class GoogleChatBot:
    SCOPES = ['https://www.googleapis.com/auth/chat.bot']
    SPACE_NAME: str
    CREDENTIALS: ServiceAccountCredentials

    def __init__(self, space_name: str, sa_json_file: Path, scopes: list = None):
        self.SPACE_NAME = space_name
        self.CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
            sa_json_file, self.SCOPES
        )

        self.SCOPES = scopes if scopes else self.SCOPES

    def send_msg(self, msg):
        chat = build('chat', 'v1', http=self.CREDENTIALS.authorize(Http()))
        result = chat.spaces().messages().create(
            parent=f'spaces/{self.SPACE_NAME}',
            body={'text': msg}
        ).execute()
        print(result)


@click.command()
@click.option('--space-name', '-s', required=True, help='Google Chat Space Name')
@click.option('--sa-json-file', '-j', required=True, help='Service Account JSON File', type=click.Path(exists=True))
@click.option('--msg', '-m', required=False, help='Message to send')
def cli(space_name: str, sa_json_file: Path, msg):
    bot = GoogleChatBot(space_name, sa_json_file)
    msg = msg if msg else 'Hello World!'
    bot.send_msg(msg)


if __name__ == '__main__':
    cli()
