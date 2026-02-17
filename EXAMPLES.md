# Simplog Parser - Examples and Use Cases

## Example 1: Basic Primitive and Syntax Declarations

### Source Code
```simplog
prim <term>
prim <statement>
syn {<term> \and <term>}
```

### AST Structure
```
Statement 1: TermDeclaration
  kind: "prim"
  content: IdentifierTerm("<term>")

Statement 2: TermDeclaration
  kind: "prim"
  content: IdentifierTerm("<statement>")

Statement 3: StatementDeclaration
  kind: "syn"
  statement: ConjunctionStatement
    left: SimpleStatement
      term: IdentifierTerm("<term>")
    right: SimpleStatement
      term: IdentifierTerm("<term>")
```

### Parsing Code
```python
from parser import parse_code, ast_to_string, TermDeclaration, StatementDeclaration

source = open("simple syntax.slg").read()[:200]
ast = parse_code(source)

for stmt in ast:
    if isinstance(stmt, TermDeclaration):
        print(f"Primitive: {stmt.kind}")
    elif isinstance(stmt, StatementDeclaration):
        print(f"Declaration: {stmt.kind}")
        print(ast_to_string(stmt))
```

---

## Example 2: Type-Qualified Terms

### Source Code
```simplog
form {t::<object-term>, g::<type-term>; {t::g ?= t:\is g}}
```

### AST Structure
```
TermDeclaration
  kind: "form"
  content: PredictionStatement
    term: CommaSeqTerm
      terms:
        - QualifiedTerm
          term: IdentifierTerm("t")
          qualifier_type: "dcolon"
          qualifier: IdentifierTerm("<object-term>")
        - QualifiedTerm
          term: IdentifierTerm("g")
          qualifier_type: "dcolon"
          qualifier: IdentifierTerm("<type-term>")
    predicate: BlockStatement
      statement: SimpleStatement
        term: RelationTerm
          left: QualifiedTerm
            term: IdentifierTerm("t")
            qualifier_type: "dcolon"
            qualifier: IdentifierTerm("g")
          relation: IdentifierTerm("\is")
          right: IdentifierTerm("g")
```

### Usage Pattern
```python
from parser import parse_code, TermDeclaration, PredictionStatement, CommaSeqTerm

code = "form {t::<object-term>, g::<type-term>; ...}"
ast = parse_code(code)

form_decl = ast[0]
if isinstance(form_decl, TermDeclaration) and form_decl.kind == "form":
    pred_stmt = form_decl.content
    if isinstance(pred_stmt, PredictionStatement):
        term_list = pred_stmt.term
        if isinstance(term_list, CommaSeqTerm):
            first_qualified = term_list.terms[0]
            print(f"First term: {first_qualified.term}")
            print(f"  qualified as: {first_qualified.qualifier_type}")
            print(f"  type: {first_qualified.qualifier}")
```

---

## Example 3: Relation Statements

### Source Code
```simplog
syn {<term> <relation> <term>}
syn {<object-term> \is <type-term>}
```

### AST Structure
```
StatementDeclaration
  kind: "syn"
  statement: RelationStatement
    left: IdentifierTerm("<term>")
    relation: IdentifierTerm("<relation>")
    right: IdentifierTerm("<term>")

StatementDeclaration
  kind: "syn"
  statement: RelationStatement
    left: IdentifierTerm("<object-term>")
    relation: IdentifierTerm("\is")
    right: IdentifierTerm("<type-term>")
```

### Usage Pattern
```python
from parser import parse_code, RelationStatement

code = "syn {<term> <relation> <term>}"
ast = parse_code(code)
rel_stmt = ast[0].statement

if isinstance(rel_stmt, RelationStatement):
    left_type = type(rel_stmt.left).__name__
    relation_name = rel_stmt.relation.name
    right_type = type(rel_stmt.right).__name__
    print(f"{left_type} {relation_name} {right_type}")
```

---

## Example 4: Conjunction and Logical Operators

### Source Code
```simplog
syn {<statement> \and <statement>}
def {<list> = '{x,v: x \is t \and v \is (<list> t)} \union t}
```

### AST Structure
```
StatementDeclaration
  kind: "syn"
  statement: ConjunctionStatement
    left: SimpleStatement
      term: IdentifierTerm("<statement>")
    right: SimpleStatement
      term: IdentifierTerm("<statement>")
```

### Usage Pattern
```python
from parser import parse_code, ConjunctionStatement

def flatten_conjunctions(node):
    """Extract all conjuncts from a conjunction tree"""
    if isinstance(node, ConjunctionStatement):
        return flatten_conjunctions(node.left) + flatten_conjunctions(node.right)
    else:
        return [node]

code = "syn {a \and b \and c}"
ast = parse_code(code)
conjuncts = flatten_conjunctions(ast[0].statement)
for conj in conjuncts:
    print(f"Conjunct: {conj}")
```

---

## Example 5: Predication Statements

