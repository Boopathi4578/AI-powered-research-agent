"""
Main Research Agent using Agno framework.
Orchestrates paper fetching, summarization, and report generation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agno.agent import Agent
from agno.models.aws import AwsBedrock
from agno.tools import tool
from typing import List, Dict, Optional
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

from utils.paper_fetcher import PaperFetcher
from utils.report_generator import ReportGenerator

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchAgent:
    """
    AI-powered research agent that fetches and summarizes academic papers.
    Uses AWS Bedrock for LLM inference.
    """

    def __init__(self, max_papers: int = 10):
        """
        Initialize the Research Agent.

        Args:
            max_papers: Maximum number of papers to fetch
        """
        self.paper_fetcher = PaperFetcher(max_results=max_papers)
        self.report_generator = ReportGenerator()

        # Get AWS Bedrock model ID from environment
        model_id = os.getenv("BEDROCK_MODEL_ID")
        if not model_id:
            raise ValueError("BEDROCK_MODEL_ID environment variable is required")

        # Initialize AWS Bedrock model using Agno's built-in support
        self.model = AwsBedrock(id=model_id)

        # Create Agno agent for summarization
        self.summarizer_agent = Agent(
            name="Paper Summarizer",
            model=self.model,
            description="Expert at analyzing and summarizing academic research papers",
            instructions=[
                "You are an expert research analyst specializing in academic papers.",
                "Provide clear, concise summaries that capture the key contributions.",
                "Identify the main findings, methodology, and significance of each paper.",
                "Use technical language appropriately but ensure clarity.",
            ],
            markdown=True,
        )
        
        # Create Agno agent for synthesis
        self.synthesis_agent = Agent(
            name="Research Synthesizer",
            model=self.model,
            description="Expert at synthesizing multiple research papers into coherent insights",
            instructions=[
                "You are an expert at synthesizing research across multiple papers.",
                "Identify common themes, trends, and patterns across papers.",
                "Highlight contradictions or different approaches to similar problems.",
                "Provide actionable insights and recommendations.",
            ],
            markdown=True,
        )
    
    def fetch_papers(self, query: str, sources: List[str] = ['arxiv']) -> List[Dict]:
        """
        Fetch papers based on research query.
        
        Args:
            query: Research query string
            sources: List of sources to search
            
        Returns:
            List of paper dictionaries
        """
        logger.info(f"Fetching papers for query: '{query}'")
        papers = self.paper_fetcher.fetch_papers(query, sources=sources)
        return papers
    
    def summarize_paper(self, paper: Dict) -> Dict:
        """
        Summarize a single paper using the LLM.
        
        Args:
            paper: Paper dictionary with metadata
            
        Returns:
            Paper dictionary with added summary and key findings
        """
        prompt = f"""
Analyze the following research paper and provide:
1. A concise summary (2-3 paragraphs)
2. Key findings (bullet points)

**Title:** {paper['title']}

**Authors:** {', '.join(paper['authors'])}

**Abstract:**
{paper['abstract']}

**Published:** {paper['published']}

Please provide a structured analysis.
"""
        
        try:
            response = self.summarizer_agent.run(prompt)
            
            # Extract the response content
            summary_text = response.content if hasattr(response, 'content') else str(response)
            
            # Split into summary and key findings (simple heuristic)
            parts = summary_text.split('Key findings')
            if len(parts) == 2:
                summary = parts[0].strip()
                key_findings = 'Key findings' + parts[1].strip()
            else:
                summary = summary_text
                key_findings = "See summary above."
            
            paper['summary'] = summary
            paper['key_findings'] = key_findings
            
        except Exception as e:
            logger.error(f"Error summarizing paper: {str(e)}")
            paper['summary'] = paper['abstract']
            paper['key_findings'] = "Error generating key findings."

        return paper

    def synthesize_research(self, papers: List[Dict], query: str) -> Dict:
        """
        Synthesize insights from multiple papers.

        Args:
            papers: List of summarized papers
            query: Original research query

        Returns:
            Dictionary with synthesis results
        """
        # Prepare paper summaries for synthesis
        papers_text = "\n\n".join([
            f"Paper {i+1}: {p['title']}\n{p['summary']}\n{p['key_findings']}"
            for i, p in enumerate(papers)
        ])

        synthesis_prompt = f"""
