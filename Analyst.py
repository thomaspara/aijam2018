#This is the v 1 of the translated code
#this does not include an implimented analyst
#since I found a python library with like 200 indicators
#that I want to learn instead of re-writing what I made.
# it's called ta-lib and i think uuusing that will make the dev time a lot shorter and give us more to work with
# I am also working on implimenting Zipline for our backtesting framework
# it's what quantopian uses and its robust.

#i made the decision to merge 'analyst and broker' and 'account and accountant' here
#as opposed to having seperate classes, it works out better that way in python
#also the logging is left unimplimented in account, we need to design that alongside the interface
import math
from abc import ABC, abstractmethod


class Analyst(ABC):

    buy_percent = 0.01
    min_percent = 0.001
    min_low = 100
    min_high = 1000

    def __init__(self, account):
        self.account = account
        super().__init__()

    def set_buy_param(self, buy_percent, min_percent, min_low, min_high):
        self.buy_percent = buy_percent
        self.min_percent = min_percent
        self.min_low = min_low
        self.min_high = min_high

    def trade(self):
        self.sell()
        self.buy()

    def sell(self):
        sellable_stocks = self.analyze_sell(self.account.get_positions)

        for stock in sellable_stocks:
            self.account.sell(stock)

    def buy(self):
        port_val = self.account.get_port_val()
        capital = self.account.get_capital()

        principal = port_val * self.buy_percent
        min_principal = self.get_min_prin(port_val)

        if principal < min_principal:
            principal = min_principal

        num_stocks_bought = math.floor(capital/principal)

        viable_stocks = self.analyze_buy()

        for i in (0,num_stocks_bought):
            self.account.buy(viable_stocks[i], principal)

    def get_min_prin(self,port_val):
        if port_val > self.min_high/self.min_low:
            return self.min_high
        elif self.min_low > self.min_percent * port_val:
            return self.min_low
        else:
            return self.min_percent * port_val

    @abstractmethod
    def analyze_sell(self, positions):
        pass

    @abstractmethod
    def analyze_buy(self):
        pass
