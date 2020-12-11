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
INTJ = gram('INTJ')
ROD = gram('gent')
TITLE = true()

ANUM = rule(INT, DASH.optional(), in_caseless({
    'я', 'й', 'ая', 'ий', 'ой', 'ое'
}))

COMPLEX = morph_pipeline(COMPLEX_CITIES)
SIMPLE = dictionary(SIMPLE_CITIES)

CITY_NAME_EXCEPTION = rule(normalized('сургут')).interpretation(AddrPart.city.const('сургут'))
CITY_NAME = or_(
    rule(SIMPLE),
    COMPLEX,
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
    rule(CITY_NAME),
    rule(CITY_WORDS, CITY_NAME),
    rule(CITY_NAME, CITY_WORDS)
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

DAY = and_(INT, gte(1), lte(31))
YEAR = and_(INT, gte(1), lte(2100))
YEAR_WORDS = normalized('год')
DATE = or_(
    rule(DAY, MONTH_WORDS),
    rule(ADJF, normalized('дней')),
    rule(YEAR, YEAR_WORDS))

TITLE_RULE = and_(
    TITLE,
    not_(INT),
    not_(INTJ),
    not_(length_eq(3)),
    not_(normalized('проезд')),
    not_(normalized('видный')),
    not_(normalized('крылова')),
    not_(normalized('питер'))
)

PART = and_(
    TITLE_RULE,
    or_(gram('Name'), gram('Surn')))

MAYBE_FIO = or_(
    rule(gram('Surn')),
    rule(gram('Name')),
    rule(gram('Surn'), gram('Surn')),
    rule(TITLE_RULE, PART),
    rule(PART, TITLE_RULE),
)

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

SIMPLE = and_(
    or_(ADJF, and_(NOUN, ROD)),
    TITLE_RULE)
COMPLEX = or_(
    rule(and_(ADJF, TITLE_RULE), NOUN),
    rule(TITLE_RULE, DASH.optional(), TITLE_RULE))

EXCEPTION = dictionary({'арбат', 'варварка'})
MAYBE_NAME = or_(
    rule(SIMPLE),
    rule(EXCEPTION))

MAIL_STREET = rule(INT, ADJF, NOUN)

GARDEN_EXCEPTION = rule(normalized('парковая')).interpretation(AddrPart.street.const('парковая'))

LET_NAME = or_(MAYBE_NAME, LET, DATE, IMENI)
MODIFIER_NAME = rule(MODIFIER_WORDS, NOUN)
NAME = or_(
    LET_NAME,
    MODIFIER_NAME,
    MAIL_STREET,
    # ANUM,
    # rule(MODIFIER_NAME, ANUM),
    # rule(ANUM, NAME)
)
ADDR_NAME = NAME

CITY_NAME_ABBR = rule(normalized('питер')).interpretation(AddrPart.city.const('санкт-петербург'))
SBP_NAME = LET_NAME.interpretation(AddrPart.street)
SPB_STREET = rule(CITY_NAME_ABBR, SBP_NAME).interpretation(AddrPart)

# улица
STREET_NAME = ADDR_NAME.interpretation(AddrPart.street)
STREET_WORDS = or_(
    rule(normalized('улица')),
    rule(normalized('улица'), normalized('значит')),
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

# аллея
ALLEY_WORDS = rule(normalized('аллеи')).interpretation(AddrPart.street_type.const('аллеи'))
ALLEY_NAME = ADDR_NAME.interpretation(AddrPart.street)
ALLEY = rule(ALLEY_NAME, ALLEY_WORDS).interpretation(AddrPart)

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
    rule(caseless('пр'), DOT.optional())
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

LETTER = in_('aбвгдежзиклмнопрстуфхшщэюя')
QUOTE = in_(QUOTES)
LETTER = or_(
    rule(LETTER),
    rule(QUOTE, LETTER, QUOTE))
SEP = in_(r' /\-')
VALUE = or_(
    # rule(INT, SEP, LETTER),
    rule(INT, LETTER),
    rule(INT, SPACE, LETTER),

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


STREET_HOUSE_CORPUS = rule(
    CITY.optional(),
    or_(HIGHWAY, STREET, STREET_NAME, AVENUE,
        DRIVEWAY, TRACT, SQUARE, EMBANKMENT, ALLEY,
        BOULEVARD, DISTRICT, GAI, VAL, ALLEYWAY),
    HOUSE_WORDS.optional(),
    HOUSE_VALUE,
    CORPUS_WORDS,
    CORPUS_VALUE
).interpretation(AddrPart)

HOUSE_CORPUS = rule(
    HOUSE_VALUE,
    CORPUS_WORDS,
    CORPUS_VALUE
).interpretation(AddrPart)

HOUSE_BUILDING = rule(
    CITY.optional(),
    or_(HIGHWAY, STREET, STREET_NAME, AVENUE,
        DRIVEWAY, TRACT, SQUARE, EMBANKMENT, ALLEY,
        BOULEVARD, DISTRICT, GAI, VAL, ALLEYWAY),
    HOUSE_WORDS.optional(),
    HOUSE_VALUE,
    BUILDING_WORDS,
    BUILDING_VALUE
).interpretation(AddrPart)

HOUSE_STREET = rule(
    CITY.optional(),
    or_(HIGHWAY, STREET, STREET_NAME, AVENUE,
        DRIVEWAY, TRACT, SQUARE, EMBANKMENT, ALLEY,
        BOULEVARD, DISTRICT, GAI, VAL, ALLEYWAY),
    HOUSE_WORDS.optional(),
    HOUSE_VALUE
).interpretation(AddrPart)


VALUE_HOUSE = rule(INT).interpretation(AddrPart.house)

NUMBER_HOUSE = rule(
    rule(normalized('номер')),
    VALUE_HOUSE
).interpretation(AddrPart)


TRIPLE_HOUSE = rule(
    rule(normalized('дом')),
    rule(normalized('дом')),
    rule(normalized('дом')),
    VALUE_HOUSE
).interpretation(AddrPart)


DOM_APARTMENT = rule(HOUSE_VALUE, APARTMENT_VALUE).interpretation(AddrPart)

ADDR_PART = or_(
    SPB_STREET, GARDEN_EXCEPTION, CITY_NAME_EXCEPTION, CITY, NUMBER_HOUSE, HOUSE_CORPUS, HOUSE_BUILDING, TRIPLE_HOUSE,
    HOUSE_STREET, DOM_APARTMENT, STREET, DRIVEWAY, ALLEYWAY, SQUARE, HIGHWAY, TRACT, EMBANKMENT, VAL, GAI, ALLEY, HOUSE,
    STREET_HOUSE_CORPUS, HOUSE_BUILDING, BOULEVARD, DISTRICT, CORPUS, APARTMENT, BUILDING
).interpretation(AddrPart)
