"""Mock data for the compliance dashboard"""

# Compliance standards data
STANDARDS = [
    {
        "id": "gdpr",
        "name": "GDPR",
        "fullName": "General Data Protection Regulation",
        "description": "EU regulation on data protection and privacy",
        "region": "European Union",
        "lastUpdated": "2023-11-15",
        "status": "active",
        "contractsCompliant": 42
    },
    {
        "id": "soc2",
        "name": "SOC 2",
        "fullName": "Service Organization Control 2",
        "description": "Trust service criteria for security, availability, and confidentiality",
        "region": "Global",
        "lastUpdated": "2023-10-20",
        "status": "active",
        "contractsCompliant": 38
    },
    {
        "id": "ccpa",
        "name": "CCPA",
        "fullName": "California Consumer Privacy Act",
        "description": "California state statute on consumer privacy rights",
        "region": "California, USA",
        "lastUpdated": "2023-09-08",
        "status": "active",
        "contractsCompliant": 35
    },
    {
        "id": "hipaa",
        "name": "HIPAA",
        "fullName": "Health Insurance Portability and Accountability Act",
        "description": "US legislation providing data privacy for medical information",
        "region": "United States",
        "lastUpdated": "2023-08-12",
        "status": "active",
        "contractsCompliant": 12
    }
]

# Completed contract reviews
CONTRACTS = [
    {
        "id": "CT-2024-001",
        "name": "Enterprise SaaS Agreement - TechCorp",
        "vendor": "TechCorp Solutions Inc.",
        "reviewDate": "2024-01-15",
        "status": "Approved",
        "overallScore": 94,
        "standards": ["GDPR", "SOC 2", "CCPA"],
        "reviewer": "Sarah Johnson",
        "riskLevel": "Low"
    },
    {
        "id": "CT-2024-002",
        "name": "Cloud Services Agreement - DataFlow",
        "vendor": "DataFlow Systems",
        "reviewDate": "2024-01-12",
        "status": "Approved with Conditions",
        "overallScore": 87,
        "standards": ["GDPR", "SOC 2"],
        "reviewer": "Michael Chen",
        "riskLevel": "Medium"
    },
    {
        "id": "CT-2024-003",
        "name": "Data Processing Agreement - AnalyticsPro",
        "vendor": "AnalyticsPro Ltd.",
        "reviewDate": "2024-01-10",
        "status": "Rejected",
        "overallScore": 62,
        "standards": ["GDPR"],
        "reviewer": "Emily Rodriguez",
        "riskLevel": "High"
    },
    {
        "id": "CT-2024-004",
        "name": "Software License - SecureApp",
        "vendor": "SecureApp Technologies",
        "reviewDate": "2024-01-08",
        "status": "Approved",
        "overallScore": 96,
        "standards": ["GDPR", "SOC 2", "HIPAA"],
        "reviewer": "David Park",
        "riskLevel": "Low"
    },
    {
        "id": "CT-2024-005",
        "name": "API Integration Agreement - CloudSync",
        "vendor": "CloudSync Inc.",
        "reviewDate": "2024-01-05",
        "status": "Approved",
        "overallScore": 91,
        "standards": ["SOC 2", "CCPA"],
        "reviewer": "Sarah Johnson",
        "riskLevel": "Low"
    }
]

# Trend data for analytics
TREND_DATA = [
    {"month": "Jul", "score": 82},
    {"month": "Aug", "score": 85},
    {"month": "Sep", "score": 83},
    {"month": "Oct", "score": 88},
    {"month": "Nov", "score": 90},
    {"month": "Dec", "score": 89},
    {"month": "Jan", "score": 92}
]

