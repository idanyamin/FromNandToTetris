from jackTokenizer import JackTokenizer


class CompilationEngine:

    LET_STATEMENT_OPEN = '<letStatement>\n'
    LET_STATEMENT_CLOSE = '</letStatement>\n'
    EXPRESSION_OPEN = '<expression>\n'
    EXPRESSION_CLOSE = '</expression>\n'
    TERM_OPEN = '<term>\n'
    TERM_CLOSE = '</term>\n'
    EXPRESSION_LIST_OPEN = '<expressionList>\n'
    EXPRESSION_LIST_CLOSE = '</expressionList>\n'
    WHILE_STATEMENT_OPEN = '<whileStatement>\n'
    WHILE_STATEMENT_CLOSE = '</whileStatement>\n'
    IF_STATEMENT_OPEN = '<ifStatement>\n'
    IF_STATEMENT_CLOSE = '</ifStatement>\n'
    SUBROUTINE_CALL_OPEN = '<doStatement>\n'
    SUBROUTINE_CALL_CLOSE = '</doStatement>\n'
    RETURN_OPEN = '<returnStatement>\n'
    RETURN_CLOSE = '</returnStatement>\n'
    STATEMENTS_OPEN = '<statements>\n'
    STATEMENTS_CLOSE = '</statements>\n'
    VAR_DEC_OPEN = '<varDec>\n'
    VAR_DEC_CLOSE = '</varDec>\n'
    CLASS_VAR_DEC_OPEN = '<classVarDec>\n'
    CLASS_VAR_DEC_CLOSE = '</classVarDec>\n'
    PARAMETER_LIST_OPEN = '<parameterList>\n'
    PARAMETER_LIST_CLOSE = '</parameterList>\n'
    SUBROUTINE_BODY_OPEN = '<subroutineBody>\n'
    SUBROUTINE_BODY_CLOSE = '</subroutineBody>\n'
    SUBROUTINE_DEC_OPEN = '<subroutineDec>\n'
    SUBROUTINE_DEC_CLOSE = '</subroutineDec>\n'
    CLASS_OPEN = '<class>\n'
    CLASS_CLOSE = '</class>\n'

    def __init__(self, tokenizer):
        """Creates a new compilation engine with the given input and output.
         The next routine called must be compileClass(). """
        self.tokenizer = tokenizer
        self.tags = []
        self.scope = 0

    def compile_class(self):
        """Compiles a complete class."""
        if self.tokenizer.get_token() != 'class':
            return None
        self.tags.append('\t' * self.scope + self.CLASS_OPEN)
        self.scope += 1
        self.compile_basic_tag()  # class
        self.compile_basic_tag()  # class name
        if self.tokenizer.get_token() != '{':
            return None
        self.compile_basic_tag()  # {
        while self.tokenizer.get_token() == 'static' or \
                        self.tokenizer.get_token() == 'field':
            self.compile_class_var_dec()
        while self.tokenizer.get_token() == 'constructor' or \
                        self.tokenizer.get_token() == 'function' or  \
                        self.tokenizer.get_token() == 'method':
            self.compile_subroutine()
        if self.tokenizer.get_token() != '}':
            return None
        self.compile_basic_tag()  # }
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.CLASS_CLOSE)
        return

    def compile_class_var_dec(self):
        """Compiles a static declaration or a field declaration. """
        if self.tokenizer.get_token() != 'static' and \
                        self.tokenizer.get_token() != 'field':
            return None
        self.tags.append('\t' * self.scope + self.CLASS_VAR_DEC_OPEN)
        self.scope += 1
        self.compile_basic_tag()  # var
        self.compile_basic_tag()  # type
        self.compile_basic_tag()  # var name
        while self.tokenizer.get_token() == ',':
            self.compile_basic_tag()  # ,
            self.compile_basic_tag()  # var name
        if self.tokenizer.get_token() != ';':
            return None
        self.compile_basic_tag()  # ;
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.CLASS_VAR_DEC_CLOSE)
        return

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor. """
        self.tags.append('\t' * self.scope + self.SUBROUTINE_DEC_OPEN)
        self.scope += 1
        self.compile_basic_tag()  # method/function/constructor
        self.compile_basic_tag()  # type/void
        self.compile_basic_tag()  # subroutineName
        if self.tokenizer.get_token() != '(':
            return None
        self.compile_basic_tag()  # (
        self.compile_parameter_list()
        if self.tokenizer.get_token() != ')':
            return None
        self.compile_basic_tag()  # )
        self.compile_subroutine_body()
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.SUBROUTINE_DEC_CLOSE)
        return

    def compile_subroutine_body(self):
        """Compiles the subroutine's body - the statements. """
        if self.tokenizer.get_token() != '{':
            return None
        self.tags.append('\t' * self.scope + self.SUBROUTINE_BODY_OPEN)
        self.scope += 1
        self.compile_basic_tag()  # {
        while self.tokenizer.get_token() == 'var':
            self.compile_var_dec()
        self.compile_statements()
        if self.tokenizer.get_token() != '}':
            return None
        self.compile_basic_tag()  # }
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.SUBROUTINE_BODY_CLOSE)
        return

    def compile_parameter_list(self):
        """
        Compiles a (possibly empty) parameter list, not including the
        enclosing '()'.
        """
        if self.tokenizer.get_token() == ')':
            self.tags.append('\t' * self.scope + self.PARAMETER_LIST_OPEN +
                             ' ' + self.PARAMETER_LIST_CLOSE)
            return
        self.tags.append('\t' * self.scope + self.PARAMETER_LIST_OPEN)
        self.scope += 1
        self.compile_basic_tag()  # type
        self.compile_basic_tag()  # var name
        while self.tokenizer.get_token() == ',':
            self.compile_basic_tag()  # ,
            self.compile_basic_tag()  # type
            self.compile_basic_tag()  # var nam
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.PARAMETER_LIST_CLOSE)
        return

    def compile_var_dec(self):
        """Compiles a var declaration. """
        if self.tokenizer.get_token() != 'var':
            return None
        self.tags.append('\t' * self.scope + self.VAR_DEC_OPEN)
        self.scope += 1
        self.compile_basic_tag()  # var
        self.compile_basic_tag()  # type
        self.compile_basic_tag()  # var name
        while self.tokenizer.get_token() == ',':
            self.compile_basic_tag()  # ,
            self.compile_basic_tag()  # var name
        if self.tokenizer.get_token() != ';':
            return None
        self.compile_basic_tag()  # ;
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.VAR_DEC_CLOSE)
        return

    def compile_statements(self):
        """
        Compiles a sequence of statements, not including the enclosing '{
        }'.
        """
        current_token = self.tokenizer.get_token()
        first = True
        while current_token == 'let' or current_token == 'if' or \
                        current_token == 'while' or current_token == 'do' \
                or current_token == 'return':
            if first:
                self.tags.append('\t' * self.scope + self.STATEMENTS_OPEN)
                self.scope += 1
            if current_token == 'let':
                self.compile_let()
            elif current_token == 'if':
                self.compile_if()
            elif current_token == 'while':
                self.compile_while()
            elif current_token == 'do':
                self.compile_do()
            elif current_token == 'return':
                self.compile_return()
            first = False
            current_token = self.tokenizer.get_token()
        if not first:
            self.scope -= 1
            self.tags.append('\t' * self.scope + self.STATEMENTS_CLOSE)
        return

    def compile_do(self):
        """Compiles a do statement. """
        if self.tokenizer.get_token() != 'do':
            return None
        self.tags.append('\t' * self.scope + self.SUBROUTINE_CALL_OPEN)
        self.scope += 1
        self.compile_basic_tag()  # do
        if self.tokenizer.identifier() is None:
            return None
        self.compile_basic_tag()
        if self.tokenizer.get_token() == '.':
            self.compile_basic_tag()
            if self.tokenizer.identifier() is None:
                return None
            self.compile_basic_tag()
        if self.tokenizer.get_token() != '(':
            return None
        self.compile_basic_tag()
        self.compile_expression_list()
        if self.tokenizer.get_token() != ')':
            return None
        self.compile_basic_tag()
        if self.tokenizer.get_token() != ';':
            return None
        self.compile_basic_tag()  # ;
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.SUBROUTINE_CALL_CLOSE)
        return

    def compile_let(self):
        """Compiles a let statement. """
        if self.tokenizer.get_token() != 'let':
            return None
        self.tags.append('\t'*self.scope + self.LET_STATEMENT_OPEN)
        self.scope += 1
        self.compile_basic_tag()  # let
        if self.tokenizer.identifier() is None:
            return None
        self.compile_basic_tag()  # var name
        if self.tokenizer.get_token() == '[':
            self.compile_basic_tag()
            self.compile_expression()
            if self.tokenizer.get_token() == ']':
                self.compile_basic_tag()
        self.compile_basic_tag()  # = symbol
        self.compile_expression()
        if self.tokenizer.get_token() != ';':
            return None
        self.compile_basic_tag()  # ;
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.LET_STATEMENT_CLOSE)
        return

    def compile_while(self):
        """Compiles a while statement. """
        if self.tokenizer.get_token() != 'while':
            return None
        self.tags.append('\t' * self.scope + self.WHILE_STATEMENT_OPEN)
        self.scope += 1
        self.compile_basic_tag()  # while
        if self.tokenizer.get_token() != '(':
            return None
        self.compile_basic_tag()
        self.compile_expression()
        if self.tokenizer.get_token() != ')':
            return None
        self.compile_basic_tag()
        if self.tokenizer.get_token() != '{':
            return None
        self.compile_basic_tag()
        self.compile_statements()
        if self.tokenizer.get_token() != '}':
            return None
        self.compile_basic_tag()
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.WHILE_STATEMENT_CLOSE)
        return

    def compile_return(self):
        """Compiles a return statement. """
        if self.tokenizer.get_token() != 'return':
            return None
        self.tags.append('\t' * self.scope + self.RETURN_OPEN)
        self.scope += 1
        self.compile_basic_tag()  # return
        if self.tokenizer.get_token() != ';':
            self.compile_expression()
        self.compile_basic_tag()  # ;
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.RETURN_CLOSE)
        return

    def compile_if(self):
        """Compiles an if statement, possibly with a trailing else clause. """
        if self.tokenizer.get_token() != 'if':
            return None
        self.tags.append('\t' * self.scope + self.IF_STATEMENT_OPEN)
        self.scope += 1
        self.compile_basic_tag()  # if
        if self.tokenizer.get_token() != '(':
            return None
        self.compile_basic_tag()
        self.compile_expression()
        if self.tokenizer.get_token() != ')':
            return None
        self.compile_basic_tag()
        if self.tokenizer.get_token() != '{':
            return None
        self.compile_basic_tag()
        self.compile_statements()
        if self.tokenizer.get_token() != '}':
            return None
        self.compile_basic_tag()
        if self.tokenizer.get_token() == 'else':
            self.compile_basic_tag()
            if self.tokenizer.get_token() != '{':
                return None
            self.compile_basic_tag()
            self.compile_statements()
            if self.tokenizer.get_token() != '}':
                return None
            self.compile_basic_tag()
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.IF_STATEMENT_CLOSE)
        return

    def compile_expression(self):
        """Compiles an expression. """
        self.tags.append('\t'*self.scope + self.EXPRESSION_OPEN)
        self.scope += 1
        self.compile_term()
        while self.tokenizer.operator():
            self.compile_basic_tag()
            self.compile_term()
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.EXPRESSION_CLOSE)
        return

    def compile_term(self):
        """Compiles a term. """
        self.tags.append('\t'*self.scope + self.TERM_OPEN)
        self.scope += 1
        if self.tokenizer.int_val() or self.tokenizer.string_val() or \
                self.tokenizer.keyword_constant():
            self.compile_basic_tag()
        elif self.tokenizer.identifier():
            self.compile_basic_tag()
            if self.tokenizer.get_token() == '[':
                self.compile_basic_tag()
                self.compile_expression()
                if self.tokenizer.get_token() == ']':
                    self.compile_basic_tag()
            elif self.tokenizer.get_token() == '(':
                self.compile_basic_tag()
                self.compile_expression_list()
                if self.tokenizer.get_token() == ')':
                    self.compile_basic_tag()
            elif self.tokenizer.get_token() == '.':
                self.compile_basic_tag()
                self.compile_basic_tag()
                self.compile_basic_tag()
                self.compile_expression_list()
                if self.tokenizer.get_token() == ')':
                    self.compile_basic_tag()
        elif self.tokenizer.unary_op():
            self.compile_basic_tag()
            self.compile_term()
        elif self.tokenizer.get_token() == '(':
            self.compile_basic_tag()  # (
            self.compile_expression()
            self.compile_basic_tag()  # )
        self.scope -= 1
        self.tags.append('\t'*self.scope + self.TERM_CLOSE)
        return

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions. """
        self.tags.append('\t'*self.scope + self.EXPRESSION_LIST_OPEN)
        self.scope += 1
        if self.tokenizer.get_token() == ')':
            self.scope -= 1
            self.tags.append('\t' * self.scope + self.EXPRESSION_LIST_CLOSE)
            return
        self.compile_expression()
        while self.tokenizer.get_token() == ',':
            self.compile_basic_tag()
            self.compile_expression()
        self.scope -= 1
        self.tags.append('\t' * self.scope + self.EXPRESSION_LIST_CLOSE)
        return

    def compile_basic_tag(self):
        """compile a basic token by its type"""
        token = self.tokenizer.get_token()
        if self.tokenizer.token_type() == JackTokenizer.STRING_CONSTANT_TYPE:
            token = token[1:-1]
        self.tags.append('\t'*self.scope + '<' + self.tokenizer.token_type() +
                         '> ' + token + ' </' +
                         self.tokenizer.token_type() + '>\n')
        self.tokenizer.advance()
