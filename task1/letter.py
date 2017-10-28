import json
import operator

class Letter:

    def __init__(self, fromLetter, frequency):
        self.letter = fromLetter
        self.candidates = {}
        self.candidatesProbability = {'a': 100, 'b': 100, 'c': 100, 'd': 100, 'e': 100, 'f': 100, 'g': 100, 'h': 100, 'i': 100, 'j': 100, 'k': 100,
      'l': 100, 'm': 100, 'n': 100, 'o': 100, 'p': 100, 'q': 100, 'r': 100, 's': 100, 't': 100, 'u': 100, 'v': 100,
      'w': 100, 'x': 100, 'y': 100, 'z': 100}
        self.solution = '_'
        self.score = frequency
        self.frequency = 0

    def set_frequency(self, frequency):
        self.frequency = frequency

    # candidates is meant to be a list
    def add_candidates(self, cands):
        self.candidates.update(dict((c,{}) for c in cands))

        # candidates is meant to be a list
    def add_candidate(self, candidate):
        if candidate not in self.candidates:
            self.candidates[candidate] = {}

    # candidates is meant to be a list
    def remove_candidates(self, cands):
        for cand in cands:
            del self.candidates[cand]
            self.candidatesProbability[cand] = 100

    # candidate is meant to be a string
    def remove_candidate(self, candidate):
        if candidate in self.candidates.keys():
            # print("deleted cand " + candidate)
            del self.candidates[candidate]
        # else:
            # print("did not delete cand "+ candidate)
        self.candidatesProbability[candidate] = 100

    def clean_candidates(self):
        self.candidates = {}

    def set_probability(self, toLetter, probability):
        assert toLetter in self.candidatesProbability
        self.candidatesProbability[toLetter] = probability

    # toLetter is meant to be a string
    # dependency is meant to be a dict
    def add_dependency(self, toLetter, key, value):
        assert toLetter in self.candidates

        #print("CAND " + toLetter + " ADD " + key + "="+ value)

        dict1 = self.candidates.get(toLetter)

        if not self.candidates.get(toLetter) or not key in self.candidates.get(toLetter):
            dict1[key] = {value};
        else:
            self.candidates.get(toLetter)[key].update(value)

    def get_dependencies_for_letter(self, letter):
        assert letter in self.candidates
        self.candidates.get(letter)

    def remove_dependency(self, toLetter, dependency):
        del self.candidates[toLetter][dependency]

    def set_solution(self, solution):
        self.solution = solution

    def validate_dependency(self, key, value):
        #print("searching " + key + "=" + str(value) + " in " + str(self.candidates))
        if key in self.candidates and value in self.candidates[key]:
            del self.candidates[key]
            assert len(self.candidates) > 0

    def to_string(self):
        string = ""
        for cand in self.candidates:
            string += str(cand) + " (if "  + " ) "
        sortedProbs = sorted(self.candidatesProbability.items(), key=operator.itemgetter(1))
        return "Letter: ", self.letter, " is " , self.solution, "or could be ", json.dumps(list(self.candidates)) + " with probabilites " + json.dumps(sortedProbs)


