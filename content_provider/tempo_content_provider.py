import json
from enum import Enum

import requests

from typing import List, Dict

class AccountCategory(Enum):
    TimeAndMaterial=1,
    FixedPrice=2,
    Canone=3

    @staticmethod
    def parse(value: str) -> 'AccountCategory':
        if value == 'TIMEANDMAT':
            return AccountCategory.TimeAndMaterial
        if value == 'FIXED':
            return AccountCategory.FixedPrice
        if value == 'CANONE':
            return AccountCategory.Canone

        raise ValueError(f"Invalid enum value found: {value}")


class TempoAccountItem:
    def __init__(self) -> None:
        self.apiLink: str
        self.key: str
        self.id: int
        self.name: str
        self.status: str
        self.categoryApiLink: str
        self.categoryId: int
        self.categoryKey: AccountCategory
        self.categoryName: str
        self.customerApiLink: str
        self.customerKey: str
        self.customerName: str


class TempoAccounts:
    def __init__(self) -> None:
        self._accounts: List[TempoAccountItem] = []
        self._categoryMap: Dict[AccountCategory, List[TempoAccountItem]] = {AccountCategory.TimeAndMaterial: [],
                                                                            AccountCategory.FixedPrice: [],
                                                                            AccountCategory.Canone: []}

    def add(self, itm: TempoAccountItem) -> None:
        self._categoryMap[itm.categoryKey].append(itm)
        self._accounts.append(itm)

    def accounts(self) -> List[TempoAccountItem]:
        return self._accounts

    def accountsInCategory(self, category: AccountCategory) -> List[TempoAccountItem]:
        return self._categoryMap[category]

    def account(self, id: int) -> TempoAccountItem:
        for account in self._accounts:
            if account.id == id:
                return account

        raise ValueError(f"No account with id: {id}")

    def containsId(self, category: AccountCategory, id: int) -> bool:
        for account in self._categoryMap[category]:
            if account.id == id:
                return True

        return False

    def len(self) -> int:
        return len(self._accounts)

    def isValid(self) -> bool:
        partedLen: int = 0
        partedLen += len(self.accountsInCategory(AccountCategory.TimeAndMaterial))
        partedLen += len(self.accountsInCategory(AccountCategory.FixedPrice))
        partedLen += len(self.accountsInCategory(AccountCategory.Canone))

        return partedLen == self.len()


class TempoContentProvider:
    def __init__(self, authToken: str) -> None:
        self.__authToken: str = authToken

    def accounts(self) -> TempoAccounts:
        myResponse = requests.get("https://api.tempo.io/core/3/accounts", headers={f"Authorization":f"Bearer {self.__authToken}"})
        myResponse.raise_for_status()  # Se call KO: raise exception

        jDoc = json.loads(myResponse.content)
        #print(json.dumps(jDoc, indent=2))

        accounts: TempoAccounts = TempoAccounts()
        for res in jDoc["results"]:
            itm: TempoAccountItem = TempoAccountItem()
            itm.apiLink         =  res["self"]
            itm.key             =  res["key"]
            itm.id              =  res["id"]
            itm.name            =  res["name"]
            itm.status          =  res["status"]
            itm.categoryApiLink =  res["category"]["self"]
            itm.categoryId      =  res["category"]["id"]
            itm.categoryKey     =  AccountCategory.parse(res["category"]["key"])
            itm.categoryName    =  res["category"]["name"]
            itm.customerApiLink =  res["customer"]["self"]
            itm.customerKey     =  res["customer"]["key"]
            itm.customerName    =  res["customer"]["name"]
            accounts.add(itm)

        return accounts
