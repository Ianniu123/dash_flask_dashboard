"""
Quick script to verify that back-to-reviews-btn exists in the layout
"""
from app import app

def find_component_by_id(component, target_id, path=""):
    """Recursively search for a component with a specific ID"""
    # Check if this component has an id
    if hasattr(component, 'id') and component.id == target_id:
        return True, path
    
    # Check children
    if hasattr(component, 'children'):
        children = component.children
        if children is None:
            return False, ""
        
        # Handle different types of children
        if isinstance(children, list):
            for i, child in enumerate(children):
                found, child_path = find_component_by_id(child, target_id, f"{path}[{i}]")
                if found:
                    return True, child_path
        else:
            found, child_path = find_component_by_id(children, target_id, f"{path}.children")
            if found:
                return True, child_path
    
    return False, ""

# Check if back-to-reviews-btn exists
found, path = find_component_by_id(app.layout, 'back-to-reviews-btn')

if found:
    print("✓ back-to-reviews-btn found in layout!")
    print(f"  Path: {path}")
else:
    print("✗ back-to-reviews-btn NOT found in layout")
    print("\nSearching for all button IDs in layout...")
    
    def find_all_ids(component, prefix=""):
        """Find all component IDs"""
        ids = []
        if hasattr(component, 'id') and component.id:
            ids.append(component.id)
        
        if hasattr(component, 'children'):
            children = component.children
            if children is not None:
                if isinstance(children, list):
                    for child in children:
                        ids.extend(find_all_ids(child, prefix))
                else:
                    ids.extend(find_all_ids(children, prefix))
        
        return ids
    
    all_ids = find_all_ids(app.layout)
    print(f"Found {len(all_ids)} components with IDs:")
    for comp_id in sorted(all_ids):
        if isinstance(comp_id, str):
            print(f"  - {comp_id}")
        else:
            print(f"  - {comp_id} (pattern matching)")
