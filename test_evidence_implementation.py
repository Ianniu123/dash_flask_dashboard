"""
Quick validation script for evidence and analysis implementation
Run this to verify the implementation is working correctly
"""

def test_data_structure():
    """Test that the data structure has the required fields"""
    from contract_detail_view import COMPLIANCE_TERMS
    
    print("Testing COMPLIANCE_TERMS data structure...")
    print(f"Total terms: {len(COMPLIANCE_TERMS)}")
    
    evidence_count = 0
    analysis_count = 0
    
    for term in COMPLIANCE_TERMS:
        for sp in term['subPoints']:
            if sp.get('evidence'):
                evidence_count += len(sp.get('evidence', []))
            if sp.get('analysis'):
                analysis_count += 1
    
    print(f"Total evidence items: {evidence_count}")
    print(f"Total subpoints with analysis: {analysis_count}")
    
    # Check first term with evidence
    first_term = COMPLIANCE_TERMS[0]
    first_subpoint = first_term['subPoints'][0]
    
    print(f"\nSample subpoint: {first_subpoint['heading']}")
    print(f"  - Has evidence: {bool(first_subpoint.get('evidence'))}")
    print(f"  - Evidence count: {len(first_subpoint.get('evidence', []))}")
    print(f"  - Has analysis: {bool(first_subpoint.get('analysis'))}")
    
    if first_subpoint.get('evidence'):
        print(f"  - First evidence excerpt: {first_subpoint['evidence'][0]['excerpt'][:50]}...")
    
    return True

def test_component_imports():
    """Test that all components can be imported"""
    print("\nTesting component imports...")
    
    try:
        from evidence_offcanvas import create_evidence_offcanvas, render_evidence_content
        print("  ✓ evidence_offcanvas imports successful")
    except Exception as e:
        print(f"  ✗ evidence_offcanvas import failed: {e}")
        return False
    
    try:
        from contract_detail_view import get_contract_detail_layout, COMPLIANCE_TERMS
        print("  ✓ contract_detail_view imports successful")
    except Exception as e:
        print(f"  ✗ contract_detail_view import failed: {e}")
        return False
    
    return True

def test_offcanvas_creation():
    """Test that the offcanvas component can be created"""
    print("\nTesting offcanvas creation...")
    
    try:
        from evidence_offcanvas import create_evidence_offcanvas
        offcanvas = create_evidence_offcanvas()
        print(f"  ✓ Offcanvas created: {offcanvas.id}")
        print(f"  ✓ Offcanvas placement: {offcanvas.placement}")
    except Exception as e:
        print(f"  ✗ Offcanvas creation failed: {e}")
        return False
    
    return True

def test_evidence_rendering():
    """Test that evidence content can be rendered"""
    print("\nTesting evidence content rendering...")
    
    try:
        from evidence_offcanvas import render_evidence_content
        from contract_detail_view import COMPLIANCE_TERMS
        
        # Get first subpoint with evidence
        first_term = COMPLIANCE_TERMS[0]
        first_subpoint = first_term['subPoints'][0]
        
        content = render_evidence_content(first_subpoint, 0)
        print(f"  ✓ Evidence content rendered successfully")
        print(f"  ✓ Content type: {type(content)}")
    except Exception as e:
        print(f"  ✗ Evidence rendering failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("="*60)
    print("Evidence and Analysis Implementation Validation")
    print("="*60)
    
    tests = [
        ("Data Structure", test_data_structure),
        ("Component Imports", test_component_imports),
        ("Offcanvas Creation", test_offcanvas_creation),
        ("Evidence Rendering", test_evidence_rendering)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("\n✓ All tests passed! Implementation is ready to use.")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
