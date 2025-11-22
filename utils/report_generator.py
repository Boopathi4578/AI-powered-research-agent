"""
Report generation utilities for creating structured research reports.
"""

from typing import List, Dict
from datetime import datetime
import json
from jinja2 import Template


class ReportGenerator:
    """Generates structured reports from summarized research papers."""
    
    MARKDOWN_TEMPLATE = """# Research Report: {{ query }}

**Generated on:** {{ date }}  
**Total Papers Analyzed:** {{ total_papers }}

---

## Executive Summary

{{ executive_summary }}

---

## Detailed Paper Summaries

{% for paper in papers %}
### {{ loop.index }}. {{ paper.title }}

**Authors:** {{ paper.authors | join(', ') }}  
**Published:** {{ paper.published }}  
**Source:** {{ paper.source }}  
**arXiv URL:** [{{ paper.arxiv_url }}]({{ paper.arxiv_url }})

#### Summary
{{ paper.summary }}

#### Key Findings
{{ paper.key_findings }}

---

{% endfor %}

## Key Themes and Trends

{{ key_themes }}

---

## Recommendations for Further Reading

{{ recommendations }}

---

## Conclusion

{{ conclusion }}

---

*This report was automatically generated using AI-powered research analysis.*
"""
    
    def __init__(self):
        """Initialize the report generator."""
        self.template = Template(self.MARKDOWN_TEMPLATE)
    
    def generate_markdown_report(
        self,
        query: str,
        papers: List[Dict],
        executive_summary: str,
        key_themes: str,
        recommendations: str,
        conclusion: str
    ) -> str:
        """
        Generate a markdown report from analyzed papers.
        
        Args:
            query: Original research query
            papers: List of paper dictionaries with summaries
            executive_summary: Overall summary of findings
            key_themes: Key themes identified across papers
            recommendations: Recommendations for further reading
            conclusion: Concluding remarks
            
        Returns:
            Formatted markdown report as string
        """
        report = self.template.render(
            query=query,
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_papers=len(papers),
            papers=papers,
            executive_summary=executive_summary,
            key_themes=key_themes,
            recommendations=recommendations,
            conclusion=conclusion
        )
        
        return report
    
    def save_report(self, report: str, filename: str) -> str:
        """
        Save report to a file.
        
        Args:
            report: Report content
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        filepath = f"data/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filepath
    
    def save_json_data(self, data: Dict, filename: str) -> str:
        """
        Save raw data as JSON.
        
        Args:
            data: Data to save
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        filepath = f"data/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath

