from NER.data.cities import SIMPLE_CITIES, COMPLEX_CITIES
from NER.data.positions import POSITIONS
from NER.rules.rules import *

AddrPart = fact(
    'AddrPart',
    ['city', 'city_type',
     'street', 'street_type',
     'house', 'house_type',
     'corpus', 'corpus_type',
     'apartment', 'apartment_type',
     'building', 'building_type']
)

DASH = eq('-')
DOT = eq('.')
SPACE = eq(' ')
ADJF = gram('ADJF')
NOUN = gram('NOUN')
INT = type('INT')
TITLE = true()

ANUM = rule(INT, DASH.optional(), in_caseless({
    'я', 'й', 'ая', 'ий', 'ой'
}))

COMPLEX = morph_pipeline(COMPLEX_CITIES)
SIMPLE = dictionary(SIMPLE_CITIES)

CITY_ABBR = in_caseless({
    'питер', 'спб', 'мск', 'нск', 'нн'
})

CITY_NAME = or_(
    rule(CITY_ABBR),
    rule(SIMPLE),
    COMPLEX
).interpretation(AddrPart.city)

SIMPLE = and_(
    TITLE,
    or_(NOUN, ADJF))
COMPLEX = or_(
    rule(SIMPLE, DASH.optional(), SIMPLE),
    rule(TITLE, DASH.optional(), caseless('на'), DASH.optional(), TITLE))
NAME = or_(
    rule(SIMPLE),
    COMPLEX)
MAYBE_CITY_NAME = or_(
    NAME,
    rule(NAME, '-', INT)
).interpretation(AddrPart.city)

CITY_WORDS = or_(
    rule(normalized('город')),
    rule(caseless('г'), DOT.optional())
).interpretation(AddrPart.city_type.const('город'))

CITY = or_(
    rule(CITY_WORDS.optional(), CITY_NAME)
).interpretation(AddrPart)

MODIFIER_WORDS_ = rule(
    dictionary({'большой', 'малый', 'средний', 'верхний', 'центральный', 'нижний', 'северный', 'дальний',
                'первый', 'второй', 'старый', 'новый', 'красный', 'лесной', 'тихий', 'зелёный'}),
    DASH.optional())

SHORT_MODIFIER_WORDS = rule(
    in_caseless({'больше', 'мало', 'средне', 'верх', 'верхне', 'центрально', 'нижне', 'северо', 'дальне',
                 'восточно', 'западно', 'перво', 'второ', 'старо', 'ново', 'красно', 'тихо', 'горно', }),
    DASH.optional())

MODIFIER_WORDS = or_(
    MODIFIER_WORDS_,
    SHORT_MODIFIER_WORDS)

LET_WORDS = or_(
    rule(caseless('лет')),
    rule(DASH.optional(), caseless('летия')))

LET_NAME = in_caseless({'влксм', 'ссср', 'алтая', 'башкирии', 'бурятии', 'дагестана', 'калмыкии', 'колхоза',
                        'комсомола', 'космонавтики', 'москвы', 'октября', 'пионерии', 'победы', 'приморья',
                        'района', 'совхоза', 'совхозу', 'татарстана', 'тувы', 'удмуртии', 'улуса', 'хакасии',
                        'целины', 'чувашии', 'якутии', })

LET = rule(INT, LET_WORDS, LET_NAME)

MONTH_WORDS = dictionary(
    {'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август',
     'сентябрь', 'октябрь', 'ноябрь', 'декабрь', })

ERROR = not_(normalized('ну'))
DAY = and_(INT, gte(1), lte(31))
YEAR = and_(INT, gte(1), lte(2100))
YEAR_WORDS = normalized('год')
DATE = or_(
    rule(DAY, MONTH_WORDS),
    rule(YEAR, YEAR_WORDS))
PART = and_(
    TITLE,
    or_(gram('Name'), gram('Surn')))

MAYBE_FIO = or_(
    rule(TITLE, PART),
    rule(PART, TITLE),
    rule(gram('Name'), gram('Surn')))

POSITION_WORDS = or_(
    rule(normalized('академик')),
    rule(dictionary(POSITIONS)),
    rule(normalized('генерал'), normalized('армия')),
    rule(normalized('герой'), normalized('россия')),
    rule(normalized('герой'), normalized('российский'), normalized('федерация')),
    rule(normalized('герой'), normalized('советский'), normalized('союз')))

MAYBE_PERSON = or_(
    MAYBE_FIO,
    rule(POSITION_WORDS, MAYBE_FIO))

IMENI_WORDS = or_(
    rule(caseless('им'), DOT.optional()),
    rule(caseless('имени')))
IMENI = rule(IMENI_WORDS.optional(), MAYBE_PERSON)

ROD = gram('gent')
SIMPLE = and_(
    or_(ADJF, and_(NOUN, ROD)),
    TITLE)
COMPLEX = or_(
    rule(and_(ADJF, TITLE), NOUN),
    rule(TITLE, DASH.optional(), TITLE))

EXCEPTION = dictionary({'арбат', 'варварка'})
MAYBE_NAME = or_(
    rule(SIMPLE),
    rule(EXCEPTION))

LET_NAME = or_(MAYBE_NAME, LET, DATE, IMENI)
MODIFIER_NAME = rule(MODIFIER_WORDS, NAME)
NAME = or_(
    LET_NAME,
    ANUM,
    rule(MODIFIER_NAME, ANUM),
    rule(ANUM, NAME))
ADDR_NAME = NAME

# улица
STREET_NAME = ADDR_NAME.interpretation(AddrPart.street)
STREET_WORDS = or_(
    rule(normalized('улица')),
    rule(caseless('ул'), DOT.optional())
).interpretation(AddrPart.street_type.const('улица'))
STREET = or_(
    rule(STREET_WORDS, STREET_NAME),
    rule(STREET_NAME, STREET_WORDS)
).interpretation(AddrPart)

# бульвар
BOULEVARD_WORDS = or_(
    rule(caseless('б'), '-', caseless('р')),
    rule(caseless('бул'), DOT.optional()),
    rule(normalized('бульвар'))
).interpretation(AddrPart.street_type.const('бульвар'))
BOULEVARD_NAME = ADDR_NAME.interpretation(AddrPart.street)
BOULEVARD = or_(
    rule(BOULEVARD_WORDS, BOULEVARD_NAME),
    rule(BOULEVARD_NAME, BOULEVARD_WORDS)
).interpretation(AddrPart)

# шоссе
HIGHWAY_WORDS = or_(
    rule(caseless('ш'), DOT),
    rule(normalized('шоссе'))
).interpretation(AddrPart.street_type.const('шоссе'))
HIGHWAY_NAME = ADDR_NAME.interpretation(AddrPart.street)
HIGHWAY = or_(
    rule(HIGHWAY_WORDS, HIGHWAY_NAME),
    rule(HIGHWAY_NAME, HIGHWAY_WORDS)
).interpretation(AddrPart)

# тракт
TRACT_WORDS = or_(
    rule(caseless('тр'), DOT),
    rule(normalized('тракт'))
).interpretation(AddrPart.street_type.const('тракт'))
TRACT_NAME = ADDR_NAME.interpretation(AddrPart.street)
TRACT = or_(
    rule(TRACT_WORDS, TRACT_NAME),
    rule(TRACT_NAME, TRACT_WORDS)
).interpretation(AddrPart)

# гай
GAI_WORDS = rule(normalized('гай'))
GAI_NAME = ADDR_NAME
GAI = or_(
    rule(GAI_WORDS, GAI_NAME),
    rule(GAI_NAME, GAI_WORDS)
).interpretation(AddrPart.street)

# вал
VAL_WORDS = rule(normalized('вал'))
VAL_NAME = ADDR_NAME
VAL = or_(
    rule(VAL_WORDS, VAL_NAME),
    rule(VAL_NAME, VAL_WORDS)
).interpretation(AddrPart.street)

# проспект
AVENUE_WORDS = or_(
    rule(in_caseless({'пр', 'просп'}), DOT.optional()),
    rule(caseless('пр'), '-', in_caseless({'кт', 'т'}), DOT.optional()),
    rule(normalized('проспект'))
).interpretation(AddrPart.street_type.const('проспект'))
AVENUE_NAME = ADDR_NAME.interpretation(AddrPart.street)
AVENUE = or_(
    rule(AVENUE_WORDS, AVENUE_NAME),
    rule(AVENUE_NAME, AVENUE_WORDS)
).interpretation(AddrPart)

# микрорайон
DISTRICT_WORDS = or_(
    rule(in_caseless({'мк', 'мкр'}), DOT.optional()),
    rule(caseless('мк'), '-', in_caseless({'рн', 'н'}), DOT.optional()),
    rule(normalized('микрорайон'))
).interpretation(AddrPart.street_type.const('микрорайон'))
DISTRICT_NAME = ADDR_NAME.interpretation(AddrPart.street)
DISTRICT = or_(
    rule(DISTRICT_WORDS, DISTRICT_NAME),
    rule(DISTRICT_NAME, DISTRICT_WORDS)
).interpretation(AddrPart)

# проезд
DRIVEWAY_WORDS = or_(
    rule(normalized('проезд')),
    rule(caseless('пр'), DOT.optional()),
    rule(caseless('пр'), '-', in_caseless({'зд', 'д'}), DOT.optional())
).interpretation(AddrPart.street_type.const('проезд'))
DRIVEWAY_NAME = ADDR_NAME.interpretation(AddrPart.street)
DRIVEWAY = or_(
    rule(DRIVEWAY_NAME, DRIVEWAY_WORDS),
    rule(DRIVEWAY_WORDS, DRIVEWAY_NAME)
).interpretation(AddrPart)

# переулок
ALLEYWAY_WORDS = or_(
    rule(caseless('п'), DOT),
    rule(caseless('пер'), DOT.optional()),
    rule(normalized('переулок'))
).interpretation(AddrPart.street_type.const('переулок'))