### Source Code
```simplog
syn {<term>;<statement>}
def {... ; {t:: <type-term>; ...}}
```

### AST Structure
```
StatementDeclaration
  kind: "syn"
  statement: PredictionStatement
    term: IdentifierTerm("<term>")
    predicate: SimpleStatement
      term: IdentifierTerm("<statement>")
```

### Usage Pattern
```python
from parser import parse_code, PredictionStatement, BlockStatement

code = "syn {subject; {property \and other}}"
ast = parse_code(code)
stmt = ast[0].statement

if isinstance(stmt, PredictionStatement):
    subject = stmt.term
    property_stmt = stmt.predicate
    
    if isinstance(property_stmt, BlockStatement):
        inner = property_stmt.statement
```

---

## Example 6: Proofs and Deductions

### Source Code
```simplog
prv {T::<statement>| S::<statement> \trfr T}
prv {l:: (<list> t)\\t; {\exist x:: t, v:: (<list> t); l=(x,v)}|
    (<list> t)\\t= '{x,v: x \is t \and v \is (<list> t)} \trfr
    l \in '{x,v: x \is t \and v \is (<list> t)} \trfr
    \exist x:: t, v:: (<list> t); l=(x,v)
}
```

### AST Structure
```
ArgumentStatement
  statement: SimpleStatement (the original statement)
  deduction: Deduction
    premises: Premise
      content: PredictionStatement or Deduction
    conclusion: Conclusion
      content: Statement or Deduction or False_
```

### Usage Pattern
```python
from parser import parse_code, ArgumentStatement, Deduction

code = "prv {stmt1 | logic1 \\trfr logic2}"
ast = parse_code(code)

if isinstance(ast[0], ArgumentStatement):
    arg = ast[0]
    proof_stmt = arg.statement
    deduction = arg.deduction
    
    premise = deduction.premises
    conclusion = deduction.conclusion
    
    # Traverse deduction chain
    current = conclusion
    while hasattr(current, 'content'):
        if isinstance(current.content, Deduction):
            current = current.content.conclusion
        else:
            break
```

---

## Example 7: Comma-Separated Terms

### Source Code
```simplog
form {a:a \is <term>, b: b \is <term>, s: s \is statement; ...}
syn {a,b: a,b \is <term>}
```

### AST Structure
```
CommaSeqTerm
  terms:
    - QualifiedTerm (a:a \is <term>)
    - QualifiedTerm (b: b \is <term>)
    - QualifiedTerm (s: s \is statement)
```

### Usage Pattern
```python
from parser import parse_code, CommaSeqTerm

code = "form {a:a, b:b, c:c; ...}"
ast = parse_code(code)

# Extract all comma-separated elements
def extract_comma_terms(term):
    if isinstance(term, CommaSeqTerm):
        return term.terms
    else:
        return [term]

terms = extract_comma_terms(ast[0].content.term)
for t in terms:
    print(f"Term: {t}")
```

---

## Example 8: Comment Handling

### Source Code
```simplog
/* Block comment 1 */
prim <term>
/* Block comment 2 */

/# Line comment 1
prim <statement>
/# Line comment with continuation \
   and more content

syn {<term> \and <term>}
```

### Behavior
- All comments are stripped during lexing
- No comment nodes appear in the AST
- Line continuations with `\` are handled transparently

### Usage Pattern
```python
from parser import Lexer, parse_code

code = """
/* This comment won't appear in tokens */
prim <term>
/# Neither will this one
"""

# Lexing strips all comments
lexer = Lexer(code)
tokens = lexer.tokenize()
# Comments are gone; only content tokens remain

# Parsing is unaffected by comments
ast = parse_code(code)
# Works the same as code without comments
```

---

## Example 9: Numeric and Simple Identifiers

### Source Code
```simplog
prim 123
prim 3.14
prim identifier
prim <bracketed-identifier>
syn {len(v) + len(u)}
```

### AST Structure
```
TermDeclaration
  kind: "prim"
  content: NumberTerm(value=123)

TermDeclaration
  kind: "prim"
  content: NumberTerm(value=3.14)

TermDeclaration
  kind: "prim"
  content: IdentifierTerm(name="identifier")

TermDeclaration
  kind: "prim"
  content: IdentifierTerm(name="<bracketed-identifier>")
```

### Usage Pattern
```python
from parser import parse_code, IdentifierTerm, NumberTerm, CommaSeqTerm

code = "prim {len(v) + len(u)}"
ast = parse_code(code)

def identify_term_types(term):
    if isinstance(term, IdentifierTerm):
        return f"Identifier: {term.name}"
    elif isinstance(term, NumberTerm):
        return f"Number: {term.value}"
    elif isinstance(term, CommaSeqTerm):
        return f"Sequence: {len(term.terms)} terms"

print(identify_term_types(ast[0].content))
```

---

## Example 10: Parenthesized Terms

### Source Code
```simplog
prim ((x))
syn {(a \and b)}
form {((t::<term>))}
```

### AST Structure
```
ParenthesizedTerm
  term: ParenthesizedTerm
    term: IdentifierTerm("x")
