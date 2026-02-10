"""
CLI for Nova Reasoning Layer.

Commands:
- analyze: Perform complete case analysis
- fraud-check: Check for fraud indicators
- ocr: Extract text from images
- report: Generate PDF/JSON reports
"""

import click
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Optional
from nova_analyzer import NovaAnalyzer
from fraud_detector import FraudDetector
from report_generator import ReportGenerator

console = Console()


@click.group()
def cli():
    """Omni-Inspector AI - Nova Reasoning Layer CLI"""
    pass


@cli.command()
@click.option('--case-id', required=True, help='Case ID')
@click.option('--forensic-report', required=True, help='Path or S3 URL to forensic report JSON')
@click.option('--yolo-report', required=True, help='Path or S3 URL to YOLO detection report JSON')
@click.option('--image', required=True, help='S3 URL of the image')
@click.option('--module', type=click.Choice(['underwriting', 'claims', 'legal']), default='claims', help='Business module')
@click.option('--model', default='amazon.nova-lite-v1:0', help='Bedrock model ID')
@click.option('--output', help='Output file path for JSON report')
def analyze(case_id: str, forensic_report: str, yolo_report: str, image: str, module: str, model: str, output: Optional[str]):
    """Perform complete case analysis using Nova."""
    
    console.print(f"\n[bold cyan]Analyzing case: {case_id}[/bold cyan]\n")
    
    try:
        # Load reports
        forensic_data = _load_json(forensic_report)
        yolo_data = _load_json(yolo_report)
        
        # Initialize analyzer
        analyzer = NovaAnalyzer(model=model)
        
        # Analyze
        with console.status("[bold green]Analyzing with Nova..."):
            result = analyzer.analyze_case(
                case_id=case_id,
                forensic_data=forensic_data,
                yolo_data=yolo_data,
                image_url=image,
                module=module
            )
        
        # Display results
        _display_analysis_result(result)
        
        # Save output
        if output:
            with open(output, 'w') as f:
                json.dump(result.dict(), f, indent=2)
            console.print(f"\n[green]✓[/green] Report saved to: {output}")
        
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {str(e)}")
        raise click.Abort()


@cli.command()
@click.option('--case-id', required=True, help='Case ID')
@click.option('--image', required=True, help='S3 URL of the image')
@click.option('--forensic-report', required=True, help='Path or S3 URL to forensic report JSON')
@click.option('--check-duplicates', is_flag=True, help='Check for duplicate images')
@click.option('--output', help='Output file path for JSON report')
def fraud_check(case_id: str, image: str, forensic_report: str, check_duplicates: bool, output: Optional[str]):
    """Check for fraud indicators."""
    
    console.print(f"\n[bold cyan]Fraud check for case: {case_id}[/bold cyan]\n")
    
    try:
        # Load forensic data
        forensic_data = _load_json(forensic_report)
        
        # Initialize detector
        detector = FraudDetector()
        
        # Check fraud
        with console.status("[bold green]Analyzing for fraud..."):
            result = detector.check_image(
                image_url=image,
                metadata=forensic_data.get('metadata', {}),
                case_id=case_id
            )
        
        # Display results
        _display_fraud_result(result)
        
        # Check duplicates if requested
        if check_duplicates:
            is_dup, similar_cases = detector.check_duplicate(image)
            if is_dup:
                console.print(f"\n[yellow]⚠ Duplicate detected![/yellow]")
                console.print(f"Similar cases: {', '.join(similar_cases)}")
        
        # Save output
        if output:
            with open(output, 'w') as f:
                json.dump(result.dict(), f, indent=2)
            console.print(f"\n[green]✓[/green] Report saved to: {output}")
        
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {str(e)}")
        raise click.Abort()


@cli.command()
@click.option('--image', required=True, help='S3 URL of the image')
@click.option('--extract', required=True, help='Comma-separated list: container-id,seal-number,csc-plate,license-plate')
@click.option('--model', default='amazon.nova-lite-v1:0', help='Bedrock model ID')
@click.option('--output', help='Output file path for JSON results')
def ocr(image: str, extract: str, model: str, output: Optional[str]):
    """Extract text from images using Nova OCR."""
    
    console.print(f"\n[bold cyan]OCR Extraction[/bold cyan]\n")
    
    try:
        # Parse extract types
        extract_types = [t.strip() for t in extract.split(',')]
        
        # Initialize analyzer
        analyzer = NovaAnalyzer(model=model)
        
        # Extract OCR
        with console.status("[bold green]Extracting text..."):
            result = analyzer.extract_ocr(image, extract_types)
        
        # Display results
        table = Table(title="OCR Results")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in result.items():
            table.add_row(key, value or "Not found")
        
        console.print(table)
        
        # Save output
        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            console.print(f"\n[green]✓[/green] Results saved to: {output}")
        
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {str(e)}")
        raise click.Abort()


