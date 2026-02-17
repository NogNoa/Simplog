# Simplog Parser - Documentation Index

## 📑 Quick Navigation

### Start Here
- **[PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md)** - Overview of entire package and getting started checklist

### Learning Path
1. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** ⭐ START HERE - API and syntax at a glance
2. **[EXAMPLES.md](EXAMPLES.md)** - 10 detailed examples with code
3. **[README_PARSER.md](README_PARSER.md)** - Complete feature and API documentation
4. **[GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md)** - How BNF maps to AST nodes

### Implementation
- **[parser.py](parser.py)** - Source code (~30 KB)
- **[test_parser.py](test_parser.py)** - Test suite and examples

---

## 📚 Documentation Overview

### [QUICK_REFERENCE.md](QUICK_REFERENCE.md) (6 KB)
**Best for**: Developers who want quick answers

- Common functions cheat sheet
- Token types at a glance
- Statement/term type reference tables
- Debugging tips and tricks
- Common error reference

### [EXAMPLES.md](EXAMPLES.md) (25 KB)
**Best for**: Learning by example

**Contains 10 complete examples:**
1. Basic primitive and syntax declarations
2. Type-qualified terms (`::`  operator)
3. Relation statements
4. Conjunction and logical operators
5. Predication statements (`;` operator)
6. Proofs and deductions (`\trfr`)
7. Comma-separated terms
8. Comment handling
9. Numeric and identifier terms
10. Parenthesized terms

**Plus:**
- Complete workflow example
- Performance analysis example
- AST traversal utilities

### [README_PARSER.md](README_PARSER.md) (8 KB)
**Best for**: Complete reference

- Component descriptions
- Language features supported
- Complete usage examples
- AST node reference with all types
- Testing instructions
- Error handling guide
- Implementation notes
- Future enhancements

### [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md) (10 KB)
**Best for**: Understanding AST structure

**Contains:**
- Grammar rule to AST node mapping for each production
- Token to keyword mapping table
- Operator mapping table
- Comment pattern reference
- Example mappings showing BNF → AST

### [PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md) (8 KB)
**Best for**: Architecture and design decisions

- Features overview
- File descriptions
- Architecture explanation
- Design decisions
- Extending the parser
- Performance notes
- Future work roadmap

---

## 🎯 Find Documentation By Task

### "I want to use the parser - where do I start?"
➜ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Installation and basic usage

### "Show me how to parse simplog code"
➜ [EXAMPLES.md](EXAMPLES.md) - Example 1 and 10 for basic parsing

### "What AST node types exist?"
➜ [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md) - Complete mapping with descriptions

### "How do I work with parsed AST?"
➜ [EXAMPLES.md](EXAMPLES.md) - Usage pattern sections in examples 1-7

### "What are all the language features?"
➜ [README_PARSER.md](README_PARSER.md) - Language Features section

### "I'm getting a parse error - what's wrong?"
➜ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Common Errors section

### "How do I extend the parser?"
➜ [PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md) - Extending the Parser section

### "How does the parser work internally?"
➜ [PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md) - Architecture section

### "Show me the BNF grammar compatibility"
➜ [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md) - All grammar rules mapped

