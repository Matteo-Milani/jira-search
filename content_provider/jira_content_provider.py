import json

import requests
from requests.auth import HTTPBasicAuth

from typing import List


class UnauthorizedError(Exception):
    def __init__(self, msg: str) -> None:
        self.message: str = msg


class MergeError(Exception):
    def __init__(self, msg: str) -> None:
        self.message: str = msg


class JiraItem:
    def __init__(self) -> None:
        self.id: str = ""
        self.key: str = ""
        self.timeSpent: int = 0
        self.status: str = ""
        self.summary: str = ""
        self.accountId: int = 0
        self.accountName: str = ""


class JiraPage:
    def __init__(self) -> None:
        self.items: List[JiraItem] = []
        self.total: int = 0

    def merge(self, other: 'JiraPage') -> None:
        if self.total != other.total:
            raise MergeError("Can't merge two result sets from different queries")

        for item in other.items:
            self.items.append(item)


class JIRAContentProvider:
    def __init__(self, jiraBaseUrl: str, userName: str, password: str) -> None:
        self._baseUrl = jiraBaseUrl
        self._auth = HTTPBasicAuth(userName, password)
        self._pageSize = 50

    def search(self, jql: str, start: int = 0) -> JiraPage:
        url = f"{self._baseUrl}/rest/api/latest/search?maxResults={self._pageSize}&startAt={start}&jql={jql}"
        #print(f"  [JIRA] Searching tasks: {url}")

        myResponse = requests.get(url, auth=self._auth)
        if myResponse.status_code == 401:
            raise UnauthorizedError("HTTP 401 Unauthorized, are your credential correct?")

        myResponse.raise_for_status()  # Se call KO: raise exception

        jDoc = json.loads(myResponse.content)
        #print(json.dumps(jDoc, indent=2))

        jiraPage: JiraPage = JiraPage()
        jiraPage.total = jDoc["total"]

        for issue in jDoc["issues"]:
            item: JiraItem = JiraItem()
            item.id = issue["id"]
            item.key = issue["key"]

            if issue["fields"]["timespent"] is not None:
                item.timeSpent = issue["fields"]["timespent"]

            item.summary = issue["fields"]["summary"]
            item.status = issue["fields"]["status"]["name"]

            item.accountId = issue["fields"]["customfield_10009"]["id"]
            item.accountName = issue["fields"]["customfield_10009"]["value"]
            jiraPage.items.append(item)

        if start + self._pageSize < jiraPage.total:
            jiraPage.merge(self.search(jql, start + self._pageSize))

        return jiraPage