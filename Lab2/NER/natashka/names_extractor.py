from NER.rules.persons import NAME
from yargy import Parser


class Person(dict):
    def __new__(cls, *args, **kwargs):
        self = dict.__new__(cls, *args, **kwargs)
        self.__dict__ = self
        return self


class NERPersonModel:
    def __init__(self):
        self.names_extractor = Parser(NAME)
        self.empty_dict = {'first': None, 'last': None, 'middle': None}
        self.overall_dict = {}

    def predict(self, person):
        matches = [match for match in self.names_extractor.findall(person)]
        facts = [_.fact.as_json for _ in matches]
        for fact in facts:
            self.overall_dict = {**self.overall_dict, **dict(fact)}
        json_fact = Person({**self.empty_dict, **self.overall_dict})
        return json_fact

