# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        copy_of_words = self.valid_words
        return copy_of_words

    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        d = {}
        for index in range(26):
            if chr(65+index) == 'A':
                d[chr(65+index)] = vowels_permutation[0].upper()
            elif chr(65+index) == 'E':
                d[chr(65+index)] = vowels_permutation[1].upper()
            elif chr(65+index) == 'I':
                d[chr(65+index)] = vowels_permutation[2].upper()
            elif chr(65+index) == 'O':
                d[chr(65+index)] = vowels_permutation[3].upper()
            elif chr(65+index) == 'U':
                d[chr(65+index)] = vowels_permutation[4].upper()
            else:
                d[chr(65+index)] = chr(65+index)
            if chr(97+index) == 'a':
                d[chr(97+index)] = vowels_permutation[0].lower()
            elif chr(97+index) == 'e':
                d[chr(97+index)] = vowels_permutation[1].lower()
            elif chr(97+index) == 'i':
                d[chr(97+index)] = vowels_permutation[2].lower()
            elif chr(97+index) == 'o':
                d[chr(97+index)] = vowels_permutation[3].lower()
            elif chr(97+index) == 'u':
                d[chr(97+index)] = vowels_permutation[4].lower()
            else:
                d[chr(97+index)] = chr(97+index)
        # print(d)
        return d
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        copy_of_message = self.message_text
        copy_of_message = copy_of_message.split(' ')
        
        final_str = []
        for words in copy_of_message:
            # print(words)
            shifted_message = []
            for letters in words:
                if letters in transpose_dict:
                    shifted_message.append(transpose_dict[letters])
                else:
                    shifted_message.append(letters)
            final_str.append(''.join(shifted_message))        
        return ' '.join(final_str)

# test = SubMessage('ewer')
# print(test.build_transpose_dict('eioau'))
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self,text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        all_list = get_permutations('aeiou')
        maxcountwords = 0
        key = []
        for transpose_dict in all_list:
            number_of_real_words = 0
            enc_dict = self.build_transpose_dict(transpose_dict)
            decrypted_message = self.apply_transpose(enc_dict)
            decrypted_message = decrypted_message.split(' ')
            for singleword in decrypted_message:
                if is_word(self.valid_words, singleword):
                    number_of_real_words += 1
            if number_of_real_words > maxcountwords:
                maxcountwords = number_of_real_words
                key = transpose_dict
        enc_dict = self.build_transpose_dict(key)
        return self.apply_transpose(enc_dict)
if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)

    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print(enc_message.get_message_text())
    print("Decrypted message:", enc_message.decrypt_message())
     
    #TODO: WRITE YOUR TEST CASES HERE