```

### Usage Pattern
```python
from parser import parse_code, ParenthesizedTerm

code = "prim (((nested)))"
ast = parse_code(code)

# Unwrap parentheses
def unwrap_parens(term):
    if isinstance(term, ParenthesizedTerm):
        return unwrap_parens(term.term)
    else:
        return term

core_term = unwrap_parens(ast[0].content)
print(f"Core term: {core_term}")
```

---

## Complete Parsing Workflow Example

```python
from parser import parse_code, ast_to_string
from parser import (TermDeclaration, StatementDeclaration, 
                   SimpleStatement, RelationStatement)

# Load and parse file
with open("simple syntax.slg") as f:
    source = f.read()

try:
    ast = parse_code(source)
    print(f"Successfully parsed {len(ast)} statements")
    
    # Categorize statements
    term_decls = [s for s in ast if isinstance(s, TermDeclaration)]
    stmt_decls = [s for s in ast if isinstance(s, StatementDeclaration)]
    
    print(f"Term declarations: {len(term_decls)}")
    print(f"  - prim: {sum(1 for s in term_decls if s.kind == 'prim')}")
    print(f"  - def: {sum(1 for s in term_decls if s.kind == 'def')}")
    print(f"  - form: {sum(1 for s in term_decls if s.kind == 'form')}")
    print(f"  - let: {sum(1 for s in term_decls if s.kind == 'let')}")
    
    print(f"Statement declarations: {len(stmt_decls)}")
    print(f"  - asrt: {sum(1 for s in stmt_decls if s.kind == 'asrt')}")
    print(f"  - syn: {sum(1 for s in stmt_decls if s.kind == 'syn')}")
    
    # Print first few statements
    print("\nFirst 3 statements:")
    for i, stmt in enumerate(ast[:3]):
        print(f"\n--- Statement {i+1} ---")
        print(ast_to_string(stmt))
        
except SyntaxError as e:
    print(f"Parse error: {e}")
    import traceback
    traceback.print_exc()
```

---

## Performance Analysis Example

```python
from parser import parse_code, TermDeclaration, CommaSeqTerm
import time

# Profile parsing
with open("lists.slg") as f:
    source = f.read()

start = time.time()
ast = parse_code(source)
elapsed = time.time() - start

print(f"Parsed {len(source)} characters in {elapsed:.3f}s")
print(f"Rate: {len(source)/elapsed/1000:.1f} KB/s")
print(f"Total statements: {len(ast)}")

# Analyze complexity
def count_nodes(node):
    count = 1
    for attr in ['term', 'statement', 'terms', 'left', 'right', 'content']:
        value = getattr(node, attr, None)
        if value is None:
            continue
        if isinstance(value, list):
            count += sum(count_nodes(v) for v in value)
        elif hasattr(value, '__dict__'):
            count += count_nodes(value)
    return count

total_nodes = sum(count_nodes(s) for s in ast)
print(f"Total AST nodes: {total_nodes}")
print(f"Average depth: {total_nodes / len(ast):.1f}")
```

---

## AST Traversal Utilities

Here are reusable functions for working with the AST:

```python
from parser import *
from typing import Callable, Any, List

def walk_ast(node: ASTNode, callback: Callable[[ASTNode], Any] = None):
    """Traverse AST and call callback on each node"""
    if callback:
        callback(node)
    
    # Recursively visit child nodes
    for attr_name in ['term', 'statement', 'terms', 'left', 'right', 
                      'content', 'premises', 'conclusion', 'predicate']:
        attr = getattr(node, attr_name, None)
        if attr is None:
            continue
        if isinstance(attr, list):
            for child in attr:
                if isinstance(child, ASTNode):
                    walk_ast(child, callback)
        elif isinstance(attr, ASTNode):
            walk_ast(attr, callback)

def find_all(ast: List[Statement], node_type: type) -> List[ASTNode]:
    """Find all nodes of a specific type"""
    results = []
    
    def collector(node):
        if isinstance(node, node_type):
            results.append(node)
    
    for stmt in ast:
        walk_ast(stmt, collector)
    
    return results

def ast_depth(node: ASTNode) -> int:
    """Calculate maximum depth of AST node"""
    max_child_depth = 0
    
    for attr_name in ['term', 'statement', 'terms', 'left', 'right', 'content']:
        attr = getattr(node, attr_name, None)
        if attr is None:
            continue
        if isinstance(attr, list):
            for child in attr:
                if isinstance(child, ASTNode):
                    max_child_depth = max(max_child_depth, ast_depth(child))
        elif isinstance(attr, ASTNode):
            max_child_depth = max(max_child_depth, ast_depth(attr))
    
    return 1 + max_child_depth
```

---

See the main documentation files for more details:
- [README_PARSER.md](README_PARSER.md)  
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md)
