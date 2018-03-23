from abc import ABC, abstractmethod

class Analyst(ABC):

    name= None

    def __init__(self, name):
        self.name = name
        super().__init__()

    @abstractmethod
    def get_price(self):
        pass

    @abstractmethod
    def get_hist_prices(self, freq, period):
        pass

    #add in additional information retreval as needed