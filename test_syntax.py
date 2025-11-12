"""Test if contract_detail_view.py has syntax errors"""
import sys

try:
    import contract_detail_view
    print("✓ contract_detail_view.py - No syntax errors")
except SyntaxError as e:
    print(f"✗ contract_detail_view.py - Syntax Error:")
    print(f"  Line {e.lineno}: {e.msg}")
    print(f"  Text: {e.text}")
except Exception as e:
    print(f"✗ contract_detail_view.py - Import Error: {e}")

try:
    import callbacks
    print("✓ callbacks.py - No syntax errors")
except SyntaxError as e:
    print(f"✗ callbacks.py - Syntax Error:")
    print(f"  Line {e.lineno}: {e.msg}")
    print(f"  Text: {e.text}")
except Exception as e:
    print(f"✗ callbacks.py - Import Error: {e}")
