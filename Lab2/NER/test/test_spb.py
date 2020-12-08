import unittest
from NER.natashka.address_extractor import NERAddressModel


class TestStreet(unittest.TestCase):
    def setUp(self):
        self.NERInstance = NERAddressModel()

    def test_1(self):
        testing_address = 'санкт-петербург школьная 20'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('санкт-петербург', None), (res.city, res.city_type))
        self.assertEqual(('школьная', None), (res.street, res.street_type))
        self.assertEqual(('20', None, None), (res.house, res.corpus, res.building))

    def test_2(self):
        testing_address = 'санкт-петербург юрия гагарина 22 к2'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('санкт-петербург', None), (res.city, res.city_type))
        self.assertEqual(('юрия гагарина', None), (res.street, res.street_type))
        self.assertEqual(('22', '2', None), (res.house, res.corpus, res.building))

    def test_3(self):
        testing_address = 'питер гагарина 22 к 2'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('санкт-петербург', None), (res.city, res.city_type))
        self.assertEqual(('гагарина', None), (res.street, res.street_type))
        self.assertEqual(('22', '2', None), (res.house, res.corpus, res.building))

    def test_4(self):
        testing_address = "санкт-петербург;юнтоловский 43 корпус 1"
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('санкт-петербург', None), (res.city, res.city_type))
        self.assertEqual(('юнтоловский', None), (res.street, res.street_type))
        self.assertEqual(('43', '1', None), (res.house, res.corpus, res.building))

    def test_5(self):
        testing_address = "санкт-петербург;юнтоловский 43 строение 1"
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('санкт-петербург', None), (res.city, res.city_type))
        self.assertEqual(('юнтоловский', None), (res.street, res.street_type))
        self.assertEqual(('43',  None, '1'), (res.house, res.corpus, res.building))

    def test_6(self):
        testing_address = "юнтоловский 43 ст 1"
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('юнтоловский', None), (res.street, res.street_type))
        self.assertEqual(('43',  None, '1'), (res.house, res.corpus, res.building))


if __name__ == '__main__':
    unittest.main()
