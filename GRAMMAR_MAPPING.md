# Simplog BNF to AST Mapping

This document maps the formal grammar rules in `simplog.bnf` to the corresponding AST node types in the parser implementation.

## Grammar to AST Node Mapping

### Terms (`<term>`)

BNF:
```
<term> ::= "(" <term> ")" | <type-term> | <object-term> | 
           <qualified-term> | <relation-term> | <term> "," <term>
```

AST Nodes:
- `ParenthesizedTerm` - for `"(" <term> ")"`
- `IdentifierTerm` - for simple terms like `<type-term>`, `<object-term>`
- `QualifiedTerm` - for `<qualified-term>`
- `RelationTerm` - for `<relation-term>`
- `CommaSeqTerm` - for comma-separated terms

---

### Qualified Terms (`<qualified-term>`)

BNF:
```
<qualified-term> ::= <object-term>::<type-term> | 
                     <term> ":" <statement> | 
                     <term> ":" <decapitated-relation>
```

AST Node:
- `QualifiedTerm`
  - `qualifier_type`: `"dcolon"` (for `::`) or `"colon"` (for `:`)
  - `qualifier`: Either a `Term`, `Statement`, or `DecapitatedRelation`

---

### Statements (`<statement>`)

BNF:
```
<statement> ::= "{" <statement> "}" | 
                <term-declaration> | 
                <statement-declaration> | 
                <predication-statement> | 
                <relation-statement> | 
                <argument> | 
                <statement> "\and" <statement>
```

AST Nodes:
- `BlockStatement` - for `"{" <statement> "}"`
- `TermDeclaration` - for `<term-declaration>`
- `StatementDeclaration` - for `<statement-declaration>`
- `PredictionStatement` - for `<predication-statement>`
- `RelationStatement` - for `<relation-statement>`
- `ArgumentStatement` - for `<argument>`
- `ConjunctionStatement` - for `<statement> "\and" <statement>`
- `SimpleStatement` - fallback for term-based statements

---

### Term Declarations

BNF:
```
<term-declaration> ::= "prim" "{" <term> "}" | 
                       "def" "{" <predication-statement> "}" |
                       "form" "{" <term> "}" | 
                       "form" "{" <term> "?=" <term> "}"
```

AST Node:
- `TermDeclaration`
  - `kind`: `"prim"`, `"def"`, `"form"`, or `"let"`
  - `content`: The term, statement, or predication
  - `pattern`: Optional (for `form` with `?=`)

---

### Statement Declarations

BNF:
```
<statement-declaration> ::= "asrt" "{" <statement> "}" | 
                            "syn" "{" <statement> "}"
```

AST Node:
- `StatementDeclaration`
  - `kind`: `"asrt"` or `"syn"`
  - `statement`: The nested statement

---

### Predication Statements

BNF:
```
<predication-statement> ::= <term> ";" <statement> | 
                            <term> ";" <decapitated-relation>
```

AST Node:
- `PredictionStatement`
  - `term`: The left-hand term
  - `predicate`: Either a `Statement` or `DecapitatedRelation`

---

### Relation Statements

BNF:
```
<relation-statement> ::= <term> <relation-term> <term>
```

AST Node:
- `RelationStatement`
  - `left`: First term
  - `relation`: The relation term
  - `right`: The second term

---

### Decapitated Relations (Headless Relations)

BNF:
```
<decapitated-relation> ::= <relation-term> <term>
```

AST Node:
- `DecapitatedRelation`
  - `relation`: The relation term
  - `right`: The right operand

---

### Arguments (Proofs)

BNF:
```
<argument> ::= "prv" "{" <statement> "|" <deduction> "}"
```

AST Node:
- `ArgumentStatement`
  - `statement`: The statement being proven
  - `deduction`: The proof/deduction

---

### Deductions

BNF:
```
<deduction> ::= "{" <deduction> "}" | <premise> "\trfr" <conclusion>
```

AST Node:
- `Deduction`
  - `premises`: A `Premise` node
  - `conclusion`: A `Conclusion` node

---

### Premises