ALLEYWAY_NAME = ADDR_NAME.interpretation(AddrPart.street)
ALLEYWAY = or_(
    rule(ALLEYWAY_WORDS, ALLEYWAY_NAME),
    rule(ALLEYWAY_NAME, ALLEYWAY_WORDS)
).interpretation(AddrPart)


# площадь
SQUARE_WORDS = or_(
    rule(caseless('пл'), DOT.optional()),
    rule(normalized('площадь'))
).interpretation(AddrPart.street_type.const('площадь'))
SQUARE_NAME = ADDR_NAME.interpretation(AddrPart.street)
SQUARE = or_(
    rule(SQUARE_WORDS, SQUARE_NAME),
    rule(SQUARE_NAME, SQUARE_WORDS)
).interpretation(AddrPart)

# набережная
EMBANKMENT_WORDS = or_(
    rule(caseless('наб'), DOT.optional()),
    rule(normalized('набережная'))
).interpretation(AddrPart.street_type.const('набережная'))
EMBANKMENT_NAME = ADDR_NAME.interpretation(AddrPart.street)
EMBANKMENT = or_(
    rule(EMBANKMENT_WORDS, EMBANKMENT_NAME),
    rule(EMBANKMENT_NAME, EMBANKMENT_WORDS)
).interpretation(AddrPart)

LETTER = in_caseless(set('абвгдежзиклмнопрстуфхшщэюя'))
QUOTE = in_(QUOTES)
LETTER = or_(
    rule(LETTER),
    rule(QUOTE, LETTER, QUOTE))
SEP = in_(r' /\-')
VALUE = or_(
    rule(INT, SEP, LETTER),
    rule(INT, SPACE, LETTER),
    rule(INT, LETTER),
    rule(INT),
    rule(INT, SEP, INT))
ADDR_VALUE = rule(eq('№').optional(), VALUE)

# дом
HOUSE_EXCEPTION = or_(
    rule(normalized('дом дом')),
    rule(normalized('номер'))
)
HOUSE_WORDS = or_(
    rule(normalized('дом'), HOUSE_EXCEPTION.optional()),
    rule(caseless('д'), DOT)
).interpretation(AddrPart.house_type.const('дом'))
HOUSE_VALUE = ADDR_VALUE.interpretation(AddrPart.house)
HOUSE = rule(HOUSE_WORDS, HOUSE_VALUE).interpretation(AddrPart)

# квартира
APARTMENT_WORDS = or_(
    rule(in_caseless('кв'), DOT.optional()),
    rule(normalized('квартира'))
).interpretation(AddrPart.corpus_type.const('корпус'))
APARTMENT_VALUE = ADDR_VALUE.interpretation(AddrPart.apartment)
APARTMENT = or_(
    rule(APARTMENT_WORDS, APARTMENT_VALUE),
    rule(APARTMENT_VALUE, APARTMENT_WORDS)
).interpretation(AddrPart)

# корпус
CORPUS_WORDS = or_(
    rule(in_caseless({'к', 'корп', 'кор'}), DOT.optional()),
    rule(normalized('корпус'))
).interpretation(AddrPart.corpus_type.const('корпус'))
CORPUS_VALUE = ADDR_VALUE.interpretation(AddrPart.corpus)
CORPUS = rule(CORPUS_WORDS, CORPUS_VALUE).interpretation(AddrPart)

# строение
BUILDING_WORDS = or_(
    rule(in_caseless({'ст'}), DOT.optional()),
    rule(normalized('строение'))
).interpretation(AddrPart.building_type.const('строение'))
BUILDING_VALUE = ADDR_VALUE.interpretation(AddrPart.building)
BUILDING = rule(BUILDING_WORDS, BUILDING_VALUE).interpretation(AddrPart)

DOM_STREET = rule(
    CITY.optional(),
    or_(HIGHWAY, STREET, STREET_NAME, AVENUE,
        DRIVEWAY, TRACT, SQUARE, EMBANKMENT,
        BOULEVARD, DISTRICT, GAI, VAL, ALLEYWAY),
    HOUSE_WORDS.optional(),
    HOUSE_VALUE
).interpretation(AddrPart)

VALUE_HOUSE = rule(INT).interpretation(AddrPart.house)

NUMBER_HOUSE = rule(
    rule(normalized('номер')),
    VALUE_HOUSE
).interpretation(AddrPart)

DOUBLE_HOUSE = rule(
    rule(normalized('дом')),
    VALUE_HOUSE
).interpretation(AddrPart)


DOM_APARTMENT = rule(HOUSE_VALUE, APARTMENT_VALUE).interpretation(AddrPart)

ADDR_PART = or_(
    NUMBER_HOUSE, DOUBLE_HOUSE, DOM_STREET, DOM_APARTMENT, CITY, STREET, DRIVEWAY, ALLEYWAY,
    SQUARE, HIGHWAY, TRACT, EMBANKMENT, VAL, GAI,
    BOULEVARD, DISTRICT, CORPUS, APARTMENT, BUILDING
).interpretation(AddrPart)
