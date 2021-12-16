from abc import ABC, abstractmethod
import random


class AbstractRandomize(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def randomize(self) -> str:
        pass


class FallbackRandomize(AbstractRandomize):
    def __init__(self, data):
        self.browsers = data['browsers']
        self.percents = data['percents']

    def randomize(self):
        return random.choices(self.browsers, self.percents)[0]


class ParsedRandomize(AbstractRandomize):
    def __init__(self, randomize_dict, browsers_dict):
        self.percents = randomize_dict['percents']
        self.browser_keys = randomize_dict['browsers']
        self.useragents = browsers_dict

    def randomize(self):
        key = random.choices(self.browser_keys, self.percents)[0]
        return random.choice(self.useragents[key])


class DataRandomize:

    def fallback(data) -> AbstractRandomize:
        return FallbackRandomize(data)

    def parsed(randomize_dict, browsers_dict) -> AbstractRandomize:
        return ParsedRandomize(randomize_dict, browsers_dict)