Based on the following research papers about "{query}", provide:

1. **Executive Summary**: A high-level overview of the research landscape (2-3 paragraphs)
2. **Key Themes and Trends**: Common themes, methodologies, and trends across papers
3. **Recommendations**: Suggestions for further reading or research directions
4. **Conclusion**: Final thoughts on the state of research in this area

Papers:
{papers_text}

Please provide a comprehensive synthesis.
"""

        try:
            response = self.synthesis_agent.run(synthesis_prompt)
            synthesis_text = response.content if hasattr(response, 'content') else str(response)

            # Parse the synthesis (simple heuristic)
            sections = {
                'executive_summary': '',
                'key_themes': '',
                'recommendations': '',
                'conclusion': ''
            }

            # Try to extract sections
            current_section = 'executive_summary'
            for line in synthesis_text.split('\n'):
                line_lower = line.lower()
                if 'key themes' in line_lower or 'themes and trends' in line_lower:
                    current_section = 'key_themes'
                elif 'recommendation' in line_lower:
                    current_section = 'recommendations'
                elif 'conclusion' in line_lower:
                    current_section = 'conclusion'
                else:
                    sections[current_section] += line + '\n'

            # Clean up sections
            for key in sections:
                sections[key] = sections[key].strip()
                if not sections[key]:
                    sections[key] = "See full synthesis above."

            return sections

        except Exception as e:
            logger.error(f"Error synthesizing research: {str(e)}")
            return {
                'executive_summary': 'Error generating synthesis.',
                'key_themes': 'Error generating synthesis.',
                'recommendations': 'Error generating synthesis.',
                'conclusion': 'Error generating synthesis.'
            }

    def generate_report(
        self,
        query: str,
        sources: List[str] = ['arxiv'],
        output_filename: Optional[str] = None
    ) -> str:
        """
        Complete research workflow: fetch, summarize, synthesize, and generate report.

        Args:
            query: Research query
            sources: Sources to search
            output_filename: Optional custom filename for report

        Returns:
            Path to generated report
        """
        logger.info(f"Starting research workflow for: '{query}'")

        # Step 1: Fetch papers
        papers = self.fetch_papers(query, sources)

        if not papers:
            logger.warning("No papers found for the query.")
            return None

        # Step 2: Summarize each paper
        logger.info(f"Summarizing {len(papers)} papers...")
        summarized_papers = []
        for i, paper in enumerate(papers, 1):
            logger.info(f"Summarizing paper {i}/{len(papers)}: {paper['title'][:50]}...")
            summarized_paper = self.summarize_paper(paper)
            summarized_papers.append(summarized_paper)

        # Step 3: Synthesize research
        logger.info("Synthesizing research insights...")
        synthesis = self.synthesize_research(summarized_papers, query)

        # Step 4: Generate report
        logger.info("Generating report...")
        report = self.report_generator.generate_markdown_report(
            query=query,
            papers=summarized_papers,
            executive_summary=synthesis['executive_summary'],
            key_themes=synthesis['key_themes'],
            recommendations=synthesis['recommendations'],
            conclusion=synthesis['conclusion']
        )

        # Step 5: Save report
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"research_report_{timestamp}.md"

        report_path = self.report_generator.save_report(report, output_filename)
        logger.info(f"Report saved to: {report_path}")

        # Also save raw data
        json_filename = output_filename.replace('.md', '.json')
        data = {
            'query': query,
            'papers': summarized_papers,
            'synthesis': synthesis,
            'generated_at': datetime.now().isoformat()
        }
        self.report_generator.save_json_data(data, json_filename)

        return report_path

