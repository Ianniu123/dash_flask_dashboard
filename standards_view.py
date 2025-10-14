"""
Standards View - Supported compliance review standards
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

def icon(name, **kwargs):
    """Helper function to create DashIconify icons"""
    return DashIconify(icon=name, **kwargs)

SUPPORTED_REVIEW_TYPES = [
    {
        "typeId": "GDPR-2024",
        "typeName": "GDPR Compliance Review",
        "publishedDate": "2024-01-15",
        "author": "Emily Rodriguez",
        "typeVersionId": "v2.3.0",
        "status": "active"
    },
    {
        "typeId": "SOC2-TYPE2-2024",
        "typeName": "SOC 2 Type II Compliance Review",
        "publishedDate": "2024-02-20",
        "author": "Michael Chen",
        "typeVersionId": "v1.8.2",
        "status": "active"
    },
    {
        "typeId": "HIPAA-2024",
        "typeName": "HIPAA Compliance Review",
        "publishedDate": "2024-01-30",
        "author": "Sarah Johnson",
        "typeVersionId": "v3.1.0",
        "status": "active"
    },
    {
        "typeId": "CCPA-2024",
        "typeName": "CCPA Compliance Review",
        "publishedDate": "2024-03-10",
        "author": "David Park",
        "typeVersionId": "v1.5.1",
        "status": "active"
    },
    {
        "typeId": "ISO27001-2024",
        "typeName": "ISO 27001:2022 Compliance Review",
        "publishedDate": "2024-02-05",
        "author": "Emily Rodriguez",
        "typeVersionId": "v2.0.0",
        "status": "active"
    },
    {
        "typeId": "PCI-DSS-2024",
        "typeName": "PCI DSS v4.0 Compliance Review",
        "publishedDate": "2024-03-25",
        "author": "Michael Chen",
        "typeVersionId": "v4.0.1",
        "status": "active"
    },
    {
        "typeId": "GDPR-2023",
        "typeName": "GDPR Compliance Review",
        "publishedDate": "2023-06-12",
        "author": "Sarah Johnson",
        "typeVersionId": "v2.2.0",
        "status": "deprecated"
    },
    {
        "typeId": "SOC2-TYPE2-2023",
        "typeName": "SOC 2 Type II Compliance Review",
        "publishedDate": "2023-08-18",
        "author": "David Park",
        "typeVersionId": "v1.7.5",
        "status": "deprecated"
    }
]

def get_standards_layout():
    """Get the standards view layout"""
    
    active_standards = [s for s in SUPPORTED_REVIEW_TYPES if s['status'] == 'active']
    
    # Active standards table rows
    active_rows = []
    for standard in active_standards:
        active_rows.append(
            html.Tr([
                html.Td([
                    html.Code(
                        standard['typeId'],
                        style={
                            'fontSize': '12px',
                            'backgroundColor': '#f1f5f9',
                            'padding': '4px 8px',
                            'borderRadius': '4px',
                            'color': '#334155'
                        }
                    )
                ], style={'padding': '12px'}),
                html.Td(standard['typeName'], style={'padding': '12px', 'color': '#0f172a'}),
                html.Td(standard['publishedDate'], style={'padding': '12px', 'color': '#475569'}),
                html.Td(standard['author'], style={'padding': '12px', 'color': '#475569'}),
                html.Td([
                    html.Span(
                        standard['typeVersionId'],
                        style={
                            'backgroundColor': '#dbeafe',
                            'color': '#1d4ed8',
                            'border': '1px solid #bfdbfe',
                            'padding': '4px 8px',
                            'borderRadius': '4px',
                            'fontSize': '12px',
                            'fontWeight': 500
                        }
                    )
                ], style={'padding': '12px'}),
                html.Td([
                    html.Span(
                        "Active",
                        style={
                            'backgroundColor': '#dcfce7',
                            'color': '#166534',
                            'padding': '4px 8px',
                            'borderRadius': '4px',
                            'fontSize': '12px',
                            'fontWeight': 500
                        }
                    )
                ], style={'padding': '12px'})
            ], style={'borderBottom': '1px solid #e2e8f0'}, className='table-row-hover')
        )
    
    return html.Div([
        # Header
        html.Div([
            html.H2("Standards Supported", style={'color': '#0f172a', 'margin': 0}),
            html.P("Review types available for contract compliance analysis",
                   style={'fontSize': '14px', 'color': '#64748b', 'margin': '4px 0 0 0'})
        ], style={'marginBottom': '24px'}),
        
        # Search
        dbc.Card([
            dbc.CardHeader([
                html.H5("Search Review Types", style={'margin': 0}),
                html.P("Filter by type ID, name, author, or version",
                       style={'fontSize': '14px', 'color': '#64748b', 'margin': '8px 0 0 0'})
            ]),
            dbc.CardBody([
                html.Div([
                    icon("mdi:magnify", width=16, style={
                        'position': 'absolute',
                        'left': '12px',
                        'top': '50%',
                        'transform': 'translateY(-50%)',
                        'color': '#94a3b8'
                    }),
                    dbc.Input(
                        id='standards-search',
                        placeholder="Search standards...",
                        style={'paddingLeft': '36px'}
                    )
                ], style={'position': 'relative'})
            ])
        ], style={'marginBottom': '24px'}),
        
        # Active Standards
        dbc.Card([
            dbc.CardHeader([
                html.Div([
                    html.Div(icon("mdi:file-document", width=20, color='#2563eb'), style={'marginRight': '8px'}),
                    html.H5("Active Review Types", style={'margin': 0})
                ], style={'display': 'flex', 'alignItems': 'center'}),
                html.P(f"Currently supported compliance review standards ({len(active_standards)})",
                       style={'fontSize': '14px', 'color': '#64748b', 'margin': '8px 0 0 0'})
            ]),
            dbc.CardBody([
                html.Div([
                    html.Table([
                        html.Thead([
                            html.Tr([
                                html.Th("Type ID", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                                html.Th("Type Name", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                                html.Th("Published Date", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                                html.Th("Author", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                                html.Th("Version", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'}),
                                html.Th("Status", style={'padding': '12px', 'fontSize': '14px', 'fontWeight': 500, 'color': '#64748b', 'borderBottom': '2px solid #e2e8f0'})
                            ])
                        ]),
                        html.Tbody(active_rows)
                    ], style={'width': '100%', 'borderCollapse': 'collapse', 'fontSize': '14px'})
                ], style={'border': '1px solid #e2e8f0', 'borderRadius': '8px', 'overflow': 'hidden'})
            ], style={'padding': '16px'})
        ], style={'marginBottom': '24px'}),
    
    ])
