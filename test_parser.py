#!/usr/bin/env python3
"""
Example usage of the simplog parser
"""

from parser import parse_code, ast_to_string, Lexer

# Example 1: Simple primitive declaration
example1 = """
prim <term>
prim <statement>
"""

# Example 2: Keyword definitions from simple syntax
example2 = """
prim :
prim ;
prim ?=
"""

# Example 3: Operator definition
example3 = """
prim <relation>
syn {<term> <relation> <term>}
"""

# Example 4: More complex statement with conjunction
example4 = """
syn {<term> \and <term>}
"""

# Example 5: Form with pattern
example5 = """
form {<term>:<statement>}
"""

# Example 6: Predication statement (from lists.slg)
example6 = """
prim <object-term>
form {t::<object-term>, g::<type-term>; {t::g ?= t:\\is g}} 
"""


def test_lexer(source: str, label: str):
    """Test the lexer on source code"""
    print(f"\n{'='*60}")
    print(f"LEXER TEST: {label}")
    print(f"{'='*60}")
    print(f"Source:\n{source}\n")
    
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        print("Tokens:")
        for token in tokens[:-1]:  # Skip EOF
            print(f"  {token.type.name:15} {repr(token.value)}")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def test_parser(source: str, label: str):
    """Test the full parser on source code"""
    print(f"\n{'='*60}")
    print(f"PARSER TEST: {label}")
    print(f"{'='*60}")
    print(f"Source:\n{source}\n")
    
    try:
        ast = parse_code(source)
        print("AST:")
        for i, node in enumerate(ast):
            print(f"Statement {i+1}:")
            print(ast_to_string(node, indent=1))
            print()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Test lexer on simple examples
    print("\n" + "="*60)
    print("SIMPLOG PARSER TEST SUITE")
    print("="*60)
    
    test_lexer(example1, "Primitive declarations")
    test_lexer(example2, "Operator declarations")
    test_lexer(example3, "Relation with syntax")
    test_lexer(example4, "Conjunction")
    test_lexer(example5, "Form with colon")
    
    # Test parser
    test_parser(example1, "Primitive declarations")
    test_parser(example2, "Operator declarations")
    test_parser(example3, "Relation with syntax")
    test_parser(example4, "Conjunction")
    test_parser(example5, "Form with colon")
    test_parser(example6, "Complex form from lists.slg")
    
    # Test on actual simplog code
    with open("simple syntax.slg", "r", encoding="utf-8") as f:
        syntax_code = f.read()
    
    test_parser(syntax_code[:500], "Real simplog code (partial)")
