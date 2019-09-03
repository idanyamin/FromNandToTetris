from VMWriter import *
from SymbolTable import *


class CompilationEngine:

    OP_DICT_BIN = {'+': 'add', '-': 'sub', '=': 'eq', '&gt;': 'gt',
                   '&lt;': 'lt', '&amp;': 'and', '|': 'or'}
    OP_DICT_UN = {'-': 'neg', '~': 'not'}
    KEYWORD_DICT = {'true': ('constant', -1), 'false': ('constant', 0),
                    'null': ('constant', 0), 'this': ('pointer', 0)}

    VAR_DICT = {'static': 'static', 'field': 'this', 'var': 'local',
                'argument': 'argument'}

    def __init__(self, tokenizer, output):
        """Creates a new compilation engine with the given input and output.
                 The next routine called must be compileClass(). """
        self.tokenizer = tokenizer
        self.tags = []
        self.scope = 0
        self.writer = VMWriter(output)
        self.class_table = SymbolTable()
        self.method_table = SymbolTable()
        self.class_name = ''
        self.method_or_constructor = False

    def compile_class(self):
        """Compiles a complete class."""
        self.tokenizer.advance()  # class
        self.class_name = self.tokenizer.get_token()  # class name
        self.tokenizer.advance()
        self.tokenizer.advance()  # {
        while self.tokenizer.get_token() == 'static' or \
                self.tokenizer.get_token() == 'field':
            self.compile_class_var_dec()
        while self.tokenizer.get_token() == 'constructor' or \
                self.tokenizer.get_token() == 'function' or  \
                self.tokenizer.get_token() == 'method':
            self.compile_subroutine()
        self.tokenizer.advance()  # }
        self.writer.close()
        self.writer.close()
        return

    def compile_class_var_dec(self):
        """Compiles a static declaration or a field declaration. """
        kind = self.tokenizer.get_token()  # var
        self.tokenizer.advance()
        var_type = self.tokenizer.get_token()  # type
        self.tokenizer.advance()
        name = self.tokenizer.get_token()  # var name
        self.class_table.define(name, var_type, kind)
        self.tokenizer.advance()
        while self.tokenizer.get_token() == ',':
            self.tokenizer.advance()  # ,
            name = self.tokenizer.get_token()  # var name
            self.class_table.define(name, var_type, kind)
            self.tokenizer.advance()  # var name
        self.tokenizer.advance()  # ;
        return

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor. """
        func_type = self.tokenizer.get_token()  # method/function/constructor
        self.tokenizer.advance()
        self.tokenizer.advance()  # type/void
        func_name = self.tokenizer.get_token()  # subroutineName
        self.tokenizer.advance()  # (
        self.tokenizer.advance()
        self.method_table.start_subroutine()
        if func_type == 'method':
            self.method_or_constructor = True
            self.method_table.define('this', self.class_name, 'argument')
            self.compile_parameter_list()
            num_locals = 0
            self.tokenizer.advance()  # {
            while self.tokenizer.get_token() == 'var':
                num_locals += self.compile_var_dec()
            self.writer.write_function(self.class_name + '.' + func_name,
                                       num_locals)
            self.writer.write_push('argument', 0)
            self.writer.write_pop('pointer', 0)
        elif func_type == 'function':
            self.method_or_constructor = False
            self.compile_parameter_list()
            num_locals = 0
            self.tokenizer.advance()  # {
            while self.tokenizer.get_token() == 'var':
                num_locals += self.compile_var_dec()
            self.writer.write_function(self.class_name + '.' + func_name, num_locals)
        elif func_type == 'constructor':
            self.method_or_constructor = True
            self.compile_parameter_list()
            num_locals = 0
            self.tokenizer.advance()  # {
            while self.tokenizer.get_token() == 'var':
                num_locals += self.compile_var_dec()
            self.writer.write_function(self.class_name + '.' + func_name, num_locals)
            self.writer.write_push('constant', self.class_table.var_count('field'))
            self.writer.write_call('Memory.alloc', 1)
            self.writer.write_pop('pointer', 0)
        self.compile_subroutine_body()
        return

    def compile_subroutine_body(self):
        """Compiles the subroutine's body - the statements. """
        self.compile_statements()
        self.tokenizer.advance()  # }
        return

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the
                enclosing . """
        if self.tokenizer.get_token() == ')':
            self.tokenizer.advance()  # )
            return 0
        var_type = self.tokenizer.get_token()  # type
        self.tokenizer.advance()
        name = self.tokenizer.get_token()  # var name
        self.tokenizer.advance()
        num = 1
        self.method_table.define(name, var_type, 'argument')
        while self.tokenizer.get_token() == ',':
            self.tokenizer.advance()  # ,
            var_type = self.tokenizer.get_token()  # type
            self.tokenizer.advance()
            name = self.tokenizer.get_token()  # var nam
            self.tokenizer.advance()
            num += 1
            self.method_table.define(name, var_type, 'argument')
        self.tokenizer.advance()  # )
        return num

    def compile_var_dec(self):
        """Compiles a var declaration. """
        var = self.tokenizer.get_token()  # var
        self.tokenizer.advance()
        var_type = self.tokenizer.get_token()  # type
        self.tokenizer.advance()
        name = self.tokenizer.get_token()  # var name
        self.method_table.define(name, var_type, var)
        self.tokenizer.advance()
        num_vars = 1
        while self.tokenizer.get_token() == ',':
            num_vars += 1
            self.tokenizer.advance()  # ,
            name = self.tokenizer.get_token()  # var name
            self.method_table.define(name, var_type, var)
            self.tokenizer.advance()  # var name
        self.tokenizer.advance()  # ;
        return num_vars

    def compile_statements(self):
        """Compiles a sequence of statements, not including the enclosing . """
        current_token = self.tokenizer.get_token()
        while current_token == 'let' or current_token == 'if' or \
                current_token == 'while' or current_token == 'do' \
                or current_token == 'return':
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
            current_token = self.tokenizer.get_token()
        return

    def compile_do(self):
        """Compiles a do statement. """
        self.tokenizer.advance()  # do
        name = self.tokenizer.get_token()
        self.tokenizer.advance()  # function name
        if self.tokenizer.get_token() == '(':
            name = self.class_name + '.' + name # *************************
            self.writer.write_comment('//function call')
            self.compile_subroutine_call(name, False)
        elif self.tokenizer.get_token() == '.':
            self.writer.write_comment('//function object call')
            if name in self.method_table.symbol_table:
                self.compile_var_name(name)
            elif name in self.class_table.symbol_table:
                self.compile_var_name(name)
            self.compile_subroutine_call(name, True)
        self.tokenizer.advance()  # ;
        self.writer.write_pop('temp', 0)
        return

    def compile_let(self):
        """Compiles a let statement. """
        self.writer.write_comment('//let statement')
        self.tokenizer.advance()  # let
        name = self.tokenizer.get_token()  # var name
        self.tokenizer.advance()
        if self.tokenizer.get_token() == '[':
            self.compile_var_name(name)
            self.tokenizer.advance()  # [
            self.compile_expression()
            self.writer.write_arithmetic('add')
            self.tokenizer.advance()  # ]
            self.tokenizer.advance()  # =
            self.compile_expression()
            self.writer.write_pop('temp', 0)
            self.writer.write_pop('pointer', 1)
            self.writer.write_push('temp', 0)
            self.writer.write_pop('that', 0)
        else:
            self.tokenizer.advance()  # = symbol
            self.compile_expression()
            self.compile_pop_var_name(name)
        self.tokenizer.advance()  # ;
        return

    def compile_while(self):
        """Compiles a while statement. """
        self.writer.write_comment('//while statement')
        self.tokenizer.advance()  # while
        num_while = str(self.tokenizer.current_token)
        self.writer.write_label('while' + num_while)
        self.tokenizer.advance()  # (
        self.compile_expression()
        self.writer.write_arithmetic('not')
        self.tokenizer.advance()  # )
        end_num = str(self.tokenizer.current_token)
        self.writer.write_if('end' + end_num)
        self.tokenizer.advance()  # {
        self.compile_statements()
        self.tokenizer.advance()  # }
        self.writer.write_go_to('while' + num_while)
        self.writer.write_label('end' + end_num)
        return

    def compile_return(self):
        """Compiles a return statement. """
        self.writer.write_comment('//return statement')
        self.tokenizer.advance()  # return
        if self.tokenizer.get_token() != ';':
            self.compile_expression()
        else:
            self.writer.write_push('constant', 0)
        self.writer.write_return()
        self.tokenizer.advance()  # ;
        return

    def compile_if(self):
        """Compiles an if statement, possibly with a trailing else clause. """
        self.writer.write_comment('//if statement')
        self.tokenizer.advance()  # if
        self.tokenizer.advance()  # (
        self.compile_expression()
        self.writer.write_arithmetic('not')
        self.tokenizer.advance()  # )
        else_num = str(self.tokenizer.current_token)
        self.writer.write_if('else' + else_num)
        self.tokenizer.advance()  # {
        self.compile_statements()
        end_num = str(self.tokenizer.current_token)
        self.writer.write_go_to('end' + end_num)
        self.tokenizer.advance()  # }
        self.writer.write_label('else' + else_num)
        if self.tokenizer.get_token() == 'else':
            self.tokenizer.advance()  # else
            self.tokenizer.advance()  # {
            self.compile_statements()
            self.tokenizer.advance()  # }
        self.writer.write_label('end' + end_num)
        return

    def compile_expression(self):
        """Compiles an expression. """
        self.compile_term()
        while self.tokenizer.operator():
            bin_op = self.tokenizer.get_token()
            self.tokenizer.advance()
            self.compile_term()
            if bin_op == '*':
                self.writer.write_multiply()
            elif bin_op == '/':
                self.writer.write_divide()
            else:
                self.writer.write_arithmetic(self.OP_DICT_BIN[bin_op])
        return

    def compile_term(self):
        """Compiles a term. """
        if self.tokenizer.int_val():
            self.writer.write_push('constant', self.tokenizer.get_token())
            self.tokenizer.advance()
        elif self.tokenizer.string_val():
            self.writer.write_string(self.tokenizer.get_token())
            self.tokenizer.advance()
        elif self.tokenizer.keyword_constant():
            self.compile_keyword_const()
        elif self.tokenizer.identifier():
            name = self.tokenizer.get_token()
            self.tokenizer.advance()
            if self.tokenizer.get_token() == '[':
                self.tokenizer.advance()  # '['
                self.compile_array(name)
            elif self.tokenizer.get_token() == '(':
                self.writer.write_comment('//function call')
                self.compile_subroutine_call(name, False)
            elif self.tokenizer.get_token() == '.':
                self.writer.write_comment('//function object call')
                self.compile_subroutine_call(name, True)
            else:
                self.compile_var_name(name)
        elif self.tokenizer.unary_op():
            unary_op = self.tokenizer.get_token()
            self.tokenizer.advance()
            self.compile_term()
            self.compile_un_op(unary_op)
        elif self.tokenizer.get_token() == '(':
            self.tokenizer.advance()  # (
            self.compile_expression()
            self.tokenizer.advance()  # )
        return

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions. """
        if self.tokenizer.get_token() == ')':
            return 0
        self.compile_expression()
        num = 1
        while self.tokenizer.get_token() == ',':
            self.tokenizer.advance()
            self.compile_expression()
            num += 1
        return num

    def compile_bin_op(self, operator):
        """compiles a binary operator"""
        self.writer.write_arithmetic(self.OP_DICT_BIN[operator])

    def compile_un_op(self, operator):
        """compiles an unary operator"""
        self.writer.write_arithmetic(self.OP_DICT_UN[operator])

    def compile_keyword_const(self):
        """compiles a keyword constant"""
        if self.tokenizer.get_token() == 'true':
            self.writer.write_push('constant', 1)
            self.writer.write_arithmetic('neg')
        else:
            self.writer.write_push(self.KEYWORD_DICT[self.tokenizer.get_token()][0],
                                   self.KEYWORD_DICT[self.tokenizer.get_token()][1])
        self.tokenizer.advance()

    def compile_var_name(self, name):
        """compile a identifier push command"""
        if name in self.method_table.symbol_table:
            self.writer.write_push(self.VAR_DICT[self.method_table.kind_of(
                name)], self.method_table.index_of(name))
        else:
            self.writer.write_push(self.VAR_DICT[self.class_table.kind_of(name)], self.class_table.index_of(name))

    def compile_pop_var_name(self, name):
        """compile a identifier pop command"""
        if name in self.method_table.symbol_table:
            self.writer.write_pop(self.VAR_DICT[self.method_table.kind_of(
                name)], self.method_table.index_of(name))
        else:
            self.writer.write_pop(self.VAR_DICT[self.class_table.kind_of(
                name)], self.class_table.index_of(name))

    def compile_array(self, name):
        """compiles an array operation"""
        self.compile_expression()
        self.tokenizer.advance()  # ']'
        self.compile_var_name(name)
        self.writer.write_arithmetic('add')
        self.writer.write_pop('pointer', 1)
        self.writer.write_push('that', 0)

    def compile_subroutine_call(self, name, obj):
        """compiles a subroutine call. obj is true if the call command was:
        obj_name.func_name(), and false if the call command was func_name() """
        var_type = ''
        if obj:
            if name in self.method_table.symbol_table:
                self.compile_var_name(name)
                var_type = self.method_table.type_of(name)
                self.tokenizer.advance()
                name = self.tokenizer.get_token()
                self.tokenizer.advance()
            elif name in self.class_table.symbol_table:
                self.compile_var_name(name)
                var_type = self.class_table.type_of(name)
                self.tokenizer.advance()
                name = self.tokenizer.get_token()
                self.tokenizer.advance()
            elif self.tokenizer.get_token() == '.':
                self.tokenizer.advance()
                name += '.' + self.tokenizer.get_token()
                self.tokenizer.advance()
        else:
            self.tokenizer.advance()
        if obj:
            self.tokenizer.advance()  # (
        else:
            self.writer.write_push('pointer', 0)
        num_args = self.compile_expression_list()
        #todo 11/27 could be problematic for the case 'do Output.printInt(1 + (2 * 3));'
        if var_type:
            num_args += 1
            name = var_type + '.' + name
        if not obj and self.method_or_constructor:
            num_args += 1
        self.writer.write_call(name, num_args)
        self.tokenizer.advance()




