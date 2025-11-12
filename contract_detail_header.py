"""
Helper functions for contract detail view header and instructions
"""

from dash import html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

def icon(name, **kwargs):
    """Helper function to create DashIconify icons"""
    return DashIconify(icon=name, **kwargs)

def create_contract_detail_header(total_terms):
    """Create header with back button and export button"""
    return html.Div([
        dbc.Button([
            icon("mdi:arrow-left", width=16, style={'marginRight': '8px'}),
            "Back to Reviews"
        ], 
            id='back-to-reviews-btn',
            color="light",
            size="sm",
            style={'display': 'flex', 'alignItems': 'center'}
        ),
        dbc.Button([
            icon("mdi:download", width=16, style={'marginRight': '8px'}),
            "Export Results"
        ], 
            id='export-results-btn',
            color="light",
            size="sm",
            outline=True,
            style={'display': 'flex', 'alignItems': 'center'}
        )
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '24px'})

def create_instructions_banner(total_terms, is_attested=False):
    """Create instructions banner for contract review"""
    if is_attested:
        return None
    
    return dbc.Alert([
        html.Div([
            icon("mdi:information-outline", width=16, color='#475569'),
        ], style={'marginRight': '12px', 'marginTop': '2px'}),
        html.Div([
            html.Div([
                html.P("Review Instructions", style={'fontWeight': 500, 'margin': 0, 'marginBottom': '8px', 'color': '#334155'})
            ]),
            html.Ol([
                html.Li(f"Review each of the {total_terms} compliance terms below by expanding the accordions", 
                       style={'marginBottom': '4px'}),
                html.Li([
                    "For each term, either ",
                    html.Strong("Approve"),
                    " the AI result or ",
                    html.Strong("Override"),
                    " it with your assessment"
                ], style={'marginBottom': '4px'}),
                html.Li("Provide a reason when overriding any term result", 
                       style={'marginBottom': '4px'}),
                html.Li([
                    f"Once all {total_terms} terms are reviewed, click ",
                    html.Strong("Attest Review"),
                    " to finalize"
                ], style={'marginBottom': '4px'}),
                html.Li([
                    "Use the ",
                    html.Strong("Export Results"),
                    " button above to download the complete review report"
                ], style={'marginBottom': 0})
            ], style={'marginBottom': 0, 'paddingLeft': '20px'})
        ], style={'flex': 1})
    ], 
        color="light",
        style={
            'display': 'flex',
            'backgroundColor': '#f8fafc',
            'border': '1px solid #cbd5e1',
            'padding': '12px 16px',
            'borderRadius': '6px',
            'marginBottom': '16px',
            'fontSize': '14px',
            'color': '#475569'
        }
    )
