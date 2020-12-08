from NER.rules.rules import *

Name = fact(
    'Name',
    ['first', 'last', 'middle']
)

TITLE = true()

ABBR = gram('Abbr')
LEN = or_(length_eq(3), length_eq(4), length_eq(5), length_eq(6), length_eq(7),
          length_eq(8), length_eq(9), length_eq(10), length_eq(11), length_eq(12),
          length_eq(13), length_eq(14), length_eq(15), length_eq(16), length_eq(17))
NAME = and_(gram('Name'), not_(ABBR), LEN)
PATR = and_(gram('Patr'), not_(ABBR), LEN)
SURN = and_(gram('Surn'), LEN)

FIRST = NAME.interpretation(Name.first)
FIRST_ABBR = and_(ABBR, TITLE).interpretation(Name.first)
LAST = SURN.interpretation(Name.last)
MAYBE_LAST = and_(TITLE, not_(ABBR), LEN).interpretation(Name.last)
MIDDLE = PATR.interpretation(Name.middle)
MIDDLE_ABBR = and_(ABBR, TITLE).interpretation(Name.middle)

FIRST_LAST = rule(FIRST, MAYBE_LAST)
LAST_FIRST = rule(MAYBE_LAST, FIRST)
ABBR_FIRST_LAST = rule(FIRST_ABBR, '.', MAYBE_LAST)
LAST_ABBR_FIRST = rule(MAYBE_LAST, FIRST_ABBR, '.')
ABBR_FIRST_MIDDLE_LAST = rule(FIRST_ABBR, '.', MIDDLE_ABBR, '.', MAYBE_LAST)
LAST_ABBR_FIRST_MIDDLE = rule(MAYBE_LAST, FIRST_ABBR, '.', MIDDLE_ABBR, '.')

FIRST_MIDDLE = rule(FIRST, MIDDLE)
FIRST_MIDDLE_LAST = rule(FIRST, MIDDLE, LAST)
LAST_FIRST_MIDDLE = rule(LAST, FIRST, MIDDLE)

SINGLE_FIRST = FIRST
SINGLE_LAST = LAST
SINGLE_MIDDLE = MIDDLE

NAME = or_(
    LAST_FIRST_MIDDLE,
    FIRST_MIDDLE_LAST,
    FIRST_MIDDLE,
    FIRST_LAST,
    LAST_FIRST,

    ABBR_FIRST_LAST,
    LAST_ABBR_FIRST,
    ABBR_FIRST_MIDDLE_LAST,
    LAST_ABBR_FIRST_MIDDLE,
    SINGLE_LAST,
    SINGLE_MIDDLE,
    SINGLE_FIRST
).interpretation(Name)
