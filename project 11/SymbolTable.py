class SymbolTable:

    class Symbol:
        # constants
        ARGUMENT = 'argument'
        VAR = 'var'
        STATIC = 'static'
        FIELD = 'field'
        INT = 'int'
        CHAR = 'char'
        BOOLEAN = 'boolean'

        def __init__(self, type, kind,index):
            """
            constructor
            :param type: type of symbol
            :param kind: static/field/argument/var
            :param index: index of symbol
            """
            self.type = type
            self.kind = kind
            self.index = index

    def __init__(self):
        """Creates a new empty symbol table """
        self.symbol_table = dict()
        self.counters = {self.Symbol.ARGUMENT: 0, self.Symbol.VAR: 0,
                         self.Symbol.STATIC: 0, self.Symbol.FIELD: 0}

    def start_subroutine(self):
        """Starts a new subroutine scope"""
        self.symbol_table = dict()
        for kind in self.counters:
            self.counters[kind] = 0

    def define(self, name, type, kind):
        """Defines a new identifier of a given name, type, and kind and
        assigns it a running index. STATIC and FIELD identifiers have a
        class scope, while ARG and VAR identifiers have a subroutine scope. """
        self.symbol_table[name] = self.Symbol(type, kind, self.counters[kind])
        self.counters[kind] += 1

    def var_count(self, kind):
        """Returns the number of variables of the given kind already defined in
        the current scope. """
        return self.counters[kind]

    def kind_of(self, name):
        """Returns the kind of the named identifier in the current scope.
        Returns NONE if the identifier is unknown in the current scope. """
        if name in self.symbol_table:
            return self.symbol_table[name].kind
        return None

    def type_of(self, name):
        """Returns the type of the named identifier in the current scope. """
        if name in self.symbol_table:
            return self.symbol_table[name].type
        return None

    def index_of(self, name):
        """Returns the index assigned to named identifier. """
        if name in self.symbol_table:
            return self.symbol_table[name].index
        return None
