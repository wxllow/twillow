# Requires google-api-python-client

from itertools import islice

from googleapiclient.discovery import build
from twilio.twiml.messaging_response import MessagingResponse

from config import get_config

config = get_config()

api_key = config['modules']['search']['google_api_key']
cse_id = config['modules']['search']['google_cse_id']


class SearchModule:
    def __init__(self, client) -> None:
        self.client = client

    def search(self, *q):
        query = ' '.join(q)
        limit = config['modules']['search'].get('limit', 3)

        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cse_id).execute()

        resp = MessagingResponse()

        for item in islice(res['items'], 0, limit):
            resp.message(f"{item['title']}\n\n{item['link']}")

        return resp

    def _command(self, *args, **kwargs):
        return self.search


def module():
    return SearchModule
