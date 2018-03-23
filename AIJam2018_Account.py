import sys
import os


from abc import ABC, abstractmethod


class Account(ABC):

    funds = None  #total money on hand changes with buying and selling
    hold = None  #money not available for trading
    income = None  #realized gains and losses
    take_home_percent = None  #percent of income to take home, typicically arround 1-5%
    profit = None  #money set aside to withdraw for money, change with income
    taxes = None  #money set aside to withdraw for taxes, change with income
    capital = None  #funds for trading, funds - (profit + taxes + hold)

    def __init__(self, logger, hold, take_home_percent):
        self.logger = logger
        self.hold = hold
        self.take_home_percent = take_home_percent
        super().__init__()

        self.change_income()
        self.change_funds()
        self.change_capital()

    @abstractmethod
    def do_something(self):
        pass

    def sell(self, stock_name):
        self.sell_stock(stock_name)
        self.change_income()
        self.change_funds()
        self.change_capital()
        self.logger.log("info goes here")

    @abstractmethod
    def sell_stock(self, stock_name):
        pass

    def buy(self, stock_name, principal):
        self.buy_stock(stock_name, principal)
        self.change_funds()
        self.change_capital()
        self.logger.log("info goes here")

    @abstractmethod
    def buy_stock(self, stock_name, principal):
        pass

    def get_capital(self):
        return self.capital

    @abstractmethod
    #ask the account for its funds and positions
    def get_port_val(self):
        pass

    @abstractmethod
    #ask which stocks we have positions in
    def get_positions(self):
        pass

    #'mutator'
    def change_funds(self):
        self.funds = self.retrive_funds()

    @abstractmethod
    #getter, uses the account to ask the platform for the about of funds
    def retrive_funds(self):
        pass

    def change_capital(self):
        self.capital = self.funds - (self.taxes + self.profit + self.hold)

    def change_income(self):
        self.income = self.retrive_income()
        self.change_profit()
        self.change_taxes()

    #could use some refinement
    def change_profit(self):
        if self.income > 0 :
            self.profit = self.income * self.take_home_percent
        else:
            self.profit = 0

    def change_taxes(self):
        self.taxes = self.get_taxes(self.income)

    @abstractmethod
    # gets relized gains and losses from platform
    def retrive_income(self):
        pass

    @abstractmethod
    def get_taxes(self, income):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass