import json
from typing import List

import requests
from requests.auth import HTTPBasicAuth


class UnauthorizedError(Exception):
    def __init__(self, msg: str) -> None:
        self.message: str = msg

class JiraItem:
    def __init__(self) -> None:
        self.key: str = ""
        self.timeSpent: int = 0
        self.summary: str = ""
        self.resolutionDate: str = ""
        self.created: str = ""
        self.status: str = ""

class JiraPage:
    def __init__(self) -> None:
        self.total: int = 0
        self.items: List[JiraItem] = []

    def append(self, otherPage: 'JiraPage') -> None:
        for itm in otherPage.items:
            self.items.append(itm)


class JIRAContentProvider:
    def __init__(self, jiraBaseUrl: str, userName: str, password: str) -> None:
        self._baseUrl = jiraBaseUrl
        self._auth = HTTPBasicAuth(userName, password)
        self._pageSize = 50

    def search(self, jql: str, start: int = 0) -> JiraPage:
        url = f"{self._baseUrl}/rest/api/latest/search?maxResults={self._pageSize}&startAt={start}&jql={jql}"
        print(f"[JIRA] Searching tasks: {url}")

        myResponse = requests.get(url, auth=self._auth)
        if myResponse.status_code == 401:
            raise UnauthorizedError("HTTP 401 Unauthorized, are your credential correct?")

        myResponse.raise_for_status()  # Se call KO: raise exception

        jDoc = json.loads(myResponse.content)
        # print(json.dumps(jDoc, indent=2))

        currentPage: JiraPage = JiraPage()
        currentPage.total = jDoc["total"]

        for issue in jDoc["issues"]:
            itm: JiraItem = JiraItem()
            itm.key = issue["key"]
            itm.timeSpent = issue["fields"]["timespent"]
            itm.summary = issue["fields"]["summary"]
            itm.resolutionDate = issue["fields"]["resolutiondate"]
            itm.created = issue["fields"]["created"]
            itm.status = issue["fields"]["status"]["name"]
            currentPage.items.append(itm)

        if start + self._pageSize < currentPage.total:
            currentPage.append(self.search(jql, start + self._pageSize))

        return currentPage