@cli.command()
@click.option('--case-id', required=True, help='Case ID')
@click.option('--analysis-report', required=True, help='Path to analysis result JSON')
@click.option('--module', type=click.Choice(['underwriting', 'claims', 'legal']), required=True, help='Business module')
@click.option('--output', required=True, help='Output file path (.pdf or .json)')
def report(case_id: str, analysis_report: str, module: str, output: str):
    """Generate PDF or JSON report."""
    
    console.print(f"\n[bold cyan]Generating {module} report[/bold cyan]\n")
    
    try:
        # Load analysis result
        analysis_data = _load_json(analysis_report)
        
        # Initialize generator
        generator = ReportGenerator()
        
        # Generate report
        with console.status("[bold green]Generating report..."):
            # Convert dict to AnalysisResult (simplified)
            from nova_analyzer import AnalysisResult, DamageAssessment
            
            damages = [
                DamageAssessment(**d) for d in analysis_data.get('damages', [])
            ]
            
            analysis_result = AnalysisResult(
                case_id=analysis_data['case_id'],
                timestamp=analysis_data['timestamp'],
                module=analysis_data['module'],
                verdict=analysis_data['verdict'],
                confidence=analysis_data['confidence'],
                damages=damages,
                fraud_score=analysis_data.get('fraud_score', 0.0),
                risk_score=analysis_data.get('risk_score', 5.0),
                reasoning=analysis_data['reasoning'],
                recommendations=analysis_data['recommendations'],
                estimated_total_cost=analysis_data.get('estimated_total_cost'),
                processing_time_ms=analysis_data['processing_time_ms']
            )
            
            report_obj = generator.generate(analysis_result, module)
        
        # Save report
        if output.endswith('.pdf'):
            generator.save_pdf(report_obj, output)
        else:
            report_obj.save_json(output)
        
        console.print(f"\n[green]✓[/green] Report saved to: {output}")
        
    except Exception as e:
        console.print(f"[red]✗ Error:[/red] {str(e)}")
        raise click.Abort()


@cli.command()
@click.option('--image', required=True, help='Test image path or S3 URL')
def test(image: str):
    """Test Nova connection and basic functionality."""
    
    console.print("\n[bold cyan]Testing Nova Reasoning Layer[/bold cyan]\n")
    
    try:
        # Test 1: Initialize analyzer
        console.print("[yellow]1.[/yellow] Initializing Nova analyzer...")
        analyzer = NovaAnalyzer()
        console.print("[green]✓[/green] Analyzer initialized\n")
        
        # Test 2: Initialize fraud detector
        console.print("[yellow]2.[/yellow] Initializing fraud detector...")
        detector = FraudDetector()
        console.print("[green]✓[/green] Fraud detector initialized\n")
        
        # Test 3: Initialize report generator
        console.print("[yellow]3.[/yellow] Initializing report generator...")
        generator = ReportGenerator()
        console.print("[green]✓[/green] Report generator initialized\n")
        
        console.print("[bold green]All tests passed![/bold green]")
        
    except Exception as e:
        console.print(f"[red]✗ Test failed:[/red] {str(e)}")
        raise click.Abort()


def _load_json(path: str) -> dict:
    """Load JSON from file or S3."""
    if path.startswith('s3://'):
        # TODO: Download from S3
        raise NotImplementedError("S3 download not implemented yet")
    else:
        with open(path, 'r') as f:
            return json.load(f)


def _display_analysis_result(result):
    """Display analysis result in rich format."""
    
    # Verdict panel
    verdict_color = {
        'APPROVED': 'green',
        'REJECTED': 'red',
        'REVIEW_REQUIRED': 'yellow',
        'COURT_READY': 'blue'
    }.get(result.verdict, 'white')
    
    console.print(Panel(
        f"[bold {verdict_color}]{result.verdict}[/bold {verdict_color}]",
        title="Verdict",
        border_style=verdict_color
    ))
    
    # Scores table
    table = Table(title="Analysis Scores")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Confidence", f"{result.confidence:.1%}")
    table.add_row("Fraud Score", f"{result.fraud_score:.1%}")
    table.add_row("Risk Score", f"{result.risk_score:.1f}/10")
    table.add_row("Processing Time", f"{result.processing_time_ms}ms")
    
    console.print(table)
    
    # Damages
    if result.damages:
        console.print("\n[bold]Damages Detected:[/bold]")
        for damage in result.damages:
            console.print(f"  • {damage.damage_type} ({damage.severity}) - {damage.location}")
    
    # Reasoning
    console.print(f"\n[bold]Reasoning:[/bold]\n{result.reasoning}")
    
    # Recommendations
    if result.recommendations:
        console.print("\n[bold]Recommendations:[/bold]")
        for rec in result.recommendations:
            console.print(f"  • {rec}")


def _display_fraud_result(result):
    """Display fraud result in rich format."""
    
    # Status panel
    status_color = 'red' if result.is_suspicious else 'green'
    status_text = 'SUSPICIOUS' if result.is_suspicious else 'CLEAN'
    
    console.print(Panel(
        f"[bold {status_color}]{status_text}[/bold {status_color}]",
        title="Fraud Status",
        border_style=status_color
    ))
    
    # Scores
    table = Table(title="Fraud Analysis")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="yellow" if result.is_suspicious else "green")
    
    table.add_row("Fraud Score", f"{result.fraud_score:.1%}")
    table.add_row("Confidence", f"{result.confidence:.1%}")
    
    console.print(table)
    
    # Reasons
    console.print("\n[bold]Indicators:[/bold]")
    for reason in result.reasons:
        icon = "⚠" if result.is_suspicious else "✓"
        console.print(f"  {icon} {reason}")


if __name__ == '__main__':
    cli()
