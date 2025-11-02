"""
Callbacks for the Contract Compliance Dashboard
"""

from dash import Input, Output, State, ALL, MATCH, ctx, callback, no_update
from dash.exceptions import PreventUpdate
import json

def register_callbacks(app, MOCK_CONTRACTS, COLORS, REVIEW_REQUEST_ITEMS):
    """Register all callbacks for the application"""
    
    # Sidebar collapse toggle
    @app.callback(
        [Output('sidebar-container', 'style'),
         Output('sidebar-collapsed', 'data')],
        [Input('sidebar-toggle', 'n_clicks'),
         Input('header-sidebar-trigger', 'n_clicks')],
        [State('sidebar-collapsed', 'data'),
         State('sidebar-container', 'style')]
    )
    def toggle_sidebar(toggle_clicks, header_clicks, is_collapsed, current_style):
        """Toggle sidebar collapsed state"""
        if not toggle_clicks and not header_clicks:
            raise PreventUpdate
        
        new_collapsed = not is_collapsed
        
        if new_collapsed:
            # Collapsed state - narrow sidebar
            new_style = {
                **current_style,
                'minWidth': '60px',
                'maxWidth': '60px',
                'width': '60px'
            }
        else:
            # Expanded state - full width sidebar
            new_style = {
                **current_style,
                'minWidth': '250px',
                'maxWidth': '250px',
                'width': '250px'
            }
        
        return new_style, new_collapsed
    
    # Update sidebar content visibility based on collapsed state
    @app.callback(
        [Output('sidebar-text-header', 'style'),
         Output('request-review-submenu', 'style', allow_duplicate=True)],
        [Input('sidebar-collapsed', 'data')],
        [State('request-review-submenu', 'style')],
        prevent_initial_call=True
    )
    def update_sidebar_content(is_collapsed, submenu_style):
        """Hide/show sidebar header text and submenu when collapsed"""
        if is_collapsed:
            return {'display': 'none'}, {'display': 'none'}
        return {'marginLeft': '8px'}, submenu_style
    
    # Navigation callback
    @app.callback(
        Output('active-view', 'data'),
        [Input({'type': 'nav-item', 'index': ALL}, 'n_clicks')],
        [State('active-view', 'data')]
    )
    def handle_navigation(nav_clicks, current_view):
        """Handle navigation between views"""
        if not any(nav_clicks):
            raise PreventUpdate
        
        # Get which nav item was clicked
        triggered = ctx.triggered_id
        if triggered and 'index' in triggered:
            view_id = triggered['index']
            return view_id
        
        return no_update
    
    # Update active view styling
    @app.callback(
        [Output({'type': 'nav-item', 'index': 'analytics'}, 'style'),
         Output({'type': 'nav-item', 'index': 'reviews'}, 'style'),
         Output({'type': 'nav-item', 'index': 'standards'}, 'style')],
        [Input('active-view', 'data')]
    )
    def update_nav_styling(active_view):
        """Update navigation item styling based on active view"""
        base_style = {
            'padding': '10px 16px',
            'cursor': 'pointer',
            'display': 'flex',
            'alignItems': 'center',
            'fontSize': '14px',
            'color': '#0f172a',
            'transition': 'background-color 0.2s',
            'borderRadius': '6px',
            'margin': '0 8px'
        }
        
        active_style = {
            **base_style,
            'backgroundColor': '#eff6ff',
            'color': '#2563eb',
            'fontWeight': 500
        }
        
        return (
            active_style if active_view == 'analytics' else base_style,
            active_style if active_view == 'reviews' else base_style,
            active_style if active_view == 'standards' else base_style
        )
    
    # Main content callback
    @app.callback(
        Output('main-content', 'children'),
        [Input('active-view', 'data'),
         Input('selected-contract', 'data')]
    )
    def update_main_content(active_view, selected_contract):
        """Update main content area based on active view and selected contract"""
        from layouts import (
            create_analytics_view,
            create_completed_reviews_view,
            create_standards_view,
            create_contract_detail_view
        )
        
        # If a contract is selected, show detail view
        if selected_contract:
            return create_contract_detail_view(selected_contract)
        
        # Otherwise show the appropriate view
        if active_view == 'analytics':
            return create_analytics_view()
        elif active_view == 'reviews':
            return create_completed_reviews_view(MOCK_CONTRACTS)
        elif active_view == 'standards':
            return create_standards_view()
        
        return create_analytics_view()
    
    # Request Review collapsible toggle
    @app.callback(
        [Output('request-review-submenu', 'style'),
         Output('request-review-chevron', 'style')],
        [Input('request-review-trigger', 'n_clicks')],
        [State('request-review-submenu', 'style')]
    )
    def toggle_request_review(n_clicks, current_style):
        """Toggle the Request New Review submenu"""
        if not n_clicks:
            raise PreventUpdate
        
        is_hidden = current_style.get('display') == 'none'
        
        submenu_style = {'display': 'block' if is_hidden else 'none'}
        chevron_style = {
            'transform': 'rotate(180deg)' if is_hidden else 'rotate(0deg)',
            'transition': 'transform 0.2s'
        }
        
        return submenu_style, chevron_style
    
    # Combined contract selection, back button, and navigation callback
    @app.callback(
        Output('selected-contract', 'data'),
        [Input({'type': 'view-contract-btn', 'index': ALL}, 'n_clicks'),
         Input('back-to-reviews-btn', 'n_clicks'),
         Input({'type': 'nav-item', 'index': ALL}, 'n_clicks')],
        [State({'type': 'view-contract-btn', 'index': ALL}, 'id')],
        prevent_initial_call=True
    )
    def handle_contract_selection(view_clicks, back_clicks, nav_clicks, btn_ids):
        """Handle contract selection from table, back button, and navigation"""
        if not ctx.triggered:
            raise PreventUpdate
        
        triggered = ctx.triggered_id
        
        # Handle back button
        if triggered == 'back-to-reviews-btn':
            return None
        
        # Handle navigation - clear selected contract
        if triggered and isinstance(triggered, dict) and triggered.get('type') == 'nav-item':
            return None
        
        # Handle view contract button
        if triggered and isinstance(triggered, dict) and 'index' in triggered:
            contract_id = triggered['index']
            # Find the contract data
            contract = next((c for c in MOCK_CONTRACTS if c['id'] == contract_id), None)
            return contract
        
        raise PreventUpdate
    
    # Toggle collapsible term status breakdowns in contract detail view
    @app.callback(
        Output('collapse-met', 'is_open'),
        [Input('collapse-met-btn', 'n_clicks')],
        [State('collapse-met', 'is_open')],
        prevent_initial_call=True
    )
    def toggle_met_collapse(n_clicks, is_open):
        """Toggle met terms collapse"""
        if n_clicks:
            return not is_open
        return is_open
    
    @app.callback(
        Output('collapse-partial', 'is_open'),
        [Input('collapse-partial-btn', 'n_clicks')],
        [State('collapse-partial', 'is_open')],
        prevent_initial_call=True
    )
    def toggle_partial_collapse(n_clicks, is_open):
        """Toggle partially met terms collapse"""
        if n_clicks:
            return not is_open
        return is_open
    
    @app.callback(
        Output('collapse-missing', 'is_open'),
        [Input('collapse-missing-btn', 'n_clicks')],
        [State('collapse-missing', 'is_open')],
        prevent_initial_call=True
    )
    def toggle_missing_collapse(n_clicks, is_open):
        """Toggle missing terms collapse"""
        if n_clicks:
            return not is_open
        return is_open
    
    # Toggle overall analysis sections in accordion items
    @app.callback(
        Output({'type': 'overall-analysis-collapse', 'index': MATCH}, 'is_open'),
        [Input({'type': 'overall-analysis-btn', 'index': MATCH}, 'n_clicks')],
        [State({'type': 'overall-analysis-collapse', 'index': MATCH}, 'is_open')],
        prevent_initial_call=True
    )
    def toggle_overall_analysis(n_clicks, is_open):
        """Toggle overall analysis collapsible for each term"""
        if n_clicks:
            return not is_open
        return is_open
    
    # Toggle accordion items (main term expansion)
    @app.callback(
        Output({'type': 'accordion-collapse', 'index': MATCH}, 'is_open'),
        [Input({'type': 'accordion-btn', 'index': MATCH}, 'n_clicks')],
        [State({'type': 'accordion-collapse', 'index': MATCH}, 'is_open')],
        prevent_initial_call=True
    )
    def toggle_accordion_item(n_clicks, is_open):
        """Toggle accordion item expansion"""
        if n_clicks:
            return not is_open
        return is_open
    
    # Toggle analysis collapse for individual subpoints
    @app.callback(
        Output({'type': 'analysis-collapse', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'is_open'),
        [Input({'type': 'toggle-analysis-btn', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'n_clicks')],
        [State({'type': 'analysis-collapse', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'is_open')],
        prevent_initial_call=True
    )
    def toggle_analysis_collapse(n_clicks, is_open):
        """Toggle analysis collapse for a subpoint"""
        if n_clicks:
            return not is_open
        return is_open
    
    # Open evidence offcanvas
    @app.callback(
        [Output('evidence-offcanvas', 'is_open'),
         Output('evidence-data-store', 'data'),
         Output('evidence-current-index', 'data')],
        [Input({'type': 'view-evidence-btn', 'term_id': ALL, 'subpoint_idx': ALL}, 'n_clicks'),
         Input('evidence-prev-btn', 'n_clicks'),
         Input('evidence-next-btn', 'n_clicks')],
        [State('evidence-offcanvas', 'is_open'),
         State('evidence-data-store', 'data'),
         State('evidence-current-index', 'data')],
        prevent_initial_call=True
    )
    def handle_evidence_offcanvas(view_clicks_list, prev_clicks, next_clicks, is_open, stored_data, current_index):
        """Handle opening evidence offcanvas and navigation"""
        from contract_detail_view import COMPLIANCE_TERMS
        
        triggered_id = ctx.triggered_id
        
        # Handle navigation buttons
        if triggered_id == 'evidence-prev-btn':
            if stored_data and 'evidence' in stored_data:
                evidence_count = len(stored_data['evidence'])
                new_index = (current_index - 1) % evidence_count
                return is_open, stored_data, new_index
        
        elif triggered_id == 'evidence-next-btn':
            if stored_data and 'evidence' in stored_data:
                evidence_count = len(stored_data['evidence'])
                new_index = (current_index + 1) % evidence_count
                return is_open, stored_data, new_index
        
        # Handle view evidence button clicks
        elif isinstance(triggered_id, dict) and triggered_id.get('type') == 'view-evidence-btn':
            # Find which button was clicked
            term_id = triggered_id.get('term_id')
            subpoint_idx = triggered_id.get('subpoint_idx')
            
            # Find the term and subpoint
            term = next((t for t in COMPLIANCE_TERMS if t['id'] == term_id), None)
            if term and subpoint_idx < len(term['subPoints']):
                subpoint = term['subPoints'][subpoint_idx]
                
                # Store the subpoint data
                subpoint_data = {
                    'heading': subpoint.get('heading', ''),
                    'description': subpoint.get('description', ''),
                    'met': subpoint.get('met', False),
                    'evidence': subpoint.get('evidence', [])
                }
                
                return True, subpoint_data, 0
        
        return no_update, no_update, no_update
    
    # Update evidence offcanvas content
    @app.callback(
        Output('evidence-offcanvas-content', 'children'),
        [Input('evidence-data-store', 'data'),
         Input('evidence-current-index', 'data')],
        prevent_initial_call=True
    )
    def update_evidence_content(subpoint_data, current_index):
        """Update the evidence offcanvas content based on stored data and current index"""
        from evidence_offcanvas import render_evidence_content
        
        if not subpoint_data:
            return html.Div("No evidence selected")
        
        return render_evidence_content(subpoint_data, current_index)
    
    # Update evidence offcanvas title
    @app.callback(
        Output('evidence-offcanvas', 'title'),
        [Input('evidence-data-store', 'data')],
        prevent_initial_call=True
    )
    def update_evidence_title(subpoint_data):
        """Update the offcanvas title based on the subpoint"""
        if subpoint_data:
            return "Evidence Details"
        return "Evidence"
    
    # === ATTESTATION CALLBACKS ===
    
    # Handle Approve button clicks
    @app.callback(
        Output('attestation-store', 'data', allow_duplicate=True),
        [Input({'type': 'approve-btn', 'term_id': ALL, 'subpoint_idx': ALL}, 'n_clicks')],
        [State('attestation-store', 'data'),
         State({'type': 'approve-btn', 'term_id': ALL, 'subpoint_idx': ALL}, 'id')],
        prevent_initial_call=True
    )
    def handle_approve_click(n_clicks_list, attestations, btn_ids):
        """Handle approval of a subpoint result"""
        if not any(n_clicks_list):
            raise PreventUpdate
        
        triggered_id = ctx.triggered_id
        if not triggered_id:
            raise PreventUpdate
        
        term_id = triggered_id['term_id']
        subpoint_idx = triggered_id['subpoint_idx']
        
        # Check if attestation already exists
        existing_idx = None
        for i, att in enumerate(attestations):
            if att['termId'] == term_id and att['subPointIndex'] == subpoint_idx:
                existing_idx = i
                break
        
        # Create or update attestation
        attestation = {
            'termId': term_id,
            'subPointIndex': subpoint_idx,
            'agreed': True,
            'overriddenValue': None,
            'reason': None
        }
        
        if existing_idx is not None:
            attestations[existing_idx] = attestation
        else:
            attestations.append(attestation)
        
        return attestations
    
    # Handle Override button clicks (show editing form)
    @app.callback(
        [Output({'type': 'attestation-initial', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'style'),
         Output({'type': 'attestation-editing', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'style')],
        [Input({'type': 'override-btn', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'n_clicks'),
         Input({'type': 'change-approval-btn', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'n_clicks'),
         Input({'type': 'edit-override-btn', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'n_clicks')],
        prevent_initial_call=True
    )
    def show_override_form(override_click, change_click, edit_click):
        """Show the override editing form"""
        if not any([override_click, change_click, edit_click]):
            raise PreventUpdate
        
        return {'display': 'none'}, {'display': 'block'}
    
    # Handle Cancel Override button
    @app.callback(
        [Output({'type': 'attestation-initial', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'style', allow_duplicate=True),
         Output({'type': 'attestation-editing', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'style', allow_duplicate=True),
         Output({'type': 'attestation-approved', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'style', allow_duplicate=True),
         Output({'type': 'attestation-overridden', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'style', allow_duplicate=True)],
        [Input({'type': 'cancel-override-btn', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'n_clicks')],
        [State('attestation-store', 'data'),
         State({'type': 'cancel-override-btn', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'id')],
        prevent_initial_call=True
    )
    def cancel_override(n_clicks, attestations, btn_id):
        """Cancel override editing and return to previous state"""
        if not n_clicks:
            raise PreventUpdate
        
        term_id = btn_id['term_id']
        subpoint_idx = btn_id['subpoint_idx']
        
        # Find existing attestation
        attestation = None
        for att in attestations:
            if att['termId'] == term_id and att['subPointIndex'] == subpoint_idx:
                attestation = att
                break
        
        # Return to appropriate state
        if attestation:
            if attestation['agreed'] == True:
                return {'display': 'none'}, {'display': 'none'}, {'display': 'flex'}, {'display': 'none'}
            elif attestation['agreed'] == False:
                return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}
        
        return {'display': 'flex'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    
    # Handle Save Override button - update attestation store only (ALL pattern)
    @app.callback(
        Output('attestation-store', 'data', allow_duplicate=True),
        [Input({'type': 'save-override-btn', 'term_id': ALL, 'subpoint_idx': ALL}, 'n_clicks')],
        [State({'type': 'override-dropdown', 'term_id': ALL, 'subpoint_idx': ALL}, 'value'),
         State({'type': 'override-reason-input', 'term_id': ALL, 'subpoint_idx': ALL}, 'value'),
         State('attestation-store', 'data'),
         State({'type': 'save-override-btn', 'term_id': ALL, 'subpoint_idx': ALL}, 'id')],
        prevent_initial_call=True
    )
    def update_attestation_store(n_clicks_list, override_values, reason_values, store, btn_ids):
        if not any(n_clicks_list):
            raise PreventUpdate
        triggered = ctx.triggered_id
        idx = [i for i, idval in enumerate(btn_ids) if idval == triggered][0]
        term_id = btn_ids[idx]['term_id']
        subpoint_idx = btn_ids[idx]['subpoint_idx']
        override_value = override_values[idx]
        reason = reason_values[idx]
        from contract_detail_view import COMPLIANCE_TERMS
        # Helper to convert boolean to status if needed
        def boolean_to_status(met):
            return 'supported' if met else 'not-supported'
        # Find the original value
        original_value = None
        for term in COMPLIANCE_TERMS:
            if term['id'] == term_id:
                if subpoint_idx < len(term['subPoints']):
                    original_value = boolean_to_status(term['subPoints'][subpoint_idx]['met'])
                    break
        # Update store logic, mimicking previous approach
        existing_idx = None
        for i, att in enumerate(store):
            if att['termId'] == term_id and att['subPointIndex'] == subpoint_idx:
                existing_idx = i
                break
        attestation = {
            'termId': term_id,
            'subPointIndex': subpoint_idx,
            'agreed': False,
            'overriddenValue': override_value,
            'reason': reason if reason else None
        }
        if existing_idx is not None:
            store[existing_idx] = attestation
        else:
            store.append(attestation)
        return store
    
    # Handle Save Override UI state - update only subpoint UI (MATCH pattern)
    @app.callback(
        [Output({'type': 'attestation-initial', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'style', allow_duplicate=True),
         Output({'type': 'attestation-editing', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'style', allow_duplicate=True),
         Output({'type': 'attestation-approved', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'style', allow_duplicate=True),
         Output({'type': 'attestation-overridden', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'style', allow_duplicate=True),
         Output({'type': 'override-status-text', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'children'),
         Output({'type': 'override-reason-display', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'children')],
        Input({'type': 'save-override-btn', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'n_clicks'),
        [State({'type': 'override-dropdown', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'value'),
         State({'type': 'override-reason-input', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'value')],
        prevent_initial_call=True
    )
    def update_attestation_ui(n_clicks, override_value, reason):
        if not n_clicks:
            raise PreventUpdate
        # Prepare display values - map status to display text
        status_display = {
            'supported': 'Supported',
            'partially-supported': 'Partially Supported',
            'not-supported': 'Not Supported'
        }
        status_text = f"Overridden: {status_display.get(override_value, override_value)}"
        # Create reason display with bold Reason prefix
        from dash import html
        if reason:
            reason_display = html.Div([
                html.Span("Reason: ", style={'fontWeight': 500}),
                reason
            ])
        else:
            reason_display = ""
        # Show overridden state (hide editing, show overridden)
        return ({'display': 'none'}, {'display': 'none'},
                {'display': 'none'}, {'display': 'block'}, status_text, reason_display)
    
    # Update reason label when dropdown changes
    @app.callback(
        [Output({'type': 'reason-optional-label', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'children'),
         Output({'type': 'reason-asterisk', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'children')],
        [Input({'type': 'override-dropdown', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'value')],
        [State({'type': 'override-dropdown', 'term_id': MATCH, 'subpoint_idx': MATCH}, 'id')],
        prevent_initial_call=True
    )
    def update_reason_label(value, dropdown_id):
        """Update the reason label when dropdown changes"""
        from contract_detail_view import COMPLIANCE_TERMS
        
        term_id = dropdown_id['term_id']
        subpoint_idx = dropdown_id['subpoint_idx']
        
        # Helper to convert boolean to status
        def boolean_to_status(met):
            return 'supported' if met else 'not-supported'
        
        # Find the original value
        original_value = None
        for term in COMPLIANCE_TERMS:
            if term['id'] == term_id:
                if subpoint_idx < len(term['subPoints']):
                    original_value = boolean_to_status(term['subPoints'][subpoint_idx]['met'])
                    break
        
        # Show asterisk if value changed, show "(Optional)" if not changed
        if value == original_value:
            optional_label = " (Optional)"
            asterisk = ""
        else:
            optional_label = ""
            asterisk = "*"
        
        return optional_label, asterisk
    
    # Update all subpoint states based on attestation-store
    @app.callback(
        [Output({'type': 'attestation-initial', 'term_id': ALL, 'subpoint_idx': ALL}, 'style', allow_duplicate=True),
         Output({'type': 'attestation-approved', 'term_id': ALL, 'subpoint_idx': ALL}, 'style', allow_duplicate=True),
         Output({'type': 'attestation-overridden', 'term_id': ALL, 'subpoint_idx': ALL}, 'style', allow_duplicate=True),
         Output({'type': 'override-status-text', 'term_id': ALL, 'subpoint_idx': ALL}, 'children', allow_duplicate=True),
         Output({'type': 'override-reason-display', 'term_id': ALL, 'subpoint_idx': ALL}, 'children', allow_duplicate=True)],
        [Input('attestation-store', 'data')],
        [State({'type': 'attestation-initial', 'term_id': ALL, 'subpoint_idx': ALL}, 'id')],
        prevent_initial_call=True
    )
    def update_all_attestation_states(attestations, all_ids):
        """Update all subpoint attestation states based on the attestation store"""
        initial_styles = []
        approved_styles = []
        overridden_styles = []
        status_texts = []
        reason_displays = []
        
        for comp_id in all_ids:
            term_id = comp_id['term_id']
            subpoint_idx = comp_id['subpoint_idx']
            
            # Find attestation for this subpoint
            attestation = None
            for att in attestations:
                if att['termId'] == term_id and att['subPointIndex'] == subpoint_idx:
                    attestation = att
                    break
            
            if attestation:
                if attestation['agreed'] == True:
                    initial_styles.append({'display': 'none'})
                    approved_styles.append({'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'padding': '8px 12px', 'backgroundColor': '#dcfce7', 'borderRadius': '6px', 'border': '1px solid #bbf7d0'})
                    overridden_styles.append({'display': 'none'})
                    status_texts.append("")
                    reason_displays.append("")
                elif attestation['agreed'] == False:
                    from dash import html
                    initial_styles.append({'display': 'none'})
                    approved_styles.append({'display': 'none'})
                    overridden_styles.append({'display': 'block', 'padding': '8px 12px', 'backgroundColor': '#fffbeb', 'borderRadius': '6px', 'border': '1px solid #fde68a'})
                    status_text = f"Overridden: {'Met' if attestation.get('overriddenValue') else 'Not Met'}"
                    status_texts.append(status_text)
                    
                    # Create reason display with bold "Reason:" prefix
                    if attestation.get('reason'):
                        reason_display = html.Div([
                            html.Span("Reason: ", style={'fontWeight': 500}),
                            attestation.get('reason')
                        ])
                    else:
                        reason_display = ""
                    reason_displays.append(reason_display)
                else:
                    initial_styles.append({'display': 'flex', 'alignItems': 'center', 'gap': '8px'})
                    approved_styles.append({'display': 'none'})
                    overridden_styles.append({'display': 'none'})
                    status_texts.append("")
                    reason_displays.append("")
            else:
                initial_styles.append({'display': 'flex', 'alignItems': 'center', 'gap': '8px'})
                approved_styles.append({'display': 'none'})
                overridden_styles.append({'display': 'none'})
                status_texts.append("")
                reason_displays.append("")
        
        return initial_styles, approved_styles, overridden_styles, status_texts, reason_displays
    
    # Update attestation progress
    @app.callback(
        [Output('reviewed-count', 'children'),
         Output('progress-percentage', 'children'),
         Output('attestation-progress', 'value'),
         Output('attest-review-btn', 'disabled'),
         Output('attest-message', 'children')],
        [Input('attestation-store', 'data')],
        prevent_initial_call=True
    )
    def update_attestation_progress(attestations):
        """Update the attestation progress bar and button state"""
        from contract_detail_view import COMPLIANCE_TERMS
        
        # Calculate total subpoints
        total_points = sum(len(term['subPoints']) for term in COMPLIANCE_TERMS)
        
        # Count reviewed subpoints
        reviewed_count = len([a for a in attestations if a.get('agreed') is not None])
        
        # Calculate percentage
        percentage = (reviewed_count / total_points * 100) if total_points > 0 else 0
        
        # Determine if can attest
        can_attest = reviewed_count == total_points
        
        message = "Click to attest the review" if can_attest else "Please review all subpoints before attesting"
        
        return str(reviewed_count), f"{int(percentage)}%", percentage, not can_attest, message
    
    # Handle Attest Review button
    @app.callback(
        [Output('is-attested-store', 'data'),
         Output('attestation-progress-container', 'style'),
         Output('attested-confirmation', 'style')],
        [Input('attest-review-btn', 'n_clicks')],
        [State('is-attested-store', 'data')],
        prevent_initial_call=True
    )
    def handle_attest_review(n_clicks, is_attested):
        """Handle the attestation of the review"""
        if not n_clicks:
            raise PreventUpdate
        
        # Set attested state
        return True, {'display': 'none'}, {'marginTop': '24px', 'display': 'block'}

# --- Dedicated callback for contract detail 'Back to Reviews' button ---