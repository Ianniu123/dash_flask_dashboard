"""
Analytics View - Contract compliance analytics dashboard
"""

from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash
from dash import dash_table
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

def icon(name, **kwargs):
    """Helper function to create DashIconify icons"""
    return DashIconify(icon=name, **kwargs)

# Generate mock analytics data
def generate_mock_analytics_data():
    """Generate mock contract analytics data"""
    vendors = ["Acme Corp", "TechStack Inc", "CloudServe Ltd", "DataFlow Systems", 
               "Global Solutions", "Consulting Partners", "Innovation Labs", "HostTech Inc"]
    reviewers = ["Sarah Johnson", "Michael Chen", "Emily Rodriguez", "David Park"]
    standards = ["gdpr", "soc2", "hipaa", "ccpa", "iso27001", "pci-dss"]
    
    contracts = []
    for i in range(25):
        days_ago = random.randint(0, 180)
        review_date = datetime.now() - timedelta(days=days_ago)
        
        total_terms = 40
        terms_met = random.randint(15, 35)
        terms_missing = random.randint(0, 10)
        terms_partial = total_terms - terms_met - terms_missing
        
        # Generate individual term status for all 40 terms
        term_status = {}
        for term in COMPLIANCE_TERMS:
            rand = random.random()
            # Weighted distribution: more terms are met than missing
            if rand < 0.6:
                term_status[term] = "met"
            elif rand < 0.85:
                term_status[term] = "partially-met"
            else:
                term_status[term] = "missing"
        
        contracts.append({
            'id': f'contract-{i}',
            'name': f'{random.choice(vendors)} Agreement {i+1}',
            'vendor': random.choice(vendors),
            'reviewDate': review_date,
            'standard': random.choice(standards),
            'reviewer': random.choice(reviewers),
            'reviewDuration': random.randint(2, 14),
            'termsMet': terms_met,
            'termsMissing': terms_missing,
            'termsPartiallyMet': terms_partial,
            'termStatus': term_status
        })
    
    return contracts

# All 40 compliance terms
COMPLIANCE_TERMS = [
    "Data Encryption Requirements",
    "Third-Party Data Disclosure",
    "Data Breach Notification",
    "Data Retention and Deletion",
    "Access Control and Authentication",
    "Audit Rights and Compliance Reporting",
    "Liability and Indemnification",
    "Subprocessor Management",
    "Business Continuity and Disaster Recovery",
    "Termination and Data Portability",
    "Privacy Impact Assessment",
    "Vendor Security Training",
    "Incident Response Procedures",
    "Penetration Testing Requirements",
    "Data Classification Standards",
    "Change Management Process",
    "Vulnerability Management",
    "Physical Security Controls",
    "Secure Development Lifecycle",
    "Network Segmentation",
    "Logging and Monitoring",
    "API Security Standards",
    "Mobile Device Security",
    "Email Security Controls",
    "Password Policy Compliance",
    "Cloud Security Requirements",
    "Endpoint Protection Standards",
    "Vendor Risk Assessment",
    "Data Anonymization Standards",
    "Cryptographic Standards",
    "Wireless Network Security",
    "Database Security Controls",
    "Backup and Recovery Standards",
    "Secure Configuration Management",
    "Social Engineering Defense",
    "Intellectual Property Protection",
    "Regulatory Compliance Reporting",
    "Supply Chain Security",
    "Zero Trust Architecture",
    "Decommissioning and Asset Disposal"
]

# Simplified terms for gaps chart
SIMPLIFIED_TERMS = [
    "Data Processing", "User Rights", "Data Retention", "Security Measures",
    "Data Breach", "Third-Party", "Consent", "Privacy Policy",
    "Data Transfer", "Audit Rights"
]

