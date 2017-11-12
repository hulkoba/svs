INPUT_FILENAME = "2017_samples/sample.txt"
OUPUT_FILENAME = "2017_samples/sample.txt_enc.txt"

FREQUENT_LETTERS = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w',
                    'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']


LETTER_PERCENTAGE = {'e': 12.702, 't': 9.056, 'a': 8.167, 'o': 7.507, 'i': 6.966,
                     'n': 6.749, 's': 6.327, 'h': 6.094, 'r': 5.987, 'd': 4.253,
                     'l': 4.025, 'c': 2.782, 'u': 2.758, 'm': 2.406, 'w': 2.360,
                     'f': 2.228, 'g': 2.015, 'y': 1.974, 'p': 1.929, 'b': 1.492,
                     'v': 0.978, 'k': 0.772, 'j': 0.153, 'x': 0.150, 'q': 0.095, 'z': 0.074}


# eher Ausschlusskriterien als Reihenfolge bzgl. Haeufigkeit
ONE_LETTER_WORDS = ['a', 'i']

TWO_LETTER_WORDS = ['he', 'at', 'it', 'if', 'in', 'is',
                    'on', 'to', 'do', 'go', 'of', 'an',
                    'so', 'of', 'up', 'as', 'my', 'me',
                    'be', 'as', 'or', 'we', 'by', 'no', 'am', 'us']

THREE_LETTER_WORDS = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any',
                      'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get',
                      'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two',
                      'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'too', 'use']
