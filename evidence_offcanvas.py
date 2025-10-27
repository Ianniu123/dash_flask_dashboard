"""
Evidence Offcanvas Component - Shows evidence details for compliance subpoints
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

def icon(name, **kwargs):
    """Helper function to create DashIconify icons with CSS color styling"""
    color = kwargs.pop('color', None)
    if color:
        return html.Span(
            DashIconify(icon=name, **kwargs),
            style={'color': color}
        )
    return DashIconify(icon=name, **kwargs)

def create_evidence_offcanvas():
    """Create the evidence viewing offcanvas (modal/drawer)"""
    return dbc.Offcanvas(
        id='evidence-offcanvas',
        title='',  # Will be set dynamically
        is_open=False,
        placement='end',
        style={'width': '100%', 'maxWidth': '768px'},
        children=[
            # Hidden stores for state management
            dcc.Store(id='evidence-data-store', data={}),
            dcc.Store(id='evidence-current-index', data=0),
            
            # Content container
            html.Div(id='evidence-offcanvas-content', style={'maxWidth': '672px', 'margin': '0 auto'})
        ]
    )

def render_evidence_content(subpoint, current_index=0):
    """Render the content for the evidence offcanvas"""
    if not subpoint:
        return html.Div("No evidence selected")
    
    evidence_list = subpoint.get('evidence', [])
    evidence_count = len(evidence_list)
    
    if evidence_count == 0:
        return html.Div([
            html.Div([
                html.P("No evidence available", style={
                    'fontSize': '14px',
                    'color': '#64748b',
                    'fontStyle': 'italic',
                    'textAlign': 'center',
                    'padding': '64px 0'
                })
            ])
        ])
    
    # Ensure index is within bounds
    current_index = max(0, min(current_index, evidence_count - 1))
    current_evidence = evidence_list[current_index]
    
    return html.Div([
        # Header with subpoint info
        html.Div([
            html.Div([
                # Icon
                html.Div([
                    (html.Div(
                        icon("mdi:check-circle", width=24, color='#16a34a'),
                        style={
                            'width': '40px',
                            'height': '40px',
                            'borderRadius': '9999px',
                            'backgroundColor': '#dcfce7',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center'
                        }
                    ) if subpoint.get('met') else html.Div(
                        icon("mdi:close-circle", width=24, color='#dc2626'),
                        style={
                            'width': '40px',
                            'height': '40px',
                            'borderRadius': '9999px',
                            'backgroundColor': '#fee2e2',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center'
                        }
                    ))
                ], style={'flexShrink': 0, 'marginTop': '4px'}),
                # Title and description
                html.Div([
                    html.H3(subpoint.get('heading', ''), style={
                        'fontSize': '20px',
                        'color': '#0f172a',
                        'margin': 0,
                        'marginBottom': '8px',
                        'lineHeight': '1.3'
                    }),
                    html.P(subpoint.get('description', ''), style={
                        'fontSize': '16px',
                        'color': '#64748b',
                        'margin': 0,
                        'lineHeight': '1.6'
                    })
                ], style={'flex': 1})
            ], style={'display': 'flex', 'alignItems': 'start', 'gap': '16px', 'marginBottom': '32px'})
        ]),
        
        # Navigation section
        (html.Div([
            html.Div([
                html.H4("Supporting Evidence", style={
                    'fontSize': '14px',
                    'color': '#0f172a',
                    'margin': 0
                }),
                html.Span(
                    f"{evidence_count} {'source' if evidence_count == 1 else 'sources'}",
                    style={
                        'fontSize': '12px',
                        'padding': '2px 8px',
                        'borderRadius': '9999px',
                        'backgroundColor': '#f1f5f9',
                        'color': '#475569',
                        'marginLeft': '12px'
                    }
                )
            ], style={'display': 'flex', 'alignItems': 'center'}),
            
            # Navigation controls (only show if more than 1 evidence)
            (html.Div([
                dbc.Button(
                    icon("mdi:chevron-left", width=16),
                    id='evidence-prev-btn',
                    color='light',
                    outline=True,
                    size='sm',
                    style={'width': '36px', 'height': '36px', 'padding': 0}
                ),
                html.Span(
                    f"{current_index + 1} of {evidence_count}",
                    style={
                        'fontSize': '14px',
                        'color': '#64748b',
                        'minWidth': '75px',
                        'textAlign': 'center'
                    }
                ),
                dbc.Button(
                    icon("mdi:chevron-right", width=16),
                    id='evidence-next-btn',
                    color='light',
                    outline=True,
                    size='sm',
                    style={'width': '36px', 'height': '36px', 'padding': 0}
                )
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '12px'}) if evidence_count > 1 else None)
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'paddingTop': '16px',
            'paddingBottom': '16px',
            'borderTop': '1px solid #e2e8f0',
            'borderBottom': '1px solid #e2e8f0',
            'marginBottom': '32px'
        }) if evidence_count > 0 else None),
        
        # Evidence content
        (html.Div([
            # Excerpt section
            html.Div([
                html.Div([
                    html.Div(style={
                        'width': '4px',
                        'height': '20px',
                        'backgroundColor': '#94a3b8',
                        'borderRadius': '9999px'
                    }),
                    html.H5("CONTRACT EXCERPT", style={
                        'fontSize': '10px',
                        'color': '#64748b',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'margin': 0
                    })
                ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '12px'}),
                html.Div([
                    html.P(f'"{current_evidence.get("excerpt", "")}"', style={
                        'fontSize': '14px',
                        'color': '#1e293b',
                        'fontStyle': 'italic',
                        'lineHeight': '1.6',
                        'margin': 0
                    })
                ], style={
                    'backgroundColor': '#ffffff',
                    'padding': '24px',
                    'borderRadius': '8px',
                    'border': '2px solid #e2e8f0',
                    'boxShadow': '0 1px 2px 0 rgba(0, 0, 0, 0.05)'
                })
            ], style={'marginBottom': '32px'}),
            
            # Explanation section
            html.Div([
                html.Div([
                    html.Div(style={
                        'width': '4px',
                        'height': '20px',
                        'backgroundColor': '#3b82f6',
                        'borderRadius': '9999px'
                    }),
                    html.H5("EVIDENCE EXPLANATION", style={
                        'fontSize': '10px',
                        'color': '#2563eb',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em',
                        'margin': 0
                    })
                ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'marginBottom': '12px'}),
                html.Div([
                    html.P(current_evidence.get("explanation", ""), style={
                        'fontSize': '14px',
                        'color': '#1e293b',
                        'lineHeight': '1.6',
                        'margin': 0
                    })
                ], style={
                    'backgroundColor': '#eff6ff',
                    'padding': '24px',
                    'borderRadius': '8px',
                    'border': '2px solid #bfdbfe',
                    'boxShadow': '0 1px 2px 0 rgba(0, 0, 0, 0.05)'
                })
            ])
        ], style={'paddingBottom': '32px'}) if current_evidence else None)
    ], style={'padding': '0'})