def get_analytics_layout():
    """Get the analytics view layout"""
    
    # Generate gaps data for chart (using simplified terms)
    gaps_data = [
        {"term": term, "gaps": random.randint(5, 45)}
        for term in SIMPLIFIED_TERMS
    ]
    gaps_data.sort(key=lambda x: x['gaps'], reverse=True)
    
    # Create gaps chart
    gaps_fig = go.Figure(data=[
        go.Bar(
            y=[item['term'] for item in gaps_data],
            x=[item['gaps'] for item in gaps_data],
            orientation='h',
            marker_color='#ef4444',
            marker_line_width=0,
            text=[item['gaps'] for item in gaps_data],
            textposition='outside'
        )
    ])
    
    gaps_fig.update_layout(
        height=400,
        margin=dict(l=130, r=20, t=20, b=40),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='system-ui', size=12, color='#64748b'),
        xaxis=dict(
            title='Number of Gaps',
            showgrid=True,
            gridcolor='#e2e8f0',
            showline=False
        ),
        yaxis=dict(
            showgrid=False,
            showline=False
        ),
        hovermode='closest'
    )
    
    # Review duration chart
    duration_data = [
        {"name": f"Contract {i+1}", "duration": random.randint(2, 14)}
        for i in range(15)
    ]
    
    duration_fig = go.Figure(data=[
        go.Bar(
            x=[item['name'] for item in duration_data],
            y=[item['duration'] for item in duration_data],
            marker_color='#3b82f6',
            marker_line_width=0
        )
    ])
    
    duration_fig.update_layout(
        height=400,
        margin=dict(l=40, r=20, t=20, b=120),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='system-ui', size=11, color='#64748b'),
        xaxis=dict(
            showgrid=False,
            showline=False,
            tickangle=-45
        ),
        yaxis=dict(
            title='Days',
            showgrid=True,
            gridcolor='#e2e8f0',
            showline=False
        )
    )
    
    # Terms compliance chart
    compliance_names = [f"Contract {i+1}" for i in range(15)]
    terms_fig = go.Figure(data=[
        go.Bar(name='Terms Met', x=compliance_names, y=[random.randint(20, 35) for _ in range(15)], marker_color='#10b981'),
        go.Bar(name='Partially Met', x=compliance_names, y=[random.randint(3, 10) for _ in range(15)], marker_color='#f59e0b'),
        go.Bar(name='Terms Missing', x=compliance_names, y=[random.randint(0, 8) for _ in range(15)], marker_color='#ef4444')
    ])
    
    terms_fig.update_layout(
        barmode='stack',
        height=450,
        margin=dict(l=40, r=20, t=20, b=120),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='system-ui', size=11, color='#64748b'),
        xaxis=dict(
            showgrid=False,
            showline=False,
            tickangle=-45
        ),
        yaxis=dict(
            title='Number of Terms',
            showgrid=True,
            gridcolor='#e2e8f0',
            showline=False
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    return html.Div([
        # Header
        html.Div([
            html.Div([
                html.H2("Analytics Dashboard", style={'color': '#0f172a', 'margin': 0}),
                html.P("Comprehensive insights into contract compliance", 
                       style={'fontSize': '14px', 'color': '#64748b', 'margin': '4px 0 0 0'})
            ]),
            dbc.Button([
                icon("mdi:download", width=16, style={'marginRight': '8px'}),
                "Export Report"
            ], color="primary", size="sm", style={'display': 'flex', 'alignItems': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'start', 'marginBottom': '24px'}),
        
        # Filters Card
        dbc.Card([
            dbc.CardHeader([
                html.Div([
                    html.Div(icon("mdi:filter", width=20, color='#64748b'), style={'marginRight': '8px'}),
                    html.H5("Filters", style={'margin': 0})
                ], style={'display': 'flex', 'alignItems': 'center'}),
                html.P("Select a compliance standard and date range to analyze contracts",
                       style={'fontSize': '14px', 'color': '#64748b', 'margin': '8px 0 0 0'})
            ], style={'backgroundColor': 'white', 'borderBottom': '1px solid #e2e8f0'}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Compliance Standard", style={'fontSize': '14px', 'color': '#475569', 'marginBottom': '8px'}),
                        dbc.Select(
                            id='analytics-standard-filter',
                            options=[
                                {'label': 'All Standards - View all contract reviews', 'value': 'all'},
                                {'label': 'GDPR - General Data Protection Regulation', 'value': 'gdpr'},
                                {'label': 'SOC 2 - Service Organization Control 2', 'value': 'soc2'},
                                {'label': 'HIPAA - Health Insurance Portability and Accountability Act', 'value': 'hipaa'},
                                {'label': 'CCPA - California Consumer Privacy Act', 'value': 'ccpa'},
                                {'label': 'ISO 27001 - Information Security Management', 'value': 'iso27001'},
                                {'label': 'PCI DSS - Payment Card Industry Data Security Standard', 'value': 'pci-dss'}
                            ],
                            value='all'
                        )
                    ], md=6),
                    dbc.Col([
                        html.Label("Date Range", style={'fontSize': '14px', 'color': '#475569', 'marginBottom': '8px'}),
                        dcc.DatePickerRange(
                            id='analytics-date-range',
                            start_date=(datetime.now() - timedelta(days=180)).date(),
                            end_date=datetime.now().date(),
                            display_format='MMM DD, YYYY',
                            style={'width': '100%'}
                        )
                    ], md=6)
                ]),
                html.Div([
                    html.P([
                        html.Span("Active Filters: ", style={'fontWeight': 500}),
                        html.Span("All Standards • Last 6 months", id='analytics-active-filters')
                    ], style={'fontSize': '14px', 'color': '#475569', 'margin': '0'}),
                    html.P("Showing 25 reviews", id='analytics-review-count',
                           style={'fontSize': '14px', 'color': '#64748b', 'margin': '4px 0 0 0'})
                ], style={
                    'marginTop': '16px',
                    'padding': '12px',
                    'backgroundColor': '#f8fafc',
                    'borderRadius': '8px'
                })
            ])
        ], style={'marginBottom': '24px'}),
        
        # Key Metrics
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Div(icon("mdi:file-document", width=20, color='#2563eb'), style={'marginRight': '8px'}),
                            html.P("Total Number of Reviews", style={'fontSize': '14px', 'color': '#64748b', 'margin': 0})
                        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '8px'}),
                        html.H2("25", style={'fontSize': '36px', 'color': '#2563eb', 'margin': '0 0 8px 0'}),
                        html.P("Completed contract reviews in selected period",
                               style={'fontSize': '12px', 'color': '#64748b', 'margin': 0})
                    ])
                ])
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.P("Avg. Terms Matching Rate", style={'fontSize': '14px', 'color': '#64748b', 'margin': '0 0 8px 0'}),
                        html.H2("84%", style={'fontSize': '36px', 'color': '#10b981', 'margin': '0 0 8px 0'}),
                        html.P("Average percentage of terms fully met",
                               style={'fontSize': '12px', 'color': '#64748b', 'margin': 0})
                    ])
                ])
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.P("Avg. Points Matching Rate", style={'fontSize': '14px', 'color': '#64748b', 'margin': '0 0 8px 0'}),
                        html.H2("81%", style={'fontSize': '36px', 'color': '#059669', 'margin': '0 0 8px 0'}),
                        html.P("Average compliance score (partial = 50%)",
                               style={'fontSize': '12px', 'color': '#64748b', 'margin': 0})
                    ])
                ])
            ], md=4)
        ], style={'marginBottom': '24px'}),
        
        # Compliance Terms Analysis Table
        dbc.Card([
            dbc.CardHeader([
                html.Div([
                    html.Div([
                        html.H5("Compliance Terms Analysis", style={'margin': 0}),
                        html.P("Breakdown of met, partially met, and missing status for each compliance term across all reviews",
                               style={'fontSize': '14px', 'color': '#64748b', 'margin': '8px 0 0 0'})
                    ]),
                ]),
                html.Div([
                    html.Div([
                        icon("mdi:magnify", width=16, style={'position': 'absolute', 'left': '12px', 'top': '50%', 'transform': 'translateY(-50%)', 'color': '#94a3b8'}),
                        dbc.Input(
                            id='term-search-input',
                            placeholder='Search compliance terms...',
                            type='text',
                            style={
                                'paddingLeft': '36px',
                                'backgroundColor': '#f8fafc',
                                'border': '1px solid #e2e8f0'
                            }
                        )
                    ], style={'position': 'relative', 'marginTop': '16px'})
                ])
            ], style={'backgroundColor': 'white', 'borderBottom': '1px solid #e2e8f0'}),
            dbc.CardBody([
                html.Div(id='compliance-terms-table-container')
            ])
        ], style={'marginBottom': '24px'}),
        
        # Charts
        dbc.Card([
            dbc.CardHeader([
                html.H5("Compliance Gaps by Term", style={'margin': 0}),
                html.P("Total number of gaps identified for each compliance term across all reviews",
                       style={'fontSize': '14px', 'color': '#64748b', 'margin': '8px 0 0 0'})
            ]),
            dbc.CardBody([
                dcc.Graph(figure=gaps_fig, config={'displayModeBar': False})
            ])
        ], style={'marginBottom': '24px'}),
        
        dbc.Card([
            dbc.CardHeader([
                html.H5("Review Duration by Request", style={'margin': 0}),
                html.P("Number of days taken to complete each contract review (15 most recent)",
                       style={'fontSize': '14px', 'color': '#64748b', 'margin': '8px 0 0 0'})
            ]),
            dbc.CardBody([
                dcc.Graph(figure=duration_fig, config={'displayModeBar': False})
            ])
        ], style={'marginBottom': '24px'}),
        
        dbc.Card([
            dbc.CardHeader([
                html.H5("Terms Compliance Status by Request", style={'margin': 0}),
                html.P("Number of terms met, missing, and partially met for each contract (15 most recent)",
                       style={'fontSize': '14px', 'color': '#64748b', 'margin': '8px 0 0 0'})
            ]),
            dbc.CardBody([
                dcc.Graph(figure=terms_fig, config={'displayModeBar': False})
            ])
        ])
    ])