BNF:
```
<premise> ::= "{" <premise> "}" | 
              <statement> | 
              <deduction> | 
              <premise> "\and" <premise>
```

AST Node:
- `Premise`
  - `content`: Can be a `Statement`, `Deduction`, or nested `Premise`
- `ConjunctionPremise` - for `<premise> "\and" <premise>`

---

### Conclusions

BNF:
```
<conclusion> ::= <statement> | 
                 <deduction> "\trfr" <conclusion> | 
                 "F"
```

AST Node:
- `Conclusion`
  - `content`: Can be a `Statement`, `Deduction`, or `False_`
- `False_` - represents the `"F"` (contradiction)

---

## Token to Keyword Mapping

| Keyword | Token Type | Usage |
|---------|-----------|-------|
| `prim` | `PRIM` | Primitive term/statement declaration |
| `def` | `DEF` | Defined term/statement declaration |
| `form` | `FORM` | Formal/well-formed declaration |
| `asrt` | `ASRT` | Assertion declaration |
| `syn` | `SYN` | Syntax declaration |
| `prv` | `PRV` | Proof/argument proof |
| `let` | `LET` | Let-binding declaration |
| `\and` | `AND` | Logical conjunction |
| `\is` | `IS` | Type membership |
| `\trfr` | `TRFR` | Therefore (inference) |
| `\not` | `NOT` | Logical negation |

## Operator Mapping

| Operator | Token Type | Meaning |
|----------|-----------|---------|
| `::` | `DCOLON` | Type qualification |
| `:` | `COLON` | Type/statement qualification or relation |
| `;` | `SEMICOLON` | Assertion/predication separator |
| `,` | `COMMA` | Term conjunction/sequencing |
| `?=` | `QEQS` | Equivalence pattern (in `form`) |
| `\|` | `PIPE` | Proof separator (in `prv`) |
| `=` | `EQUALS` | Equality/definition |

## Comments

| Comment Type | Pattern | Token Handling |
|--------------|---------|-----------------|
| Block | `/* ... */` | Stripped during lexing |
| Line | `/#  ... \n` | Stripped during lexing |
| Continuation | `... \` at line end | Merged with next line before comment stripping |

---

## Example Mappings

### Example 1: Simple Declaration

```simplog
prim <term>
```

Maps to:
```python
TermDeclaration(
    kind="prim",
    content=IdentifierTerm(name="<term>")
)
```

### Example 2: Qualified Term Declaration

```simplog
form {t::<object-term>, g::<type-term>; {t::g ?= t:\is g}}
```

Maps to:
```python
TermDeclaration(
    kind="form",
    content=PredictionStatement(
        term=CommaSeqTerm([
            QualifiedTerm(
                term=IdentifierTerm("<object-term>"),
                qualifier_type="dcolon",
                qualifier=IdentifierTerm("<object-term>")
            ),
            QualifiedTerm(
                term=IdentifierTerm("g"),
                qualifier_type="dcolon",
                qualifier=IdentifierTerm("<type-term>")
            )
        ]),
        predicate=BlockStatement(...)
    )
)
```

### Example 3: Relation and Conjunction

```simplog
syn {<term> <relation> <term>}
syn {<statement> \and <statement>}
```

Maps to:
```python
StatementDeclaration(
    kind="syn",
    statement=BlockStatement(
        statement=RelationStatement(
            left=IdentifierTerm("<term>"),
            relation=IdentifierTerm("<relation>"),
            right=IdentifierTerm("<term>")
        )
    )
),
StatementDeclaration(
    kind="syn",
    statement=ConjunctionStatement(
        left=SimpleStatement(IdentifierTerm("<statement>")),
        right=SimpleStatement(IdentifierTerm("<statement>"))
    )
)
```

---

## Notes

1. The parser treats `<angle-bracketed>` identifiers as special term/type placeholders
2. `def` can introduce either term or statement declarations depending on syntax
3. `let` is treated as a variant of term declaration with `kind="let"`
4. Qualified terms are highly flexible and can chain different qualification types
5. Block and line comments are completely stripped during lexing, leaving no trace in the AST
