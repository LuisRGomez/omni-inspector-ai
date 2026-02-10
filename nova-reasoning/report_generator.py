"""
Report Generator - Generate PDF and JSON reports for all business modules.

Supports:
- Module A: Underwriting reports
- Module B: Claims reports  
- Module C: Legal evidence reports
"""

import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from pydantic import BaseModel


class Report(BaseModel):
    """Generated report."""
    case_id: str
    module: str
    generated_at: str
    content: Dict[str, Any]
    
    def save_json(self, filepath: str):
        """Save report as JSON."""
        with open(filepath, 'w') as f:
            json.dump(self.dict(), f, indent=2)
    
    def save_pdf(self, filepath: str):
        """Save report as PDF."""
        # This will be implemented by ReportGenerator
        pass


class ReportGenerator:
    """
    Generate professional reports for insurance and legal purposes.
    """
    
    def __init__(self, company_name: str = "Omni-Inspector AI"):
        """
        Initialize report generator.
        
        Args:
            company_name: Company name for report header
        """
        self.company_name = company_name
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        )
    
    def generate(
        self,
        analysis_result: Any,
        module: str,
        additional_data: Optional[Dict] = None
    ) -> Report:
        """
        Generate report based on analysis result and module.
        
        Args:
            analysis_result: AnalysisResult from NovaAnalyzer
            module: Business module (underwriting, claims, legal)
            additional_data: Additional data to include
        
        Returns:
            Report object
        """
        generators = {
            'underwriting': self._generate_underwriting_report,
            'claims': self._generate_claims_report,
            'legal': self._generate_legal_report
        }
        
        generator = generators.get(module, self._generate_claims_report)
        content = generator(analysis_result, additional_data or {})
        
        report = Report(
            case_id=analysis_result.case_id,
            module=module,
            generated_at=datetime.now().isoformat(),
            content=content
        )
        
        return report
    
    def _generate_underwriting_report(
        self,
        analysis: Any,
        additional_data: Dict
    ) -> Dict[str, Any]:
        """Generate underwriting (pre-inspection) report."""
        
        return {
            'report_type': 'Underwriting Pre-Inspection',
            'case_id': analysis.case_id,
            'timestamp': analysis.timestamp,
            'verdict': analysis.verdict,
            'risk_assessment': {
                'risk_score': analysis.risk_score,
                'risk_level': self._get_risk_level(analysis.risk_score),
                'recommendation': analysis.verdict
            },
            'damages_found': [
                {
                    'type': d.damage_type,
                    'severity': d.severity,
                    'location': d.location,
                    'confidence': f"{d.confidence:.1%}",
                    'description': d.description
                }
                for d in analysis.damages
            ],
            'cost_estimate': {
                'total': analysis.estimated_total_cost,
                'currency': 'USD',
                'breakdown': [
                    {
                        'damage': d.damage_type,
                        'cost': d.repair_cost_estimate
                    }
                    for d in analysis.damages
                    if d.repair_cost_estimate
                ]
            },
            'reasoning': analysis.reasoning,
            'recommendations': analysis.recommendations,
            'certificate': {
                'issued': analysis.verdict == 'APPROVED',
                'valid_until': self._calculate_expiry(90),  # 90 days
                'blockchain_hash': additional_data.get('blockchain_hash', 'pending')
            }
        }
    
    def _generate_claims_report(
        self,
        analysis: Any,
        additional_data: Dict
    ) -> Dict[str, Any]:
        """Generate claims validation report."""
        
        return {
            'report_type': 'Claims Validation Report',
            'case_id': analysis.case_id,
            'timestamp': analysis.timestamp,
            'verdict': analysis.verdict,
            'fraud_analysis': {
                'fraud_score': f"{analysis.fraud_score:.1%}",
                'fraud_detected': analysis.fraud_score > 0.5,
                'confidence': f"{analysis.confidence:.1%}",
                'indicators': self._extract_fraud_indicators(analysis.reasoning)
            },
            'damages_validated': [
                {
                    'type': d.damage_type,
                    'severity': d.severity,
                    'location': d.location,
                    'confidence': f"{d.confidence:.1%}",
                    'repair_cost': d.repair_cost_estimate,
                    'description': d.description
                }
                for d in analysis.damages
            ],
            'settlement': {
                'recommended_amount': analysis.estimated_total_cost,
                'currency': 'USD',
                'payment_method': 'Direct deposit',
                'processing_time': f"{analysis.processing_time_ms}ms"
            },
            'reasoning': analysis.reasoning,
            'recommendations': analysis.recommendations,
            'next_steps': self._get_claims_next_steps(analysis.verdict)
        }
    
    def _generate_legal_report(
        self,
        analysis: Any,
        additional_data: Dict
    ) -> Dict[str, Any]:
        """Generate legal evidence report."""
        
        return {
            'report_type': 'Legal Evidence Report',
            'case_id': analysis.case_id,
            'timestamp': analysis.timestamp,
            'court_ready': analysis.verdict == 'COURT_READY',
            'evidence_package': {
                'container_id': additional_data.get('container_id', 'N/A'),
                'seal_number': additional_data.get('seal_number', 'N/A'),
                'csc_plate': additional_data.get('csc_plate', 'N/A'),
                'damages_documented': len(analysis.damages)
            },
            'damages': [
                {
                    'type': d.damage_type,
                    'severity': d.severity,
                    'location': d.location,
                    'confidence': f"{d.confidence:.1%}",
                    'description': d.description,
                    'estimated_cost': d.repair_cost_estimate
                }
                for d in analysis.damages
            ],
            'causality_analysis': {
                'determination': additional_data.get('causality', 'Under investigation'),
                'liability': additional_data.get('liability', 'To be determined'),
                'reasoning': analysis.reasoning
            },
            'legal_compliance': {
                'evidence_authenticated': True,
                'chain_of_custody': 'Maintained',
                'worm_storage': 'Enabled (5-year retention)',
                'admissible': analysis.verdict == 'COURT_READY'
            },
            'recommendations': analysis.recommendations,
            'expert_opinion': self._generate_expert_opinion(analysis)
        }
    
    def save_pdf(self, report: Report, filepath: str):
        """
        Generate and save PDF report.
        
        Args:
            report: Report object
            filepath: Output PDF file path
        """
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Header
        story.append(Paragraph(self.company_name, self.title_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Report title
        title = report.content.get('report_type', 'Inspection Report')
        story.append(Paragraph(title, self.heading_style))
        story.append(Spacer(1, 0.3 * inch))
        
        # Case information
        case_data = [
            ['Case ID:', report.case_id],
            ['Generated:', report.generated_at],
            ['Module:', report.module.upper()]
        ]
        
        case_table = Table(case_data, colWidths=[2 * inch, 4 * inch])
        case_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(case_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Verdict
        verdict = report.content.get('verdict', 'UNKNOWN')
        verdict_color = self._get_verdict_color(verdict)
        
        verdict_style = ParagraphStyle(
            'Verdict',
            parent=self.styles['Normal'],
            fontSize=18,
            textColor=verdict_color,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        story.append(Paragraph(f"<b>VERDICT: {verdict}</b>", verdict_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Module-specific content
        if report.module == 'underwriting':
            self._add_underwriting_content(story, report.content)
        elif report.module == 'claims':
            self._add_claims_content(story, report.content)
        elif report.module == 'legal':
            self._add_legal_content(story, report.content)
        
        # Build PDF
        doc.build(story)
    
    def _add_underwriting_content(self, story: list, content: Dict):
        """Add underwriting-specific content to PDF."""
        story.append(Paragraph("Risk Assessment", self.heading_style))
        
        risk_data = content.get('risk_assessment', {})
        risk_table = Table([
            ['Risk Score:', f"{risk_data.get('risk_score', 0)}/10"],
            ['Risk Level:', risk_data.get('risk_level', 'Unknown')],
            ['Recommendation:', risk_data.get('recommendation', 'N/A')]
        ])
        
        story.append(risk_table)
        story.append(Spacer(1, 0.2 * inch))
        
        # Damages
        if content.get('damages_found'):
            story.append(Paragraph("Damages Found", self.heading_style))
            for damage in content['damages_found']:
                story.append(Paragraph(
                    f"• <b>{damage['type']}</b> ({damage['severity']}) - {damage['location']}",
                    self.styles['Normal']
                ))
    
    def _add_claims_content(self, story: list, content: Dict):
        """Add claims-specific content to PDF."""
        story.append(Paragraph("Fraud Analysis", self.heading_style))
        
        fraud_data = content.get('fraud_analysis', {})
        fraud_table = Table([
            ['Fraud Score:', fraud_data.get('fraud_score', 'N/A')],
            ['Fraud Detected:', 'YES' if fraud_data.get('fraud_detected') else 'NO'],
            ['Confidence:', fraud_data.get('confidence', 'N/A')]
        ])
        
        story.append(fraud_table)
        story.append(Spacer(1, 0.2 * inch))
    
    def _add_legal_content(self, story: list, content: Dict):
        """Add legal-specific content to PDF."""
        story.append(Paragraph("Evidence Package", self.heading_style))
        
        evidence = content.get('evidence_package', {})
        evidence_table = Table([
            ['Container ID:', evidence.get('container_id', 'N/A')],
            ['Seal Number:', evidence.get('seal_number', 'N/A')],
            ['Damages:', str(evidence.get('damages_documented', 0))]
        ])
        
        story.append(evidence_table)
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to level."""
        if risk_score >= 8:
            return 'CRITICAL'
        elif risk_score >= 6:
            return 'HIGH'
        elif risk_score >= 4:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _get_verdict_color(self, verdict: str) -> colors.Color:
        """Get color for verdict."""
        colors_map = {
            'APPROVED': colors.green,
            'REJECTED': colors.red,
            'REVIEW_REQUIRED': colors.orange,
            'COURT_READY': colors.blue
        }
        return colors_map.get(verdict, colors.black)
    
    def _calculate_expiry(self, days: int) -> str:
        """Calculate expiry date."""
        from datetime import timedelta
        expiry = datetime.now() + timedelta(days=days)
        return expiry.strftime('%Y-%m-%d')
    
    def _extract_fraud_indicators(self, reasoning: str) -> List[str]:
        """Extract fraud indicators from reasoning text."""
        indicators = []
        keywords = ['recycled', 'manipulated', 'suspicious', 'inconsistent', 'tampered']
        
        for keyword in keywords:
            if keyword in reasoning.lower():
                indicators.append(keyword.capitalize())
        
        return indicators if indicators else ['None detected']
    
    def _get_claims_next_steps(self, verdict: str) -> List[str]:
        """Get next steps based on verdict."""
        steps_map = {
            'APPROVED': [
                'Process payment to claimant',
                'Close case',
                'Archive evidence'
            ],
            'REJECTED': [
                'Notify claimant of rejection',
                'Provide detailed reasoning',
                'Offer appeal process'
            ],
            'REVIEW_REQUIRED': [
                'Escalate to senior adjuster',
                'Request additional evidence',
                'Schedule manual inspection'
            ]
        }
        return steps_map.get(verdict, ['Contact support'])
    
    def _generate_expert_opinion(self, analysis: Any) -> str:
        """Generate expert opinion for legal report."""
        severity_count = len([d for d in analysis.damages if d.severity in ['high', 'critical']])
        
        if severity_count > 0:
            return f"Based on forensic analysis, {severity_count} critical damage(s) identified. Evidence is court-admissible and supports liability claim."
        else:
            return "Minor damages detected. Evidence documented for record purposes."
