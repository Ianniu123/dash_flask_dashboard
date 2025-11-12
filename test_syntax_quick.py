#!/usr/bin/env python3
"""Quick syntax check for contract_detail_view.py"""

import sys
import py_compile

try:
    py_compile.compile('contract_detail_view.py', doraise=True)
    print("✅ contract_detail_view.py - No syntax errors!")
    sys.exit(0)
except SyntaxError as e:
    print(f"❌ contract_detail_view.py - Syntax Error:")
    print(f"  Line {e.lineno}: {e.msg}")
    if e.text:
        print(f"  Text: {e.text.strip()}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
