from typing import List

from content_provider.jira_content_provider import JIRAContentProvider, JiraPage

projects = [
    #{"product": "PROM", "accounts": [ "Progetto Prometheus", "Addendum - I" ]},
    #{"product": "I285", "accounts": [ "2019-11-01 - Innocenti 285", "I285 - Adendum Mailing ", "I285 - Addendum Rendicontazione" ]},
    {"product": "AWS", "accounts": [ "08_20180219_FB_InformaticaComTofani - Progetto Turni Lavoro",
                                     "09-20200406-CS-AIP-nuove sviluppi e canone di manutenzione v2",
                                     "AIP-Sprint 001"]}
]

jira: JIRAContentProvider = JIRAContentProvider("https://giuneco.atlassian.net", "matteo.milani@giuneco.it", "zDm2VCHLFWLJcESwXdea3AF3")

for project in projects:
    for account in project["accounts"]:
        projectTaskInAccount: JiraPage = jira.search(f'project = "{project["product"]}" AND Account = "{account}" ORDER BY created DESC')

        totalSeconds: int = 0
        for itm in projectTaskInAccount.items:
            totalSeconds += itm.timeSpent

        print(f'[{project["product"]}/{account}] Worked {projectTaskInAccount.total} tasks: {totalSeconds/60/60}h '
              f'spent, TotH/Tasks: {totalSeconds/projectTaskInAccount.total/60/60}')

    accountList: List[str] = []
    for account in project["accounts"]:
        accountList.append(f'Account != "{account}"')

    notInAccountSentence = " AND ".join(accountList)

    inWrongAccount: JiraPage = jira.search(f'project = "{project["product"]}" AND ({notInAccountSentence}) ORDER BY created DESC')
    for itm in inWrongAccount.items:
        print(f'Item {itm.key} of {project["product"]} is not in {project["accounts"]}')