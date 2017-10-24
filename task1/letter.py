import json

class Letter:

    def __init__(self, fromLetter):
        self.letter = fromLetter
        self.candidates = {'a': {}, 'b': {}, 'c': {}, 'd': {}, 'e': {}, 'f': {}, 'g': {}, 'h': {}, 'i': {}, 'j': {}, 'k': {},
      'l': {}, 'm': {}, 'n': {}, 'o': {}, 'p': {}, 'q': {}, 'r': {}, 's': {}, 't': {}, 'u': {}, 'v': {},
      'w': {}, 'x': {}, 'y': {}, 'z': {}}
        self.solution = '_'

    # candidates is meant to be a list
    def set_candidates(self, toLetter, cands):
        self.candidates = dict((c,{}) for c in cands)

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

    # candidate is meant to be a string
    def remove_candidates(self, candidate):
        if candidate in self.candidates:
            del self.candidates[candidate]

    def clean_candidates(self):
    	self.candidates = {}

    # toLetter is meant to be a string
    # dependency is meant to be a dict
    def add_dependency(self, toLetter, key, value):
        assert toLetter in self.candidates

        dict1 = self.candidates.get(toLetter)

        if not self.candidates.get(toLetter) or not key in self.candidates.get(toLetter):
             dict1[key] = [value];
        else:
            self.candidates.get(toLetter)[key].append(value)

    def get_dependencies_for_letter(self, letter):
        assert letter in self.candidates
        self.candidates.get(letter)

    def remove_dependency(self, toLetter, dependency):
         del self.candidates[toLetter][dependency]

    def set_solution(self, solution):
         self.solution = solution

    def validate_dependency(self, key, value):
        if key in self.candidates and self.candidates[key] == value:
            del self.candidates[key]
            assert len(self.candidates) > 0

    def to_string(self):
        string = ""
        for cand in self.candidates:
            string += str(cand) + " (if "  + " ) "
        return "Letter: ", self.letter, " is " , self.solution, "or could be ", json.dumps(self.candidates)