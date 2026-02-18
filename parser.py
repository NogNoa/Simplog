"""
Simplog Parser
A parser for the simplog logic language as defined by simplog.bnf
"""

import re
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Union, Any


class TokenType(Enum):
    """Token types for the simplog language"""
    # Literals
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LANGLE = auto()
    RANGLE = auto()
    
    # Operators
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    DCOLON = auto()  # ::
    PIPE = auto()    # |
    EQUALS = auto()  # =
    QEQ = auto()     # ?=
    
    # Keywords
    PRIM = auto()
    DEF = auto()
    FORM = auto()
    ASRT = auto()
    SYN = auto()
    PRV = auto()
    
    # Operators/Relations
    AND = auto()      # \and
    IS = auto()       # \is
    TRFR = auto()     # \trfr
    NOT = auto()      # \not
    
    # Identifiers and values
    IDENTIFIER = auto()
    NUMBER = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()
    

@dataclass
class Token:
    """Represents a single token"""
    type: TokenType
    value: Any
    line: int
    column: int


class Lexer:
    """Tokenizes simplog source code"""
    
    KEYWORDS = {
        'prim': TokenType.PRIM,
        'def': TokenType.DEF,
        'form': TokenType.FORM,
        'asrt': TokenType.ASRT,
        'syn': TokenType.SYN,
        'prv': TokenType.PRV,
    }
    
    OPERATORS = {
        '\\and': TokenType.AND,
        '\\is': TokenType.IS,
        '\\trfr': TokenType.TRFR,
        '\\not': TokenType.NOT,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source"""
        while self.pos < len(self.source):
            self._skip_whitespace_and_comments()
            if self.pos >= len(self.source):
                break
                
            if self._match_single_token():
                continue
            if self._match_operator():
                continue
            if self._match_identifier_or_keyword():
                continue
            if self._match_number():
                continue
                
            # Unknown character
            self._error(f"Unexpected character: {self.source[self.pos]}")
            
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
    
    def _current_char(self) -> str:
        if self.pos < len(self.source):
            return self.source[self.pos]
        return ''
    
    def _peek_char(self, offset: int = 1) -> str:
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return ''
    
    def _advance(self) -> str:
        if self.pos < len(self.source):
            ch = self.source[self.pos]
            self.pos += 1
            if ch == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return ch
        return ''
    
    def _skip_whitespace_and_comments(self):
        """Skip whitespace and comments"""
        while self.pos < len(self.source):
            ch = self._current_char()
            
            # Skip whitespace
            if ch in ' \t\n\r':
                self._advance()
                continue
            
            # Block comment /* ... */
            if ch == '/' and self._peek_char() == '*':
                self._skip_block_comment()
                continue
            
            # Line comment /# ... 
            if ch == '/' and self._peek_char() == '#':
                self._skip_line_comment()
                continue
            
            break
    
    def _skip_block_comment(self):
        """Skip a block comment"""
        self._advance()  # /
        self._advance()  # *
        
        while self.pos < len(self.source):
            if self._current_char() == '*' and self._peek_char() == '/':
                self._advance()  # *
                self._advance()  # /
                return
            self._advance()
    
    def _skip_line_comment(self):
        """Skip a line comment"""
        self._advance()  # /
        self._advance()  # #
        
        while self.pos < len(self.source):
            if self._current_char() == '\n':
                break
            if self._current_char() == '\\' and self._peek_char() == '\n':
                self._advance()  # \
                self._advance()  # \n
                continue
            self._advance()
    
    def _match_single_token(self) -> bool:
        """Match single character tokens"""
        ch = self._current_char()
        token_type = None
        
        single_char_tokens = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '<': TokenType.LANGLE,
            '>': TokenType.RANGLE,
            ',': TokenType.COMMA,
            ';': TokenType.SEMICOLON,
            '|': TokenType.PIPE,
        }
        
        if ch in single_char_tokens:
            token_type = single_char_tokens[ch]
            start_line, start_col = self.line, self.column
            self._advance()
            self.tokens.append(Token(token_type, ch, start_line, start_col))
            return True
        
        # Check for multi-char operators
        if ch == ':':
            start_line, start_col = self.line, self.column
            self._advance()
            if self._current_char() == ':':
                self._advance()
                self.tokens.append(Token(TokenType.DCOLON, '::', start_line, start_col))
            else:
                self.tokens.append(Token(TokenType.COLON, ':', start_line, start_col))
            return True
        
        if ch == '=':
            start_line, start_col = self.line, self.column
            # Single '=' token only (no '==')
            self._advance()
            self.tokens.append(Token(TokenType.EQUALS, '=', start_line, start_col))
            return True
        
        if ch == '?':
            if self._peek_char() == '=':
                start_line, start_col = self.line, self.column
                self._advance()
                self._advance()
                self.tokens.append(Token(TokenType.QEQ, '?=', start_line, start_col))
                return True
        
        if ch == '=':
            start_line, start_col = self.line, self.column
            self._advance()
            self.tokens.append(Token(TokenType.EQUALS, '=', start_line, start_col))
            return True
        
        return False
    
    def _match_operator(self) -> bool:
        """Match multi-character operators"""
        ch = self._current_char()
        
        if ch == '\\':
            start_line, start_col = self.line, self.column
            start_pos = self.pos
            self._advance()
            
            # Build operator name
            op_chars = '\\'
            while self.pos < len(self.source) and self._current_char().isalpha():
                op_chars += self._current_char()
                self._advance()
            
            if op_chars in self.OPERATORS:
                self.tokens.append(Token(self.OPERATORS[op_chars], op_chars, start_line, start_col))
                return True
            else:
                # Not a known operator, put it back
                self.pos = start_pos
                self.column = start_col
                return False
        
        return False
    
    def _match_identifier_or_keyword(self) -> bool:
        """Match identifiers and keywords"""
        ch = self._current_char()
        
        if ch and (ch.isalpha() or ch == '_' or ch == '<'):
            start_line, start_col = self.line, self.column
            
            # Handle <...> identifiers
            if ch == '<':
                self._advance()
                ident = '<'
                while self.pos < len(self.source) and self._current_char() != '>':
                    ident += self._current_char()
                    self._advance()
                if self._current_char() == '>':
                    ident += '>'
                    self._advance()
                    self.tokens.append(Token(TokenType.IDENTIFIER, ident, start_line, start_col))
                    return True
                else:
                    self._error("Unclosed angle bracket")
            
            # Regular identifier
            ident = ''
            while self.pos < len(self.source) and (self._current_char().isalnum() or self._current_char() in '_-'):
                ident += self._current_char()
                self._advance()
            
            if ident in self.KEYWORDS:
                self.tokens.append(Token(self.KEYWORDS[ident], ident, start_line, start_col))
            else:
                self.tokens.append(Token(TokenType.IDENTIFIER, ident, start_line, start_col))
            return True
        
        return False
    
    def _match_number(self) -> bool:
        """Match numeric literals"""
        ch = self._current_char()
        
        if ch and ch.isdigit():
            start_line, start_col = self.line, self.column
            num = ''
            
            while self.pos < len(self.source) and self._current_char().isdigit():
                num += self._current_char()
                self._advance()
            
            # Handle decimal numbers
            if self._current_char() == '.' and self._peek_char() and self._peek_char().isdigit():
                num += self._current_char()
                self._advance()
                while self.pos < len(self.source) and self._current_char().isdigit():
                    num += self._current_char()
                    self._advance()
            
            self.tokens.append(Token(TokenType.NUMBER, float(num) if '.' in num else int(num), start_line, start_col))
            return True
        
        return False
    
    def _error(self, msg: str):
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {msg}")


# AST Node Classes
@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    line: int = field(init=False, default=0)
    column: int = field(init=False, default=0)


@dataclass
class Term(ASTNode):
    """Base class for terms"""
    pass


@dataclass
class AtomicTerm(Term):
    """Atomic term: identifier, relation, or parenthesized atomic"""
    term: Term  # the inner atomic term


@dataclass
class TupleTerm(Term):
    """Tuple of atomic terms: a, b, c or just a"""
    terms: List['AtomicTerm']  # list of atomic terms


@dataclass
class IdentifierTerm(Term):
    """Simple identifier term"""
    name: str
    declared: bool = False


@dataclass
class NumberTerm(Term):
    """Numeric term"""
    value: Union[int, float]


@dataclass
class ParenthesizedTerm(Term):
    """Parenthesized term"""
    term: Term


@dataclass
class CommaSeqTerm(Term):
    """Comma-separated terms"""
    terms: List[Term]


@dataclass
class QualifiedTerm(Term):
    """Qualified term (with type, colon, or relation)"""
    term: Term
    qualifier_type: str  # 'dccolon', 'colon', 'rel'
    qualifier: Union['Term', 'Statement', 'DecapitatedRelation']


@dataclass
class RelationTerm(Term):
    """Relation between terms"""
    left: Term
    relation: Term
    right: Term


@dataclass
class DecapitatedRelation(ASTNode):
    """Relation without left operand"""
    relation: Term
    right: Term


@dataclass
class Statement(ASTNode):
    """Base class for statements"""
    pass


@dataclass
class SimpleStatement(Statement):
    """Simple statement - contains a term"""
    term: Term


@dataclass
class BlockStatement(Statement):
    """Statement wrapped in braces"""
    statement: Statement


@dataclass
class TermDeclaration(Statement):
    """Term declaration: prim, def, or form"""
    kind: str  # 'prim', 'def', 'form'
    content: Union[Term, Statement]
    pattern: Optional[Term] = None  # For form with ?=


@dataclass
class StatementDeclaration(Statement):
    """Statement declaration: asrt or syn"""
    kind: str  # 'asrt', 'syn'
    statement: Statement


@dataclass
class PredictionStatement(Statement):
    """Term ; statement or term ; decapitated-relation"""
    term: Term
    predicate: Union[Statement, DecapitatedRelation]


@dataclass
class RelationStatement(Statement):
    """Relation statement: term relation term"""
    left: Term
    relation: Term
    right: Term


@dataclass
class ConjunctionStatement(Statement):
    """Conjunction of statements: s1 \\and s2"""
    left: Statement
    right: Statement


@dataclass
class ArgumentStatement(Statement):
    """Argument: prv { statement | deduction }"""
    statement: Statement
    deduction: 'Deduction'


@dataclass
class Deduction(ASTNode):
    """Deduction: premise \\trfr conclusion"""
    premises: 'Premise'
    conclusion: 'Conclusion'


@dataclass
class Premise(ASTNode):
    """Premise in deduction"""
    content: Union[Statement, Deduction, 'ConjunctionPremise']


@dataclass
class ConjunctionPremise(Premise):
    """Conjunction of premises"""
    left: Premise
    right: Premise


@dataclass
class Conclusion(ASTNode):
    """Conclusion in deduction"""
    content: Union[Statement, Deduction, 'False_']


@dataclass
class False_(ASTNode):
    """False conclusion"""
    pass


class Parser:
    """Parses simplog tokens into an AST"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.known_terms: set[str] = set()
        self.parsed_statements: List[Statement] = []
        
    def parse(self) -> List[Statement]:
        """Parse tokens into a list of statements"""
        self.parsed_statements = []
        
        while not self._is_at_end():
            if self._check(TokenType.EOF):
                break
            stmt = self._parse_statement()
            self.parsed_statements.append(stmt)
        
        return self.parsed_statements
    
    def _current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def _is_at_end(self) -> bool:
        return self._check(TokenType.EOF)
    
    def _check(self, token_type: TokenType) -> bool:
        return self._current_token().type == token_type
    
    def _match(self, *token_types: TokenType) -> bool:
        for token_type in token_types:
            if self._check(token_type):
                return True
        return False
    
    def _consume(self, token_type: TokenType, msg: str = "") -> Token:
        if self._check(token_type):
            token = self._current_token()
            self.pos += 1
            return token
        self._error(msg or f"Expected {token_type}")
    
    def _advance(self) -> Token:
        token = self._current_token()
        if not self._is_at_end():
            self.pos += 1
        return token
    
    def _peek_ahead(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]  # EOF
    
    def _error(self, msg: str):
        token = self._current_token()
        raise SyntaxError(f"Parse error at line {token.line}, column {token.column}: {msg}")

    # Declaration / symbol table helpers
    def _walk_node(self, node: Any, fn):
        """Recursively walk AST node and call fn(node) for each AST node"""
        if node is None:
            return
        fn(node)
        # traverse known child attributes
        for attr in ('term', 'terms', 'left', 'right', 'relation', 'predicate', 'content', 'statement', 'qualifier', 'premises', 'conclusion'):
            child = getattr(node, attr, None)
            if child is None:
                continue
            if isinstance(child, list):
                for c in child:
                    if hasattr(c, '__dict__'):
                        self._walk_node(c, fn)
            elif hasattr(child, '__dict__'):
                self._walk_node(child, fn)

    def _collect_identifier_names(self, node: Any) -> set:
        names = set()
        def collect(n):
            if isinstance(n, IdentifierTerm):
                names.add(n.name)
        self._walk_node(node, collect)
        return names

    def _mark_declared_in_node(self, node: Any, names: set[str]):
        def mark(n):
            if isinstance(n, IdentifierTerm) and n.name in names:
                n.declared = True
        self._walk_node(node, mark)

    def _register_declaration(self, decl: TermDeclaration):
        # extract identifier names from declaration content
        names = set()
        if isinstance(decl.content, Term):
            names = self._collect_identifier_names(decl.content)
        elif isinstance(decl.content, PredictionStatement):
            names = self._collect_identifier_names(decl.content.term)
        elif isinstance(decl.content, Statement):
            # defensively collect any identifiers inside
            names = self._collect_identifier_names(decl.content)

        if not names:
            return

        # add to known terms
        self.known_terms.update(names)

        # mark identifiers in this declaration as declared
        self._mark_declared_in_node(decl, names)

        # retroactively mark any earlier parsed statements
        for stmt in self.parsed_statements:
            self._mark_declared_in_node(stmt, names)
    
    # Main parsing methods
    
    def _parse_statement(self) -> Statement:
        """Parse a statement"""
        if self._match(TokenType.PRIM):
            return self._parse_term_declaration('prim')
        elif self._match(TokenType.DEF):
            return self._parse_term_or_statement_declaration('def')
        elif self._match(TokenType.FORM):
            return self._parse_term_declaration('form')
        elif self._match(TokenType.ASRT):
            return self._parse_statement_declaration('asrt')
        elif self._match(TokenType.SYN):
            return self._parse_statement_declaration('syn')
        elif self._match(TokenType.PRV):
            return self._parse_argument()
        elif self._match(TokenType.LBRACE):
            self._advance()  # consume '{'
            stmt = self._parse_statement()
            self._consume(TokenType.RBRACE, "Expected '}'")
            return BlockStatement(statement=stmt)
        else:
            # Try to parse as a term-based statement
            return self._parse_base_statement()
    
    def _parse_term_declaration(self, kind: str) -> TermDeclaration:
        """Parse prim ( tuple-term ) or form ( term )"""
        self._advance()  # consume keyword

        # Parens are optional in existing practice; accept either form
        has_paren = False
        if self._match(TokenType.LPAREN):
            has_paren = True
            self._advance()

        if kind == 'prim':
            term = self._parse_tuple_term()
        else:  # form
            term = self._parse_term()

        if kind == 'form' and self._match(TokenType.QEQ):
            self._advance()
            pattern = self._parse_term()
            if has_paren:
                self._consume(TokenType.RPAREN, "Expected ')'")
            decl = TermDeclaration(kind=kind, content=term, pattern=pattern)
        else:
            if has_paren:
                self._consume(TokenType.RPAREN, "Expected ')'")
            decl = TermDeclaration(kind=kind, content=term)

        # register prim/form terms so later occurrences are recognised
        if kind in ('prim', 'form'):
            self._register_declaration(decl)

        return decl

    
    def _parse_term_or_statement_declaration(self, kind: str) -> Union[TermDeclaration, StatementDeclaration]:
        """Parse def ( predication-statement ) where predication = term ; statement"""
        self._advance()  # consume 'def'

        # Parens optional: accept def (t, g; stmt) or def t, g; stmt
        has_paren = False
        if self._match(TokenType.LPAREN):
            has_paren = True
            self._advance()

        # Parse the tuple-term (or single atomic)
        term = self._parse_tuple_term()

        # If predication separator present, parse predicate statement
        if self._match(TokenType.SEMICOLON):
            self._advance()
            statement = self._parse_statement()
            if has_paren:
                self._consume(TokenType.RPAREN, "Expected ')'")
            pred = PredictionStatement(term=term, predicate=statement)
            decl = TermDeclaration(kind=kind, content=pred)
        else:
            if has_paren:
                self._consume(TokenType.RPAREN, "Expected ')'")
            decl = TermDeclaration(kind=kind, content=term)

        # def introduces term names
        self._register_declaration(decl)
        return decl

    
    def _parse_statement_declaration(self, kind: str) -> StatementDeclaration:
        """Parse asrt { statement } or syn { statement }"""
        self._advance()  # consume keyword
        self._consume(TokenType.LBRACE, "Expected '{'")
        
        statement = self._parse_statement()
        self._consume(TokenType.RBRACE, "Expected '}'")
        
        return StatementDeclaration(kind=kind, statement=statement)
    
    def _parse_argument(self) -> ArgumentStatement:
        """Parse prv { statement | deduction }"""
        self._advance()  # consume 'prv'
        self._consume(TokenType.LBRACE, "Expected '{'")
        
        statement = self._parse_statement()
        self._consume(TokenType.PIPE, "Expected '|'")
        
        deduction = self._parse_deduction()
        self._consume(TokenType.RBRACE, "Expected '}'")
        
        return ArgumentStatement(statement=statement, deduction=deduction)
    
    def _parse_deduction(self) -> Deduction:
        """Parse premise \\trfr conclusion"""
        premise = self._parse_premise()
        self._consume(TokenType.TRFR, "Expected '\\trfr'")
        conclusion = self._parse_conclusion()
        
        return Deduction(premises=premise, conclusion=conclusion)
    
    def _parse_premise(self) -> Premise:
        """Parse premise"""
        if self._match(TokenType.LBRACE):
            self._advance()
            premise = self._parse_premise()
            self._consume(TokenType.RBRACE, "Expected '}'")
            return premise
        
        # Simple premise (statement or deduction)
        if self._is_deduction_start():
            return Premise(content=self._parse_deduction())
        else:
            return Premise(content=self._parse_statement())
    
    def _parse_conclusion(self) -> Conclusion:
        """Parse conclusion"""
        if self._current_token().value == 'F':
            self._advance()
            return Conclusion(content=False_())
        elif self._match(TokenType.TRFR):
            # Chained conclusion
            self._advance()
            next_conclusion = self._parse_conclusion()
            return next_conclusion
        else:
            stmt = self._parse_statement()
            return Conclusion(content=stmt)
    
    def _is_deduction_start(self) -> bool:
        """Check if current position starts a deduction"""
        # Look ahead for \trfr
        for i in range(self.pos, min(self.pos + 10, len(self.tokens))):
            if self.tokens[i].type == TokenType.TRFR:
                return True
            if self.tokens[i].type in (TokenType.RBRACE, TokenType.PIPE):
                return False
        return False
    
    def _parse_base_statement(self) -> Statement:
        """Parse base statement (term-based)"""
        term = self._parse_term()
        
        if self._match(TokenType.SEMICOLON):
            self._advance()
            predicate = self._parse_statement()
            return PredictionStatement(term=term, predicate=predicate)
        elif self._check(TokenType.IDENTIFIER) or self._check(TokenType.LANGLE):
            # Could be relation statement
            if self._is_relation():
                relation = self._parse_term()
                right = self._parse_term()
                return RelationStatement(left=term, relation=relation, right=right)
        
        if self._match(TokenType.AND):
            self._advance()
            right = self._parse_statement()
            return ConjunctionStatement(left=SimpleStatement(term=term), right=right)
        
        return SimpleStatement(term=term)
    
    def _is_relation(self) -> bool:
        """Check if current position is a relation"""
        return (self._check(TokenType.IDENTIFIER) or 
                self._check(TokenType.IS) or 
                self._match(TokenType.LANGLE))
    
    def _parse_term(self) -> Term:
        """Parse a term: (term) | tuple-term | qualified-term"""
        # Handle parenthesized term
        if self._match(TokenType.LPAREN):
            self._advance()
            term = self._parse_term()
            self._consume(TokenType.RPAREN, "Expected ')'")
            return ParenthesizedTerm(term=term)
        
        # Try qualified-term first (object-term::type-term or term:statement)
        # These have special markers (:: or :) so we can detect them
        qualified = self._try_parse_qualified_term()
        if qualified:
            return qualified
        
        # Otherwise parse as tuple-term
        return self._parse_tuple_term()

    def _parse_tuple_term(self) -> Term:
        """Parse tuple-term: atomic-term | atomic-term "," tuple-term"""
        terms = []
        terms.append(self._parse_atomic_term())
        
        while self._match(TokenType.COMMA):
            self._advance()
            terms.append(self._parse_atomic_term())
        
        if len(terms) == 1:
            return terms[0]
        return TupleTerm(terms=terms)

    def _parse_atomic_term(self) -> AtomicTerm:
        """Parse atomic-term: (atomic-term) | identifier | relation"""
        # Parenthesized atomic term
        if self._match(TokenType.LPAREN):
            self._advance()
            inner = self._parse_atomic_term()
            self._consume(TokenType.RPAREN, "Expected ')'")
            return AtomicTerm(term=ParenthesizedTerm(term=inner.term if isinstance(inner, AtomicTerm) else inner))
        
        # Parse simple atomic: identifier or relation-term
        left = self._parse_simple_term()
        
        # Check for relation (left-hand side)
        if self._check(TokenType.IDENTIFIER) or self._check(TokenType.LANGLE):
            if self._is_relation():
                relation = self._parse_simple_term()
                right = self._parse_simple_term()
                return AtomicTerm(term=RelationTerm(left=left, relation=relation, right=right))
        
        return AtomicTerm(term=left)

    def _parse_simple_term(self) -> Term:
        """Parse simple term without operators: identifier or number"""
        if self._match(TokenType.IDENTIFIER):
            token = self._advance()
            return IdentifierTerm(name=token.value, declared=(token.value in self.known_terms))
        elif self._match(TokenType.NUMBER):
            token = self._advance()
            return NumberTerm(value=token.value)
        elif self._match(TokenType.LANGLE):
            token = self._advance()
            return IdentifierTerm(name=token.value, declared=(token.value in self.known_terms))
        else:
            self._error(f"Expected term, got {self._current_token().type}")

    def _try_parse_qualified_term(self) -> Optional[Term]:
        """Try to parse qualified-term, return None if not applicable"""
        # Look ahead for :: or : markers
        save_pos = self.pos
        
        try:
            # Try to parse first atomic/identifier
            if self._match(TokenType.IDENTIFIER) or self._match(TokenType.LANGLE):
                first = self._parse_simple_term()
                
                # Check for :: (type qualification)
                if self._match(TokenType.DCOLON):
                    self._advance()
                    qualifier = self._parse_simple_term()
                    return QualifiedTerm(term=first, qualifier_type='dcolon', qualifier=qualifier)
                
                # Check for : (statement or relation qualification)
                if self._match(TokenType.COLON):
                    self._advance()
                    if self._check(TokenType.LBRACE):
                        # term : statement
                        self._advance()
                        statement = self._parse_statement()
                        self._consume(TokenType.RBRACE, "Expected '}'")
                        return QualifiedTerm(term=first, qualifier_type='colon', qualifier=statement)
                    else:
                        # term : decapitated-relation
                        relation = self._parse_simple_term()
                        if self._match(TokenType.IDENTIFIER, TokenType.LANGLE):
                            right = self._parse_simple_term()
                            decap_rel = DecapitatedRelation(relation=relation, right=right)
                            return QualifiedTerm(term=first, qualifier_type='colon', qualifier=decap_rel)
                        else:
                            return QualifiedTerm(term=first, qualifier_type='colon', qualifier=relation)
        except:
            pass
        
        # Not a qualified term, reset and return None
        self.pos = save_pos
        return None


def parse_code(source: str) -> List[Statement]:
    """Convenience function to lex and parse code"""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


# Pretty printing
def ast_to_string(node: ASTNode, indent: int = 0) -> str:
    """Convert AST to readable string representation"""
    prefix = "  " * indent
    
    if isinstance(node, IdentifierTerm):
        return f"{prefix}Identifier: {node.name}"
    elif isinstance(node, NumberTerm):
        return f"{prefix}Number: {node.value}"
    elif isinstance(node, ParenthesizedTerm):
        return f"{prefix}Parenthesized:\n{ast_to_string(node.term, indent + 1)}"
    elif isinstance(node, CommaSeqTerm):
        terms_str = '\n'.join(ast_to_string(t, indent + 1) for t in node.terms)
        return f"{prefix}CommaSequence:\n{terms_str}"
    elif isinstance(node, QualifiedTerm):
        term_str = ast_to_string(node.term, indent + 1)
        qual_str = ast_to_string(node.qualifier, indent + 1)
        return f"{prefix}QualifiedTerm ({node.qualifier_type}):\n{term_str}\n{qual_str}"
    elif isinstance(node, RelationTerm):
        left_str = ast_to_string(node.left, indent + 1)
        rel_str = ast_to_string(node.relation, indent + 1)
        right_str = ast_to_string(node.right, indent + 1)
        return f"{prefix}RelationTerm:\n{left_str}\n{rel_str}\n{right_str}"
    elif isinstance(node, TermDeclaration):
        content_str = ast_to_string(node.content, indent + 1)
        pattern_str = f"\nPattern:\n{ast_to_string(node.pattern, indent + 1)}" if node.pattern else ""
        return f"{prefix}TermDeclaration ({node.kind}):\n{content_str}{pattern_str}"
    elif isinstance(node, SimpleStatement):
        term_str = ast_to_string(node.term, indent + 1)
        return f"{prefix}SimpleStatement:\n{term_str}"
    elif isinstance(node, BlockStatement):
        stmt_str = ast_to_string(node.statement, indent + 1)
        return f"{prefix}BlockStatement:\n{stmt_str}"
    elif isinstance(node, PredictionStatement):
        term_str = ast_to_string(node.term, indent + 1)
        pred_str = ast_to_string(node.predicate, indent + 1)
        return f"{prefix}PredictionStatement:\n{term_str}\n{pred_str}"
    elif isinstance(node, RelationStatement):
        left_str = ast_to_string(node.left, indent + 1)
        rel_str = ast_to_string(node.relation, indent + 1)
        right_str = ast_to_string(node.right, indent + 1)
        return f"{prefix}RelationStatement:\n{left_str}\n{rel_str}\n{right_str}"
    elif isinstance(node, ConjunctionStatement):
        left_str = ast_to_string(node.left, indent + 1)
        right_str = ast_to_string(node.right, indent + 1)
        return f"{prefix}ConjunctionStatement:\n{left_str}\n{right_str}"
    elif isinstance(node, StatementDeclaration):
        stmt_str = ast_to_string(node.statement, indent + 1)
        return f"{prefix}StatementDeclaration ({node.kind}):\n{stmt_str}"
    elif isinstance(node, DecapitatedRelation):
        rel_str = ast_to_string(node.relation, indent + 1)
        right_str = ast_to_string(node.right, indent + 1)
        return f"{prefix}DecapitatedRelation:\n{rel_str}\n{right_str}"
    else:
        return f"{prefix}{node.__class__.__name__}"
