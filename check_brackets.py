"""
Check for bracket mismatches in contract_detail_view.py
"""

def check_brackets(filename):
    """Check if brackets are balanced in a Python file"""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Track bracket counts
    brackets = {
        '(': 0,
        '[': 0,
        '{': 0
    }
    
    # Track positions for debugging
    positions = {
        '(': [],
        '[': [],
        '{': []
    }
    
    in_string = False
    in_comment = False
    escape_next = False
    string_char = None
    
    for i, char in enumerate(content):
        # Handle escape characters
        if escape_next:
            escape_next = False
            continue
        
        if char == '\\':
            escape_next = True
            continue
        
        # Handle strings
        if char in ['"', "'"] and not in_comment:
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None
            continue
        
        # Skip if in string or comment
        if in_string:
            continue
        
        # Handle comments
        if char == '#':
            in_comment = True
            continue
        
        if char == '\n':
            in_comment = False
            continue
        
        # Count brackets
        if char in '([{':
            brackets[char] += 1
            positions[char].append(i)
        elif char == ')':
            brackets['('] -= 1
        elif char == ']':
            brackets['['] -= 1
        elif char == '}':
            brackets['{'] -= 1
    
    print(f"Bracket Analysis for {filename}:")
    print(f"  Parentheses ( ): {brackets['(']}")
    print(f"  Square brackets [ ]: {brackets['[']}")
    print(f"  Curly braces {{ }}: {brackets['{']}")
    
    if all(count == 0 for count in brackets.values()):
        print("  ✓ All brackets are balanced!")
        return True
    else:
        print("  ✗ Brackets are NOT balanced!")
        return False

if __name__ == '__main__':
    check_brackets('contract_detail_view.py')
