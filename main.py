from content_provider.jira_content_provider import JIRAContentProvider, JiraPage

searches = [
    {"product": "PROM", "account": "Progetto Prometheus"},
    {"product": "PROM", "account": "Addendum - I"},
    {"product": "I285", "account": "2019-11-01 - Innocenti 285"},
    {"product": "I285", "account": "I285 - Adendum Mailing "},
    {"product": "I285", "account": "I285 - Addendum Rendicontazione"},

    #{"product": "AWS", "account": "082018021AIP"},
    #{"product": "AWS", "account": "082018021AIPCON"},
    #{"product": "AWS", "account": "09-2020040"},
    #{"product": "AWS", "account": "AIPCARNET01"},
    #{"product": "AWS", "account": "AIP-NOASS"},
]

jira: JIRAContentProvider = JIRAContentProvider("https://giuneco.atlassian.net", "matteo.milani@giuneco.it", "zDm2VCHLFWLJcESwXdea3AF3")

for s in searches:
    result: JiraPage = jira.search(f'project = "{s["product"]}" AND Account = "{s["account"]}" AND timespent > 0 ORDER BY created DESC')

    totalSeconds: int = 0
    for itm in result.items:
        totalSeconds += itm.timeSpent

    print(f'[{s["product"]}/{s["account"]}] Worked {result.total} tasks: {totalSeconds/60/60}h spent')