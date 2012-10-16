from __future__ import division
import itertools

class Answer(object):
    def __init__(self, complement = None):
        if complement is None:
            self.c = Answer(complement = self)
        else:
            self.c = complement

class Survey(object):
    def __init__(self, answers, data):
        self.data = dict()
        # Turn the keys into sets so that order won't matter
        for key, value in data.items():
            self.data.update({frozenset(key): value})

        self.answers = answers

    def p(self, answers, background):
        # Numerator conjunction
        n_conj = frozenset(answers).union(frozenset(background))

        # Denominator conjunction
        d_conj = frozenset(background)

        # Find number of people who answered with the conjunction in the
        # numberator of the conditional probability, by summing up the
        # the number of people whose complete answers were a conjunction
        # in the set of complete answer conjunctions whose disjunction
        # is the numerator conjunction
        # s_conj stands for "state conjunction": that is, a conjunction
        # that contains, for every answer, either the anwer itself
        # or its negation
        n_people = sum(self.data[s_conj] \
                       for s_conj in fill(n_conj, self.answers))
        # Same for the denominator
        d_people = sum(self.data[s_conj] \
                       for s_conj in fill(d_conj, self.answers))

        # Return the conditional probability
        return n_people/d_people
        

def fill(partial, complete):
    # Convert to sets:
    partial = set(partial)
    complete = set(complete)

    answers_incorporated = list(partial)
    partial_states = [partial]
    next_partial_states = list()
    # Find what propositions from complete do not have themselves or their
    # negation in partial
    difference = set()
    for answer in complete:
        if answer not in partial and answer.c not in partial:
            difference.add(answer)

    # Fill out the conjunction "partial" into a list of state
    # conjunctions whose union is "partial"
    for i in difference:
        for j in partial_states:
            next_partial_states.append(j.union({i}))
            next_partial_states.append(j.union({i.c}))
        partial_states = next_partial_states
        next_partial_states = list()

    # Return frozensets, since the keys to the mapping from conjunctions
    # to probabilities are frozensets
    return [frozenset(i) for i in partial_states]

O = Answer()
I = Answer()
E = Answer()
name = {O: 'overweight',
       O.c: 'not overweight',
       I: 'reads lots of internet',
       I.c: "doesn't read much internet",
       E: 'exercises',
       E.c: "doesn't excercise"}
def display(conj):
    return '  '.join(name[answer] for answer in conj)

x = {O}
y = {O, I, E}
# From Yudkowsky's "Causal Diagrams" post:
data_dict = {frozenset({O  , E  , I  }): 1119,
             frozenset({O  , E  , I.c}): 16104,
             frozenset({O  , E.c, I  }): 11121,
             frozenset({O  , E.c, I.c}): 60032,
             frozenset({O.c, E  , I  }): 18102,
             frozenset({O.c, E  , I.c}): 132111,
             frozenset({O.c, E.c, I  }): 29120,
             frozenset({O.c, E.c, I.c}): 155033}
data = Survey({O, E, I}, data_dict)