# Callback for compliance terms table
@callback(
    Output('compliance-terms-table-container', 'children'),
    [Input('term-search-input', 'value'),
     Input('analytics-standard-filter', 'value'),
     Input('analytics-date-range', 'start_date'),
     Input('analytics-date-range', 'end_date')]
)
def update_compliance_terms_table(search_query, selected_standard, start_date, end_date):
    """Update the compliance terms analysis table based on filters"""
    
    # Generate mock data
    contracts = generate_mock_analytics_data()
    
    # Filter contracts based on standard and date range
    filtered_contracts = []
    for contract in contracts:
        matches_standard = selected_standard == 'all' or contract['standard'] == selected_standard
        
        if start_date and end_date:
            contract_date = contract['reviewDate'].date()
            start = datetime.fromisoformat(start_date).date() if isinstance(start_date, str) else start_date
            end = datetime.fromisoformat(end_date).date() if isinstance(end_date, str) else end_date
            matches_date = start <= contract_date <= end
        else:
            matches_date = True
        
        if matches_standard and matches_date:
            filtered_contracts.append(contract)
    
    if len(filtered_contracts) == 0:
        return html.Div(
            html.P("No compliance data available for the selected filters",
                   style={'textAlign': 'center', 'padding': '48px', 'color': '#64748b', 'fontSize': '14px'}),
            style={'backgroundColor': '#f8fafc', 'borderRadius': '8px', 'minHeight': '200px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}
        )
    
    # Calculate term-level compliance statistics
    term_stats = []
    for term in COMPLIANCE_TERMS:
        met_count = 0
        partial_count = 0
        missing_count = 0
        
        for contract in filtered_contracts:
            status = contract['termStatus'].get(term, 'missing')
            if status == 'met':
                met_count += 1
            elif status == 'partially-met':
                partial_count += 1
            else:
                missing_count += 1
        
        total = len(filtered_contracts)
        met_pct = round((met_count / total) * 100) if total > 0 else 0
        partial_pct = round((partial_count / total) * 100) if total > 0 else 0
        missing_pct = round((missing_count / total) * 100) if total > 0 else 0
        
        term_stats.append({
            'term': term,
            'met': met_count,
            'partiallyMet': partial_count,
            'missing': missing_count,
            'total': total,
            'metPercentage': met_pct,
            'partialPercentage': partial_pct,
            'missingPercentage': missing_pct
        })
    
    # Filter based on search query
    if search_query:
        query_lower = search_query.lower()
        filtered_stats = [stat for stat in term_stats if query_lower in stat['term'].lower()]
    else:
        filtered_stats = term_stats
    
    if len(filtered_stats) == 0:
        return html.Div([
            html.Div(
                html.P("No terms match your search",
                       style={'textAlign': 'center', 'padding': '48px', 'color': '#64748b', 'fontSize': '14px'}),
                style={'backgroundColor': '#f8fafc', 'borderRadius': '8px', 'minHeight': '200px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}
            )
        ])
    
    # Create table rows
    table_rows = []
    for stat in filtered_stats:
        table_rows.append(
            html.Tr([
                # Term name
                html.Td(
                    html.Div([
                        html.Span(stat['term'], style={'fontSize': '14px', 'color': '#0f172a'})
                    ]),
                    style={'padding': '12px'}
                ),
                # Met count
                html.Td([
                    html.Div([
                        html.Span(str(stat['met']), style={'fontSize': '14px', 'color': '#15803d', 'display': 'block'}),
                        html.Span(f"({stat['metPercentage']}%)", style={'fontSize': '12px', 'color': '#64748b'})
                    ], style={'textAlign': 'center'})
                ], style={'padding': '12px'}),
                # Partially met count
                html.Td([
                    html.Div([
                        html.Span(str(stat['partiallyMet']), style={'fontSize': '14px', 'color': '#b45309', 'display': 'block'}),
                        html.Span(f"({stat['partialPercentage']}%)", style={'fontSize': '12px', 'color': '#64748b'})
                    ], style={'textAlign': 'center'})
                ], style={'padding': '12px'}),
                # Missing count
                html.Td([
                    html.Div([
                        html.Span(str(stat['missing']), style={'fontSize': '14px', 'color': '#b91c1c', 'display': 'block'}),
                        html.Span(f"({stat['missingPercentage']}%)", style={'fontSize': '12px', 'color': '#64748b'})
                    ], style={'textAlign': 'center'})
                ], style={'padding': '12px'}),
                # Total
                html.Td(
                    html.Span(str(stat['total']), style={'fontSize': '14px', 'color': '#0f172a'}),
                    style={'padding': '12px', 'textAlign': 'center'}
                ),
                # Compliance rate with progress bar
                html.Td([
                    html.Div([
                        html.Div([
                            html.Div(
                                style={
                                    'width': f"{stat['metPercentage']}%",
                                    'height': '8px',
                                    'backgroundColor': '#10b981',
                                    'borderRadius': '9999px'
                                }
                            )
                        ], style={
                            'width': '96px',
                            'height': '8px',
                            'backgroundColor': '#f1f5f9',
                            'borderRadius': '9999px',
                            'overflow': 'hidden',
                            'marginRight': '8px'
                        }),
                        html.Span(f"{stat['metPercentage']}%", style={'fontSize': '14px', 'color': '#0f172a', 'width': '48px', 'textAlign': 'right'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'flex-end'})
                ], style={'padding': '12px'}),
            ], style={'borderBottom': '1px solid #e2e8f0'}, className='hover-bg-slate-50')
        )
    
    table = html.Div([
        html.Div([
            dbc.Table([
                html.Thead(
                    html.Tr([
                        html.Th('Compliance Term', style={'width': '40%', 'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#475569'}),
                        html.Th('Met', style={'textAlign': 'center', 'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#475569'}),
                        html.Th('Partially Met', style={'textAlign': 'center', 'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#475569'}),
                        html.Th('Missing', style={'textAlign': 'center', 'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#475569'}),
                        html.Th('Total Reviews', style={'textAlign': 'center', 'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#475569'}),
                        html.Th('Compliance Rate', style={'textAlign': 'right', 'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#475569'}),
                    ], style={'backgroundColor': '#f8fafc', 'borderBottom': '1px solid #e2e8f0'})
                ),
                html.Tbody(table_rows)
            ], bordered=False, hover=True, responsive=True, style={'marginBottom': '0'})
        ], style={'border': '1px solid #e2e8f0', 'borderRadius': '8px', 'overflow': 'hidden'}),
        
        # Search result count
        html.P(
            f"Showing {len(filtered_stats)} of {len(term_stats)} terms",
            style={'fontSize': '14px', 'color': '#64748b', 'marginTop': '16px', 'marginBottom': '0'}
        ) if search_query and len(filtered_stats) != len(term_stats) else None
    ])
    
    return table
