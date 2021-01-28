from content_provider.jira_content_provider import JIRAContentProvider, JiraPage

searches = [
    {"product": "PROM", "account": "Progetto Prometheus"},
    {"product": "PROM", "account": "Addendum - I"},

    #{"product": "I285", "account": "2019-11-01 - Innocenti 285"},
    #{"product": "I285", "account": "I285 - Adendum Mailing "},
    #{"product": "I285", "account": "I285 - Addendum Rendicontazione"},
#
    #{"product": "AWS", "account": "08_20180219_FB_InformaticaComTofani - Progetto Turni Lavoro"},
    #{"product": "AWS", "account": "09-20200406-CS-AIP-nuove sviluppi e canone di manutenzione v2"},
]

jira: JIRAContentProvider = JIRAContentProvider("https://giuneco.atlassian.net", "matteo.milani@giuneco.it", "zDm2VCHLFWLJcESwXdea3AF3")

for s in searches:
    result: JiraPage = jira.search(f'project = "{s["product"]}" AND Account = "{s["account"]}" ORDER BY created DESC')
    #result: JiraPage = jira.search(f'project = "{s["product"]}" AND timespent > 0 ORDER BY created DESC')

    totalSeconds: int = 0
    for itm in result.items:
        if itm.timeSpent is not None:
            totalSeconds += itm.timeSpent

    print(f'[{s["product"]}/{s["account"]}] Worked {result.total} tasks: {totalSeconds/60/60}h spent, TotH/Tasks: {totalSeconds/result.total/60/60}')