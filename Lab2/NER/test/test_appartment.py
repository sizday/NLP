import unittest
from NER.natashka.address_extractor import NERAddressModel


class TestApartment(unittest.TestCase):
    def setUp(self):
        self.NERInstance = NERAddressModel()

    def test_1(self):
        testing_address = 'проспект комсомольский 50'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(res.apartment, None)

    def test_2(self):
        testing_address = 'город липецк улица катукова 36 a'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(res.apartment, None)

    def test_3(self):
        testing_address = 'сургут улица рабочая дом 31а'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(res.apartment, None)

    def test_4(self):
        testing_address = 'город липецк доватора 18'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(res.apartment, None)

    def test_5(self):
        testing_address = 'ну бехтеева 9 квартира 310'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(res.apartment, '310')

    def test_6(self):
        testing_address = 'Кусковская 19 корпус 1'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(res.apartment, None)

    def test_7(self):
        testing_address = 'марша захарова 12 маршала захарова дом 12'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(res.apartment, None)

    def test_8(self):
        testing_address = 'null'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(res.apartment, None)


if __name__ == '__main__':
    unittest.main()
