import unittest
from NER.natashka.address_extractor import NERAddressModel


class TestHome(unittest.TestCase):
    def setUp(self):
        self.NERInstance = NERAddressModel()

    def test_1(self):
        testing_address = 'проспект комсомольский 50'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((res.house, res.corpus, None), ('50', None, None))

    def test_2(self):
        testing_address = 'город липецк улица катукова 36 a'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((res.house, res.corpus, None), ('36 a', None, None))

    def test_3(self):
        testing_address = 'сургут улица рабочая дом 31а'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((res.house, res.corpus, None), ('31а', None, None))

    def test_4(self):
        testing_address = 'город липецк доватора 18'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((res.house, res.corpus, None), ('18', None, None))

    def test_5(self):
        testing_address = 'ну бехтеева 9 квартира 310'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((res.house, res.corpus, None), ('9', None, None))

    def test_6(self):
        testing_address = 'артема 32 квартира 8'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((res.house, res.corpus, None), ('32', None, None))

    def test_7(self):
        testing_address = 'город липецк полиграфическая дом 4'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((res.house, res.corpus, None), ('4', None, None))

    def test_8(self):
        testing_address = 'сколько стоит нет arkadata у нас есть москва каширское шоссе 55 корпус 1'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((res.house, res.corpus, None), ('55', '1', None))

    def test_9(self):
        testing_address = 'люберцы октябрьский проспект 10 корпус 1'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((res.house, res.corpus, None), ('10', '1', None))

    def test_10(self):
        testing_address = 'бульвар миттова 24'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((res.house, res.corpus, None), ('24', None, None))

    def test_11(self):
        testing_address = 'стол вы знаете москва алтуфьевское 78'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((res.house, res.corpus, None), ('78', None, None))


if __name__ == '__main__':
    unittest.main()
