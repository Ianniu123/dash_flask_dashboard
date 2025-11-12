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
    
    # === TERM-LEVEL ATTESTATION CALLBACKS ===
    
    # Handle Approve Term button clicks
    @app.callback(
        Output('term-attestation-store', 'data', allow_duplicate=True),
        [Input({'type': 'approve-term-btn', 'term_id': ALL}, 'n_clicks')],
        [State('term-attestation-store', 'data'),
         State({'type': 'approve-term-btn', 'term_id': ALL}, 'id')],
        prevent_initial_call=True
    )
    def handle_approve_term_click(n_clicks_list, attestations, btn_ids):
        """Handle approval of a term result"""
        if not any(n_clicks_list):
            raise PreventUpdate
        
        triggered_id = ctx.triggered_id
        if not triggered_id:
            raise PreventUpdate
        
        term_id = triggered_id['term_id']
        
        # Check if attestation already exists
        existing_idx = None
        for i, att in enumerate(attestations):
            if att['termId'] == term_id:
                existing_idx = i
                break
        
        # Create or update attestation
        attestation = {
            'termId': term_id,
            'agreed': True,
            'overriddenValue': None,
            'reason': None
        }
        
        if existing_idx is not None:
            attestations[existing_idx] = attestation
        else:
            attestations.append(attestation)
        
        return attestations
    
    # Handle Override Term button clicks (show editing form)
    @app.callback(
        [Output({'type': 'term-attestation-initial', 'term_id': MATCH}, 'style'),
         Output({'type': 'term-attestation-editing', 'term_id': MATCH}, 'style')],
        [Input({'type': 'override-term-btn', 'term_id': MATCH}, 'n_clicks'),
         Input({'type': 'change-term-approval-btn', 'term_id': MATCH}, 'n_clicks'),
         Input({'type': 'change-term-override-btn', 'term_id': MATCH}, 'n_clicks')],
        prevent_initial_call=True
    )
    def show_term_override_form(override_click, change_click, edit_click):
        """Show the term override editing form"""
        if not any([override_click, change_click, edit_click]):
            raise PreventUpdate
        
        return {'display': 'none'}, {'display': 'block'}
    
    # Handle Cancel Term Override button
    @app.callback(
        [Output({'type': 'term-attestation-initial', 'term_id': MATCH}, 'style', allow_duplicate=True),
         Output({'type': 'term-attestation-editing', 'term_id': MATCH}, 'style', allow_duplicate=True),
         Output({'type': 'term-attestation-approved', 'term_id': MATCH}, 'style', allow_duplicate=True),
         Output({'type': 'term-attestation-overridden', 'term_id': MATCH}, 'style', allow_duplicate=True)],
        [Input({'type': 'cancel-term-override-btn', 'term_id': MATCH}, 'n_clicks')],
        [State('term-attestation-store', 'data'),
         State({'type': 'cancel-term-override-btn', 'term_id': MATCH}, 'id')],
        prevent_initial_call=True
    )
    def cancel_term_override(n_clicks, attestations, btn_id):
        """Cancel term override editing and return to previous state"""
        if not n_clicks:
            raise PreventUpdate
        
        term_id = btn_id['term_id']
        
        # Find existing attestation
        attestation = None
        for att in attestations:
            if att['termId'] == term_id:
                attestation = att
                break
        
        # Return to appropriate state
        if attestation:
            if attestation['agreed'] == True:
                return {'display': 'none'}, {'display': 'none'}, {'display': 'flex'}, {'display': 'none'}
            elif attestation['agreed'] == False:
                return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}
        
        return {'display': 'flex'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    
    # Handle Save Term Override button
    @app.callback(
        Output('term-attestation-store', 'data', allow_duplicate=True),
        [Input({'type': 'save-term-override-btn', 'term_id': ALL}, 'n_clicks')],
        [State({'type': 'term-override-dropdown', 'term_id': ALL}, 'value'),
         State({'type': 'term-override-reason-input', 'term_id': ALL}, 'value'),
         State('term-attestation-store', 'data'),
         State({'type': 'save-term-override-btn', 'term_id': ALL}, 'id')],
        prevent_initial_call=True
    )
    def save_term_override(n_clicks_list, override_values, reasons, attestations, btn_ids):
        """Save term override decision"""
        from contract_detail_view import COMPLIANCE_TERMS, get_term_status
        
        if not any(n_clicks_list):
            raise PreventUpdate
        
        # Find which button was clicked
        triggered_id = ctx.triggered_id
        if not triggered_id:
            raise PreventUpdate
        
        term_id = triggered_id['term_id']
        
        # Find the index of the clicked button
        btn_index = None
        for i, btn_id in enumerate(btn_ids):
            if btn_id['term_id'] == term_id:
                btn_index = i
                break
        
        if btn_index is None:
            raise PreventUpdate
        
        override_value = override_values[btn_index]
        reason = reasons[btn_index]
        
        # Helper to convert term status to dropdown value (now they match)
        def status_to_value(status):
            return status  # Status values now match dropdown values directly
        
        # Find the original value
        original_value = None
        for term in COMPLIANCE_TERMS:
            if term['id'] == term_id:
                original_value = status_to_value(get_term_status(term))
                break
        
        # Validate: if changing the value, reason is required
        if override_value != original_value and (not reason or not reason.strip()):
            raise PreventUpdate
        
        # Check if attestation already exists
        existing_idx = None
        for i, att in enumerate(attestations):
            if att['termId'] == term_id:
                existing_idx = i
                break
        
        # Create or update attestation
        attestation = {
            'termId': term_id,
            'agreed': False,
            'overriddenValue': override_value,
            'reason': reason if reason else None
        }
        
        if existing_idx is not None:
            attestations[existing_idx] = attestation
        else:
            attestations.append(attestation)
        
        return attestations
    
    # Hide editing form after save
    @app.callback(
        Output({'type': 'term-attestation-editing', 'term_id': ALL}, 'style', allow_duplicate=True),
        [Input('term-attestation-store', 'data')],
        [State({'type': 'term-attestation-editing', 'term_id': ALL}, 'id')],
        prevent_initial_call=True
    )
    def hide_editing_forms_after_save(attestations, editing_ids):
        """Hide all editing forms after any save"""
        # Return display:none for all editing forms
        return [{'display': 'none'} for _ in editing_ids]
    
    # Update all term states based on term-attestation-store
    @app.callback(
        [Output({'type': 'term-attestation-initial', 'term_id': ALL}, 'style', allow_duplicate=True),
         Output({'type': 'term-attestation-approved', 'term_id': ALL}, 'style', allow_duplicate=True),
         Output({'type': 'term-attestation-overridden', 'term_id': ALL}, 'style', allow_duplicate=True),
         Output({'type': 'term-override-status-text', 'term_id': ALL}, 'children', allow_duplicate=True),
         Output({'type': 'term-override-reason-display', 'term_id': ALL}, 'children', allow_duplicate=True)],
        [Input('term-attestation-store', 'data')],
        [State({'type': 'term-attestation-initial', 'term_id': ALL}, 'id')],
        prevent_initial_call=True
    )
    def update_all_term_attestation_states(attestations, all_ids):
        """Update all term attestation states based on the attestation store"""
        initial_styles = []
        approved_styles = []
        overridden_styles = []
        status_texts = []
        reason_displays = []
        
        for comp_id in all_ids:
            term_id = comp_id['term_id']
            
            # Find attestation for this term
            attestation = None
            for att in attestations:
                if att['termId'] == term_id:
                    attestation = att
                    break
            
            if attestation:
                if attestation['agreed'] == True:
                    initial_styles.append({'display': 'none'})
                    approved_styles.append({'display': 'flex', 'alignItems': 'center', 'padding': '6px 12px', 'backgroundColor': '#f0fdf4', 'borderRadius': '6px', 'border': '1px solid #bbf7d0'})
                    overridden_styles.append({'display': 'none'})
                    status_texts.append("")
                    reason_displays.append("")
                elif attestation['agreed'] == False:
                    from dash import html
                    initial_styles.append({'display': 'none'})
                    approved_styles.append({'display': 'none'})
                    overridden_styles.append({'display': 'flex', 'alignItems': 'flex-start', 'justifyContent': 'space-between', 'padding': '6px 12px', 'backgroundColor': '#fffbeb', 'borderRadius': '6px', 'border': '1px solid #fde68a'})
                    
                    status_display = {
                        'met': 'Met',
                        'partially-met': 'Partially Met',
                        'missing': 'Missing'
                    }
                    status_text = f"Overridden: {status_display.get(attestation.get('overriddenValue'), attestation.get('overriddenValue'))}"
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
    
    # Update attestation progress (now based on terms instead of subpoints)
    @app.callback(
        [Output('reviewed-count', 'children'),
         Output('progress-percentage', 'children'),
         Output('attestation-progress', 'value'),
         Output('attest-review-btn', 'disabled'),
         Output('attest-message', 'children'),
         Output('attestation-banner-message', 'children')],
        [Input('term-attestation-store', 'data')],
        prevent_initial_call=True
    )
    def update_attestation_progress(attestations):
        """Update the attestation progress bar and button state"""
        from contract_detail_view import COMPLIANCE_TERMS
        
        # Calculate total terms
        total_terms = len(COMPLIANCE_TERMS)
        
        # Count reviewed terms
        reviewed_count = len([a for a in attestations if a.get('agreed') is not None])
        
        # Calculate percentage
        percentage = (reviewed_count / total_terms * 100) if total_terms > 0 else 0
        
        # Determine if can attest
        can_attest = reviewed_count == total_terms
        
        message = "Click to attest the review" if can_attest else "Please review all terms before attesting"
        banner_message = f" - Please review all {total_terms} compliance terms and attest the review when complete ({reviewed_count} of {total_terms} reviewed)."
        
        return str(reviewed_count), f"{int(percentage)}%", percentage, not can_attest, message, banner_message
    
    # Handle Attest Review button
    @app.callback(
        [Output('is-attested-store', 'data'),
         Output('attestation-progress-container', 'style'),
         Output('attested-confirmation', 'style'),
         Output('attested-banner', 'style'),
         Output('unattested-banner', 'style')],
        [Input('attest-review-btn', 'n_clicks')],
        [State('is-attested-store', 'data')],
        prevent_initial_call=True
    )
    def handle_attest_review(n_clicks, is_attested):
        """Handle the attestation of the review"""
        if not n_clicks:
            raise PreventUpdate
        
        # Set attested state
        return True, {'display': 'none'}, {'marginTop': '24px', 'display': 'block'}, {'display': 'block'}, {'display': 'none'}

    # Handle column header clicks for sorting
    @app.callback(
        [Output('reviews-sort-column', 'data'),
         Output('reviews-sort-direction', 'data')],
        [Input({'type': 'sort-header', 'column': ALL}, 'n_clicks')],
        [State('reviews-sort-column', 'data'),
         State('reviews-sort-direction', 'data'),
         State({'type': 'sort-header', 'column': ALL}, 'id')],
        prevent_initial_call=True
    )
    def handle_sort_click(n_clicks, current_column, current_direction, header_ids):
        """Handle sorting when column headers are clicked"""
        if not any(n_clicks):
            raise PreventUpdate
        
        # Find which header was clicked
        triggered = ctx.triggered_id
        if not triggered:
            raise PreventUpdate
        
        clicked_column = triggered['column']
        
        # If same column, toggle direction; otherwise, default to ascending
        if clicked_column == current_column:
            new_direction = 'desc' if current_direction == 'asc' else 'asc'
        else:
            new_direction = 'asc'
        
        return clicked_column, new_direction
    
    # Update table header icons based on sort state
    @app.callback(
        Output('reviews-table-header', 'children'),
        [Input('reviews-sort-column', 'data'),
         Input('reviews-sort-direction', 'data')],
        prevent_initial_call=False
    )
    def update_table_headers(sort_column, sort_direction):
        """Update table headers with sort indicators"""
        from completed_reviews_view import get_sortable_header
        from dash import html
        
        return [
            get_sortable_header("Contract Name", "name", sort_column, sort_direction),
            get_sortable_header("Vendor", "vendor", sort_column, sort_direction),
            get_sortable_header("Review Date", "reviewDate", sort_column, sort_direction),
            get_sortable_header("Terms Matching", "termMatchingRate", sort_column, sort_direction),
            get_sortable_header("Points Matching", "pointsMatchingRate", sort_column, sort_direction),
            get_sortable_header("Jira ID", "jiraId", sort_column, sort_direction),
            get_sortable_header("Athena ID", "athenaId", sort_column, sort_direction),
            get_sortable_header("Reviewer", "reviewer", sort_column, sort_direction),
            html.Th("Actions", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0', 'textAlign': 'right'})
        ]
    
    # Update table body with sorted and filtered data
    @app.callback(
        [Output('reviews-table-body', 'children'),
         Output('reviews-count-display', 'children'),
         Output('reviews-pagination', 'max_value')],
        [Input('reviews-sort-column', 'data'),
         Input('reviews-sort-direction', 'data'),
         Input('reviews-pagination', 'active_page'),
         Input('reviews-search', 'value'),
         Input('reviews-performance-filter', 'value'),
         Input('reviews-start-date', 'date'),
         Input('reviews-end-date', 'date')],
        prevent_initial_call=False
    )
    def update_reviews_table(sort_column, sort_direction, current_page, search_query, 
                            performance_filter, start_date, end_date):
        """Update the reviews table with sorted and filtered data"""
        from completed_reviews_view import get_matching_rate_badge, icon
        from dash import html
        import dash_bootstrap_components as dbc
        from datetime import datetime
        import math
        
        # Start with all contracts
        filtered_contracts = list(MOCK_CONTRACTS)
        
        # Apply search filter
        if search_query:
            search_lower = search_query.lower()
            filtered_contracts = [
                c for c in filtered_contracts
                if search_lower in c['name'].lower() or
                   search_lower in c['vendor'].lower() or
                   search_lower in c['reviewer'].lower() or
                   search_lower in c['jiraEngagementId'].lower() or
                   search_lower in c['athenaId'].lower()
            ]
        
        # Apply performance filter
        if performance_filter and performance_filter != 'all':
            def matches_performance(contract):
                avg_rate = (contract['termMatchingRate'] + contract['pointsMatchingRate']) / 2
                if performance_filter == 'excellent':
                    return avg_rate >= 90
                elif performance_filter == 'good':
                    return avg_rate >= 70 and avg_rate < 90
                elif performance_filter == 'fair':
                    return avg_rate >= 50 and avg_rate < 70
                elif performance_filter == 'poor':
                    return avg_rate < 50
                return True
            
            filtered_contracts = [c for c in filtered_contracts if matches_performance(c)]
        
        # Apply date range filter
        if start_date or end_date:
            def parse_date(date_str):
                """Parse date string like 'Oct 8, 2025' to datetime"""
                try:
                    return datetime.strptime(date_str, '%b %d, %Y')
                except:
                    return None
            
            start_dt = datetime.fromisoformat(start_date) if start_date else None
            end_dt = datetime.fromisoformat(end_date) if end_date else None
            
            filtered_contracts = [
                c for c in filtered_contracts
                if (not start_dt or parse_date(c['reviewDate']) >= start_dt) and
                   (not end_dt or parse_date(c['reviewDate']) <= end_dt)
            ]
        
        # Sort the contracts
        def get_sort_key(contract):
            if sort_column == 'name':
                return contract['name'].lower()
            elif sort_column == 'vendor':
                return contract['vendor'].lower()
            elif sort_column == 'reviewDate':
                # Parse date for proper sorting
                try:
                    return datetime.strptime(contract['reviewDate'], '%b %d, %Y')
                except:
                    return datetime.min
            elif sort_column == 'termMatchingRate':
                return contract['termMatchingRate']
            elif sort_column == 'pointsMatchingRate':
                return contract['pointsMatchingRate']
            elif sort_column == 'jiraId':
                return contract['jiraEngagementId'].split('/')[-1].lower()
            elif sort_column == 'athenaId':
                return contract['athenaId'].split('/')[-1].lower()
            elif sort_column == 'reviewer':
                return contract['reviewer'].lower()
            return ''
        
        filtered_contracts.sort(key=get_sort_key, reverse=(sort_direction == 'desc'))
        
        # Pagination
        items_per_page = 5
        total_pages = math.ceil(len(filtered_contracts) / items_per_page) if len(filtered_contracts) > 0 else 1
        start_index = (current_page - 1) * items_per_page
        end_index = start_index + items_per_page
        paginated_contracts = filtered_contracts[start_index:end_index]
        
        # Build table rows
        table_rows = []
        for contract in paginated_contracts:
            jira_id = contract['jiraEngagementId'].split('/')[-1]
            athena_id = contract['athenaId'].split('/')[-1]
            
            table_rows.append(
                html.Tr([
                    html.Td(contract['name'], style={'padding': '12px', 'color': '#0f172a'}),
                    html.Td(contract['vendor'], style={'padding': '12px', 'color': '#0f172a'}),
                    html.Td(contract['reviewDate'], style={'padding': '12px', 'color': '#475569'}),
                    html.Td(get_matching_rate_badge(contract['termMatchingRate']), style={'padding': '12px'}),
                    html.Td(get_matching_rate_badge(contract['pointsMatchingRate']), style={'padding': '12px'}),
                    html.Td([
                        html.A([
                            html.Span(jira_id, style={'marginRight': '4px'}),
                            icon("mdi:open-in-new", width=12)
                        ], href=contract['jiraEngagementId'], target='_blank',
                           style={'color': '#2563eb', 'textDecoration': 'none', 'fontSize': '14px',
                                  'display': 'flex', 'alignItems': 'center'})
                    ], style={'padding': '12px'}),
                    html.Td([
                        html.A([
                            html.Span(athena_id, style={'marginRight': '4px'}),
                            icon("mdi:open-in-new", width=12)
                        ], href=contract['athenaId'], target='_blank',
                           style={'color': '#2563eb', 'textDecoration': 'none', 'fontSize': '14px',
                                  'display': 'flex', 'alignItems': 'center'})
                    ], style={'padding': '12px'}),
                    html.Td(contract['reviewer'], style={'padding': '12px', 'color': '#475569'}),
                    html.Td([
                        html.Div([
                            dbc.Button(
                                icon("mdi:eye", width=16),
                                id={'type': 'view-contract-btn', 'index': contract['id']},
                                color="link",
                                size="sm",
                                style={'padding': '4px 8px'}
                            ),
                            dbc.Button(
                                icon("mdi:download", width=16),
                                color="link",
                                size="sm",
                                style={'padding': '4px 8px'}
                            )
                        ], style={'display': 'flex', 'gap': '8px', 'justifyContent': 'flex-end'})
                    ], style={'padding': '12px', 'textAlign': 'right'})
                ], style={'borderBottom': '1px solid #e2e8f0'}, className='table-row-hover')
            )
        
        # If no results
        if not table_rows:
            table_rows = [
                html.Tr([
                    html.Td("No contracts found matching your filters",
                           colSpan=9,
                           style={'padding': '24px', 'textAlign': 'center', 'color': '#64748b'})
                ])
            ]
        
        # Update count display
        if len(filtered_contracts) > 0:
            count_text = f"Showing {start_index + 1}-{min(end_index, len(filtered_contracts))} of {len(filtered_contracts)}"
        else:
            count_text = "Showing 0 of 0"
        
        return table_rows, count_text, total_pages
    
    # Reset pagination when filters change
    @app.callback(
        Output('reviews-pagination', 'active_page'),
        [Input('reviews-search', 'value'),
         Input('reviews-performance-filter', 'value'),
         Input('reviews-start-date', 'date'),
         Input('reviews-end-date', 'date')],
        prevent_initial_call=True
    )
    def reset_pagination_on_filter(search, performance, start_date, end_date):
        """Reset to page 1 when filters change"""
        return 1
    
    # Clear date filters
    @app.callback(
        [Output('reviews-start-date', 'date'),
         Output('reviews-end-date', 'date')],
        [Input('reviews-clear-dates', 'n_clicks')],
        prevent_initial_call=True
    )
    def clear_date_filters(n_clicks):
        """Clear date range filters"""
        if not n_clicks:
            raise PreventUpdate
        return None, None
    
    # Update term status breakdown lists with review indicators
    @app.callback(
        [Output('collapse-met', 'children'),
         Output('collapse-partial', 'children'),
         Output('collapse-missing', 'children')],
        [Input('term-attestation-store', 'data')],
        prevent_initial_call=False
    )
    def update_term_status_lists(attestations):
        """Update term status breakdown lists with review indicators"""
        from contract_detail_view import COMPLIANCE_TERMS, get_term_status
        from dash import html
        import dash_bootstrap_components as dbc
        
        # Helper to create badge for review status
        def review_badge(term_id, attestations):
            attested = any(att.get('termId') == term_id and att.get('agreed') is not None 
                          for att in attestations)
            if attested:
                return html.Span('Reviewed', style={
                    'fontSize': '11px',
                    'padding': '2px 6px',
                    'borderRadius': '4px',
                    'backgroundColor': '#dbeafe',
                    'color': '#1e40af',
                    'border': '1px solid #93c5fd',
                    'marginLeft': 'auto',
                    'flexShrink': 0
                })
            else:
                return html.Span('Pending', style={
                    'fontSize': '11px',
                    'padding': '2px 6px',
                    'borderRadius': '4px',
                    'backgroundColor': '#f1f5f9',
                    'color': '#64748b',
                    'border': '1px solid #cbd5e1',
                    'marginLeft': 'auto',
                    'flexShrink': 0
                })
        
        # Met terms list
        met_terms = [term for term in COMPLIANCE_TERMS if get_term_status(term) == "met"]
        met_list = html.Div([
            html.Ul([
                html.Li([
                    html.Div([
                        html.Span("✓", style={'color': '#16a34a', 'marginRight': '8px', 'fontSize': '14px'}),
                        html.Span(term['heading'], style={'fontSize': '13px', 'color': '#334155', 'flex': 1})
                    ], style={'display': 'flex', 'alignItems': 'start', 'flex': 1}),
                    review_badge(term['id'], attestations)
                ], style={'marginBottom': '8px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'gap': '8px'})
                for term in met_terms
            ] if len(met_terms) > 0 else [
                html.Li("None", style={'fontSize': '13px', 'color': '#94a3b8', 'fontStyle': 'italic'})
            ], style={'listStyle': 'none', 'padding': 0, 'margin': 0})
        ], className='term-list-container', style={
            'border': '1px solid #e2e8f0',
            'borderRadius': '6px',
            'padding': '12px',
            'backgroundColor': '#f8fafc',
            'maxHeight': '240px',
            'overflowY': 'auto',
            'marginTop': '8px'
        })
        
        # Partially met and missing terms list (combined in collapse-partial)
        partial_terms = [term for term in COMPLIANCE_TERMS if get_term_status(term) == "partially-met"]
        missing_terms = [term for term in COMPLIANCE_TERMS if get_term_status(term) == "missing"]
        
        partial_list = html.Div([
            html.Ul([
                html.Li([
                    html.Div([
                        html.Span("◐", style={'color': '#eab308', 'marginRight': '8px', 'fontSize': '14px'}),
                        html.Span(term['heading'], style={'fontSize': '13px', 'color': '#334155', 'flex': 1})
                    ], style={'display': 'flex', 'alignItems': 'start', 'flex': 1}),
                    review_badge(term['id'], attestations)
                ], style={'marginBottom': '8px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'gap': '8px'})
                for term in partial_terms
            ] if len(partial_terms) > 0 else [
                html.Li("None", style={'fontSize': '13px', 'color': '#94a3b8', 'fontStyle': 'italic'})
            ], style={'listStyle': 'none', 'padding': 0, 'margin': 0})
        ], className='term-list-container', style={
            'border': '1px solid #e2e8f0',
            'borderRadius': '6px',
            'padding': '12px',
            'backgroundColor': '#f8fafc',
            'maxHeight': '240px',
            'overflowY': 'auto',
            'marginTop': '8px'
        })
        
        # Missing terms list (combined content)
        combined_list_content = []
        
        # Add Partially Met section if any
        if len(partial_terms) > 0:
            combined_list_content.append(
                html.Div([
                    html.Div([
                        html.Span("◐", style={'color': '#eab308', 'marginRight': '6px', 'fontSize': '12px'}),
                        html.Span("Partially Met", style={'fontSize': '12px', 'color': '#92400e', 'fontWeight': 500, 'textTransform': 'uppercase', 'letterSpacing': '0.05em'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '8px', 'paddingBottom': '8px', 'borderBottom': '1px solid #fde68a'}),
                    html.Ul([
                        html.Li([
                            html.Div([
                                html.Span("◐", style={'color': '#eab308', 'marginRight': '8px', 'fontSize': '14px'}),
                                html.Span(term['heading'], style={'fontSize': '13px', 'color': '#334155', 'flex': 1})
                            ], style={'display': 'flex', 'alignItems': 'start', 'flex': 1}),
                            review_badge(term['id'], attestations)
                        ], style={'marginBottom': '8px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'gap': '8px'})
                        for term in partial_terms
                    ], style={'listStyle': 'none', 'padding': 0, 'margin': '0 0 16px 0'})
                ])
            )
        
        # Add Not Met section
        combined_list_content.append(
            html.Div([
                html.Div([
                    html.Span("✗", style={'color': '#dc2626', 'marginRight': '6px', 'fontSize': '12px'}),
                    html.Span("Not Met", style={'fontSize': '12px', 'color': '#991b1b', 'fontWeight': 500, 'textTransform': 'uppercase', 'letterSpacing': '0.05em'})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '8px', 'paddingBottom': '8px', 'borderBottom': '1px solid #fecaca'}),
                html.Ul([
                    html.Li([
                        html.Div([
                            html.Span("✗", style={'color': '#dc2626', 'marginRight': '8px', 'fontSize': '14px'}),
                            html.Span(term['heading'], style={'fontSize': '13px', 'color': '#334155', 'flex': 1})
                        ], style={'display': 'flex', 'alignItems': 'start', 'flex': 1}),
                        review_badge(term['id'], attestations)
                    ], style={'marginBottom': '8px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'gap': '8px'})
                    for term in missing_terms
                ] if len(missing_terms) > 0 else [
                    html.Li("None", style={'fontSize': '13px', 'color': '#94a3b8', 'fontStyle': 'italic'})
                ], style={'listStyle': 'none', 'padding': 0, 'margin': 0})
            ])
        )
        
        missing_list = html.Div(
            combined_list_content,
            className='term-list-container',
            style={
                'border': '1px solid #e2e8f0',
                'borderRadius': '6px',
                'padding': '12px',
                'backgroundColor': '#f8fafc',
                'maxHeight': '240px',
                'overflowY': 'auto',
                'marginTop': '8px'
            }
        )
        
        return met_list, partial_list, missing_list
    
    # Handle export results button - Download component will handle the actual download
    @app.callback(
        [Output('download-results', 'data'),
         Output('export-results-toast', 'is_open')],
        [Input('export-results-btn', 'n_clicks')],
        [State('selected-contract', 'data'),
         State('term-attestation-store', 'data'),
         State('is-attested-store', 'data')],
        prevent_initial_call=True
    )
    def export_results(n_clicks, contract, attestations, is_attested):
        """Export contract review results to JSON file"""
        import json
        from datetime import datetime
        from contract_detail_view import COMPLIANCE_TERMS, get_term_status
        import dash
        
        if not n_clicks or not contract:
            raise PreventUpdate
        
        # Build export data
        total_terms = len(COMPLIANCE_TERMS)
        met_terms = len([t for t in COMPLIANCE_TERMS if get_term_status(t) == "met"])
        partial_terms = len([t for t in COMPLIANCE_TERMS if get_term_status(t) == "partially-met"])
        missing_terms = len([t for t in COMPLIANCE_TERMS if get_term_status(t) == "missing"])
        
        total_points = sum(len(t['subPoints']) for t in COMPLIANCE_TERMS)
        met_points = sum(len([sp for sp in t['subPoints'] if sp['met']]) for t in COMPLIANCE_TERMS)
        
        export_data = {
            'contractInfo': {
                'id': contract['id'],
                'name': contract['name'],
                'vendor': contract['vendor'],
                'reviewDate': contract['reviewDate'],
                'reviewer': contract['reviewer'],
                'status': contract['status'],
                'riskLevel': contract['riskLevel'],
                'jiraEngagementId': contract['jiraEngagementId'],
                'athenaId': contract['athenaId'],
                'termMatchingRate': contract['termMatchingRate'],
                'pointsMatchingRate': contract['pointsMatchingRate']
            },
            'complianceMetrics': {
                'totalTerms': total_terms,
                'metTerms': met_terms,
                'partiallyMetTerms': partial_terms,
                'missingTerms': missing_terms,
                'termsCompliancePercentage': round((met_terms / total_terms) * 100) if total_terms > 0 else 0,
                'totalPoints': total_points,
                'metPoints': met_points,
                'pointsCompliancePercentage': round((met_points / total_points) * 100) if total_points > 0 else 0
            },
            'reviewStatus': {
                'isAttested': is_attested,
                'totalTermsReviewed': len(attestations),
                'reviewedTerms': [
                    {
                        'termId': att['termId'],
                        'termName': next((t['heading'] for t in COMPLIANCE_TERMS if t['id'] == att['termId']), 'Unknown'),
                        'originalStatus': next((get_term_status(t) for t in COMPLIANCE_TERMS if t['id'] == att['termId']), 'unknown'),
                        'approved': att.get('agreed', False),
                        **({'overriddenStatus': att['overriddenValue'], 'overrideReason': att.get('reason')} if att.get('overriddenValue') else {})
                    }
                    for att in attestations
                ]
            },
            'complianceTermsDetails': [
                {
                    'id': term['id'],
                    'heading': term['heading'],
                    'description': term['description'],
                    'overallAnalysis': term.get('overallAnalysis', ''),
                    'status': get_term_status(term),
                    'subPoints': [
                        {
                            'heading': sp['heading'],
                            'description': sp['description'],
                            'met': sp['met'],
                            'analysis': sp.get('analysis', ''),
                            'evidenceCount': len(sp.get('evidence', []))
                        }
                        for sp in term['subPoints']
                    ]
                }
                for term in COMPLIANCE_TERMS
            ],
            'exportDate': datetime.now().isoformat(),
            'exportedBy': contract['reviewer']
        }
        
        # Generate filename
        filename = f"contract-review-{contract['id']}-{datetime.now().strftime('%Y-%m-%d')}.json"
        
        # Return download data
        return dash.dcc.send_string(json.dumps(export_data, indent=2), filename), True