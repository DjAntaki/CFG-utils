from nltk import ChartParser
#from nltk.parse import RecursiveDescentParser
from itertools import product
from nltk import grammar

"""
Some functions to quickly use nltk to create and test context-free grammars.

To see the functions associated with nltk.grammar.CFG :
htt://www.nltk.org/api/nltk.html#nltk.grammar.CFG

"""
#
# Functions to test accepted words
#
def accepted_under(cfg, length):
    """
    Returns a list of every accepted word of a context-free grammar under a given length.
    cfg : a nltk.grammar.CFG instance. 
    """
    terminals = _get_terminal_symbols(cfg)

    parser = ChartParser(cfg)
    accepted = []
    for x in range(1, length):
        for y in product(terminals, repeat=x):
            if _recognizes(parser, y):
                accepted.append(' '.join(y))
    return accepted


def accepted_length(cfg, x):
    """
    Returns a list of every accepted word of a context-free grammar with a specific length
    """
    terminals = _get_terminal_symbols(cfg)
    parser = ChartParser(cfg)
    accepted = []
    for y in product(terminals, repeat=x):
        if _recognizes(parser, y):
            accepted.append(' '.join(y))
    return accepted


def _recognizes(parser, word):
    """
    Returns True if the CFG accepts that word and False if it doesnt.

    parser : a nltk.parser instance for a cfg.
    word : a list of tokens
    """
    if len(list(parser.parse(word))) > 0:
        return True
    return False


def recognizes(cfg, word):
    """
    cfg : a nltk.grammar.CFG instance
    word : a string with tokens separated with spaces.

    A parser is created at every call of this function.
    """
    return _recognizes(ChartParser(cfg), word.split())

def recognizesAll(cfg, words):
    """
    Returns a list of boolean values corresponding to [recognizes(cfg,w) for w in words].
    cfg : a nltk.grammar.CFG instance
    words must be a list of string with tokens separated with spaces.

    """
    r = []
    parser = ChartParser(cfg)
    for word in words:
        r.append(_recognizes(parser, word.split()))
    return r

def language_equals_under(cfg1, cfg2, length):
    """
    Compares all accepted words under a given length accepted by context-free grammar 1 and context-free grammar 2.

    cfg1 & cfg2 : nltk.grammar.CFG instances
    :return True if the they accept the same words, False if they do not.

    """
    return accepted_under(cfg1,length) == accepted_under(cfg2,length)

#
#   Administrative-ish function
#

def _get_terminal_symbols(cfg):
    """
    Returns a set of all the terminal symbols used in a nltk context-free grammar.
    """
    terminal_symbols = set()
    for prod in cfg.productions():
        terminal_symbols.update(list(filter(lambda x: grammar.is_terminal(x), prod.rhs())))
    return terminal_symbols


def load_grammar(path):
    """
    Loads a nltk.CFG instance previously saved in binary with pickle at given path.
    """
    import pickle

    return pickle.load(open(path, 'rb'))


#
# Prompt and prompt-related functions
#

def quickprompt():
    """
    Interactive prompt to create a context-free grammar.

    This prompt assumes that the non-terminal symbols is the uppercase alphabet and that the terminal symbols is lowercase alphabet. You only input rules and starting state.
    """
    from string import ascii_lowercase, ascii_uppercase

    nonterminals = ascii_uppercase
    terminals = ascii_lowercase

    print("Non-terminal symbols : " + str(list(nonterminals)))
    print("Terminal symbols : " + str(list(terminals)))

    while True:
        x = input("Input starting symbol :")
        if x in nonterminals and len(x) == 1:
            start = grammar.Nonterminal(x)
            break
        else:
            print('Incorrect input.')

    grammar_rules = _rules_input_prompt(nonterminals, terminals)
    return grammar.CFG(start, grammar_rules)


def _rules_input_prompt(nonterminals, terminals):
    """
    Given a list of nonterminals and a list of terminals, this function creates a list of rules
    (aka grammar.Production instances) and returns it. There must be a whitespace between all terminals and nonterminals symbols. Extra whitespaces are ignored/conside.
    """
    print("You will now enter the rules of the grammar.")
    print("Rule must be respect the following format : "
          "\n 1. the two characters \"->\" are used for separating the right hand side from the left hand side"
          "\n 2. There must be a whitespace between all symbols in the grammar (including non-terminals)"
          "\n 3. The character \'|\' means \"or\" "
          "\n ex. A -> b c|A b|d")
    print("Press enter when you are done.")
    grammar_rules = []
    while (True):
        try:
            x = input()
            if x == '':
                break
            elif '->' in x:

                y = x.split('->')
                left_hand_side = y[0].replace(' ', '')

                assert len(y) == 2
                assert left_hand_side in nonterminals
                left_hand_side = grammar.Nonterminal(left_hand_side)
                y[1] = y[1].split('|')
                for rhs in y[1]:
                    right_hand_side = []
                    for y in rhs.split(' '):
                        if y != '':
                            if y in nonterminals:
                                right_hand_side.append(grammar.Nonterminal(y))


                            elif y in terminals:
                                right_hand_side.append(y)
                            else:
                                print(y + " is not a valid input.")
                                raise Exception

                    grammar_rules.append(grammar.Production(left_hand_side, right_hand_side))
            else:
                print("Invalid input. no \'->\'  in the input.")
                raise Exception

        except Exception as e:
            print("Invalid Input.")
            pass

    return grammar_rules