# Detailed compliance terms for contract detail view
COMPLIANCE_TERMS = [
    {
        "id": "data-protection",
        "title": "Data Protection & Privacy",
        "status": "met",
        "score": 95,
        "overallAnalysis": "The contract demonstrates strong data protection provisions with comprehensive privacy safeguards. All major requirements for data subject rights, data minimization, and security measures are clearly articulated and meet regulatory standards.",
        "subPoints": [
            {
                "heading": "Right to Access",
                "description": "Data subjects can request access to their personal data",
                "met": True,
                "analysis": "The contract explicitly provides for data subject access requests with a 30-day response timeframe, which aligns with GDPR Article 15 requirements.",
                "evidence": [
                    {
                        "excerpt": "The Company shall respond to any data subject access request within thirty (30) days of receipt, providing a copy of all personal data being processed.",
                        "explanation": "This clause directly addresses GDPR Article 15 requirements for data subject access, providing a clear timeframe that meets regulatory standards."
                    },
                    {
                        "excerpt": "Upon request, the Company will provide information about the purposes of processing, categories of data, and recipients of the data.",
                        "explanation": "This provision ensures comprehensive transparency by covering all key information elements required under GDPR for access requests."
                    }
                ]
            },
            {
                "heading": "Right to Erasure",
                "description": "Data subjects can request deletion of their personal data",
                "met": True,
                "analysis": "The right to erasure is well-defined with appropriate exceptions for legal obligations, meeting GDPR Article 17 standards.",
                "evidence": [
                    {
                        "excerpt": "Data subjects may request erasure of their personal data, and the Company shall comply within 30 days unless retention is required by law.",
                        "explanation": "This clause balances the right to erasure with legitimate legal retention requirements, consistent with GDPR Article 17."
                    }
                ]
            },
            {
                "heading": "Data Minimization",
                "description": "Only necessary data is collected and processed",
                "met": True,
                "analysis": "Strong data minimization principles are embedded throughout the contract with clear limitations on data collection scope.",
                "evidence": [
                    {
                        "excerpt": "The Company shall collect and process only the minimum personal data necessary to fulfill the stated purposes.",
                        "explanation": "This directly implements the data minimization principle required by GDPR Article 5(1)(c)."
                    }
                ]
            }
        ]
    },
    {
        "id": "security-measures",
        "title": "Security Measures",
        "status": "met",
        "score": 92,
        "overallAnalysis": "Comprehensive security controls are specified including encryption, access controls, and incident response procedures. The contract meets industry standards for data security.",
        "subPoints": [
            {
                "heading": "Encryption Requirements",
                "description": "Data must be encrypted in transit and at rest",
                "met": True,
                "analysis": "The contract mandates AES-256 encryption for data at rest and TLS 1.2+ for data in transit, exceeding minimum security standards.",
                "evidence": [
                    {
                        "excerpt": "All personal data shall be encrypted using AES-256 encryption when stored and TLS 1.2 or higher when transmitted.",
                        "explanation": "This provision specifies industry-standard encryption protocols that provide strong security protection."
                    }
                ]
            },
            {
                "heading": "Access Controls",
                "description": "Appropriate access restrictions are in place",
                "met": True,
                "analysis": "Role-based access control (RBAC) with multi-factor authentication provides robust access security.",
                "evidence": [
                    {
                        "excerpt": "Access to personal data shall be restricted to authorized personnel only, using role-based access controls and multi-factor authentication.",
                        "explanation": "This implements defense-in-depth security by combining RBAC with MFA, significantly reducing unauthorized access risk."
                    }
                ]
            },
            {
                "heading": "Security Incident Response",
                "description": "Procedures for handling security breaches",
                "met": True,
                "analysis": "The 72-hour breach notification requirement aligns with GDPR Article 33 and includes appropriate stakeholder communication procedures.",
                "evidence": [
                    {
                        "excerpt": "In the event of a data breach, the Company shall notify affected parties within 72 hours of becoming aware of the breach.",
                        "explanation": "This meets the GDPR Article 33 requirement for timely breach notification to supervisory authorities."
                    }
                ]
            }
        ]
    },
    {
        "id": "data-transfer",
        "title": "International Data Transfer",
        "status": "partially-met",
        "score": 78,
        "overallAnalysis": "While the contract addresses international data transfers, it lacks specific mechanisms for transfers outside the EEA. Standard contractual clauses or adequacy decisions should be explicitly referenced.",
        "subPoints": [
            {
                "heading": "Transfer Mechanisms",
                "description": "Legal basis for international data transfers",
                "met": False,
                "analysis": "The contract mentions international transfers but doesn't specify the legal mechanism (SCCs, BCRs, or adequacy decisions) as required by GDPR Chapter V.",
                "evidence": []
            },
            {
                "heading": "Data Localization",
                "description": "Geographic restrictions on data storage",
                "met": True,
                "analysis": "Clear data localization requirements are specified for sensitive data categories.",
                "evidence": [
                    {
                        "excerpt": "Sensitive personal data shall be stored exclusively within EU data centers approved by the Company.",
                        "explanation": "This provision ensures compliance with data residency requirements for sensitive data."
                    }
                ]
            }
        ]
    },
    {
        "id": "vendor-management",
        "title": "Third-Party Vendor Management",
        "status": "met",
        "score": 88,
        "overallAnalysis": "The contract includes comprehensive vendor management requirements including due diligence, contractual obligations, and monitoring procedures.",
        "subPoints": [
            {
                "heading": "Subprocessor Approval",
                "description": "Prior approval required for subprocessors",
                "met": True,
                "analysis": "The contract requires written consent before engaging subprocessors, with provisions for customer objection rights.",
                "evidence": [
                    {
                        "excerpt": "The Company shall obtain prior written authorization before engaging any subprocessor to process personal data.",
                        "explanation": "This provides the necessary control over the subprocessor chain as required by GDPR Article 28(2)."
                    }
                ]
            },
            {
                "heading": "Vendor Security Assessment",
                "description": "Security evaluation of third-party vendors",
                "met": True,
                "analysis": "Annual security assessments and SOC 2 certification requirements ensure ongoing vendor security compliance.",
                "evidence": [
                    {
                        "excerpt": "All subprocessors must maintain SOC 2 Type II certification and undergo annual security assessments.",
                        "explanation": "This establishes a baseline security standard for all vendors in the processing chain."
                    }
                ]
            }
        ]
    },
    {
        "id": "audit-rights",
        "title": "Audit & Compliance Verification",
        "status": "met",
        "score": 90,
        "overallAnalysis": "Strong audit provisions allow for comprehensive compliance verification with reasonable notice periods and frequency limitations.",
        "subPoints": [
            {
                "heading": "Right to Audit",
                "description": "Customer can conduct compliance audits",
                "met": True,
                "analysis": "Annual audit rights with 30-day notice provide adequate compliance oversight while minimizing business disruption.",
                "evidence": [
                    {
                        "excerpt": "Customer may conduct an audit of the Company's compliance once per year with 30 days' prior written notice.",
                        "explanation": "This balances the need for compliance verification with operational considerations."
                    }
                ]
            },
            {
                "heading": "Documentation Access",
                "description": "Access to compliance documentation",
                "met": True,
                "analysis": "Comprehensive documentation access rights enable effective compliance monitoring.",
                "evidence": [
                    {
                        "excerpt": "The Company shall provide access to all relevant compliance documentation, including security policies and audit reports.",
                        "explanation": "This ensures transparency and enables thorough compliance review."
                    }
                ]
            }
        ]
    }
]

def get_contract_details(contract_id):
    """Get detailed compliance information for a specific contract"""
    contract = next((c for c in CONTRACTS if c["id"] == contract_id), None)
    if not contract:
        return None
    
    return {
        **contract,
        "terms": COMPLIANCE_TERMS
    }
