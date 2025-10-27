"""
Completed Reviews View - Contract reviews table with filtering
"""

from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import math

def icon(name, **kwargs):
    """Helper function to create DashIconify icons with CSS color styling"""
    color = kwargs.pop('color', None)
    if color:
        return html.Span(
            DashIconify(icon=name, **kwargs),
            style={'color': color}
        )
    return DashIconify(icon=name, **kwargs)

def get_matching_rate_badge(rate):
    """Get badge for matching rate with appropriate color"""
    if rate >= 90:
        color = '#d1fae5'
        text_color = '#065f46'
    elif rate >= 70:
        color = '#dbeafe'
        text_color = '#1e40af'
    elif rate >= 50:
        color = '#fef3c7'
        text_color = '#92400e'
    else:
        color = '#fee2e2'
        text_color = '#991b1b'
    
    return html.Span(
        f"{rate:.1f}%",
        style={
            'backgroundColor': color,
            'color': text_color,
            'padding': '4px 8px',
            'borderRadius': '4px',
            'fontSize': '12px',
            'fontWeight': 500
        }
    )

def get_completed_reviews_layout(contracts):
    """Get the completed reviews table layout"""
    
    # Pagination
    items_per_page = 5
    total_pages = math.ceil(len(contracts) / items_per_page)
    
    # Build table rows
    table_rows = []
    for contract in contracts[:items_per_page]:  # Show first page
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
    
    return dbc.Card([
        dbc.CardHeader([
            html.Div([
                html.H5("Recent Contract Reviews", style={'margin': 0}),
                html.P("View and manage all reviewed contracts",
                       style={'fontSize': '14px', 'color': '#64748b', 'margin': '8px 0 0 0'})
            ], style={'marginBottom': '16px'}),
            
            # Search
            html.Div([
                html.Div([
                    icon("mdi:magnify", width=16, style={
                        'position': 'absolute',
                        'left': '12px',
                        'top': '50%',
                        'transform': 'translateY(-50%)',
                        'color': '#94a3b8'
                    }),
                    dbc.Input(
                        id='reviews-search',
                        placeholder="Search by contract, vendor, reviewer, Jira ID, or Athena ID...",
                        style={
                            'paddingLeft': '36px',
                            'backgroundColor': '#f8fafc',
                            'border': '1px solid #e2e8f0'
                        }
                    )
                ], style={'position': 'relative', 'marginBottom': '12px'})
            ]),
            
            # Filters
            dbc.Row([
                dbc.Col([
                    dbc.Select(
                        id='reviews-performance-filter',
                        options=[
                            {'label': 'All Performance', 'value': 'all'},
                            {'label': 'Excellent (≥90%)', 'value': 'excellent'},
                            {'label': 'Good (70-89%)', 'value': 'good'},
                            {'label': 'Fair (50-69%)', 'value': 'fair'},
                            {'label': 'Poor (<50%)', 'value': 'poor'}
                        ],
                        value='all',
                        style={'fontSize': '14px'}
                    )
                ], md=3),
                dbc.Col([
                    html.Div([
                        dcc.DatePickerSingle(
                            id='reviews-start-date',
                            placeholder='Start date',
                            display_format='MMM D, YYYY',
                            style={'marginRight': '8px'}
                        ),
                        html.Span("→", style={'color': '#94a3b8', 'margin': '0 8px'}),
                        dcc.DatePickerSingle(
                            id='reviews-end-date',
                            placeholder='End date',
                            display_format='MMM D, YYYY'
                        ),
                        dbc.Button("Clear", color="link", size="sm", id='reviews-clear-dates',
                                   style={'marginLeft': '8px'})
                    ], style={'display': 'flex', 'alignItems': 'center'})
                ], md=6),
                dbc.Col([
                    html.P(f"Showing 1-{min(items_per_page, len(contracts))} of {len(contracts)}",
                           style={'fontSize': '14px', 'color': '#64748b', 'margin': 0, 'textAlign': 'right'})
                ], md=3)
            ])
        ], style={'backgroundColor': 'white', 'borderBottom': '1px solid #e2e8f0'}),
        
        dbc.CardBody([
            # Table
            html.Div([
                html.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("Contract Name", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                            html.Th("Vendor", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                            html.Th("Review Date", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                            html.Th("Terms Matching", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                            html.Th("Points Matching", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                            html.Th("Jira ID", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                            html.Th("Athena ID", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                            html.Th("Reviewer", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                            html.Th("Actions", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0', 'textAlign': 'right'})
                        ])
                    ]),
                    html.Tbody(table_rows, id='reviews-table-body')
                ], style={'width': '100%', 'borderCollapse': 'collapse', 'fontSize': '14px'})
            ], style={'overflowX': 'auto'}),
            
            # Pagination
            html.Div([
                dbc.Pagination(
                    id='reviews-pagination',
                    max_value=total_pages,
                    first_last=True,
                    previous_next=True,
                    fully_expanded=False,
                    active_page=1
                )
            ], style={'marginTop': '16px', 'display': 'flex', 'justifyContent': 'center'})
        ], style={'padding': '0'})
    ])
