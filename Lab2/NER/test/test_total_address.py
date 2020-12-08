import unittest
from NER.natashka.address_extractor import NERAddressModel


class TestStreet(unittest.TestCase):
    def setUp(self):
        self.NERInstance = NERAddressModel()

    def test_1(self):
        testing_address = 'проспект комсомольский 50'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('комсомольский', 'проспект'), (res.street, res.street_type))
        self.assertEqual(('50', None, None), (res.house, res.corpus, res.building))

    def test_2(self):
        testing_address = 'город липецк улица катукова 36 a'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('липецк', 'город'), (res.city, res.city_type))
        self.assertEqual(('катукова', 'улица'), (res.street, res.street_type))
        self.assertEqual(('36 a', None, None), (res.house, res.corpus, res.building))

    def test_3(self):
        testing_address = 'сургут улица рабочая дом 31а'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('сургут', None), (res.city, res.city_type))
        self.assertEqual(('рабочая', 'улица'), (res.street, res.street_type))
        self.assertEqual(('31а', None, None), (res.house, res.corpus, res.building))

    def test_4(self):
        testing_address = 'город липецк доватора 18'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('липецк', 'город'), (res.city, res.city_type))
        self.assertEqual(('доватора', None), (res.street, res.street_type))
        self.assertEqual(('18', None, None), (res.house, res.corpus, res.building))

    def test_5(self):
        testing_address = 'ну бехтеева 9 квартира 310'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((None, None), (res.city, res.city_type))
        self.assertEqual(('бехтеева', None), (res.street, res.street_type))
        self.assertEqual(('9', None, None), (res.house, res.corpus, res.building))
        self.assertEqual('310', res.apartment)

    def test_6(self):
        testing_address = 'московская 34б'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((None, None), (res.city, res.city_type))
        self.assertEqual(('московская', None), (res.street, res.street_type))
        self.assertEqual(('34б', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment)

    def test_7(self):
        testing_address = 'улица минина дом 1'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((None, None), (res.city, res.city_type))
        self.assertEqual(('минина', 'улица'), (res.street, res.street_type))
        self.assertEqual(('1', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment)

    def test_8(self):
        testing_address = 'сколько улица 30 лет победы 50 46'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((None, None), (res.city, res.city_type))
        self.assertEqual(('30 лет победы', 'улица'), (res.street, res.street_type))
        self.assertEqual(('50', None, None), (res.house, res.corpus, res.building))
        self.assertEqual('46', res.apartment)

    def test_9t(self):
        testing_address = 'тюменский тракт 10'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((None, None), (res.city, res.city_type))
        self.assertEqual(('тюменский', 'тракт'), (res.street, res.street_type))
        self.assertEqual(('10', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment)

    def test_10(self):
        testing_address = 'береговая 43 береговая 43 сургут'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('сургут', None), (res.city, res.city_type))
        self.assertEqual(('береговая', None), (res.street, res.street_type))
        self.assertEqual(('43', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment)

    def test_11(self):
        testing_address = 'сургут югорская 30/2'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('сургут', None), (res.city, res.city_type))
        self.assertEqual(('югорская', None), (res.street, res.street_type))
        self.assertEqual(('30/2', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment)

    def test_12(self):
        testing_address = 'индекс 12 мне вот этого не надо'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((None, None), (res.city, res.city_type))
        self.assertEqual((None, None), (res.street, res.street_type))
        self.assertEqual((None, None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment,)

    def test_13(self):
        testing_address = 'город сургут улица фармана салманова 4'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('сургут', 'город'), (res.city, res.city_type))
        self.assertEqual(('фармана салманова', 'улица'), (res.street, res.street_type))
        self.assertEqual(('4', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment,)

    def test_14(self):
        testing_address = 'зеленые аллеи город видное дом 8'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('видное', 'город'), (res.city, res.city_type))
        self.assertEqual(('зеленые аллеи', None), (res.street, res.street_type))
        self.assertEqual(('8', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment,)

    def test_15(self):
        testing_address = 'зелинского улица зелинского дом 2'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((None, None), (res.city, res.city_type))
        self.assertEqual(('зелинского', 'улица'), (res.street, res.street_type))
        self.assertEqual(('2', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment,)

    def test_16(self):
        testing_address = 'Кусковская 19 корпус 1 '
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((None, None), (res.city, res.city_type))
        self.assertEqual(('Кусковская', None), (res.street, res.street_type))
        self.assertEqual(('19', '1', None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment)

    def test_17(self):
        testing_address = 'москва щелковское шоссе 35'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('москва', None), (res.city, res.city_type))
        self.assertEqual(('щелковское', 'шоссе'), (res.street, res.street_type))
        self.assertEqual(('35', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment, )

    def test_18(self):
        testing_address = 'город москва марьинский парк дом 25 корпус 2'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('москва', 'город'), (res.city, res.city_type))
        self.assertEqual(('марьинский парк', None), (res.street, res.street_type))
        self.assertEqual(('25', '2', None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment, )

    def test_19(self):
        testing_address = 'старый гай 1 корпус 2'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('старый гай', None), (res.street, res.street_type))
        self.assertEqual(('1', '2', None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment,)

    def test_20(self):
        testing_address = 'улица 3 почтовое отделение дом 62'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual((None, None), (res.city, res.city_type))
        self.assertEqual(('3 почтовое отделение', 'улица'), (res.street, res.street_type))
        self.assertEqual(('62', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment, )

    def test_21(self):
        testing_address = 'нижний новгород улица июльских дней 19'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('нижний новгород', None), (res.city, res.city_type))
        self.assertEqual(('июльских дней', 'улица'), (res.street, res.street_type))
        self.assertEqual(('19', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment)

    def test_22(self):
        testing_address = 'так москва хамовнический вал но я думаю что я еще обсужу со своими домашними то есть вот у '\
                          'нас цифровое телевидение есть но акадо вот вы не спешите я тогда вам наберу но либо в ' \
                          'приложения '
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('москва', None), (res.city, res.city_type))
        self.assertEqual(('хамовнический вал', None), (res.street, res.street_type))
        self.assertEqual((None, None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment, )

    def test_23(self):
        testing_address = 'город сургут улица семена билецкого 1'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('сургут', 'город'), (res.city, res.city_type))
        self.assertEqual(('семена билецкого', 'улица'), (res.street, res.street_type))
        self.assertEqual(('1', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(None, res.apartment)

    def test_24(self):
        testing_address = 'улица значит антонова овсиенко дом 19/2'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('антонова овсиенко', 'улица'), (res.street, res.street_type))
        self.assertEqual(('19/2', None, None), (res.house, res.corpus, res.building))

    def test_25(self):
        testing_address = 'улица генерала армии епишева дом 9'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('генерала армии епишева', 'улица'), (res.street, res.street_type))
        self.assertEqual(('9', None, None), (res.house, res.corpus, res.building))

    def test_26(self):
        testing_address = 'улица академика байкова дом 9'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('9', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(('академика байкова', 'улица'), (res.street, res.street_type))

    def test_27(self):
        testing_address = 'улица академика байкова дом дом дом 9'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('9', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(('академика байкова', 'улица'), (res.street, res.street_type))

    def test_28(self):
        testing_address = 'улица подзаборного байкова дом дом дом 9'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('9', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(('подзаборного байкова', 'улица'), (res.street, res.street_type))

    def test_29(self):
        testing_address = 'улица монтажника байкова дом дом дом 9'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('9', None, None), (res.house, res.corpus, res.building))
        self.assertEqual(('монтажника байкова', 'улица'), (res.street, res.street_type))

    def test_30(self):
        testing_address = 'такзначит у меня дом номер 12 а улица джона рида'
        res = self.NERInstance.predict(testing_address)
        self.assertEqual(('джона рида', 'улица'), (res.street, res.street_type))
        self.assertEqual(('12', None, None), (res.house, res.corpus, res.building))


if __name__ == '__main__':
    unittest.main()
