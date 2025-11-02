"""
Layout components for the Contract Compliance Dashboard
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go

def icon(name, **kwargs):
    """Helper function to create DashIconify icons"""
    return DashIconify(icon=name, **kwargs)

def create_sidebar():
    """Create the collapsible sidebar with navigation"""
    return html.Div([
        # Sidebar Header
        html.Div([
            html.Div([
                html.Div(
                    icon("mdi:file-document", width=20, color='white'),
                    style={
                        'width': '32px',
                        'height': '32px',
                        'backgroundColor': '#2563eb',
                        'borderRadius': '8px',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'flexShrink': 0
                    }
                ),
                html.Div([
                    html.P("Contract Compliance", 
                           id='sidebar-title',
                           style={'fontSize': '14px', 'color': '#0f172a', 'margin': 0, 'fontWeight': 500}),
                    html.P("Dashboard", 
                           id='sidebar-subtitle',
                           style={'fontSize': '12px', 'color': '#64748b', 'margin': 0})
                ], style={'marginLeft': '8px'}, id='sidebar-text-header')
            ], style={'display': 'flex', 'alignItems': 'center', 'padding': '12px 16px'})
        ]),
        
        # Navigation Menu
        html.Div([
            # Analytics
            html.Div(
                id={'type': 'nav-item', 'index': 'analytics'},
                children=[
                    icon("mdi:chart-bar", width=16, style={'marginRight': '12px', 'flexShrink': 0}),
                    html.Span("Analytics", className='nav-text')
                ],
                style={
                    'padding': '10px 16px',
                    'cursor': 'pointer',
                    'display': 'flex',
                    'alignItems': 'center',
                    'fontSize': '14px',
                    'color': '#0f172a',
                    'transition': 'background-color 0.2s'
                },
                className='nav-item'
            ),
            
            # Completed Reviews
            html.Div(
                id={'type': 'nav-item', 'index': 'reviews'},
                children=[
                    icon("mdi:check-circle", width=16, style={'marginRight': '12px', 'flexShrink': 0}),
                    html.Span("Completed Reviews", className='nav-text')
                ],
                style={
                    'padding': '10px 16px',
                    'cursor': 'pointer',
                    'display': 'flex',
                    'alignItems': 'center',
                    'fontSize': '14px',
                    'color': '#0f172a',
                    'transition': 'background-color 0.2s'
                },
                className='nav-item'
            ),
            
            # Standards Supported
            html.Div(
                id={'type': 'nav-item', 'index': 'standards'},
                children=[
                    icon("mdi:shield-check", width=16, style={'marginRight': '12px', 'flexShrink': 0}),
                    html.Span("Standards Supported", className='nav-text')
                ],
                style={
                    'padding': '10px 16px',
                    'cursor': 'pointer',
                    'display': 'flex',
                    'alignItems': 'center',
                    'fontSize': '14px',
                    'color': '#0f172a',
                    'transition': 'background-color 0.2s'
                },
                className='nav-item'
            ),
            
            # Request New Review - Collapsible
            html.Div([
                html.Div(
                    id='request-review-trigger',
                    children=[
                        icon("mdi:plus", width=16, style={'marginRight': '12px', 'flexShrink': 0}),
                        html.Span("Request New Review", style={'flex': 1}, className='nav-text'),
                        icon("mdi:chevron-down", width=16, id='request-review-chevron', className='nav-text')
                    ],
                    style={
                        'padding': '10px 16px',
                        'cursor': 'pointer',
                        'display': 'flex',
                        'alignItems': 'center',
                        'fontSize': '14px',
                        'color': '#0f172a',
                        'transition': 'background-color 0.2s'
                    },
                    className='nav-item'
                ),
                html.Div(
                    id='request-review-submenu',
                    children=[
                        html.A(
                            [
                                icon("mdi:open-in-new", width=12, style={'marginRight': '8px', 'flexShrink': 0}),
                                html.Span(item['label'], className='nav-text')
                            ],
                            href=item['url'],
                            target='_blank',
                            style={
                                'padding': '8px 16px 8px 44px',
                                'display': 'flex',
                                'alignItems': 'center',
                                'fontSize': '13px',
                                'color': '#475569',
                                'textDecoration': 'none',
                                'transition': 'background-color 0.2s'
                            },
                            className='nav-subitem'
                        )
                        for item in [
                            {"label": "GDPR Review", "url": "https://forms.company.com/compliance/gdpr-review"},
                            {"label": "SOC 2 Review", "url": "https://forms.company.com/compliance/soc2-review"},
                            {"label": "HIPAA Review", "url": "https://forms.company.com/compliance/hipaa-review"},
                            {"label": "CCPA Review", "url": "https://forms.company.com/compliance/ccpa-review"},
                            {"label": "ISO 27001 Review", "url": "https://forms.company.com/compliance/iso27001-review"},
                            {"label": "PCI DSS Review", "url": "https://forms.company.com/compliance/pci-dss-review"},
                            {"label": "Custom Review", "url": "https://forms.company.com/compliance/custom-review"}
                        ]
                    ],
                    style={'display': 'none'},  # Initially hidden
                    className='request-review-submenu'
                )
            ])
        ], style={'flex': 1, 'overflowY': 'auto'}),
        
        # Sidebar Toggle Button (at bottom)
        html.Div([
            html.Div(
                id='sidebar-toggle',
                children=[
                    icon("mdi:menu", width=20, id='sidebar-toggle-icon', style={'flexShrink': 0})
                ],
                style={
                    'padding': '12px 16px',
                    'cursor': 'pointer',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'borderTop': '1px solid #e2e8f0',
                    'transition': 'background-color 0.2s'
                },
                className='sidebar-toggle-btn'
            )
        ])
    ], style={'height': '100%', 'display': 'flex', 'flexDirection': 'column'})


def create_header():
    """Create the top header bar"""
    return html.Div([
        html.Div([
            # Left side - sidebar trigger + search
            html.Div([
                # Sidebar trigger button
                html.Div(
                    id='header-sidebar-trigger',
                    children=icon("mdi:menu", width=20, color='#475569'),
                    style={
                        'width': '36px',
                        'height': '36px',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'cursor': 'pointer',
                        'borderRadius': '6px',
                        'transition': 'background-color 0.2s',
                        'marginRight': '12px'
                    },
                    className='icon-button'
                ),
                # Separator
                html.Div(
                    style={
                        'width': '1px',
                        'height': '24px',
                        'backgroundColor': '#e2e8f0',
                        'marginRight': '12px'
                    }
                ),
                html.Div(
                    id='search-container',
                    children=[
                        html.Div([
                            icon("mdi:magnify", width=16, style={
                                'position': 'absolute',
                                'left': '12px',
                                'top': '50%',
                                'transform': 'translateY(-50%)',
                                'color': '#94a3b8'
                            }),
                            dbc.Input(
                                placeholder="Search contracts...",
                                style={
                                    'paddingLeft': '36px',
                                    'width': '256px',
                                    'backgroundColor': '#f8fafc',
                                    'border': '1px solid #e2e8f0',
                                    'borderRadius': '6px'
                                }
                            )
                        ], style={'position': 'relative'})
                    ],
                    style={'display': 'none'}  # Hidden by default, shown conditionally
                )
            ], style={'display': 'flex', 'alignItems': 'center'}),
            
            # Right side - icons
            html.Div([
                html.Div(
                    icon("mdi:bell", width=20, color='#475569'),
                    style={
                        'width': '36px',
                        'height': '36px',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'cursor': 'pointer',
                        'borderRadius': '6px',
                        'transition': 'background-color 0.2s'
                    },
                    className='icon-button'
                ),
                html.Div(
                    icon("mdi:cog", width=20, color='#475569'),
                    style={
                        'width': '36px',
                        'height': '36px',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'cursor': 'pointer',
                        'borderRadius': '6px',
                        'transition': 'background-color 0.2s'
                    },
                    className='icon-button'
                ),
                html.Div(
                    icon("mdi:account", width=20, color='#475569'),
                    style={
                        'width': '36px',
                        'height': '36px',
                        'display': 'flex',
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'cursor': 'pointer',
                        'borderRadius': '9999px',
                        'transition': 'background-color 0.2s'
                    },
                    className='icon-button'
                )
            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '8px'})
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'space-between',
            'height': '64px',
            'padding': '0 16px'
        })
    ])


def create_analytics_view():
    """Create the Analytics view"""
    from analytics_view import get_analytics_layout
    return get_analytics_layout()


def create_completed_reviews_view(contracts):
    """Create the Completed Reviews view"""
    from completed_reviews_view import get_completed_reviews_layout
    return get_completed_reviews_layout(contracts)


def create_standards_view():
    """Create the Standards Supported view"""
    from standards_view import get_standards_layout
    return get_standards_layout()


def create_contract_detail_view(contract):
    """Create the Contract Detail view"""
    from contract_detail_view import get_contract_detail_layout
    return get_contract_detail_layout(contract)
