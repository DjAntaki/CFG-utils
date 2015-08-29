from nltk import ChartParser
#from nltk.parse import RecursiveDescentParser
from itertools import product
from nltk import grammar

def all_accepted_under(cfg, length):
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


def accepted_lenght(cfg, x):
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
        r.append(_recognizes(parser, word.split())
    return r

def language_equals_under(cfg1, cfg2, length):
    """
    Compares accepted words under a given length accepted by context-free grammar 1 and context-free grammar 2. 
    
    cfg1 & cfg2 : nltk.grammar.CFG instances
    :return True if the they accept the same words, False if they do not.
    
    """
    return accepted_under_length_x(cfg1,length) == accepted_under_length_x(cfg2,length)

