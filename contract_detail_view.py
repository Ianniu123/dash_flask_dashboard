"""
Contract Detail View for the Contract Compliance Dashboard
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

def icon(name, **kwargs):
    """Helper function to create DashIconify icons"""
    return DashIconify(icon=name, **kwargs)

def get_term_status(term):
    """Determine the status of a compliance term based on subpoints"""
    met_subpoints = sum(1 for sp in term['subPoints'] if sp['met'])
    total_subpoints = len(term['subPoints'])
    
    if met_subpoints == total_subpoints:
        return "met"
    elif met_subpoints == 0:
        return "missing"
    else:
        return "partially-met"

# All 40 compliance terms with detailed subpoints
COMPLIANCE_TERMS = [
    {
        'id': '1',
        'heading': 'Data Encryption Requirements',
        'description': 'Contract must specify that all data in transit and at rest is encrypted using industry-standard encryption protocols.',
        'overallAnalysis': 'The contract demonstrates comprehensive compliance with encryption requirements across all three critical dimensions.',
        'subPoints': [
            {
                'heading': 'Encryption in Transit',
                'description': 'All data transmitted over networks must use TLS 1.2 or higher with strong cipher suites.',
                'met': True,
                'analysis': 'The contract exceeds the minimum requirement by implementing TLS 1.3.',
                'evidence': [
                    {
                        'excerpt': 'Section 4.2: All data transmissions between Client and Vendor systems shall utilize Transport Layer Security (TLS) version 1.2 or higher.',
                        'explanation': 'This clause explicitly requires TLS 1.2 or higher and references NIST standards.'
                    }
                ]
            },
            {
                'heading': 'Encryption at Rest',
                'description': 'Stored data must be encrypted using AES-256 or equivalent encryption standards.',
                'met': True,
                'analysis': 'Section 4.3 provides clear requirements for data-at-rest encryption.',
                'evidence': [
                    {
                        'excerpt': 'Section 4.3: Vendor shall encrypt all Client data at rest using AES-256.',
                        'explanation': 'The contract mandates AES-256 encryption for data at rest.'
                    }
                ]
            },
            {
                'heading': 'Key Management',
                'description': 'Encryption keys must be managed securely with proper rotation and access controls.',
                'met': True,
                'analysis': 'Section 4.4 provides comprehensive key management controls.',
                'evidence': []
            }
        ]
    },
    {
        'id': '2',
        'heading': 'Third-Party Data Disclosure',
        'description': 'Contract must explicitly state restrictions on sharing data with third parties.',
        'overallAnalysis': 'The contract provides comprehensive coverage of third-party data disclosure requirements.',
        'subPoints': [
            {
                'heading': 'Prior Written Consent',
                'description': 'Third-party sharing requires explicit written approval from the data controller.',
                'met': True,
                'analysis': 'Section 6.1 requires prior written consent.',
                'evidence': []
            },
            {
                'heading': 'Disclosure Notification',
                'description': 'Vendor must notify client of legally mandated disclosures.',
                'met': True,
                'analysis': 'Contract provides clear notification requirements.',
                'evidence': []
            }
        ]
    },
    {
        'id': '3',
        'heading': 'Data Breach Notification',
        'description': 'Contract must specify timeline and procedures for breach notifications.',
        'subPoints': [
            {
                'heading': 'Notification Timeline',
                'description': 'Breaches must be reported within 72 hours.',
                'met': True,
                'analysis': 'Meets regulatory requirements.',
                'evidence': []
            },
            {
                'heading': 'Notification Content',
                'description': 'Notification must include scope and impact details.',
                'met': True,
                'analysis': 'Comprehensive requirements specified.',
                'evidence': []
            }
        ]
    }
]

# Add remaining 37 terms (simplified for brevity)
for i in range(4, 41):
    term_names = [
        'Data Retention and Deletion', 'Access Control and Authentication', 
        'Audit Rights and Compliance Reporting', 'Liability and Indemnification',
        'Subprocessor Management', 'Business Continuity and Disaster Recovery',
        'Termination and Data Portability', 'Privacy Impact Assessment',
        'Vendor Security Training', 'Incident Response Procedures',
        'Penetration Testing Requirements', 'Data Classification Standards',
        'Change Management Process', 'Vulnerability Management',
        'Physical Security Controls', 'Secure Development Lifecycle',
        'Network Segmentation', 'Log Management and Monitoring',
        'Certificate and Secret Management', 'API Security Requirements',
        'Mobile Device Management', 'Email Security Requirements',
        'Backup and Recovery Procedures', 'Security Awareness Training',
        'Third-Party Risk Assessment', 'Insurance Requirements',
        'Intellectual Property Rights', 'Service Level Agreements',
        'Force Majeure Provisions', 'Dispute Resolution',
        'Jurisdiction and Governing Law', 'Contract Amendment Procedures',
        'Confidentiality Obligations', 'Employee Background Checks',
        'Data Transfer Mechanisms', 'Right to Audit',
        'Asset Tracking'
    ]
    
    idx = i - 4
    if idx < len(term_names):
        term_name = term_names[idx]
    else:
        term_name = f'Compliance Term {i}'
    
    # Vary the compliance status for diversity
    met_count = (i * 7) % 4  # Creates variety
    total = 3
    
    subpoints = []
    for j in range(total):
        subpoints.append({
            'heading': f'{term_name} - Requirement {j+1}',
            'description': f'Description for requirement {j+1}',
            'met': j < met_count,
            'analysis': f'Analysis for requirement {j+1}',
            'evidence': []
        })
    
    COMPLIANCE_TERMS.append({
        'id': str(i),
        'heading': term_name,
        'description': f'Contract requirements for {term_name.lower()}.',
        'overallAnalysis': f'Overall analysis for {term_name}.',
        'subPoints': subpoints
    })


def get_contract_detail_layout(contract):
    """Generate the contract detail view layout"""
    from contract_detail_header import create_contract_detail_header, create_instructions_banner
    from evidence_offcanvas import create_evidence_offcanvas
    
    # Calculate compliance metrics
    total_terms = len(COMPLIANCE_TERMS)
    met_terms = len([t for t in COMPLIANCE_TERMS if get_term_status(t) == "met"])
    partial_terms = len([t for t in COMPLIANCE_TERMS if get_term_status(t) == "partially-met"])
    missing_terms = len([t for t in COMPLIANCE_TERMS if get_term_status(t) == "missing"])
    
    total_points = sum(len(t['subPoints']) for t in COMPLIANCE_TERMS)
    met_points = sum(len([sp for sp in t['subPoints'] if sp['met']]) for t in COMPLIANCE_TERMS)
    
    terms_percentage = round((met_terms / total_terms) * 100) if total_terms > 0 else 0
    points_percentage = round((met_points / total_points) * 100) if total_points > 0 else 0
    
    # Generate accordion items for all compliance terms
    accordion_items = []
    for term in COMPLIANCE_TERMS:
        term_status = get_term_status(term)
        met_subpoints = len([sp for sp in term['subPoints'] if sp['met']])
        total_subpoints = len(term['subPoints'])
        term_score = round((met_subpoints / total_subpoints) * 100) if total_subpoints > 0 else 0
        
        # Status icon and color
        if term_status == "met":
            status_icon = "✓"
            status_color = "#16a34a"
            status_bg = "#dcfce7"
            status_text = "Met"
        elif term_status == "partially-met":
            status_icon = "◐"
            status_color = "#eab308"
            status_bg = "#fef3c7"
            status_text = "Partially Met"
        else:
            status_icon = "✗"
            status_color = "#dc2626"
            status_bg = "#fee2e2"
            status_text = "Missing"
        
        # Build subpoint items
        subpoint_items = []
        for idx, subpoint in enumerate(term['subPoints']):
            sp_status_icon = "✓" if subpoint['met'] else "✗"
            sp_status_color = "#16a34a" if subpoint['met'] else "#dc2626"
            sp_status_bg = "#dcfce7" if subpoint['met'] else "#fee2e2"
            
            evidence_count = len(subpoint.get('evidence', []))
            
            subpoint_items.append(
                html.Div([
                    # Subpoint header
                    html.Div([
                        html.Div([
                            html.Span(sp_status_icon, style={
                                'color': sp_status_color,
                                'marginRight': '8px',
                                'fontSize': '16px',
                                'fontWeight': 'bold'
                            }),
                            html.Span(subpoint['heading'], style={
                                'fontSize': '14px',
                                'fontWeight': 500,
                                'color': '#0f172a'
                            })
                        ], style={'display': 'flex', 'alignItems': 'center'}),
                        html.Span(subpoint['met'] and 'Supported' or 'Not Supported', style={
                            'fontSize': '12px',
                            'padding': '2px 8px',
                            'borderRadius': '4px',
                            'backgroundColor': sp_status_bg,
                            'color': sp_status_color,
                            'fontWeight': 500
                        })
                    ], style={
                        'display': 'flex',
                        'justifyContent': 'space-between',
                        'alignItems': 'center',
                        'marginBottom': '8px'
                    }),
                    
                    # Subpoint description
                    html.P(subpoint['description'], style={
                        'fontSize': '13px',
                        'color': '#64748b',
                        'margin': '0 0 12px 0'
                    }),
                    
                    # Analysis toggle
                    html.Div([
                        dbc.Button([
                            icon("mdi:text-box-outline", width=14, style={'marginRight': '6px'}),
                            "Analysis"
                        ],
                            id={'type': 'toggle-analysis-btn', 'term_id': term['id'], 'subpoint_idx': idx},
                            color="link",
                            size="sm",
                            style={'padding': '4px 8px', 'fontSize': '12px'}
                        ),
                        dbc.Button([
                            icon("mdi:file-document-outline", width=14, style={'marginRight': '6px'}),
                            f"View Evidence ({evidence_count})"
                        ],
                            id={'type': 'view-evidence-btn', 'term_id': term['id'], 'subpoint_idx': idx},
                            color="link",
                            size="sm",
                            style={'padding': '4px 8px', 'fontSize': '12px'},
                            disabled=evidence_count == 0
                        )
                    ], style={'display': 'flex', 'gap': '8px', 'marginBottom': '8px'}),
                    
                    # Analysis collapse
                    dbc.Collapse([
                        html.Div([
                            html.P(subpoint.get('analysis', 'No analysis available'), style={
                                'fontSize': '13px',
                                'color': '#475569',
                                'margin': 0,
                                'lineHeight': 1.6
                            })
                        ], style={
                            'backgroundColor': '#f8fafc',
                            'padding': '12px',
                            'borderRadius': '6px',
                            'border': '1px solid #e2e8f0'
                        })
                    ],
                        id={'type': 'analysis-collapse', 'term_id': term['id'], 'subpoint_idx': idx},
                        is_open=False
                    )
                ], style={
                    'padding': '12px',
                    'backgroundColor': 'white',
                    'border': '1px solid #e2e8f0',
                    'borderRadius': '6px',
                    'marginBottom': '12px'
                })
            )
        
        # Term attestation section
        attestation_section = html.Div([
            # Initial state (not reviewed)
            html.Div([
                dbc.Button([
                    icon("mdi:check-circle-outline", width=16, style={'marginRight': '6px'}),
                    "Approve Result"
                ],
                    id={'type': 'approve-term-btn', 'term_id': term['id']},
                    color="success",
                    size="sm",
                    outline=True
                ),
                dbc.Button([
                    icon("mdi:pencil-outline", width=16, style={'marginRight': '6px'}),
                    "Override Result"
                ],
                    id={'type': 'override-term-btn', 'term_id': term['id']},
                    color="warning",
                    size="sm",
                    outline=True
                )
            ],
                id={'type': 'term-attestation-initial', 'term_id': term['id']},
                style={'display': 'flex', 'alignItems': 'center', 'gap': '8px'}
            ),
            
            # Approved state
            html.Div([
                html.Div([
                    icon("mdi:check-circle", width=16, color='#16a34a', style={'marginRight': '8px'}),
                    html.Span("Result Approved", style={'color': '#16a34a', 'fontWeight': 500, 'fontSize': '14px'})
                ], style={'display': 'flex', 'alignItems': 'center'}),
                dbc.Button([
                    icon("mdi:pencil", width=14),
                ],
                    id={'type': 'change-term-approval-btn', 'term_id': term['id']},
                    color="link",
                    size="sm",
                    style={'padding': '4px 8px'}
                )
            ],
                id={'type': 'term-attestation-approved', 'term_id': term['id']},
                style={'display': 'none', 'alignItems': 'center', 'padding': '6px 12px', 'backgroundColor': '#f0fdf4', 'borderRadius': '6px', 'border': '1px solid #bbf7d0'}
            ),
            
            # Overridden state
            html.Div([
                html.Div([
                    icon("mdi:alert-circle", width=16, color='#eab308', style={'marginRight': '8px'}),
                    html.Div([
                        html.P(id={'type': 'term-override-status-text', 'term_id': term['id']}, 
                               style={'margin': 0, 'fontSize': '14px', 'fontWeight': 500, 'color': '#92400e'}),
                        html.P(id={'type': 'term-override-reason-display', 'term_id': term['id']},
                               style={'margin': '4px 0 0 0', 'fontSize': '12px', 'color': '#78716c'})
                    ], style={'flex': 1})
                ], style={'display': 'flex', 'alignItems': 'start', 'flex': 1}),
                dbc.Button([
                    icon("mdi:pencil", width=14),
                ],
                    id={'type': 'change-term-override-btn', 'term_id': term['id']},
                    color="link",
                    size="sm",
                    style={'padding': '4px 8px'}
                )
            ],
                id={'type': 'term-attestation-overridden', 'term_id': term['id']},
                style={'display': 'none', 'alignItems': 'flex-start', 'justifyContent': 'space-between', 'padding': '6px 12px', 'backgroundColor': '#fffbeb', 'borderRadius': '6px', 'border': '1px solid #fde68a'}
            ),
            
            # Editing state
            html.Div([
                html.Div([
                    html.Label("Override Status:", style={'fontSize': '13px', 'fontWeight': 500, 'marginBottom': '4px', 'display': 'block'}),
                    dcc.Dropdown(
                        id={'type': 'term-override-dropdown', 'term_id': term['id']},
                        options=[
                            {'label': 'Met', 'value': 'met'},
                            {'label': 'Partially Met', 'value': 'partially-met'},
                            {'label': 'Missing', 'value': 'missing'}
                        ],
                        value=term_status,
                        style={'marginBottom': '12px', 'fontSize': '13px'}
                    ),
                    html.Label("Reason for Override:", style={'fontSize': '13px', 'fontWeight': 500, 'marginBottom': '4px', 'display': 'block'}),
                    dbc.Textarea(
                        id={'type': 'term-override-reason-input', 'term_id': term['id']},
                        placeholder="Explain why you're changing this result...",
                        style={'fontSize': '13px', 'marginBottom': '12px'},
                        rows=2
                    ),
                    html.Div([
                        dbc.Button("Save Override", 
                                 id={'type': 'save-term-override-btn', 'term_id': term['id']},
                                 color="warning", 
                                 size="sm"),
                        dbc.Button("Cancel", 
                                 id={'type': 'cancel-term-override-btn', 'term_id': term['id']},
                                 color="light", 
                                 size="sm",
                                 style={'marginLeft': '8px'})
                    ])
                ], style={'width': '100%'})
            ],
                id={'type': 'term-attestation-editing', 'term_id': term['id']},
                style={'display': 'none'}
            )
        ], style={
            'marginTop': '16px',
            'paddingTop': '16px',
            'borderTop': '1px solid #e2e8f0'
        })
        
        # Build accordion item
        accordion_items.append(
            html.Div([
                # Accordion header
                dbc.Button([
                    html.Div([
                        html.Div([
                            html.Span(status_icon, style={
                                'color': status_color,
                                'marginRight': '12px',
                                'fontSize': '18px',
                                'fontWeight': 'bold'
                            }),
                            html.Span(term['heading'], style={
                                'fontSize': '15px',
                                'fontWeight': 500,
                                'color': '#0f172a',
                                'flex': 1
                            })
                        ], style={'display': 'flex', 'alignItems': 'center', 'flex': 1}),
                        html.Div([
                            html.Span(f"{met_subpoints}/{total_subpoints}", style={
                                'fontSize': '13px',
                                'color': '#64748b',
                                'marginRight': '12px'
                            }),
                            html.Span(status_text, style={
                                'fontSize': '12px',
                                'padding': '4px 10px',
                                'borderRadius': '12px',
                                'backgroundColor': status_bg,
                                'color': status_color,
                                'fontWeight': 500,
                                'marginRight': '12px'
                            }),
                            icon("mdi:chevron-down", width=20, color='#64748b')
                        ], style={'display': 'flex', 'alignItems': 'center'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'width': '100%'})
                ],
                    id={'type': 'accordion-btn', 'index': term['id']},
                    color="light",
                    className="w-100 text-left",
                    style={
                        'display': 'flex',
                        'justifyContent': 'space-between',
                        'alignItems': 'center',
                        'padding': '16px',
                        'border': '1px solid #e2e8f0',
                        'borderRadius': '8px',
                        'marginBottom': '0'
                    }
                ),
                
                # Accordion content
                dbc.Collapse([
                    html.Div([
                        # Term description
                        html.P(term['description'], style={
                            'fontSize': '14px',
                            'color': '#64748b',
                            'margin': '0 0 16px 0'
                        }),
                        
                        # Overall Analysis section
                        html.Div([
                            dbc.Button([
                                icon("mdi:information-outline", width=14, style={'marginRight': '6px'}),
                                "Overall Analysis"
                            ],
                                id={'type': 'overall-analysis-btn', 'index': term['id']},
                                color="link",
                                size="sm",
                                style={'padding': '4px 8px', 'fontSize': '13px', 'marginBottom': '8px'}
                            ),
                            dbc.Collapse([
                                html.Div([
                                    html.P(term.get('overallAnalysis', 'No overall analysis available'), style={
                                        'fontSize': '13px',
                                        'color': '#475569',
                                        'margin': 0,
                                        'lineHeight': 1.6
                                    })
                                ], style={
                                    'backgroundColor': '#f1f5f9',
                                    'padding': '12px',
                                    'borderRadius': '6px',
                                    'border': '1px solid #cbd5e1',
                                    'marginBottom': '16px'
                                })
                            ],
                                id={'type': 'overall-analysis-collapse', 'index': term['id']},
                                is_open=False
                            )
                        ]),
                        
                        # Subpoints
                        html.Div(subpoint_items),
                        
                        # Term attestation section
                        attestation_section
                        
                    ], style={'padding': '16px', 'backgroundColor': '#fafafa', 'borderLeft': '3px solid ' + status_color})
                ],
                    id={'type': 'accordion-collapse', 'index': term['id']},
                    is_open=False
                )
            ], style={'marginBottom': '8px'})
        )
    
    # Main layout
    return html.Div([
        # Store for attestations
        dcc.Store(id='term-attestation-store', data=[]),
        dcc.Store(id='is-attested-store', data=False),
        dcc.Store(id='evidence-data-store', data=None),
        dcc.Store(id='evidence-current-index', data=0),
        
        # Evidence offcanvas
        create_evidence_offcanvas(),
        
        # Header with back button and export button
        create_contract_detail_header(total_terms),
        
        # Instructions banner
        create_instructions_banner(total_terms),
        
        # Attestation status banners
        html.Div([
            dbc.Alert([
                icon("mdi:shield-check", width=16, color='#16a34a', style={'marginRight': '12px'}),
                html.Span([
                    html.Strong("Review Attested"),
                    f" - This compliance review has been fully attested and all {total_terms} terms have been reviewed."
                ], style={'color': '#15803d'})
            ], color="success", id='attested-banner', style={'display': 'none'})
        ]),
        
        html.Div([
            dbc.Alert([
                icon("mdi:alert-circle", width=16, color='#2563eb', style={'marginRight': '12px'}),
                html.Span([
                    html.Strong("Attestation Required"),
                    html.Span(id='attestation-banner-message',
                             children=f" - Please review all {total_terms} compliance terms and attest the review when complete (0 of {total_terms} reviewed).")
                ], style={'color': '#1e40af'})
            ], color="info", id='unattested-banner')
        ]),
        
        # Contract overview card
        dbc.Card([
            dbc.CardBody([
                # Contract title and badges
                html.Div([
                    html.Div([
                        html.Div([
                            icon("mdi:file-document", width=20, color='#2563eb', style={'marginRight': '8px'}),
                            html.H4(contract['name'], style={'margin': 0, 'color': '#0f172a'})
                        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '4px'}),
                        html.P(f"Reviewed on {contract['reviewDate']} by {contract['reviewer']}", 
                               style={'fontSize': '14px', 'color': '#64748b', 'margin': 0})
                    ], style={'flex': 1}),
                    html.Div([
                        html.Span(contract['status'].replace('-', ' ').title(), style={
                            'fontSize': '13px',
                            'padding': '6px 12px',
                            'borderRadius': '6px',
                            'backgroundColor': '#dbeafe',
                            'color': '#1e40af',
                            'fontWeight': 500,
                            'marginRight': '8px'
                        }),
                        html.Span(f"{contract['riskLevel'].title()} Risk", style={
                            'fontSize': '13px',
                            'padding': '6px 12px',
                            'borderRadius': '6px',
                            'backgroundColor': '#fee2e2',
                            'color': '#991b1b',
                            'fontWeight': 500
                        })
                    ])
                ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'start', 'marginBottom': '24px'}),
                
                # Metadata grid (5 columns)
                html.Div([
                    html.Div([
                        html.P("Vendor", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 4px 0'}),
                        html.P(contract['vendor'], style={'fontSize': '14px', 'color': '#0f172a', 'margin': 0})
                    ]),
                    html.Div([
                        html.P("Review Date", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 4px 0'}),
                        html.P(contract['reviewDate'], style={'fontSize': '14px', 'color': '#0f172a', 'margin': 0})
                    ]),
                    html.Div([
                        html.P("Reviewer", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 4px 0'}),
                        html.P(contract['reviewer'], style={'fontSize': '14px', 'color': '#0f172a', 'margin': 0})
                    ]),
                    html.Div([
                        html.P("Jira Engagement ID", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 4px 0'}),
                        html.A([
                            html.Span(contract['jiraEngagementId'].split('/')[-1], style={'marginRight': '4px'}),
                            icon("mdi:open-in-new", width=12)
                        ], href=contract['jiraEngagementId'], target='_blank',
                           style={'fontSize': '14px', 'color': '#2563eb', 'textDecoration': 'none', 'display': 'flex', 'alignItems': 'center'})
                    ]),
                    html.Div([
                        html.P("Athena ID", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 4px 0'}),
                        html.A([
                            html.Span(contract['athenaId'].split('/')[-1], style={'marginRight': '4px'}),
                            icon("mdi:open-in-new", width=12)
                        ], href=contract['athenaId'], target='_blank',
                           style={'fontSize': '14px', 'color': '#2563eb', 'textDecoration': 'none', 'display': 'flex', 'alignItems': 'center'})
                    ])
                ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))', 'gap': '16px', 'marginBottom': '24px'}),
                
                # Progress cards
                html.Div([
                    # Terms compliance card
                    html.Div([
                        html.P("Terms Compliance", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 8px 0'}),
                        html.Div([
                            html.Span(f"{terms_percentage}%", style={'fontSize': '28px', 'color': '#0f172a'}),
                            html.Span(f"{met_terms} of {total_terms} terms met", style={'fontSize': '13px', 'color': '#64748b', 'marginLeft': '8px'})
                        ], style={'display': 'flex', 'alignItems': 'baseline', 'marginBottom': '8px'}),
                        dbc.Progress(value=terms_percentage, style={'height': '8px'})
                    ], style={'padding': '16px', 'backgroundColor': 'white', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'}),
                    
                    # Points compliance card
                    html.Div([
                        html.P("Points Compliance", style={'fontSize': '13px', 'color': '#64748b', 'margin': '0 0 8px 0'}),
                        html.Div([
                            html.Span(f"{points_percentage}%", style={'fontSize': '28px', 'color': '#0f172a'}),
                            html.Span(f"{met_points} of {total_points} points met", style={'fontSize': '13px', 'color': '#64748b', 'marginLeft': '8px'})
                        ], style={'display': 'flex', 'alignItems': 'baseline', 'marginBottom': '8px'}),
                        dbc.Progress(value=points_percentage, style={'height': '8px'})
                    ], style={'padding': '16px', 'backgroundColor': 'white', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
                ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))', 'gap': '16px', 'marginBottom': '24px'}),
                
                # Term Status Breakdown
                html.Div([
                    html.H5("Term Status Breakdown", style={'fontSize': '14px', 'color': '#0f172a', 'marginBottom': '12px'}),
                    
                    dbc.Row([
                        # Met terms
                        dbc.Col([
                            html.Div([
                                dbc.Button([
                                    html.Div([
                                        html.Div(style={'width': '12px', 'height': '12px', 'borderRadius': '50%', 'backgroundColor': '#16a34a', 'marginRight': '8px'}),
                                        html.Span("Met", style={'fontSize': '14px', 'color': '#0f172a'})
                                    ], style={'display': 'flex', 'alignItems': 'center'}),
                                    html.Div([
                                        html.Span(str(met_terms), style={
                                            'fontSize': '14px',
                                            'fontWeight': 500,
                                            'padding': '2px 8px',
                                            'borderRadius': '9999px',
                                            'backgroundColor': '#dcfce7',
                                            'color': '#15803d',
                                            'marginRight': '8px'
                                        }),
                                        icon("mdi:chevron-down", width=16, color='#64748b')
                                    ], style={'display': 'flex', 'alignItems': 'center'})
                                ], 
                                    id='collapse-met-btn',
                                    color="light",
                                    outline=True,
                                    className="w-100",
                                    style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'padding': '12px', 'height': 'auto'}
                                ),
                                dbc.Collapse(
                                    id='collapse-met',
                                    is_open=False
                                )
                            ])
                        ], md=4),
                        
                        # Partially met terms
                        dbc.Col([
                            html.Div([
                                dbc.Button([
                                    html.Div([
                                        html.Div(style={'width': '12px', 'height': '12px', 'borderRadius': '50%', 'backgroundColor': '#eab308', 'marginRight': '8px'}),
                                        html.Span("Partially Met", style={'fontSize': '14px', 'color': '#0f172a'})
                                    ], style={'display': 'flex', 'alignItems': 'center'}),
                                    html.Div([
                                        html.Span(str(partial_terms), style={
                                            'fontSize': '14px',
                                            'fontWeight': 500,
                                            'padding': '2px 8px',
                                            'borderRadius': '9999px',
                                            'backgroundColor': '#fef3c7',
                                            'color': '#92400e',
                                            'marginRight': '8px'
                                        }),
                                        icon("mdi:chevron-down", width=16, color='#64748b')
                                    ], style={'display': 'flex', 'alignItems': 'center'})
                                ], 
                                    id='collapse-partial-btn',
                                    color="light",
                                    outline=True,
                                    className="w-100",
                                    style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'padding': '12px', 'height': 'auto'}
                                ),
                                dbc.Collapse(
                                    id='collapse-partial',
                                    is_open=False
                                )
                            ])
                        ], md=4),
                        
                        # Missing terms (combined with partial in collapse)
                        dbc.Col([
                            html.Div([
                                dbc.Button([
                                    html.Div([
                                        html.Div(style={'width': '12px', 'height': '12px', 'borderRadius': '50%', 'backgroundColor': '#dc2626', 'marginRight': '8px'}),
                                        html.Span("Missing", style={'fontSize': '14px', 'color': '#0f172a'})
                                    ], style={'display': 'flex', 'alignItems': 'center'}),
                                    html.Div([
                                        html.Span(str(missing_terms), style={
                                            'fontSize': '14px',
                                            'fontWeight': 500,
                                            'padding': '2px 8px',
                                            'borderRadius': '9999px',
                                            'backgroundColor': '#fee2e2',
                                            'color': '#991b1b',
                                            'marginRight': '8px'
                                        }),
                                        icon("mdi:chevron-down", width=16, color='#64748b')
                                    ], style={'display': 'flex', 'alignItems': 'center'})
                                ], 
                                    id='collapse-missing-btn',
                                    color="light",
                                    outline=True,
                                    className="w-100",
                                    style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'padding': '12px', 'height': 'auto'}
                                ),
                                dbc.Collapse(
                                    id='collapse-missing',
                                    is_open=False
                                )
                            ])
                        ], md=4)
                    ])
                ], style={'paddingTop': '24px', 'borderTop': '1px solid #e2e8f0'})
            ])
        ], style={'marginBottom': '24px'}),
        
        # Compliance terms accordion
        dbc.Card([
            dbc.CardHeader([
                html.H5("Compliance Terms Review", style={'margin': 0}),
                html.P(f"Detailed review of {total_terms} compliance requirements",
                       style={'fontSize': '14px', 'color': '#64748b', 'margin': '8px 0 0 0'})
            ]),
            dbc.CardBody([
                html.Div(accordion_items, id='compliance-accordion'),
                
                # Attestation Progress and Button
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H4("Review Progress", style={'fontSize': '14px', 'color': '#0f172a', 'margin': '0 0 4px 0'}),
                                html.P([
                                    html.Span(id='reviewed-count', children='0'),
                                    f" of {total_terms} terms reviewed"
                                ], style={'fontSize': '12px', 'color': '#64748b', 'margin': 0})
                            ], style={'flex': 1}),
                            html.Div(id='progress-percentage', children='0%', style={'fontSize': '14px', 'color': '#0f172a'})
                        ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'marginBottom': '16px'}),
                        dbc.Progress(id='attestation-progress', value=0, style={'height': '8px', 'marginBottom': '16px'}),
                        html.Div([
                            dbc.Button([
                                icon("mdi:check-circle", width=16, style={'marginRight': '8px'}),
                                "Attest Review"
                            ], 
                                id='attest-review-btn',
                                color='primary',
                                disabled=True,
                                className='w-100',
                                style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}
                            ),
                            html.P(id='attest-message', children="Please review all terms before attesting",
                                   style={'fontSize': '12px', 'color': '#64748b', 'margin': '8px 0 0 0', 'textAlign': 'center'})
                        ])
                    ], style={'padding': '16px', 'backgroundColor': '#f8fafc', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
                ], id='attestation-progress-container'),
                
                # Attested confirmation message
                html.Div([
                    dbc.Alert([
                        icon("mdi:check-circle", width=20, color='#16a34a', style={'marginRight': '12px'}),
                        html.Span([
                            html.Strong("Review Complete!"),
                            " This contract review has been successfully attested. All term decisions have been recorded."
                        ], style={'color': '#15803d', 'fontSize': '14px'})
                    ], color="success")
                ], id='attested-confirmation', style={'marginTop': '24px', 'display': 'none'})
            ])
        ])
    ], style={'padding': '24px'})
