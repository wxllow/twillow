# -- Search module using CSE --
# Requires google-api-python-client
from itertools import islice

from googleapiclient.discovery import build
from twilio.twiml.messaging_response import MessagingResponse

from twillow.config import get_config

config = get_config()

try:
    api_key = config["module"]["search"]["google_api_key"]
    cse_id = config["module"]["search"]["google_cse_id"]
except KeyError:
    raise Exception("Google CSE API Key is required! See docs/google-cse.md")


class SearchModule:
    def __init__(self):
        self.name = "search"
        self.service = build("customsearch", "v1", developerKey=api_key)

    def search(self, *query):
        q = " ".join(query)
        limit = config["module"]["search"].get("limit", 3)

        res = self.service.cse().list(q=q, cx=cse_id).execute()

        resp = MessagingResponse()

        resp.message(f'🔎 Results for "{q}"')

        if int(res["searchInformation"]["totalResults"]) < 1:
            resp.message("⛔️ No results found!")
            return resp

        for item in islice(res["items"], 0, limit):
            resp.message(f"{item['title']}\n\n{item['link']}")

        return resp

    def _all(self, *args, **kwargs):
        return self.search


def module():
    return SearchModule
