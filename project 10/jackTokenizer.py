import re


class JackTokenizer:
    KEYWORD_TYPE = 'keyword'
    SYMBOL_TYPE = 'symbol'
    INTEGER_CONSTANT_TYPE = 'integerConstant'
    STRING_CONSTANT_TYPE = 'stringConstant'
    IDENTIFIER_TYPE = 'identifier'

    string_pattern = re.compile("^\"([^\"^\n]*)\"$")
    identifier_pattern = re.compile("^([a-z]|[A-Z]|[_])([a-z]|[A-Z]|_|[0-9])*$")

    keywords = {'class', 'constructor', 'function', 'method', 'field',
                'static', 'var', 'int', 'char', 'boolean', 'void', 'true',
                'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while',
                'return'}

    keyword_constants = {'true', 'false', 'null', 'this'}

    symbols = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
               '/', '&', '|', '<', '>', '=', '~', '&lt;', '&gt;',
               '&quot;', '&amp;'}

    operators = {'+', '-', '*', '/', '&', '|', '<', '>', '=', '&lt;', '&gt;',
                 '&quot;', '&amp;'}

    def __init__(self, input_file):
        self.file = input_file
        self.tokens = []
        self.words = []
        self.current_token = 0
        self.ignore_line = False

    def open_input_file(self, input_file):
        """Opens the input file/stream and gets ready to tokenize it."""
        with open(input_file, 'r') as file:
            code_words = []
            for line in file:
                line = self.remove_spaces_comments(line)
                if line == []:
                    continue
                else:
                    code_words = code_words + line
        self.words = code_words

    def remove_spaces_comments(self, line):
        """removes all the comment and multiply spaces"""
        line = line.split('//')[0]
        parts = ' '.join(line.split()).split(' ')
        if '"' in line:
            line_string = line.split('"')
            if len(line) >= 3:
                parts = ' '.join(line_string[0].split()).split(' ') +  ['"'+
                    line_string[1]+'"'] + ' '.join(line_string[2].split(
                    )).split(' ')
        if self.ignore_line:
            if parts[-1] == '*/':
                self.ignore_line = False
            return []
        if parts[0].startswith('/*'):
            self.ignore_line = True
            if parts[-1] == '*/':
                self.ignore_line = False
            return []
        if len(parts) == 1 and parts[0] == '':
            return []
        return parts

    def init_tokens(self):
        """init the tokens array"""
        for word in self.words:
            if JackTokenizer.check_word(word):
                self.tokens.append(self.check_symbol(word))
            else:
                while len(word) > 0:
                    i = JackTokenizer.check_word_by_char(word)
                    self.tokens.append(self.check_symbol(word)[:i])
                    word = word[i:]

    def set_token(self, new_token):
        """set the current token to a new one"""
        self.tokens[self.current_token] = new_token

    def check_symbol(self, word):
        """convert symbols"""
        if word == '<':
            return '&lt;'
        if word == '>':
            return '&gt;'
        if word == '"':
            return '&quot;'
        if word == '&':
            return '&amp;'
        return word

    @staticmethod
    def check_word(word):
        """checks if the word is legal"""
        if word in JackTokenizer.keywords:
            return JackTokenizer.KEYWORD_TYPE
        if word in JackTokenizer.symbols:
            return JackTokenizer.SYMBOL_TYPE
        if word.isdigit():
            return JackTokenizer.INTEGER_CONSTANT_TYPE
        if JackTokenizer.identifier_pattern.match(word):
            return JackTokenizer.IDENTIFIER_TYPE
        if JackTokenizer.string_pattern.match(word):
            return JackTokenizer.STRING_CONSTANT_TYPE
        return None

    @staticmethod
    def check_word_by_char(word):
        """checks if the words is legal char by char"""
        i = 0
        while i < len(word):
            if JackTokenizer.check_word(word[:i+1]):
                i += 1
                continue
            break
        return i

    def get_token(self):
        """return the current token"""
        return self.tokens[self.current_token]

    def has_more_tokens(self):
        """Do we have more tokens in the input? """
        return self.current_token < len(self.tokens)

    def advance(self):
        """Gets the next token from the input and makes it the current
        token. This method should only be called if hasMoreTokens() is true.
         Initially there is no current token"""
        if self.current_token < len(self.tokens) - 1:
            self.current_token += 1

    def token_type(self):
        """Returns the type of the current token. """
        return JackTokenizer.check_word(self.tokens[self.current_token])

    def key_word(self):
        """Returns the keyword which is the current token. Should be called
        only when tokenType() is KEYWORD. """
        if JackTokenizer.check_word(self.tokens[self.current_token]) == \
                JackTokenizer.KEYWORD_TYPE:
            return self.tokens[self.current_token]

    def symbol(self):
        """Returns the character which is the current token. Should be
        called only when tokenType() is SYMBOL. """
        if JackTokenizer.check_word(self.tokens[self.current_token]) == \
                JackTokenizer.SYMBOL_TYPE:
            return self.tokens[self.current_token]

    def identifier(self):
        """Returns the identifier which is the current token. Should be
        called only when tokenType() is IDENTIFIER"""
        if JackTokenizer.check_word(self.tokens[self.current_token]) == \
                JackTokenizer.IDENTIFIER_TYPE:
            return self.tokens[self.current_token]

    def int_val(self):
        """Returns the integer value of the current token. Should be called
        only when tokenType() is INT_CONST"""
        if JackTokenizer.check_word(self.tokens[self.current_token]) == \
                JackTokenizer.INTEGER_CONSTANT_TYPE:
            return self.tokens[self.current_token]

    def string_val(self):
        """Returns the string value of the current token, without the double
        quotes. Should be called only when tokenType() is STRING_CONST. """
        if JackTokenizer.check_word(self.tokens[self.current_token]) == \
                JackTokenizer.STRING_CONSTANT_TYPE:
            return self.tokens[self.current_token]

    def keyword_constant(self):
        """return if the current token is a keyword constant or not"""
        return self.get_token() in self.keyword_constants

    def unary_op(self):
        """return if the current token is an unary operator or not"""
        if self.get_token() == '~' or self.get_token() == '-':
            return True
        return False

    def operator(self):
        """return if the current token is an operator or not"""
        return self.get_token() in self.operators

