"""
Contract Detail View - Detailed compliance information for a single contract
Matches the React version exactly with all 40 compliance terms
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import json
from evidence_offcanvas import create_evidence_offcanvas

def icon(name, **kwargs):
    """Helper function to create DashIconify icons with CSS color styling"""
    color = kwargs.pop('color', None)
    if color:
        return html.Span(
            DashIconify(icon=name, **kwargs),
            style={'color': color}
        )
    return DashIconify(icon=name, **kwargs)

# Full compliance terms data (all 40 terms)
COMPLIANCE_TERMS = [
    {
        "id": "1",
        "heading": "Data Encryption Requirements",
        "description": "Contract must specify that all data in transit and at rest is encrypted using industry-standard encryption protocols.",
        "overallAnalysis": "The contract demonstrates comprehensive compliance with encryption requirements across all three critical dimensions: data in transit, data at rest, and key management. Section 4.2 mandates TLS 1.2+ with NIST-approved cipher suites, while Appendix B indicates implementation of the more secure TLS 1.3 protocol.",
        "subPoints": [
            {
                "heading": "Encryption in Transit",
                "description": "All data transmitted over networks must use TLS 1.2 or higher with strong cipher suites.",
                "met": True,
                "analysis": "The contract exceeds the minimum requirement by implementing TLS 1.3 while explicitly prohibiting deprecated protocols. Section 4.2 establishes the baseline requirement of TLS 1.2+ with NIST-approved cipher suites, while Appendix B confirms actual implementation of TLS 1.3. The explicit prohibition of SSL v2, v3, TLS 1.0, and TLS 1.1 demonstrates a proactive security posture that prevents downgrade attacks.",
                "evidence": [
                    {
                        "excerpt": "Section 4.2: All data transmissions between Client and Vendor systems shall utilize Transport Layer Security (TLS) version 1.2 or higher with approved cipher suites as defined by NIST Special Publication 800-52.",
                        "explanation": "This clause explicitly requires TLS 1.2 or higher and references NIST standards for cipher suite selection, ensuring strong encryption for data in transit and meeting the requirement for industry-standard protocols."
                    },
                    {
                        "excerpt": "Appendix B, Security Controls: Vendor's network architecture implements TLS 1.3 for all external communications and prohibits the use of deprecated protocols including SSL v2, SSL v3, TLS 1.0, and TLS 1.1.",
                        "explanation": "This supplementary provision demonstrates the vendor not only meets the minimum TLS 1.2 requirement but actually implements the more secure TLS 1.3 protocol, and explicitly prohibits weak legacy protocols, exceeding the baseline requirement."
                    }
                ]
            },
            {
                "heading": "Encryption at Rest",
                "description": "Stored data must be encrypted using AES-256 or equivalent encryption standards.",
                "met": True,
                "analysis": "Section 4.3 provides clear and unambiguous requirements for data-at-rest encryption. The specification of AES-256 meets current industry standards and regulatory expectations. The inclusion of 'or cryptographic algorithms of equivalent or greater strength' provides appropriate flexibility for future cryptographic advancements without requiring contract amendments, while maintaining the baseline security requirement.",
                "evidence": [
                    {
                        "excerpt": "Section 4.3: Vendor shall encrypt all Client data at rest using Advanced Encryption Standard (AES) with 256-bit keys or cryptographic algorithms of equivalent or greater strength.",
                        "explanation": "The contract specifically mandates AES-256 encryption for data at rest, which is the industry standard and meets the compliance requirement. The provision also allows for equivalent or stronger algorithms, providing flexibility for future standards."
                    }
                ]
            },
            {
                "heading": "Key Management",
                "description": "Encryption keys must be managed securely with proper rotation and access controls.",
                "met": True,
                "analysis": "Section 4.4 provides comprehensive key management controls that align with NIST SP 800-57 best practices. The requirement for HSM storage ensures keys are protected by hardware-based security controls that resist extraction attempts. The annual rotation schedule for production keys balances security (limiting key exposure window) with operational stability. Role-based access controls limiting key access to authorized cryptographic administrators implements the principle of least privilege.",
                "evidence": [
                    {
                        "excerpt": "Section 4.4: Encryption keys shall be managed in accordance with NIST SP 800-57 guidelines, including secure generation, storage in hardware security modules (HSMs), annual rotation for production keys, and role-based access controls limiting key access to authorized cryptographic administrators.",
                        "explanation": "This comprehensive clause addresses all aspects of key management including secure storage in HSMs, regular rotation schedules, and strict access controls. The reference to NIST SP 800-57 ensures industry best practices are followed."
                    }
                ]
            }
        ]
    },
    {
        "id": "2",
        "heading": "Third-Party Data Disclosure",
        "description": "Contract must explicitly state restrictions on sharing data with third parties.",
        "overallAnalysis": "The contract provides comprehensive coverage of third-party data disclosure requirements with strong protective measures. Section 6.1 establishes clear consent requirements, Section 6.2 ensures timely notification of compelled disclosures, and Sections 6.3-6.5 create robust flow-down provisions for subprocessors.",
        "subPoints": [
            {
                "heading": "Prior Written Consent",
                "description": "Third-party sharing requires explicit written approval from the data controller.",
                "met": True
            },
            {
                "heading": "Disclosure Notification",
                "description": "Any data disclosure to third parties must be reported within 24 hours.",
                "met": True
            },
            {
                "heading": "Third-Party Compliance",
                "description": "All third parties must adhere to the same data protection standards.",
                "met": True
            }
        ]
    },
    {
        "id": "3",
        "heading": "Data Breach Notification",
        "description": "Contract must include provisions for timely notification of data breaches.",
        "subPoints": [
            {
                "heading": "Notification Timeline",
                "description": "Data breaches must be reported within 72 hours of discovery.",
                "met": True
            },
            {
                "heading": "Breach Documentation",
                "description": "Detailed incident reports must include scope, impact, and remediation steps.",
                "met": True
            },
            {
                "heading": "Affected Party Notification",
                "description": "Process for notifying affected individuals must be clearly defined.",
                "met": True
            }
        ]
    },
    {
        "id": "4",
        "heading": "Data Retention and Deletion",
        "description": "Contract must specify clear data retention periods and secure deletion procedures.",
        "subPoints": [
            {"heading": "Retention Periods", "met": True},
            {"heading": "Secure Deletion Process", "met": False},
            {"heading": "Deletion Verification", "met": False}
        ]
    },
    {
        "id": "5",
        "heading": "Access Control and Authentication",
        "description": "Contract must require implementation of role-based access controls and multi-factor authentication.",
        "subPoints": [
            {"heading": "Role-Based Access Control", "met": True},
            {"heading": "Multi-Factor Authentication", "met": True},
            {"heading": "Access Review and Revocation", "met": True}
        ]
    },
    {
        "id": "6",
        "heading": "Audit Rights and Compliance Reporting",
        "description": "Contract must grant rights to conduct regular audits and require compliance reporting.",
        "subPoints": [
            {"heading": "Audit Frequency", "met": True},
            {"heading": "Compliance Documentation", "met": True},
            {"heading": "Remediation Timelines", "met": True}
        ]
    },
    {
        "id": "7",
        "heading": "Liability and Indemnification",
        "description": "Contract must clearly define liability limits and indemnification clauses.",
        "subPoints": [
            {"heading": "Liability Caps", "met": True},
            {"heading": "Indemnification Scope", "met": False},
            {"heading": "Insurance Requirements", "met": True}
        ]
    },
    {
        "id": "8",
        "heading": "Subprocessor Management",
        "description": "Contract must require notification and approval before engaging subprocessors.",
        "subPoints": [
            {"heading": "Subprocessor Approval", "met": True},
            {"heading": "Subprocessor List", "met": True},
            {"heading": "Subprocessor Compliance", "met": True}
        ]
    },
    {
        "id": "9",
        "heading": "Business Continuity and Disaster Recovery",
        "description": "Contract must include provisions for business continuity planning and disaster recovery.",
        "subPoints": [
            {"heading": "Recovery Time Objective", "met": True},
            {"heading": "Recovery Point Objective", "met": True},
            {"heading": "Disaster Recovery Testing", "met": True}
        ]
    },
    {
        "id": "10",
        "heading": "Termination and Data Portability",
        "description": "Contract must outline procedures for contract termination and data portability.",
        "subPoints": [
            {"heading": "Data Return Procedures", "met": True},
            {"heading": "Data Deletion Timeline", "met": True},
            {"heading": "Transition Assistance", "met": True}
        ]
    },
    # Terms 11-40
    {
        "id": "11",
        "heading": "Privacy Impact Assessment",
        "description": "Contract must require privacy impact assessments for new processing activities.",
        "subPoints": [
            {"heading": "Assessment Methodology", "description": "Privacy impact assessments must follow recognized frameworks like NIST or ISO.", "met": True},
            {"heading": "Documentation Requirements", "description": "Assessment results must be documented and shared with stakeholders.", "met": True},
            {"heading": "Remediation Plans", "description": "Identified risks must have documented remediation plans with timelines.", "met": False}
        ]
    },
    {
        "id": "12",
        "heading": "Vendor Security Training",
        "description": "Contract must mandate regular security awareness training for vendor personnel.",
        "subPoints": [
            {"heading": "Training Frequency", "description": "All personnel must complete security training at least annually.", "met": True},
            {"heading": "Training Content", "description": "Training must cover data protection, phishing, and incident response.", "met": True},
            {"heading": "Training Records", "description": "Vendor must maintain records of training completion for audit purposes.", "met": True}
        ]
    },
    {
        "id": "13",
        "heading": "Incident Response Procedures",
        "description": "Contract must define clear incident response and escalation procedures.",
        "subPoints": [
            {"heading": "Response Team", "description": "Dedicated incident response team with defined roles and responsibilities.", "met": True},
            {"heading": "Escalation Process", "description": "Clear escalation paths for different severity levels.", "met": True},
            {"heading": "Post-Incident Review", "description": "Mandatory post-incident reviews with lessons learned documentation.", "met": True}
        ]
    },
    {
        "id": "14",
        "heading": "Logging and Monitoring",
        "description": "Contract must require comprehensive logging and security monitoring capabilities.",
        "subPoints": [
            {"heading": "System Logging", "description": "All security-relevant events must be logged with timestamp and user information.", "met": True},
            {"heading": "Log Retention", "description": "Logs must be retained for at least 12 months for audit purposes.", "met": True},
            {"heading": "Security Monitoring", "description": "24/7 security monitoring with automated alerting for critical events.", "met": True}
        ]
    },
    {
        "id": "15",
        "heading": "Vulnerability Management",
        "description": "Contract must include comprehensive vulnerability management and patch procedures.",
        "subPoints": [
            {"heading": "Vulnerability Scanning", "description": "Regular automated scanning for vulnerabilities at least monthly.", "met": True},
            {"heading": "Patch Management", "description": "Critical patches must be applied within 30 days of release.", "met": True},
            {"heading": "Penetration Testing", "description": "Annual third-party penetration testing with findings remediation.", "met": True}
        ]
    },
    {
        "id": "16",
        "heading": "Change Management",
        "description": "Contract must require formal change management processes for system modifications.",
        "subPoints": [
            {"heading": "Change Approval Process", "description": "All changes must go through formal approval before implementation.", "met": True},
            {"heading": "Change Documentation", "description": "Complete documentation of changes including rationale and impact.", "met": True},
            {"heading": "Rollback Procedures", "description": "Tested rollback procedures must be in place for all changes.", "met": True}
        ]
    },
    {
        "id": "17",
        "heading": "Data Classification",
        "description": "Contract must define data classification scheme and handling requirements.",
        "subPoints": [
            {"heading": "Classification Scheme", "description": "Clear data classification levels (e.g., public, internal, confidential, restricted).", "met": True},
            {"heading": "Labeling Requirements", "description": "All data must be properly labeled according to classification.", "met": True},
            {"heading": "Handling Procedures", "description": "Specific handling procedures for each classification level.", "met": True}
        ]
    },
    {
        "id": "18",
        "heading": "Physical Security",
        "description": "Contract must address physical security controls for data center facilities.",
        "subPoints": [
            {"heading": "Access Controls", "description": "Badge-based access controls with logging and audit trails.", "met": True},
            {"heading": "Surveillance Systems", "description": "24/7 video surveillance with retention of footage for 90 days.", "met": True},
            {"heading": "Environmental Controls", "description": "Temperature, humidity, and fire suppression systems.", "met": True}
        ]
    },
    {
        "id": "19",
        "heading": "Network Security",
        "description": "Contract must specify network security controls and architecture requirements.",
        "subPoints": [
            {"heading": "Network Segmentation", "description": "Logical segmentation of networks by security zone and function.", "met": True},
            {"heading": "Firewall Configuration", "description": "Firewalls with deny-by-default rules and regular review.", "met": True},
            {"heading": "Intrusion Detection", "description": "IDS/IPS systems monitoring for malicious network activity.", "met": True}
        ]
    },
    {
        "id": "20",
        "heading": "Software Development Security",
        "description": "Contract must require secure software development lifecycle practices.",
        "subPoints": [
            {"heading": "Secure Coding Practices", "description": "Development teams must follow OWASP secure coding guidelines.", "met": True},
            {"heading": "Code Review", "description": "All code must undergo peer review before deployment.", "met": False},
            {"heading": "Security Testing", "description": "Static and dynamic security testing integrated into CI/CD pipeline.", "met": True}
        ]
    },
    {
        "id": "21",
        "heading": "Third-Party Software Components",
        "description": "Contract must address security of third-party and open-source software components.",
        "subPoints": [
            {"heading": "Vulnerability Tracking", "description": "Maintain inventory and track vulnerabilities in all third-party components.", "met": True},
            {"heading": "License Compliance", "description": "Ensure all software licenses are properly tracked and compliant.", "met": True},
            {"heading": "Update Management", "description": "Regular updates to third-party components to address security issues.", "met": False}
        ]
    },
    {
        "id": "22",
        "heading": "API Security Standards",
        "description": "Contract must specify security requirements for APIs and integrations.",
        "subPoints": [
            {"heading": "Authentication", "description": "APIs must use OAuth 2.0 or similar modern authentication standards.", "met": True},
            {"heading": "Rate Limiting", "description": "Rate limiting must be implemented to prevent abuse and DoS attacks.", "met": True},
            {"heading": "Input Validation", "description": "All API inputs must be validated and sanitized to prevent injection attacks.", "met": True}
        ]
    },
    {
        "id": "23",
        "heading": "Mobile Device Security",
        "description": "Contract must address security requirements for mobile device access.",
        "subPoints": [
            {"heading": "Device Management", "description": "Mobile devices must be enrolled in enterprise mobility management system.", "met": False},
            {"heading": "Device Encryption", "description": "Mobile devices accessing company data must have full-disk encryption enabled.", "met": True},
            {"heading": "Remote Wipe", "description": "Capability to remotely wipe data from lost or stolen devices.", "met": True}
        ]
    },
    {
        "id": "24",
        "heading": "Email Security Controls",
        "description": "Contract must define email security and anti-phishing requirements.",
        "subPoints": [
            {"heading": "SPF and DKIM", "description": "Email authentication using SPF, DKIM, and DMARC must be implemented.", "met": True},
            {"heading": "Anti-Phishing", "description": "Advanced anti-phishing and malware scanning must be deployed.", "met": True},
            {"heading": "Email Encryption", "description": "Sensitive emails must be encrypted in transit and support end-to-end encryption.", "met": False}
        ]
    },
    {
        "id": "25",
        "heading": "Password Policy Compliance",
        "description": "Contract must enforce strong password and credential management policies.",
        "subPoints": [
            {"heading": "Password Complexity", "description": "Passwords must meet minimum complexity requirements (12+ characters, mixed case).", "met": True},
            {"heading": "Password Rotation", "description": "Privileged account passwords must be rotated at least every 90 days.", "met": True},
            {"heading": "Password Storage", "description": "Passwords must be stored using approved hashing algorithms (bcrypt, Argon2).", "met": True}
        ]
    },
    {
        "id": "26",
        "heading": "Cloud Security Requirements",
        "description": "Contract must specify security requirements for cloud service usage.",
        "subPoints": [
            {"heading": "Cloud Provider Vetting", "description": "Cloud providers must meet SOC 2 Type II and ISO 27001 standards.", "met": True},
            {"heading": "Data Residency", "description": "Data must be stored in approved geographic regions with documented locations.", "met": False},
            {"heading": "Cloud Configuration", "description": "Cloud resources must follow security baseline configurations.", "met": True}
        ]
    },
    {
        "id": "27",
        "heading": "Endpoint Protection Standards",
        "description": "Contract must require endpoint detection and response capabilities.",
        "subPoints": [
            {"heading": "EDR Deployment", "description": "Endpoint detection and response tools must be deployed on all endpoints.", "met": True},
            {"heading": "Antivirus Coverage", "description": "Anti-malware protection must be maintained with daily signature updates.", "met": True},
            {"heading": "Host-Based Firewall", "description": "Host-based firewalls must be enabled on all workstations and servers.", "met": True}
        ]
    },
    {
        "id": "28",
        "heading": "Vendor Risk Assessment",
        "description": "Contract must require ongoing vendor risk assessments and reviews.",
        "subPoints": [
            {"heading": "Initial Assessment", "description": "Comprehensive security assessment must be completed before contract execution.", "met": True},
            {"heading": "Annual Reviews", "description": "Vendor security posture must be reassessed at least annually.", "met": True},
            {"heading": "Risk Scoring", "description": "Standardized risk scoring methodology must be used.", "met": True}
        ]
    },
    {
        "id": "29",
        "heading": "Data Privacy Rights",
        "description": "Contract must support data subject rights under privacy regulations.",
        "subPoints": [
            {"heading": "Access Rights", "description": "Individuals must be able to access their personal data upon request.", "met": True},
            {"heading": "Rectification Rights", "description": "Process for correcting inaccurate personal data must be defined.", "met": True},
            {"heading": "Erasure Rights", "description": "Right to deletion ('right to be forgotten') must be supported.", "met": True}
        ]
    },
    {
        "id": "30",
        "heading": "Cross-Border Data Transfer",
        "description": "Contract must address requirements for international data transfers.",
        "subPoints": [
            {"heading": "Transfer Mechanisms", "description": "Approved mechanisms for cross-border transfers must be specified.", "met": True},
            {"heading": "Adequacy Decisions", "description": "Transfers must comply with adequacy decisions where applicable.", "met": True},
            {"heading": "Standard Contractual Clauses", "description": "SCCs or binding corporate rules must be in place for EU transfers.", "met": True}
        ]
    },
    {
        "id": "31",
        "heading": "Data Protection Impact Assessment",
        "description": "Contract must require DPIAs for high-risk processing activities.",
        "subPoints": [
            {"heading": "DPIA Requirements", "description": "DPIAs must be conducted for processing likely to result in high risk.", "met": True},
            {"heading": "Risk Identification", "description": "Systematic identification of risks to data subjects' rights and freedoms.", "met": True},
            {"heading": "Mitigation Measures", "description": "Documented measures to address identified risks.", "met": True}
        ]
    },
    {
        "id": "32",
        "heading": "Consent Management",
        "description": "Contract must define processes for managing user consent.",
        "subPoints": [
            {"heading": "Consent Collection", "description": "Clear, affirmative consent must be obtained before processing.", "met": True},
            {"heading": "Consent Withdrawal", "description": "Easy mechanism for users to withdraw consent at any time.", "met": True},
            {"heading": "Consent Records", "description": "Records of consent must be maintained with timestamp and scope.", "met": True}
        ]
    },
    {
        "id": "33",
        "heading": "Data Minimization",
        "description": "Contract must enforce data minimization principles.",
        "subPoints": [
            {"heading": "Purpose Limitation", "description": "Data must be collected only for specified, legitimate purposes.", "met": True},
            {"heading": "Storage Limitation", "description": "Data must not be kept longer than necessary.", "met": True},
            {"heading": "Collection Limitation", "description": "Only minimum necessary data should be collected.", "met": True}
        ]
    },
    {
        "id": "34",
        "heading": "Backup and Recovery",
        "description": "Contract must include comprehensive backup and recovery procedures.",
        "subPoints": [
            {"heading": "Backup Frequency", "description": "Daily incremental and weekly full backups must be performed.", "met": True},
            {"heading": "Backup Testing", "description": "Quarterly testing of backup restoration procedures.", "met": True},
            {"heading": "Recovery Procedures", "description": "Documented and tested recovery procedures for all systems.", "met": True}
        ]
    },
    {
        "id": "35",
        "heading": "Social Engineering Defense",
        "description": "Contract must require defenses against social engineering attacks.",
        "subPoints": [
            {"heading": "Security Awareness", "description": "Regular security awareness training covering social engineering tactics.", "met": True},
            {"heading": "Simulated Phishing", "description": "Quarterly simulated phishing campaigns must be conducted.", "met": True},
            {"heading": "Reporting Mechanisms", "description": "Easy-to-use mechanisms for reporting suspected social engineering attempts.", "met": True}
        ]
    },
    {
        "id": "36",
        "heading": "Intellectual Property Protection",
        "description": "Contract must define protections for intellectual property and trade secrets.",
        "subPoints": [
            {"heading": "IP Ownership", "description": "Clear ownership of intellectual property created under the contract.", "met": True},
            {"heading": "Confidentiality Obligations", "description": "Strong confidentiality clauses protecting proprietary information.", "met": True},
            {"heading": "Non-Compete Provisions", "description": "Appropriate non-compete and non-solicitation provisions where applicable.", "met": False}
        ]
    },
    {
        "id": "37",
        "heading": "Regulatory Compliance Reporting",
        "description": "Contract must require compliance with applicable regulations and reporting.",
        "subPoints": [
            {"heading": "Compliance Certifications", "description": "Current certifications for applicable regulations must be maintained.", "met": True},
            {"heading": "Regulatory Changes", "description": "Vendor must notify of changes in compliance status or regulatory environment.", "met": True},
            {"heading": "Compliance Documentation", "description": "Evidence of compliance must be provided upon request.", "met": True}
        ]
    },
    {
        "id": "38",
        "heading": "Supply Chain Security",
        "description": "Contract must address security of the software and hardware supply chain.",
        "subPoints": [
            {"heading": "Vendor Vetting", "description": "Sub-vendors and suppliers must undergo security assessments.", "met": False},
            {"heading": "Software Bill of Materials", "description": "SBOM must be provided for all software components.", "met": False},
            {"heading": "Hardware Integrity", "description": "Hardware must be sourced from trusted suppliers with chain of custody.", "met": True}
        ]
    },
    {
        "id": "39",
        "heading": "Zero Trust Architecture",
        "description": "Contract must support zero trust security principles and implementation.",
        "subPoints": [
            {"heading": "Identity Verification", "description": "Continuous verification of user and device identity before granting access.", "met": True},
            {"heading": "Least Privilege Access", "description": "Access must be granted based on least privilege and need-to-know principles.", "met": True},
            {"heading": "Micro-Segmentation", "description": "Network micro-segmentation to limit lateral movement.", "met": False}
        ]
    },
    {
        "id": "40",
        "heading": "Decommissioning and Asset Disposal",
        "description": "Contract must define secure procedures for decommissioning and asset disposal.",
        "subPoints": [
            {"heading": "Data Sanitization", "description": "Media must be sanitized using NIST 800-88 guidelines before disposal.", "met": True},
            {"heading": "Certificate of Destruction", "description": "Certificates of destruction must be provided for all disposed assets.", "met": True},
            {"heading": "Asset Tracking", "description": "Complete inventory and tracking of assets through end-of-life.", "met": True}
        ]
    }
]

def get_term_status(term):
    """Determine if term is met, partially-met, or missing"""
    met_count = sum(1 for sp in term['subPoints'] if sp['met'])
    total = len(term['subPoints'])
    
    if met_count == total:
        return "met"
    elif met_count == 0:
        return "missing"
    else:
        return "partially-met"

def get_status_badge(status):
    """Get colored badge for status"""
    if status == "met":
        return html.Span("Met", style={
            'padding': '2px 8px',
            'borderRadius': '9999px',
            'fontSize': '12px',
            'fontWeight': 500,
            'backgroundColor': '#dcfce7',
            'color': '#166534',
            'border': '1px solid #bbf7d0'
        })
    elif status == "partially-met":
        return html.Span("Partially Met", style={
            'padding': '2px 8px',
            'borderRadius': '9999px',
            'fontSize': '12px',
            'fontWeight': 500,
            'backgroundColor': '#fef3c7',
            'color': '#92400e',
            'border': '1px solid #fde68a'
        })
    else:
        return html.Span("Missing", style={
            'padding': '2px 8px',
            'borderRadius': '9999px',
            'fontSize': '12px',
            'fontWeight': 500,
            'backgroundColor': '#fee2e2',
            'color': '#991b1b',
            'border': '1px solid #fecaca'
        })

def get_status_icon(status):
    """Get icon for term status"""
    if status == "met":
        return html.Div(
            icon("mdi:check-circle", width=16, color='#16a34a'),
            style={
                'width': '24px',
                'height': '24px',
                'borderRadius': '9999px',
                'backgroundColor': '#dcfce7',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center'
            }
        )
    elif status == "partially-met":
        return html.Div(
            icon("mdi:alert-circle", width=16, color='#d97706'),
            style={
                'width': '24px',
                'height': '24px',
                'borderRadius': '9999px',
                'backgroundColor': '#fef3c7',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center'
            }
        )
    else:
        return html.Div(
            icon("mdi:close-circle", width=16, color='#dc2626'),
            style={
                'width': '24px',
                'height': '24px',
                'borderRadius': '9999px',
                'backgroundColor': '#fee2e2',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center'
            }
        )

def get_contract_detail_layout(contract):
    """Get the contract detail view layout matching React version"""
    
    if not contract:
        return html.Div("No contract selected")
    
    # Calculate metrics
    total_terms = len(COMPLIANCE_TERMS)
    met_terms = sum(1 for term in COMPLIANCE_TERMS if get_term_status(term) == "met")
    partial_terms = sum(1 for term in COMPLIANCE_TERMS if get_term_status(term) == "partially-met")
    missing_terms = sum(1 for term in COMPLIANCE_TERMS if get_term_status(term) == "missing")
    
    total_points = sum(len(term['subPoints']) for term in COMPLIANCE_TERMS)
    met_points = sum(sum(1 for sp in term['subPoints'] if sp['met']) for term in COMPLIANCE_TERMS)
    
    terms_percent = round((met_terms / total_terms) * 100)
    points_percent = round((met_points / total_points) * 100)
    
    # Status color helper
    def get_status_color(status):
        colors = {
            'compliant': {'bg': '#dcfce7', 'text': '#166534', 'border': '#bbf7d0'},
            'needs-review': {'bg': '#fef3c7', 'text': '#92400e', 'border': '#fde68a'},
            'non-compliant': {'bg': '#fee2e2', 'text': '#991b1b', 'border': '#fecaca'}
        }
        return colors.get(status, colors['compliant'])
    
    def get_risk_color(risk):
        colors = {
            'low': {'bg': '#dcfce7', 'text': '#166534', 'border': '#bbf7d0'},
            'medium': {'bg': '#fef3c7', 'text': '#92400e', 'border': '#fde68a'},
            'high': {'bg': '#fee2e2', 'text': '#991b1b', 'border': '#fecaca'}
        }
        return colors.get(risk, colors['low'])
    
    status_color = get_status_color(contract['status'])
    risk_color = get_risk_color(contract['riskLevel'])
    
    # Helper function to calculate historical adherence
    def get_historical_adherence(term_heading):
        """Generate consistent but varied adherence rate based on term heading"""
        hash_val = sum(ord(c) for c in term_heading)
        return 60 + (hash_val % 36)
    
    # Build custom accordion items for all 40 terms using Collapse components
    accordion_items = []
    for term in COMPLIANCE_TERMS:
        status = get_term_status(term)
        met_subpoints = sum(1 for sp in term['subPoints'] if sp['met'])
        total_subpoints = len(term['subPoints'])
        score = round((met_subpoints / total_subpoints) * 100)
        historical_rate = get_historical_adherence(term['heading'])
        
        # Build subpoint cards with improved layout
        subpoint_cards = []
        for idx, sp in enumerate(term['subPoints']):
            subpoint_cards.append(
                html.Div([
                    # Subpoint card with improved styling
                    html.Div([
                        # Main content area
                        html.Div([
                            # Icon
                            html.Div(
                                icon("mdi:check-circle" if sp['met'] else "mdi:close-circle",
                                     width=20,
                                     color='#16a34a' if sp['met'] else '#dc2626'),
                                style={'flexShrink': 0, 'marginTop': '2px'}
                            ),
                            # Content
                            html.Div([
                                # Header row with title and badge
                                html.Div([
                                    html.Div([
                                        html.H5(sp['heading'], style={'fontSize': '14px', 'color': '#0f172a', 'margin': '0 0 4px 0', 'fontWeight': 500}),
                                        html.P(sp.get('description', ''), style={'fontSize': '12px', 'color': '#64748b', 'margin': 0, 'lineHeight': '1.5'})
                                    ], style={'flex': 1, 'minWidth': 0}),
                                    html.Div([
                                        html.Span(
                                            "Met" if sp['met'] else "Not Met",
                                            style={
                                                'padding': '2px 8px',
                                                'borderRadius': '9999px',
                                                'fontSize': '11px',
                                                'fontWeight': 500,
                                                'flexShrink': 0,
                                                'backgroundColor': '#dcfce7' if sp['met'] else '#fee2e2',
                                                'color': '#166534' if sp['met'] else '#991b1b',
                                                'border': f"1px solid {'#86efac' if sp['met'] else '#fca5a5'}"
                                            }
                                        )
                                    ], style={'display': 'flex', 'alignItems': 'center', 'gap': '8px', 'flexShrink': 0})
                                ], style={'display': 'flex', 'alignItems': 'start', 'justifyContent': 'space-between', 'gap': '12px', 'marginBottom': '8px'}),
                                
                                # Evidence and Analysis Links Row
                                html.Div([
                                    dbc.Button([
                                        icon("mdi:open-in-new", width=14, style={'marginRight': '4px'}),
                                        html.Span(f"View Evidence ({len(sp.get('evidence', []))})", style={'fontSize': '12px'})
                                    ], 
                                        id={'type': 'view-evidence-btn', 'term_id': term['id'], 'subpoint_idx': idx},
                                        color='link',
                                        size='sm',
                                        style={'display': 'inline-flex', 'alignItems': 'center', 'color': '#2563eb', 'textDecoration': 'none', 'padding': '0', 'border': 'none', 'backgroundColor': 'transparent'}
                                    ) if sp.get('evidence') and len(sp.get('evidence', [])) > 0 else None,
                                    dbc.Button([
                                        icon("mdi:file-document-outline", width=14, style={'marginRight': '4px'}),
                                        html.Span("View Analysis", style={'fontSize': '12px'})
                                    ], 
                                        id={'type': 'toggle-analysis-btn', 'term_id': term['id'], 'subpoint_idx': idx},
                                        color='link',
                                        size='sm',
                                        style={'display': 'inline-flex', 'alignItems': 'center', 'color': '#6366f1', 'textDecoration': 'none', 'padding': '0', 'border': 'none', 'backgroundColor': 'transparent'}
                                    ) if sp.get('analysis') else None
                                ], style={
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'gap': '16px',
                                    'paddingTop': '12px',
                                    'paddingBottom': '12px',
                                    'borderBottom': '1px solid #e2e8f0'
                                }) if (sp.get('evidence') and len(sp.get('evidence', [])) > 0) or sp.get('analysis') else None,
                                
                                # Attestation Controls Section
                                html.Div([
                                    # Initial state: Approve and Override buttons
                                    html.Div([
                                        dbc.Button([
                                            icon("mdi:thumb-up", width=14, style={'marginRight': '4px'}),
                                            "Approve"
                                        ], 
                                            id={'type': 'approve-btn', 'term_id': term['id'], 'subpoint_idx': idx},
                                            outline=True,
                                            size='sm',
                                            style={
                                                'display': 'inline-flex',
                                                'alignItems': 'center',
                                                'gap': '4px',
                                                'color': '#15803d',
                                                'borderColor': '#86efac',
                                                'backgroundColor': 'white',
                                                'fontSize': '12px',
                                                'padding': '4px 12px'
                                            }
                                        ),
                                        dbc.Button([
                                            icon("mdi:pencil", width=14, style={'marginRight': '4px'}),
                                            "Override"
                                        ], 
                                            id={'type': 'override-btn', 'term_id': term['id'], 'subpoint_idx': idx},
                                            outline=True,
                                            size='sm',
                                            style={
                                                'display': 'inline-flex',
                                                'alignItems': 'center',
                                                'gap': '4px',
                                                'color': '#b45309',
                                                'borderColor': '#fcd34d',
                                                'backgroundColor': 'white',
                                                'fontSize': '12px',
                                                'padding': '4px 12px',
                                                'marginLeft': '8px'
                                            }
                                        )
                                    ], id={'type': 'attestation-initial', 'term_id': term['id'], 'subpoint_idx': idx}, style={'display': 'flex', 'alignItems': 'center', 'gap': '8px'}),
                                    
                                    # Approved state
                                    html.Div([
                                        html.Div([
                                            icon("mdi:check-circle", width=16, color='#15803d', style={'marginRight': '8px'}),
                                            html.Span("Approved", style={'fontSize': '14px', 'color': '#15803d'})
                                        ], style={'display': 'flex', 'alignItems': 'center', 'flex': 1}),
                                        dbc.Button("Change", 
                                            id={'type': 'change-approval-btn', 'term_id': term['id'], 'subpoint_idx': idx},
                                            size='sm',
                                            color='link',
                                            style={'fontSize': '12px', 'color': '#64748b', 'padding': '4px 8px'}
                                        )
                                    ], id={'type': 'attestation-approved', 'term_id': term['id'], 'subpoint_idx': idx}, 
                                       style={'display': 'none', 'alignItems': 'center', 'justifyContent': 'space-between', 'padding': '8px 12px', 'backgroundColor': '#dcfce7', 'borderRadius': '6px', 'border': '1px solid #bbf7d0'}),
                                    
                                    # Overridden state
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                icon("mdi:pencil", width=16, color='#b45309', style={'marginRight': '8px'}),
                                                html.Span(id={'type': 'override-status-text', 'term_id': term['id'], 'subpoint_idx': idx}, 
                                                         children="Overridden", style={'fontSize': '14px', 'color': '#b45309'})
                                            ], style={'display': 'flex', 'alignItems': 'center', 'flex': 1}),
                                            dbc.Button("Edit", 
                                                id={'type': 'edit-override-btn', 'term_id': term['id'], 'subpoint_idx': idx},
                                                size='sm',
                                                color='link',
                                                style={'fontSize': '12px', 'color': '#64748b', 'padding': '4px 8px'}
                                            )
                                        ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'marginBottom': '8px'}),
                                        html.Div(id={'type': 'override-reason-display', 'term_id': term['id'], 'subpoint_idx': idx},
                                                children="",
                                                style={'fontSize': '12px', 'color': '#78350f', 'backgroundColor': 'white', 'padding': '8px', 'borderRadius': '4px', 'border': '1px solid #fde68a'})
                                    ], id={'type': 'attestation-overridden', 'term_id': term['id'], 'subpoint_idx': idx}, 
                                       style={'display': 'none', 'padding': '8px 12px', 'backgroundColor': '#fef3c7', 'borderRadius': '6px', 'border': '1px solid #fde68a'}),
                                    
                                    # Editing/Override form
                                    html.Div([
                                        html.Div([
                                            html.Label("Override Result", style={'fontSize': '14px', 'color': '#334155', 'marginBottom': '8px', 'display': 'block'}),
                                            html.Div([
                                                html.Span(id={'type': 'override-switch-label', 'term_id': term['id'], 'subpoint_idx': idx},
                                                         children="Met" if sp['met'] else "Not Met",
                                                         style={'fontSize': '12px', 'fontWeight': 500, 'marginRight': '8px'}),
                                                dbc.Switch(
                                                    id={'type': 'override-switch', 'term_id': term['id'], 'subpoint_idx': idx},
                                                    value=sp['met']
                                                )
                                            ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'flex-end', 'marginBottom': '12px'})
                                        ]),
                                        html.Div([
                                            html.Label([
                                                "Reason ",
                                                html.Span("*", style={'color': '#dc2626'}),
                                                html.Span(" (Optional)", id={'type': 'reason-optional-label', 'term_id': term['id'], 'subpoint_idx': idx}, 
                                                         style={'color': '#64748b'})
                                            ], style={'fontSize': '14px', 'color': '#334155', 'marginBottom': '6px', 'display': 'block'}),
                                            dbc.Textarea(
                                                id={'type': 'override-reason-input', 'term_id': term['id'], 'subpoint_idx': idx},
                                                placeholder="Explain why you are overriding this result...",
                                                style={'fontSize': '14px', 'minHeight': '80px', 'backgroundColor': 'white'}
                                            )
                                        ], style={'marginBottom': '12px'}),
                                        html.Div([
                                            dbc.Button([
                                                icon("mdi:content-save", width=14, style={'marginRight': '6px'}),
                                                "Save Override"
                                            ],
                                                id={'type': 'save-override-btn', 'term_id': term['id'], 'subpoint_idx': idx},
                                                color='success',
                                                size='sm',
                                                style={'marginRight': '8px'}
                                            ),
                                            dbc.Button([
                                                icon("mdi:close", width=14, style={'marginRight': '6px'}),
                                                "Cancel"
                                            ],
                                                id={'type': 'cancel-override-btn', 'term_id': term['id'], 'subpoint_idx': idx},
                                                outline=True,
                                                size='sm'
                                            )
                                        ], style={'display': 'flex', 'alignItems': 'center'})
                                    ], id={'type': 'attestation-editing', 'term_id': term['id'], 'subpoint_idx': idx},
                                       style={'display': 'none', 'padding': '16px', 'background': 'linear-gradient(to bottom right, #fef3c7, #fed7aa)', 'borderRadius': '8px', 'border': '2px solid #fcd34d'})
                                ], style={'marginTop': '12px'}),
                                
                                # Analysis collapse section (shown when "View Analysis" is clicked)
                                dbc.Collapse([
                                    html.Div([
                                        html.Div([
                                            html.Div(style={
                                                'width': '4px',
                                                'height': '16px',
                                                'backgroundColor': '#6366f1',
                                                'borderRadius': '9999px'
                                            }),
                                            html.H6("POINT ANALYSIS", style={
                                                'fontSize': '10px',
                                                'color': '#4f46e5',
                                                'textTransform': 'uppercase',
                                                'letterSpacing': '0.05em',
                                                'margin': 0
                                            })
                                        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '8px', 'marginBottom': '8px'}),
                                        html.P(sp.get('analysis', ''), style={
                                            'fontSize': '14px',
                                            'color': '#1e293b',
                                            'lineHeight': '1.6',
                                            'margin': 0
                                        })
                                    ], style={
                                        'backgroundColor': '#eef2ff',
                                        'padding': '16px',
                                        'borderRadius': '8px',
                                        'border': '1px solid #c7d2fe',
                                        'marginTop': '12px'
                                    })
                                ], id={'type': 'analysis-collapse', 'term_id': term['id'], 'subpoint_idx': idx}, is_open=False) if sp.get('analysis') else None
                            ], style={'flex': 1, 'minWidth': 0})
                        ], style={'display': 'flex', 'alignItems': 'start', 'gap': '12px', 'padding': '16px'})
                    ], style={
                        'borderRadius': '8px',
                        'border': '1px solid #e2e8f0',
                        'backgroundColor': 'white',
                        'marginBottom': '12px' if idx < len(term['subPoints']) - 1 else '0'
                    })
                ])
            )
        
        # Create custom accordion item using Button + Collapse
        accordion_items.append(
            html.Div([
                # Accordion header button (collapsed state)
                dbc.Button([
                    # Left side: icon + content
                    html.Div([
                        get_status_icon(status),
                        html.Div([
                            # Title row with badges
                            html.Div([
                                html.H4(term['heading'], style={'fontSize': '15px', 'color': '#0f172a', 'margin': 0, 'fontWeight': 500}),
                                html.Span(f"{met_subpoints}/{total_subpoints} points",
                                         style={'fontSize': '13px', 'color': '#64748b', 'marginLeft': '12px'}),
                                html.Span(
                                    f"{historical_rate}% historical adherence",
                                    style={
                                        'fontSize': '11px',
                                        'padding': '2px 8px',
                                        'borderRadius': '9999px',
                                        'backgroundColor': '#dbeafe',
                                        'color': '#1e40af',
                                        'border': '1px solid #bfdbfe',
                                        'marginLeft': '8px',
                                        'whiteSpace': 'nowrap'
                                    }
                                )
                            ], style={'display': 'flex', 'alignItems': 'center', 'flexWrap': 'wrap', 'gap': '4px', 'marginBottom': '4px'}),
                            # Description
                            html.P(term.get('description', ''),
                                   style={'fontSize': '13px', 'color': '#64748b', 'margin': 0, 'textAlign': 'left'})
                        ], style={'marginLeft': '12px', 'flex': 1, 'textAlign': 'left'})
                    ], style={'display': 'flex', 'alignItems': 'start', 'flex': 1}),
                    
                    # Right side: percentage + badge + chevron
                    html.Div([
                        html.Span(f"{score}%", style={
                            'fontSize': '14px',
                            'color': '#16a34a' if score == 100 else '#eab308' if score > 0 else '#dc2626',
                            'fontWeight': 500,
                            'marginRight': '12px'
                        }),
                        get_status_badge(status),
                        html.Div(icon("mdi:chevron-down", width=20, color='#64748b'), style={'marginLeft': '8px'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'flexShrink': 0})
                ],
                    id={'type': 'accordion-btn', 'index': term['id']},
                    color="light",
                    className="w-100 text-start",
                    style={
                        'display': 'flex',
                        'justifyContent': 'space-between',
                        'alignItems': 'start',
                        'padding': '16px',
                        'marginBottom': '8px',
                        'border': '1px solid #e2e8f0',
                        'borderRadius': '8px',
                        'backgroundColor': 'white'
                    }
                ),
                
                # Accordion content (expanded state)
                dbc.Collapse([
                    html.Div([
                        # Overall Analysis (if exists)
                        html.Div([
                            dbc.Button([
                                html.Div([
                                    html.Div(style={'width': '4px', 'height': '16px', 'backgroundColor': '#6366f1', 'borderRadius': '9999px', 'marginRight': '8px'}),
                                    html.Span("Overall Analysis", style={'fontSize': '14px', 'color': '#0f172a'})
                                ], style={'display': 'flex', 'alignItems': 'center'}),
                                icon("mdi:chevron-down", width=16, color='#64748b')
                            ],
                                id={'type': 'overall-analysis-btn', 'index': term['id']},
                                color="light",
                                outline=True,
                                className="w-100",
                                style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '12px'}
                            ),
                            dbc.Collapse([
                                html.Div([
                                    html.P(term.get('overallAnalysis', ''),
                                           style={'fontSize': '14px', 'color': '#1e293b', 'lineHeight': '1.6', 'margin': 0})
                                ], style={'backgroundColor': '#eef2ff', 'padding': '16px', 'borderRadius': '8px', 'border': '1px solid #c7d2fe', 'marginBottom': '16px'})
                            ], id={'type': 'overall-analysis-collapse', 'index': term['id']}, is_open=False)
                        ], style={'marginBottom': '16px'}) if term.get('overallAnalysis') else html.Div(),
                        
                        # Subpoints
                        html.Div(subpoint_cards)
                    ], style={'padding': '0 16px 16px 56px'})
                ], id={'type': 'accordion-collapse', 'index': term['id']}, is_open=False, style={'marginBottom': '8px'})
            ], style={'marginBottom': '8px'})
        )
    
    return html.Div([
        # Header with back button
        html.Div([
            dbc.Button([
                icon("mdi:arrow-left", width=16, style={'marginRight': '8px'}),
                "Back to Reviews"
            ], id='back-to-reviews-nav-btn', color="link", size="sm",
               style={'padding': '8px 16px', 'marginBottom': '16px', 'fontSize': '14px'}),
            
            html.Div([
                html.Div([
                    html.H2(contract['name'], style={'color': '#0f172a', 'margin': 0}),
                    html.P(f"Reviewed on {contract['reviewDate']} by {contract['reviewer']}",
                           style={'fontSize': '14px', 'color': '#64748b', 'margin': '4px 0 0 0'})
                ]),
                dbc.Button([
                    icon("mdi:download", width=16, style={'marginRight': '8px'}),
                    "Export Report"
                ], color="primary", outline=True, size="sm")
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'start', 'marginBottom': '24px'})
        ]),
        
        # Contract overview card
        dbc.Card([
            dbc.CardHeader([
                html.Div([
                    html.Div([
                        html.Div(icon("mdi:file-document", width=20, color='#2563eb'), style={'marginRight': '8px'}),
                        html.H5(contract['name'], style={'margin': 0})
                    ], style={'display': 'flex', 'alignItems': 'center'}),
                    html.Div([
                        html.Span(
                            contract['status'].replace('-', ' ').title(),
                            style={
                                'padding': '4px 12px',
                                'borderRadius': '9999px',
                                'fontSize': '12px',
                                'fontWeight': 500,
                                'backgroundColor': status_color['bg'],
                                'color': status_color['text'],
                                'border': f"1px solid {status_color['border']}",
                                'marginRight': '8px'
                            }
                        ),
                        html.Span(
                            f"{contract['riskLevel'].title()} Risk",
                            style={
                                'padding': '4px 12px',
                                'borderRadius': '9999px',
                                'fontSize': '12px',
                                'fontWeight': 500,
                                'backgroundColor': risk_color['bg'],
                                'color': risk_color['text'],
                                'border': f"1px solid {risk_color['border']}"
                            }
                        )
                    ], style={'display': 'flex'})
                ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'})
            ]),
            dbc.CardBody([
                # Metadata grid (5 columns only - removed matching rates)
                dbc.Row([
                    dbc.Col([
                        html.P("Vendor", style={'fontSize': '12px', 'color': '#64748b', 'margin': '0 0 4px 0'}),
                        html.P(contract['vendor'], style={'fontSize': '14px', 'color': '#0f172a', 'margin': 0, 'fontWeight': 500})
                    ], md=2),
                    dbc.Col([
                        html.P("Review Date", style={'fontSize': '12px', 'color': '#64748b', 'margin': '0 0 4px 0'}),
                        html.P(contract['reviewDate'], style={'fontSize': '14px', 'color': '#0f172a', 'margin': 0})
                    ], md=2),
                    dbc.Col([
                        html.P("Reviewer", style={'fontSize': '12px', 'color': '#64748b', 'margin': '0 0 4px 0'}),
                        html.P(contract['reviewer'], style={'fontSize': '14px', 'color': '#0f172a', 'margin': 0})
                    ], md=3),
                    dbc.Col([
                        html.P("Jira Engagement ID", style={'fontSize': '12px', 'color': '#64748b', 'margin': '0 0 4px 0'}),
                        html.A([
                            html.Span(contract['jiraEngagementId'].split('/')[-1], style={'marginRight': '4px'}),
                            icon("mdi:open-in-new", width=12)
                        ],
                            href=contract['jiraEngagementId'],
                            target='_blank',
                            style={'fontSize': '14px', 'color': '#2563eb', 'textDecoration': 'none', 'display': 'inline-flex', 'alignItems': 'center'}
                        )
                    ], md=3),
                    dbc.Col([
                        html.P("Athena ID", style={'fontSize': '12px', 'color': '#64748b', 'margin': '0 0 4px 0'}),
                        html.A([
                            html.Span(contract.get('athenaId', 'https://athena.example.com/id/ATH-2024-001').split('/')[-1], style={'marginRight': '4px'}),
                            icon("mdi:open-in-new", width=12)
                        ],
                            href=contract.get('athenaId', 'https://athena.example.com/id/ATH-2024-001'),
                            target='_blank',
                            style={'fontSize': '14px', 'color': '#2563eb', 'textDecoration': 'none', 'display': 'inline-flex', 'alignItems': 'center'}
                        )
                    ], md=2)
                ], style={'marginBottom': '24px'}),
                
                # Compliance score cards
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.P("Overall Term Status", style={'fontSize': '14px', 'color': '#64748b', 'margin': '0 0 12px 0'}),
                            html.Div([
                                html.Span(f"{terms_percent}%", style={'fontSize': '32px', 'color': '#0f172a', 'fontWeight': 500, 'marginRight': '8px'}),
                                html.Span(f"{met_terms} of {total_terms} terms fully met", style={'fontSize': '14px', 'color': '#64748b'})
                            ], style={'display': 'flex', 'alignItems': 'baseline', 'marginBottom': '12px'}),
                            dbc.Progress(value=terms_percent, style={'height': '8px'}, color="primary")
                        ], style={
                            'padding': '16px',
                            'background': 'linear-gradient(to bottom right, #eff6ff, #eef2ff)',
                            'borderRadius': '8px',
                            'border': '1px solid #bfdbfe'
                        })
                    ], md=6),
                    dbc.Col([
                        html.Div([
                            html.P("Individual Points", style={'fontSize': '14px', 'color': '#64748b', 'margin': '0 0 12px 0'}),
                            html.Div([
                                html.Span(f"{points_percent}%", style={'fontSize': '32px', 'color': '#0f172a', 'fontWeight': 500, 'marginRight': '8px'}),
                                html.Span(f"{met_points} of {total_points} points met", style={'fontSize': '14px', 'color': '#64748b'})
                            ], style={'display': 'flex', 'alignItems': 'baseline', 'marginBottom': '12px'}),
                            dbc.Progress(value=points_percent, style={'height': '8px'}, color="success")
                        ], style={
                            'padding': '16px',
                            'background': 'linear-gradient(to bottom right, #faf5ff, #fce7f3)',
                            'borderRadius': '8px',
                            'border': '1px solid #e9d5ff'
                        })
                    ], md=6)
                ], style={'marginBottom': '24px'}),
                
                # Term status breakdown - Collapsible sections
                html.Div([
                    html.H5("Term Status Breakdown", style={'fontSize': '14px', 'color': '#0f172a', 'margin': '0 0 12px 0', 'fontWeight': 500}),
                    dbc.Row([
                        # Met Terms - Collapsible
                        dbc.Col([
                            html.Div([
                                dbc.Button([
                                    html.Div([
                                        html.Div(style={'width': '12px', 'height': '12px', 'borderRadius': '9999px', 'backgroundColor': '#16a34a', 'marginRight': '8px'}),
                                        html.Span("Met", style={'fontSize': '14px', 'color': '#0f172a'}),
                                    ], style={'display': 'flex', 'alignItems': 'center'}),
                                    html.Div([
                                        html.Span(str(met_terms), style={
                                            'fontSize': '14px',
                                            'fontWeight': 500,
                                            'padding': '2px 8px',
                                            'borderRadius': '9999px',
                                            'backgroundColor': '#dcfce7',
                                            'color': '#166534',
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
                                dbc.Collapse([
                                    html.Div([
                                        html.Ul([
                                            html.Li([
                                                html.Span("✓", style={'color': '#16a34a', 'marginRight': '8px', 'fontSize': '14px'}),
                                                html.Span(term['heading'], style={'fontSize': '13px', 'color': '#334155'})
                                            ], style={'marginBottom': '8px', 'display': 'flex', 'alignItems': 'start'})
                                            for term in COMPLIANCE_TERMS if get_term_status(term) == "met"
                                        ] if met_terms > 0 else [
                                            html.Li("None", style={'fontSize': '13px', 'color': '#94a3b8', 'fontStyle': 'italic'})
                                        ], style={'listStyle': 'none', 'padding': 0, 'margin': 0})
                                    ], className='term-list-container', style={'border': '1px solid #e2e8f0', 'borderRadius': '6px', 'padding': '12px', 'backgroundColor': '#f8fafc', 'maxHeight': '240px', 'overflowY': 'auto', 'marginTop': '8px'})
                                ], id='collapse-met', is_open=False)
                            ])
                        ], md=4),
                        
                        # Partially Met Terms - Collapsible
                        dbc.Col([
                            html.Div([
                                dbc.Button([
                                    html.Div([
                                        html.Div(style={'width': '12px', 'height': '12px', 'borderRadius': '9999px', 'backgroundColor': '#eab308', 'marginRight': '8px'}),
                                        html.Span("Partially Met", style={'fontSize': '14px', 'color': '#0f172a'}),
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
                                dbc.Collapse([
                                    html.Div([
                                        html.Ul([
                                            html.Li([
                                                html.Span("◐", style={'color': '#eab308', 'marginRight': '8px', 'fontSize': '14px'}),
                                                html.Span(term['heading'], style={'fontSize': '13px', 'color': '#334155'})
                                            ], style={'marginBottom': '8px', 'display': 'flex', 'alignItems': 'start'})
                                            for term in COMPLIANCE_TERMS if get_term_status(term) == "partially-met"
                                        ] if partial_terms > 0 else [
                                            html.Li("None", style={'fontSize': '13px', 'color': '#94a3b8', 'fontStyle': 'italic'})
                                        ], style={'listStyle': 'none', 'padding': 0, 'margin': 0})
                                    ], className='term-list-container', style={'border': '1px solid #e2e8f0', 'borderRadius': '6px', 'padding': '12px', 'backgroundColor': '#f8fafc', 'maxHeight': '240px', 'overflowY': 'auto', 'marginTop': '8px'})
                                ], id='collapse-partial', is_open=False)
                            ])
                        ], md=4),
                        
                        # Missing Terms - Collapsible
                        dbc.Col([
                            html.Div([
                                dbc.Button([
                                    html.Div([
                                        html.Div(style={'width': '12px', 'height': '12px', 'borderRadius': '9999px', 'backgroundColor': '#dc2626', 'marginRight': '8px'}),
                                        html.Span("Missing", style={'fontSize': '14px', 'color': '#0f172a'}),
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
                                dbc.Collapse([
                                    html.Div([
                                        html.Ul([
                                            html.Li([
                                                html.Span("✗", style={'color': '#dc2626', 'marginRight': '8px', 'fontSize': '14px'}),
                                                html.Span(term['heading'], style={'fontSize': '13px', 'color': '#334155'})
                                            ], style={'marginBottom': '8px', 'display': 'flex', 'alignItems': 'start'})
                                            for term in COMPLIANCE_TERMS if get_term_status(term) == "missing"
                                        ] if missing_terms > 0 else [
                                            html.Li("None", style={'fontSize': '13px', 'color': '#94a3b8', 'fontStyle': 'italic'})
                                        ], style={'listStyle': 'none', 'padding': 0, 'margin': 0})
                                    ], className='term-list-container', style={'border': '1px solid #e2e8f0', 'borderRadius': '6px', 'padding': '12px', 'backgroundColor': '#f8fafc', 'maxHeight': '240px', 'overflowY': 'auto', 'marginTop': '8px'})
                                ], id='collapse-missing', is_open=False)
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
                
                # Attestation Progress and Button (hidden when attested)
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H4("Review Progress", style={'fontSize': '14px', 'color': '#0f172a', 'margin': '0 0 4px 0'}),
                                html.P([
                                    html.Span(id='reviewed-count', children='0'),
                                    f" of {total_points} subpoints reviewed"
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
                            )
                        ], id='attest-btn-container', style={'marginBottom': '8px'}),
                        html.P("Please review all subpoints before attesting",
                               id='attest-message',
                               style={'fontSize': '12px', 'color': '#64748b', 'textAlign': 'center', 'fontStyle': 'italic', 'margin': 0})
                    ], style={'padding': '16px', 'backgroundColor': '#f8fafc', 'borderRadius': '8px', 'border': '1px solid #e2e8f0'})
                ], id='attestation-progress-container', style={'marginTop': '24px'}),
                
                # Attested Confirmation (hidden initially)
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    icon("mdi:check-circle", width=24, color='#16a34a')
                                ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'width': '40px', 'height': '40px', 'borderRadius': '50%', 'backgroundColor': '#dcfce7', 'flexShrink': 0}),
                                html.Div([
                                    html.H4("Review Attested", style={'fontSize': '14px', 'color': '#166534', 'margin': '0 0 4px 0'}),
                                    html.P(f"All {total_points} subpoints have been reviewed and the attestation is complete.",
                                           style={'fontSize': '12px', 'color': '#15803d', 'margin': 0})
                                ], style={'flex': 1})
                            ], style={'display': 'flex', 'alignItems': 'center', 'gap': '12px'})
                        ])
                    ], style={'padding': '16px', 'backgroundColor': '#f0fdf4', 'borderRadius': '8px', 'border': '1px solid #bbf7d0'})
                ], id='attested-confirmation', style={'marginTop': '24px', 'display': 'none'})
            ])
        ]),
        
        # Hidden stores for attestation state
        dcc.Store(id='attestation-store', data=[]),  # List of attestations
        dcc.Store(id='is-attested-store', data=False),  # Whether review is attested
        
        # Evidence offcanvas (modal/drawer for viewing evidence)
        create_evidence_offcanvas()
    ], style={'padding': '0'})
