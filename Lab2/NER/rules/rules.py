from yargy import rule, and_, or_, not_
from yargy.interpretation import fact
from yargy.predicates import (gram, type, true, in_caseless, dictionary, eq,
                              caseless, bank, gte, lte, normalized, in_, length_eq)
from yargy.pipelines import morph_pipeline
from yargy.tokenizer import QUOTES
from natasha.data import FIRST, MAYBE_FIRST, LAST, load_dict
