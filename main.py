from typing import List

from content_provider.jira_content_provider import JIRAContentProvider, JiraPage

jira: JIRAContentProvider = JIRAContentProvider("https://giuneco.atlassian.net", "matteo.milani@giuneco.it",
                                                "ZTiCDmrBtmPLokjPt8WR6FE9")
# page: JiraPage = jira.search("project=PROM AND timespent > 0 AND Account='Progetto Prometheus' ORDER BY created DESC")
# page: JiraPage = jira.search("project=PROM AND timespent > 0 ORDER BY created DESC")
page: JiraPage = jira.search("project=PROM ORDER BY created DESC")

workedSecs: int = 0
for itm in page.items:
    workedSecs += itm.timeSpent

workedHours: float = workedSecs / 3600
workedDays: float = workedHours / 8
print(f"For {page.total} logs we worked: {workedSecs}s -> {workedHours}h -> {workedDays}d")
