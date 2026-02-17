# Simplog Parser Quick Reference

## Installation & Setup

```python
from parser import parse_code, Lexer, Parser, ast_to_string
```

## Quick Start

```python
# Parse code
ast = parse_code("""
prim <term>
syn {<term> \and <term>}
""")

# Print AST
for stmt in ast:
    print(ast_to_string(stmt))
```

## Core Functions

### `parse_code(source: str) -> List[Statement]`
Complete parse pipeline: lex + parse.

### `Lexer.tokenize() -> List[Token]`
Tokenize source into tokens.

### `Parser.parse() -> List[Statement]`
Parse tokens into AST.

### `ast_to_string(node, indent=0) -> str`
Pretty-print AST node.

## Common AST Navigation

```python
# Get statement kind
stmt = ast[0]
if isinstance(stmt, TermDeclaration):
    print(stmt.kind)  # "prim", "def", "form", "let"

# Get term from simple statement
if isinstance(stmt, SimpleStatement):
    term = stmt.term
    if isinstance(term, IdentifierTerm):
        name = term.name

# Get components of relation statement
if isinstance(stmt, RelationStatement):
    left = stmt.left
    relation = stmt.relation
    right = stmt.right

# Get conjunction parts
if isinstance(stmt, ConjunctionStatement):
    left_stmt = stmt.left
    right_stmt = stmt.right
```

## Token Types at a Glance

| Category | Types |
|----------|-------|
| Punctuation | `LPAREN`, `RPAREN`, `LBRACE`, `RBRACE`, `LANGLE`, `RANGLE` |
| Operators | `COMMA`, `COLON`, `DCOLON`, `SEMICOLON`, `PIPE`, `QEQS` |
| Keywords | `PRIM`, `DEF`, `FORM`, `ASRT`, `SYN`, `PRV`, `LET` |
| Logic Ops | `AND`, `IS`, `TRFR`, `NOT` |
| Literals | `IDENTIFIER`, `NUMBER` |

## Common Patterns

### Parse and Analyze

```python
ast = parse_code(source)

# Filter declarations by kind
prims = [s for s in ast if isinstance(s, TermDeclaration) and s.kind == "prim"]
forms = [s for s in ast if isinstance(s, TermDeclaration) and s.kind == "form"]

# Count statements
total = len(ast)
declarations = sum(1 for s in ast if isinstance(s, (TermDeclaration, StatementDeclaration)))
```

### Error Handling

```python
try:
    ast = parse_code(source)
except SyntaxError as e:
    print(f"Parse error: {e}")
```

### Recursive AST Walking

```python
def walk_ast(node, depth=0):
    indent = "  " * depth
    print(f"{indent}{node.__class__.__name__}")
    
    # Visit child nodes based on type
    if hasattr(node, 'term'):
        walk_ast(node.term, depth + 1)
    if hasattr(node, 'statement'):
        walk_ast(node.statement, depth + 1)
    if hasattr(node, 'terms'):
        for t in node.terms:
            walk_ast(t, depth + 1)
    # ... etc

walk_ast(ast[0])
```

## Statement Types Reference

| Type | Usage | Key Fields |
|------|-------|-----------|
| `TermDeclaration` | `prim {..}`, `def {..}`, `form {..}`, `let {..}` | `kind`, `content`, `pattern` |
| `StatementDeclaration` | `asrt {..}`, `syn {..}` | `kind`, `statement` |
| `SimpleStatement` | Basic term statement | `term` |
| `BlockStatement` | `{..}` | `statement` |
| `RelationStatement` | `t rel t` | `left`, `relation`, `right` |
| `PredictionStatement` | `t; stmt` | `term`, `predicate` |
| `ConjunctionStatement` | `s1 \and s2` | `left`, `right` |
| `ArgumentStatement` | `prv {s \| d}` | `statement`, `deduction` |

## Term Types Reference

| Type | Usage | Key Fields |
|------|-------|-----------|
| `IdentifierTerm` | `word`, `<angle>` | `name` |
| `NumberTerm` | `123`, `3.14` | `value` |
| `ParenthesizedTerm` | `(t)` | `term` |
| `CommaSeqTerm` | `t1, t2` | `terms` |
| `QualifiedTerm` | `t::T`, `t:s` | `term`, `qualifier_type`, `qualifier` |
| `RelationTerm` | `t1 rel t2` | `left`, `relation`, `right` |

## Debugging Tips

### Print all tokens
```python
from parser import Lexer
lexer = Lexer(source)
tokens = lexer.tokenize()
for t in tokens[:-1]:  # Skip EOF
    print(f"{t.type.name:15} {repr(t.value):20} Line {t.line}:{t.column}")
```

### Inspect specific node
```python
stmt = ast[0]
print(f"Type: {type(stmt).__name__}")
print(f"Attributes: {stmt.__dict__}")
```

### Trace parser execution
```python
parser = Parser(tokens)
parser.pos = 0  # Start at beginning
print(f"Current token: {parser._current_token()}")
print(f"Next token: {parser._peek_ahead()}")
```

## Language Syntax Cheat Sheet

```simplog
# Comments
/* block comment */
/# line comment with \
   continuation #/

# Declarations
prim <term>
def {<term> = <term>}
form {<term> ?= <term>}
asrt {<statement>}
syn {<statement>}
let {<statement>}

# Qualified terms
t :: <type>      # Type qualification
t : <stmt>       # Predication
t : rel <term>   # Decapitated relation

# Statements
<term> <rel> <term>      # Relation
s1 \and s2               # Conjunction
t ; <statement>          # Predication
prv {<stmt> | <ded>}     # Proof

# Proof structure
p1 \trfr p2              # Therefore
p1 \trfr p2 \trfr c      # Chained
prv {... | F}            # Contradiction
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "Unexpected character" | Unknown symbol | Check for typos, valid operators use `\` prefix |
| "Expected '}'" | Unmatched braces | Count opening/closing braces |
| "Expected '\\trfr'" | Missing proof separator | Add `\trfr` between premise and conclusion |
| "Unclosed angle bracket" | Missing `>` | Ensure `<identifier>` closes properly |
| "Expected token" | Parser confusion | Check for valid statement structure |

## AST Walking Template

```python
from parser import *

def process_statement(stmt):
    if isinstance(stmt, TermDeclaration):
        return f"Declare {stmt.kind}: {process_term(stmt.content)}"
    elif isinstance(stmt, StatementDeclaration):
        return f"Declare {stmt.kind}: {process_statement(stmt.statement)}"
    elif isinstance(stmt, RelationStatement):
        return f"Relation: {process_term(stmt.left)} {process_term(stmt.relation)} {process_term(stmt.right)}"
    # ... handle other types

def process_term(term):
    if isinstance(term, IdentifierTerm):
        return term.name
    elif isinstance(term, NumberTerm):
        return str(term.value)
    elif isinstance(term, CommaSeqTerm):
        return f"({', '.join(process_term(t) for t in term.terms)})"
    # ... handle other types
```

---

**See [README_PARSER.md](README_PARSER.md) for full documentation**

**See [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md) for BNF-to-AST mapping**
