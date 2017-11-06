import json
import operator
from utils import sort

class Letter:

    def __init__(self, from_letter, frequency):
        self.letter = from_letter
        self.candidates = {}
        self.candidates_probability = {
            'a': 100, 'b': 100, 'c': 100, 'd': 100, 'e': 100, 'f': 100, 'g': 100, 'h': 100,
            'i': 100, 'j': 100, 'k': 100, 'l': 100, 'm': 100, 'n': 100, 'o': 100, 'p': 100,
            'q': 100, 'r': 100, 's': 100, 't': 100, 'u': 100, 'v': 100, 'w': 100, 'x': 100,
            'y': 100, 'z': 100}
        self.solution = '_'
        self.score = frequency
        self.frequency = 0

    def set_frequency(self, frequency):
        self.frequency = frequency

    # candidates is meant to be a list
    def add_candidates(self, cands):
        self.candidates.update(dict((c, {}) for c in cands))

    # candidates is meant to be a list
    def add_candidate(self, candidate):
        if candidate not in self.candidates:
            self.candidates[candidate] = {}

    # candidates is meant to be a list
    def remove_candidates(self, cands):
        for cand in cands:
            del self.candidates[cand]
            self.candidates_probability[cand] = 100

    # candidate is meant to be a string
    def remove_candidate(self, candidate):
        if candidate in self.candidates.keys():
            # print("deleted cand " + candidate)
            del self.candidates[candidate]
        # else:
            # print("did not delete cand "+ candidate)
        self.candidates_probability[candidate] = 100

    def clean_candidates(self):
        self.candidates = {}

    def set_probability(self, to_letter, probability):
        assert to_letter in self.candidates_probability
        self.candidates_probability[to_letter] = probability

    # to_letter is meant to be a string
    # dependency is meant to be a dict
    def add_dependency(self, to_letter, key, value):
        assert to_letter in self.candidates

        #print("CAND " + to_letter + " ADD " + key + "="+ value)

        dict1 = self.candidates.get(to_letter)

        if not self.candidates.get(to_letter) or not key in self.candidates.get(to_letter):
            dict1[key] = {value}
        else:
            self.candidates.get(to_letter)[key].update(value)

    def get_dependencies_for_letter(self, letter):
        assert letter in self.candidates
        self.candidates.get(letter)

    def remove_dependency(self, to_letter, dependency):
        del self.candidates[to_letter][dependency]

    def set_solution(self, solution):
        self.solution = solution

    def validate_dependency(self, key, value):
        #print("searching " + key + "=" + str(value) + " in " + str(self.candidates))
        if key in self.candidates and value in self.candidates[key]:
            del self.candidates[key]
            assert self.candidates

    def to_string(self):
        string = ""
        for cand in self.candidates:
            string += "\n " + "" + "%.2f" % self.candidates_probability[cand] + "% \"" +  str(cand) + "\" if "
            for dep in self.candidates[cand]:
                string += dep + " = " + "/".join(self.candidates[cand][dep]) + " AND "
            string = string[:len(string)-4]
            string += " OR"

        string = string[:len(string) - 2]
        #sorted_propabilaties = sorted(self.candidates_probability.items(), key=operator.itemgetter(1))[:5]
        #sorted_propabilaties = {k: '%.2f' % v for k, v in sorted_propabilaties}
        #sorted_propabilaties = sorted(sorted_propabilaties.items(), key=operator.itemgetter(1))

        return "Letter: \"" + self.letter + "\" is  \"" + self.solution + "\" or could be " + string + " \n"
                                                                                                       #"probabilites: " + json.dumps(sorted_propabilaties)
