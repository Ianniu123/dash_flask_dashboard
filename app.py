"""
Contract Compliance Dashboard - Python Dash Application
Converted from React/TypeScript to Python using Dash, Dash Mantine Components, and Dash Bootstrap Components
"""

import dash
from dash import Dash, html, dcc, Input, Output, State, ALL, MATCH, ctx, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import json

# Initialize the Dash app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Contract Compliance Dashboard"
)

# Color scheme matching the original app
COLORS = {
    'primary': '#2563eb',  # blue-600
    'secondary': '#f1f5f9',  # slate-100
    'success': '#10b981',  # emerald-600
    'warning': '#f59e0b',  # amber-500
    'danger': '#ef4444',  # red-500
    'slate': {
        '50': '#f8fafc',
        '100': '#f1f5f9',
        '200': '#e2e8f0',
        '300': '#cbd5e1',
        '400': '#94a3b8',
        '500': '#64748b',
        '600': '#475569',
        '700': '#334155',
        '800': '#1e293b',
        '900': '#0f172a'
    },
    'blue': {
        '50': '#eff6ff',
        '100': '#dbeafe',
        '600': '#2563eb',
        '700': '#1d4ed8'
    },
    'emerald': {
        '100': '#d1fae5',
        '600': '#10b981',
        '800': '#065f46'
    },
    'amber': {
        '100': '#fef3c7',
        '500': '#f59e0b',
        '800': '#92400e'
    },
    'red': {
        '100': '#fee2e2',
        '500': '#ef4444',
        '800': '#991b1b'
    },
    'green': {
        '100': '#dcfce7',
        '600': '#16a34a',
        '800': '#166534'
    },
    'orange': {
        '50': '#fff7ed',
        '100': '#ffedd5',
        '200': '#fed7aa'
    },
    'indigo': {
        '50': '#eef2ff'
    }
}

# Mock contract data
MOCK_CONTRACTS = [
    {
        "id": "1",
        "name": "Master Service Agreement",
        "vendor": "Acme Corp",
        "reviewDate": "Oct 8, 2025",
        "status": "compliant",
        "riskLevel": "low",
        "reviewer": "Sarah Johnson",
        "termMatchingRate": 95.2,
        "pointsMatchingRate": 92.8,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2451",
        "athenaId": "https://athena.company.com/review/ATH-9821"
    },
    {
        "id": "2",
        "name": "SaaS Subscription Agreement",
        "vendor": "TechStack Inc",
        "reviewDate": "Oct 7, 2025",
        "status": "needs-review",
        "riskLevel": "medium",
        "reviewer": "Michael Chen",
        "termMatchingRate": 78.5,
        "pointsMatchingRate": 81.3,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2450",
        "athenaId": "https://athena.company.com/review/ATH-9820"
    },
    {
        "id": "3",
        "name": "Data Processing Agreement",
        "vendor": "CloudServe Ltd",
        "reviewDate": "Oct 6, 2025",
        "status": "compliant",
        "riskLevel": "low",
        "reviewer": "Emily Rodriguez",
        "termMatchingRate": 91.7,
        "pointsMatchingRate": 88.9,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2449",
        "athenaId": "https://athena.company.com/review/ATH-9819"
    },
    {
        "id": "4",
        "name": "Enterprise License Agreement",
        "vendor": "DataFlow Systems",
        "reviewDate": "Oct 5, 2025",
        "status": "non-compliant",
        "riskLevel": "high",
        "reviewer": "David Park",
        "termMatchingRate": 42.1,
        "pointsMatchingRate": 38.5,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2448",
        "athenaId": "https://athena.company.com/review/ATH-9818"
    },
    {
        "id": "5",
        "name": "Vendor Service Agreement",
        "vendor": "Global Solutions",
        "reviewDate": "Oct 4, 2025",
        "status": "compliant",
        "riskLevel": "low",
        "reviewer": "Sarah Johnson",
        "termMatchingRate": 93.4,
        "pointsMatchingRate": 90.6,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2447",
        "athenaId": "https://athena.company.com/review/ATH-9817"
    },
    {
        "id": "6",
        "name": "Professional Services Contract",
        "vendor": "Consulting Partners",
        "reviewDate": "Oct 3, 2025",
        "status": "needs-review",
        "riskLevel": "medium",
        "reviewer": "Michael Chen",
        "termMatchingRate": 72.8,
        "pointsMatchingRate": 75.2,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2446",
        "athenaId": "https://athena.company.com/review/ATH-9816"
    },
    {
        "id": "7",
        "name": "Non-Disclosure Agreement",
        "vendor": "Innovation Labs",
        "reviewDate": "Oct 2, 2025",
        "status": "compliant",
        "riskLevel": "low",
        "reviewer": "Emily Rodriguez",
        "termMatchingRate": 96.1,
        "pointsMatchingRate": 94.3,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2445",
        "athenaId": "https://athena.company.com/review/ATH-9815"
    },
    {
        "id": "8",
        "name": "Cloud Infrastructure Agreement",
        "vendor": "HostTech Inc",
        "reviewDate": "Oct 1, 2025",
        "status": "compliant",
        "riskLevel": "medium",
        "reviewer": "David Park",
        "termMatchingRate": 87.6,
        "pointsMatchingRate": 85.4,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2444",
        "athenaId": "https://athena.company.com/review/ATH-9814"
    },
    {
        "id": "9",
        "name": "Software License Agreement",
        "vendor": "DevTools Pro",
        "reviewDate": "Sep 30, 2025",
        "status": "compliant",
        "riskLevel": "low",
        "reviewer": "Sarah Johnson",
        "termMatchingRate": 92.3,
        "pointsMatchingRate": 89.7,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2443",
        "athenaId": "https://athena.company.com/review/ATH-9813"
    },
    {
        "id": "10",
        "name": "API Integration Agreement",
        "vendor": "IntegrationHub",
        "reviewDate": "Sep 28, 2025",
        "status": "needs-review",
        "riskLevel": "medium",
        "reviewer": "Michael Chen",
        "termMatchingRate": 68.9,
        "pointsMatchingRate": 71.5,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2442",
        "athenaId": "https://athena.company.com/review/ATH-9812"
    },
    {
        "id": "11",
        "name": "Security Audit Contract",
        "vendor": "CyberShield Inc",
        "reviewDate": "Sep 25, 2025",
        "status": "compliant",
        "riskLevel": "high",
        "reviewer": "Emily Rodriguez",
        "termMatchingRate": 94.8,
        "pointsMatchingRate": 91.2,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2441",
        "athenaId": "https://athena.company.com/review/ATH-9811"
    },
    {
        "id": "12",
        "name": "Marketing Services Agreement",
        "vendor": "BrandBoost Agency",
        "reviewDate": "Sep 22, 2025",
        "status": "compliant",
        "riskLevel": "low",
        "reviewer": "David Park",
        "termMatchingRate": 88.4,
        "pointsMatchingRate": 86.1,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2440",
        "athenaId": "https://athena.company.com/review/ATH-9810"
    },
    {
        "id": "13",
        "name": "Vendor Management Platform",
        "vendor": "VendorConnect",
        "reviewDate": "Sep 20, 2025",
        "status": "needs-review",
        "riskLevel": "medium",
        "reviewer": "Sarah Johnson",
        "termMatchingRate": 75.3,
        "pointsMatchingRate": 78.9,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2439",
        "athenaId": "https://athena.company.com/review/ATH-9809"
    },
    {
        "id": "14",
        "name": "HR Software License",
        "vendor": "PeopleFirst HR",
        "reviewDate": "Sep 18, 2025",
        "status": "compliant",
        "riskLevel": "low",
        "reviewer": "Michael Chen",
        "termMatchingRate": 90.6,
        "pointsMatchingRate": 87.3,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2438",
        "athenaId": "https://athena.company.com/review/ATH-9808"
    },
    {
        "id": "15",
        "name": "Cloud Storage Agreement",
        "vendor": "DataVault Solutions",
        "reviewDate": "Sep 15, 2025",
        "status": "compliant",
        "riskLevel": "medium",
        "reviewer": "Emily Rodriguez",
        "termMatchingRate": 85.2,
        "pointsMatchingRate": 82.8,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2437",
        "athenaId": "https://athena.company.com/review/ATH-9807"
    },
    {
        "id": "16",
        "name": "Payment Processing Agreement",
        "vendor": "PaySecure Gateway",
        "reviewDate": "Sep 12, 2025",
        "status": "non-compliant",
        "riskLevel": "high",
        "reviewer": "David Park",
        "termMatchingRate": 45.7,
        "pointsMatchingRate": 41.2,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2436",
        "athenaId": "https://athena.company.com/review/ATH-9806"
    },
    {
        "id": "17",
        "name": "Analytics Platform License",
        "vendor": "DataInsights Co",
        "reviewDate": "Sep 10, 2025",
        "status": "compliant",
        "riskLevel": "low",
        "reviewer": "Sarah Johnson",
        "termMatchingRate": 93.9,
        "pointsMatchingRate": 91.5,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2435",
        "athenaId": "https://athena.company.com/review/ATH-9805"
    },
    {
        "id": "18",
        "name": "Support Services Contract",
        "vendor": "TechSupport 24/7",
        "reviewDate": "Sep 8, 2025",
        "status": "compliant",
        "riskLevel": "low",
        "reviewer": "Michael Chen",
        "termMatchingRate": 89.1,
        "pointsMatchingRate": 86.7,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2434",
        "athenaId": "https://athena.company.com/review/ATH-9804"
    },
    {
        "id": "19",
        "name": "Consulting Services Agreement",
        "vendor": "Strategy Advisors",
        "reviewDate": "Sep 5, 2025",
        "status": "needs-review",
        "riskLevel": "medium",
        "reviewer": "Emily Rodriguez",
        "termMatchingRate": 70.4,
        "pointsMatchingRate": 73.8,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2433",
        "athenaId": "https://athena.company.com/review/ATH-9803"
    },
    {
        "id": "20",
        "name": "Training Services Contract",
        "vendor": "LearnTech Academy",
        "reviewDate": "Sep 1, 2025",
        "status": "compliant",
        "riskLevel": "low",
        "reviewer": "David Park",
        "termMatchingRate": 91.2,
        "pointsMatchingRate": 88.6,
        "jiraEngagementId": "https://jira.company.com/browse/ENG-2432",
        "athenaId": "https://athena.company.com/review/ATH-9802"
    }
]

# Review request items for collapsible navigation
REVIEW_REQUEST_ITEMS = [
    {"id": "gdpr", "label": "GDPR Review", "url": "https://forms.company.com/compliance/gdpr-review"},
    {"id": "soc2", "label": "SOC 2 Review", "url": "https://forms.company.com/compliance/soc2-review"},
    {"id": "hipaa", "label": "HIPAA Review", "url": "https://forms.company.com/compliance/hipaa-review"},
    {"id": "ccpa", "label": "CCPA Review", "url": "https://forms.company.com/compliance/ccpa-review"},
    {"id": "iso27001", "label": "ISO 27001 Review", "url": "https://forms.company.com/compliance/iso27001-review"},
    {"id": "pci-dss", "label": "PCI DSS Review", "url": "https://forms.company.com/compliance/pci-dss-review"},
    {"id": "custom", "label": "Custom Review", "url": "https://forms.company.com/compliance/custom-review"}
]

# Import other components
from layouts import (
    create_sidebar,
    create_header,
    create_analytics_view,
    create_completed_reviews_view,
    create_standards_view,
    create_contract_detail_view
)

# Main app layout
app.layout = dbc.Container(
    fluid=True,
    style={'height': '100vh', 'display': 'flex', 'padding': 0, 'backgroundColor': COLORS['slate']['50']},
    children=[
        # Store components for state management
        dcc.Store(id='active-view', data='analytics'),
        dcc.Store(id='selected-contract', data=None),
        dcc.Store(id='sidebar-collapsed', data=False),
        dcc.Store(id='request-review-collapsed', data=True),
        
        # Hidden button for callback compatibility (shown in contract detail view)
        dbc.Button(id='back-to-reviews-btn', style={'display': 'none'}, n_clicks=0),
        
        # Download component for export functionality
        dcc.Download(id='download-results'),
        
        # Toast for export success notification
        dbc.Toast(
            "Results exported successfully!",
            id="export-results-toast",
            header="Export Complete",
            is_open=False,
            dismissable=True,
            icon="success",
            duration=3000,
            style={"position": "fixed", "top": 66, "right": 10, "width": 350, "zIndex": 9999}
        ),
        
        # Sidebar
        html.Div(
            id='sidebar-container',
            children=create_sidebar(),
            style={
                'minWidth': '250px',
                'maxWidth': '250px',
                'width': '250px',
                'height': '100vh',
                'backgroundColor': 'white',
                'borderRight': f'1px solid {COLORS["slate"]["200"]}',
                'transition': 'all 0.3s ease',
                'display': 'flex',
                'flexDirection': 'column',
                'overflow': 'hidden'
            }
        ),
        
        # Main content area
        html.Div(
            style={'flex': 1, 'display': 'flex', 'flexDirection': 'column', 'overflow': 'hidden'},
            children=[
                # Header
                html.Div(
                    id='header-container',
                    children=create_header(),
                    style={
                        'backgroundColor': 'white',
                        'borderBottom': f'1px solid {COLORS["slate"]["200"]}',
                        'position': 'sticky',
                        'top': 0,
                        'zIndex': 10
                    }
                ),
                
                # Main content
                html.Div(
                    id='main-content',
                    style={
                        'flex': 1,
                        'padding': '24px',
                        'overflow': 'auto',
                        'backgroundColor': COLORS['slate']['50']
                    }
                )
            ]
        )
    ]
)

# Callbacks will be defined in callbacks.py
from callbacks import register_callbacks
register_callbacks(app, MOCK_CONTRACTS, COLORS, REVIEW_REQUEST_ITEMS)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