### "What operators and keywords exist?"
➜ [PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md) or [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Language Features/Operator sections

---

## 📖 Documentation by Feature

### Comments
- **Overview**: [README_PARSER.md](README_PARSER.md#comments) - Feature descriptions
- **Examples**: [EXAMPLES.md](EXAMPLES.md#example-8-comment-handling) - Example 8
- **Mapping**: [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md#comments) - Comment pattern reference

### Terms  
- **Overview**: [README_PARSER.md](README_PARSER.md#terms) - All term types
- **Mapping**: [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md#terms--term-) - Grammar to AST
- **Examples**: [EXAMPLES.md](EXAMPLES.md#example-7-comma-separated-terms) - Examples 1, 7, 9, 10

### Statements
- **Overview**: [README_PARSER.md](README_PARSER.md#statements) - All statement types  
- **Mapping**: [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md#statements--statement-) - Grammar to AST
- **Examples**: [EXAMPLES.md](EXAMPLES.md#example-2-type-qualified-terms) - Examples 2-6

### Declarations
- **Overview**: [README_PARSER.md](README_PARSER.md#declarations) - `prim`, `def`, `form`, `asrt`, `syn`, `let`
- **Examples**: [EXAMPLES.md](EXAMPLES.md#example-1-basic-primitive-and-syntax-declarations) - Example 1
- **Mapping**: [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md#declarations) - Full mapping

### Qualified Terms
- **Overview**: [README_PARSER.md](README_PARSER.md#qualified-terms) - `::`, `:` operators
- **Examples**: [EXAMPLES.md](EXAMPLES.md#example-2-type-qualified-terms) - Example 2
- **Mapping**: [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md#qualified-terms--qualified-term-) - Grammar to AST

### Relations
- **Overview**: [README_PARSER.md](README_PARSER.md#special-tokens) - Relation operators
- **Examples**: [EXAMPLES.md](EXAMPLES.md#example-3-relation-statements) - Example 3
- **Mapping**: [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md#relation-statements) - Full mapping

### Conjunctions  
- **Overview**: [README_PARSER.md](README_PARSER.md#operators) - `\and` operator
- **Examples**: [EXAMPLES.md](EXAMPLES.md#example-4-conjunction-and-logical-operators) - Example 4
- **Mapping**: [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md#statements--statement-) - Statement mapping

### Proofs/Deductions
- **Overview**: [README_PARSER.md](README_PARSER.md#statements) - Argument statements
- **Examples**: [EXAMPLES.md](EXAMPLES.md#example-6-proofs-and-deductions) - Example 6
- **Mapping**: [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md#deductions) - Full mapping

### Operators
- **Reference**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md#token-types-at-a-glance) - Quick table
- **Detailed**: [README_PARSER.md](README_PARSER.md#operators) - Complete list
- **Mapping**: [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md#operator-mapping) - Operator reference

---

## 🔧 API Reference

### Main Functions (in parser.py)

| Function | Location | Purpose |
|----------|----------|---------|
| `parse_code(source)` | [README_PARSER.md](README_PARSER.md#usage) | Lex and parse in one go |
| `Lexer.tokenize()` | [README_PARSER.md](README_PARSER.md#lexing-only) | Get tokens from source |
| `Parser.parse()` | [README_PARSER.md](README_PARSER.md#manual-parsing) | Parse tokens to AST |
| `ast_to_string(node)` | [README_PARSER.md](README_PARSER.md#usage) | Pretty-print AST |

### AST Node Classes

**All node types listed in:**
- [README_PARSER.md](README_PARSER.md#ast-node-types) - Complete with descriptions
- [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md#grammar-to-ast-node-mapping) - With grammar rules
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md#statement-types-reference) - Quick reference table

---

## 🧪 Testing

### Running Tests
```bash
python test_parser.py
```

### Test Examples Included
- [test_parser.py](test_parser.py) - 6 example test cases

### Documentation Tests
- [EXAMPLES.md](EXAMPLES.md) - 10 complete annotated examples with expected output

---

## 📋 File Structure

```
parser.py                 Main implementation (30 KB)
test_parser.py           Test suite (4 KB)
README_PARSER.md         Full documentation (8 KB)
QUICK_REFERENCE.md       Quick lookup (6 KB)
GRAMMAR_MAPPING.md       BNF-to-AST mapping (10 KB)
EXAMPLES.md              Practical examples (25 KB)
PACKAGE_CONTENTS.md      Architecture overview (8 KB)
INDEX.md                 This file - navigation guide
```

Total documentation: ~65 KB (excluding code)

---

## 🎓 Learning Paths

### Path 1: Just Use It (15 minutes)
1. Read: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) Quick Start section
2. Run: `python test_parser.py`
3. Try: Basic parse_code() example from [EXAMPLES.md](EXAMPLES.md#complete-parsing-workflow-example)

### Path 2: Learn by Example (45 minutes)
1. Read: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) overview
2. Study: [EXAMPLES.md](EXAMPLES.md) - Examples 1-6
3. Try: Modify examples and run them
4. Consult: [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md) when confused

### Path 3: Complete Understanding (2-3 hours)
1. Read: [PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md) - Architecture
2. Study: [README_PARSER.md](README_PARSER.md) - Full reference
3. Study: [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md) - BNF details
4. Read: [EXAMPLES.md](EXAMPLES.md) - All 10 examples
5. Explore: [parser.py](parser.py) source code
6. Try: Write custom AST analysis code

### Path 4: Extend the Parser (Advanced)
1. Complete Path 3 first
2. Read: [PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md#extending-the-parser) - Extension guide
3. Study: Relevant sections of [parser.py](parser.py)
4. Implement: Custom extensions or analysis tools

---

## 🐛 Troubleshooting Guide

| Problem | Documentation |
|---------|---------------|
| Parse error: which line? | [README_PARSER.md](README_PARSER.md#error-handling) - Error messages include location |
| My AST looks wrong | [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md) - Check expected structure |
| What does this node type do? | [README_PARSER.md](README_PARSER.md#ast-node-types) - Node reference |
| How do I traverse the AST? | [EXAMPLES.md](EXAMPLES.md#complete-parsing-workflow-example) - Traversal utilities |
| Parser seems slow | [PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md#performance) - Performance info |
| How do I debug? | [QUICK_REFERENCE.md](QUICK_REFERENCE.md#debugging-tips) - Debugging tutorial |

---

## 📞 Quick Reference Cheat Sheets

- **Syntax**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md#language-syntax-cheat-sheet)
- **Operators**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md#token-types-at-a-glance)
- **APIs**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md#quick-start)
- **Node Types**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md#statement-types-reference)
- **Errors**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md#common-errors)

---

## 🔗 Cross-References

### To understand a BNF rule
BNF Rule → [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md) 
→ See AST nodes and examples

### To parse a specific feature
Feature → [EXAMPLES.md](EXAMPLES.md) 
→ Find example → Copy usage pattern

### To understand an AST node
Node type → [GRAMMAR_MAPPING.md](GRAMMAR_MAPPING.md) or [README_PARSER.md](README_PARSER.md#ast-node-types)
→ See definition and mapping

### To extend the parser
Goal → [PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md#extending-the-parser)
→ Implement → Test

---

**Last Updated**: 2026-02-17  
**Version**: 1.0  
**Status**: Complete  

All 7 documentation files + parser.py ready for use!
