from NER.rules.address import ADDR_PART
from yargy import Parser
import string
import re


class Address(dict):
    def __new__(cls, *args, **kwargs):
        self = dict.__new__(cls, *args, **kwargs)
        self.__dict__ = self
        return self


class NERAddressModel:
    def __init__(self):
        self.address_extractor = Parser(ADDR_PART)
        list_elem = ['city', 'city_type',
                     'street', 'street_type',
                     'house', 'house_type',
                     'corpus', 'corpus_type',
                     'apartment', 'apartment_type',
                     'building', 'building_type',
                     'flat', 'flat_type']
        self.empty_dict = dict(zip(list_elem, [None for elem in list_elem]))
        self.overall_dict = {}

    def predict(self, person):
        matches = [match for match in self.address_extractor.findall(person)]
        facts = [_.fact.as_json for _ in matches]
        for fact in facts:
            if len(fact) > len(self.overall_dict):
                self.overall_dict = {**self.overall_dict, **dict(fact)}
            else:
                self.overall_dict = {**dict(fact), **self.overall_dict}
            print(self.overall_dict)
        json_fact = Address({**self.empty_dict, **self.overall_dict})
        for key in json_fact:
            if json_fact[key] is not None:
                my_punctuation = re.sub('[-/]', '', string.punctuation)
                json_fact[key] = "".join(l for l in json_fact[key] if l not in my_punctuation)
        print(json_fact)
        return json_fact

