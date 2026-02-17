# Simplog Parser

A complete lexer and parser for the **simplog** formal logic language, as defined by `simplog.bnf`.

## Overview

This parser converts simplog source code into an Abstract Syntax Tree (AST), enabling further processing, analysis, or interpretation of simplog programs.

### Components

1. **Lexer** (`Lexer` class) - Tokenizes source code into tokens
2. **Parser** (`Parser` class) - Parses tokens into an AST
3. **AST Nodes** - Data classes representing language constructs
4. **Utilities** - Helper functions for AST inspection and pretty-printing

## Language Features Supported

### Declarations

- **Term Declarations**: `prim {...}`, `def {...}`, `form {...}`
- **Statement Declarations**: `asrt {...}`, `syn {...}`
- **Let Statements**: `let <statement>`

### Statements

- **Simple Statements**: Term-based statements
- **Qualified Terms**: With type (`::`), predicate (`:`), or relations
- **Relation Statements**: `<term> <relation> <term>`
- **Conjunction**: `<statement> \and <statement>`
- **Predication**: `<term>; <statement>`
- **Arguments/Proofs**: `prv {<statement> | <deduction>}`

### Terms

- **Identifiers**: `word`, `<angle-bracketed>`
- **Numbers**: `123`, `3.14`
- **Parenthesized**: `(<term>)`
- **Comma Sequences**: `<term>, <term>`
- **Relations**: `<term> <relation> <term>`
- **Qualified**: `<term>::<type>`, `<term>:<predicate>`

### Operators

- `\and` - Logical AND
- `\is` - Type membership
- `\trfr` - Therefore (transitive transfer in deductions)
- `\not` - Logical NOT

### Special Tokens

- `::` - Type qualification
- `:` - Predicate/statement qualification
- `;` - Assertion separator
- `?=` - Equivalence in forms
- `|` - Alternative in proofs
- `\` prefix - Escape operator prefix

### Comments

- **Block Comments**: `/* ... */`
- **Line Comments**: `/# ... \` (can be line-continued with `\`)

## Usage

### Basic Parsing

```python
from parser import parse_code, ast_to_string

# Parse source code
source = """
prim <term>
syn {<term> \and <term>}
"""

ast = parse_code(source)

# Pretty-print AST
for statement in ast:
    print(ast_to_string(statement))
```

### Lexing Only

```python
from parser import Lexer

lexer = Lexer(source)
tokens = lexer.tokenize()

for token in tokens:
    print(f"{token.type.name}: {token.value}")
```

### Manual Parsing

```python
from parser import Lexer, Parser

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()
```

## AST Node Types

### Terms

- `IdentifierTerm(name: str)` - Simple identifier
- `NumberTerm(value: int | float)` - Numeric literal
- `ParenthesizedTerm(term: Term)` - Parenthesized term
- `CommaSeqTerm(terms: List[Term])` - Comma-separated terms
- `QualifiedTerm(term, qualifier_type, qualifier)` - Qualified term
- `RelationTerm(left, relation, right)` - Relation between terms

### Statements

- `SimpleStatement(term: Term)` - Basic term statement
- `BlockStatement(statement: Statement)` - Braced statement
- `TermDeclaration(kind, content)` - `prim`, `def`, `form`, or `let`
- `StatementDeclaration(kind, statement)` - `asrt` or `syn`
- `PredictionStatement(term, predicate)` - `term; predicate`
- `RelationStatement(left, relation, right)` - Relation statement
- `ConjunctionStatement(left, right)` - `stmt \and stmt`
- `ArgumentStatement(statement, deduction)` - Proof/argument
- `Deduction(premises, conclusion)` - `premises \trfr conclusion`

### Other Nodes

- `DecapitatedRelation(relation, right)` - Relation without left operand
- `Premise(content)` - Premise in deduction
- `Conclusion(content)` - Conclusion in deduction
- `False_()` - False value in conclusion

## Testing

Run the test suite:

```bash
python test_parser.py
```

This will test the lexer and parser on various simplog code examples.

## Example: Parsing Simple Syntax

```python
from parser import parse_code

code = """
prim <term>
prim <statement>
syn {<term> \and <term>}
"""

ast = parse_code(code)
# Returns list of 3 TermDeclaration and StatementDeclaration nodes
```

## Error Handling

The parser includes detailed error reporting with line and column information:

```python
try:
    ast = parse_code(malformed_code)
except SyntaxError as e:
    print(f"Syntax error: {e}")
    # Output: Syntax error at line 2, column 15: Expected '}'
```

## Grammar Reference

The parser implements the BNF grammar from `simplog.bnf`:

```
<term> ::= "(" <term> ")" | <identifier> | <number> | ...
<statement> ::= <term-declaration> | <statement-declaration> | ...
<qualified-term> ::= <term>::<type> | <term>:<statement> | ...
<relation-statement> ::= <term> <relation> <term>
```

See `simplog.bnf` for the complete formal grammar.

## Implementation Notes

- The lexer handles Unicode characters (supports Hebrew and other scripts)
- Comments are properly stripped before tokenization
- Line continuations in line comments are supported
- The parser uses recursive descent with lookahead
- AST nodes are immutable dataclasses (frozen=True)
- Error messages include precise location information

## Files

- `parser.py` - Main parser implementation
- `test_parser.py` - Test suite with examples
- `simplog.bnf` - Formal grammar definition
- `simple syntax.slg` - Example simplog code
- `lists.slg` - Example with list definitions

## Future Enhancements

Potential extensions:

1. **Semantic Analysis** - Type checking and scoping
2. **Interpreter** - Execute simplog programs
3. **Code Generation** - Compile to other languages
4. **Pretty Printer** - Format AST back to source code
5. **LSP Support** - Language server for IDE integration
