#!/usr/bin/python
# -*- coding: utf-8 -*-

from cfg_utils import *
from nltk import grammar

"""
Little script using nltk to create CFG grammars made for Pierre McKenzie.

Developped on python 3.4, i checked compatibility for python 2.7.

To see the functions associated with nltk.grammar.CFG :
http://www.nltk.org/api/nltk.html#nltk.grammar.CFG

"""


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

    grammar_rules = _rules_input(nonterminals, terminals)
    return grammar.CFG(start, grammar_rules)


def _rules_input(nonterminals, terminals):
    """
    Given a list of nonterminals and a list of terminals, this function creates a list of rules
    (aka grammar.Production instances) and returns it. There must be a whitespace between all terminals and nonterminals symbols. Extra whitespaces are ignored/conside.
    """
    print("You will now enter the rules of the grammar.")
    print("Rule must be respect the following format : ex. A -> b c|A b| ")
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


def CFG_prompt():
    """
    Interactive prompt to create a context-free grammar.

    This function return a nltk.grammar.CFG instance and also allow you to save your grammar.
    """

    reserved_token = ['start', '->', '', '|', '\\n', 'epsilon']
    print("")

    nonterminals = None

    while (True):
        try:
            print("Please enumerate all non-terminals symbols separated with commas.")
            print(
                "Whitespaces are ignored. The following symbols are forbidden : \'" + "\',\'".join(
                    reserved_token) + "\'")
            print("ex. \"V, W, X, Y, Z \"")
            x = input()
            nonterminals = x.replace(' ', '').split(',')

            if (any(y in reserved_token for y in nonterminals)):
                print("forbidden token used. please retry entering variables.")
                continue

        except Exception as e:
            print(str(type(e)) + " occured.")
            continue
        break

    nonterminals.append("start")
    nonterminals = {x: grammar.Nonterminal(x) for x in nonterminals}
    nonterminals_id = nonterminals.keys()
    print("Added non-terminal symbol \"start\"")
    print("Non-terminals states : " + str(nonterminals_id))

    terminals = None
    while (True):
        print("Please enumerate all terminal symbols separated with commas.")
        print("Same rules as non-terminals apply and symbol must be different. ex. \"a, b, c, d, e \"")
        #  try :
        x = input()
        terminals = set(x.replace(' ', '').split(','))
        assert all([i not in nonterminals_id and i not in reserved_token for i in terminals])

        # except Exception as e:
        #    print(str(type(e)) + " occured. Please retry.")
        #   continue
        break

    print("You will now enter the rules of the grammar.")
    print("Rule must be respect the following format : ex. Non-terminal-symbol -> symbol symbol | symbol | \'epsilon\'")
    print("Press enter when you are done.")
    grammar_rules = []
    while (True):
        try:
            x = input()

            if x == '':
                break
            elif '->' in x:

                x = x.split('->')
                left_hand_side = x[0].replace(' ', '')

                assert len(x) == 2
                assert left_hand_side in nonterminals_id  # .keys()? recuperer la non-terminal
                left_hand_side = nonterminals[left_hand_side]
                x[1] = x[1].split('|')
                for rhs in x[1]:
                    right_hand_side = []
                    for y in rhs.split(' '):
                        if y != '':  # to ignore multiples whitespace
                            if y in nonterminals_id:
                                right_hand_side.append(nonterminals[y])


                            elif y in terminals:
                                right_hand_side.append(y)
                            elif y == 'epsilon':
                                right_hand_side.append("")
                            else:
                                print(y + " is not a valid input...")
                                raise Exception

                    grammar_rules.append(grammar.Production(left_hand_side, right_hand_side))
            else:
                print("Invalid input. no \'->\'  in the input")

        except Exception as e:
            print("Exception happened. " + e.message)

    print(grammar_rules)
    print("Processing...")
    cfg = grammar.CFG(grammar.Nonterminal('start'), grammar_rules)

    print("Grammar created.")

    print("Do you wish to name and save that grammar? Enter the path you want for the file if you do, press enter if you don't.")
    x = input()
    if x != '':
        import pickle

        pickle.dump(cfg, open(x, 'wb'))
        print("Saved at " + x)
    return cfg

a = quickrompt()
print(a.productions() )
