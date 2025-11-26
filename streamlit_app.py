#!/usr/bin/env python3
"""Streamlit frontend for AI-Powered Research Agent.

This provides a web UI for the research agent with real-time progress tracking,
source selection, and report generation.
"""

import streamlit as st
import os
import sys
from datetime import datetime
from pathlib import Path
import json
import time
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.research_agent import ResearchAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI-Powered Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-top: 0rem;
        margin-bottom: 0.3rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 1rem;
    }
    .status-connected {
        color: #28a745;
        font-weight: bold;
    }
    .status-disconnected {
        color: #dc3545;
        font-weight: bold;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'report_path' not in st.session_state:
    st.session_state.report_path = None
if 'json_path' not in st.session_state:
    st.session_state.json_path = None
if 'report_content' not in st.session_state:
    st.session_state.report_content = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def add_log(message: str):
    """Add a log message with timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {message}")


def check_bedrock_status():
    """Check if AWS Bedrock is configured."""
    bedrock_model_id = os.getenv("BEDROCK_MODEL_ID")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    
    if bedrock_model_id:
        return True, bedrock_model_id, aws_region
    return False, None, aws_region


def reset_app():
    """Reset the application state."""
    st.session_state.logs = []
    st.session_state.report_path = None
    st.session_state.json_path = None
    st.session_state.report_content = None
    st.session_state.processing = False


def add_to_chat_history(topic: str, report_path: str):
    """Add a completed research to chat history."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chat_history.append({
        'timestamp': timestamp,
        'topic': topic,
        'report_path': report_path
    })


# Header
st.markdown('<div class="main-header">🔬 Research Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI driven research workflow for paper retrieval, summarization and reporting</div>', unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Research topic input
    research_topic = st.text_input(
        "Research Topic",
        placeholder="Enter your research topic (e.g., 'quantum computing applications in cryptography')",
        disabled=st.session_state.processing
    )

    # Sources selection
    st.write("**Sources:**")
    source_cols = st.columns(5)

    sources_available = {
        'openalex': 'OpenAlex',
        'arxiv': 'arXiv',
        'core': 'CORE',
        'zenodo': 'Zenodo',
        'doaj': 'DOAJ'
    }

    selected_sources = {}
    with source_cols[0]:
        selected_sources['openalex'] = st.checkbox('OpenAlex', value=True, disabled=st.session_state.processing)
    with source_cols[1]:
        selected_sources['arxiv'] = st.checkbox('arXiv', value=True, disabled=st.session_state.processing)
    with source_cols[2]:
        selected_sources['core'] = st.checkbox('CORE', value=False, disabled=st.session_state.processing)
    with source_cols[3]:
        selected_sources['zenodo'] = st.checkbox('Zenodo', value=False, disabled=st.session_state.processing)
    with source_cols[4]:
        selected_sources['doaj'] = st.checkbox('DOAJ', value=False, disabled=st.session_state.processing)

    # Configuration options
    config_col1, config_col2 = st.columns(2)

    with config_col1:
        max_papers = st.number_input(
            "Max Papers",
            min_value=1,
            max_value=50,
            value=5,
            step=1,
            disabled=st.session_state.processing
        )

    with config_col2:
        report_name = st.text_input(
            "Report Name",
            value="research_report",
            disabled=st.session_state.processing
        )

with col2:
    # About section
    st.write("### ℹ️ About")
    st.info("""
    This AI-Powered Research Agent automates the process of:

    1. **Fetching** academic papers from multiple sources
    2. **Summarizing** each paper using AWS Bedrock LLM
    3. **Synthesizing** insights across papers
    4. **Generating** structured research reports

    **Supported Sources:**
    - OpenAlex (broad coverage)
    - arXiv (STEM preprints)
    - CORE (open access)
    - Zenodo (multidisciplinary)
    - DOAJ (peer-reviewed)
    """)

# Check bedrock status for button validation
is_connected, model_id, region = check_bedrock_status()

# Action buttons
st.write("---")

# Initialize button states
generate_button = False
reset_button = False

if st.session_state.processing:
    # Show processing state
    button_col1, button_col2 = st.columns([2, 1])
    with button_col1:
        st.button("⏸️ Processing...", disabled=True, use_container_width=True, type="primary")
    with button_col2:
        st.button("🔄 Reset", disabled=True, use_container_width=True)
else:
    # Show normal buttons
    button_col1, button_col2 = st.columns([2, 1])

    with button_col1:
        generate_button = st.button(
            "🚀 Generate Report",
            type="primary",
            disabled=not is_connected or not research_topic,
            use_container_width=True
        )

    with button_col2:
        reset_button = st.button(
            "🔄 Reset",
            use_container_width=True
        )

if reset_button:
    reset_app()
    st.rerun()

# Progress and logs section
st.write("---")
st.write("### Progress & Logs")

# Progress bar placeholder
progress_placeholder = st.empty()
status_placeholder = st.empty()

# Logs area
logs_container = st.container()
with logs_container:
    st.write("**Logs:**")
    logs_area = st.empty()

    if st.session_state.logs:
        logs_text = "\n".join([f"> {log}" for log in st.session_state.logs[-20:]])  # Show last 20 logs
        logs_area.code(logs_text, language=None)
    else:
        logs_area.code("> Waiting for input...", language=None)

# Generate report logic
if generate_button and research_topic:
    # Auto-scroll to progress section
    st.markdown("""
    <script>
        window.parent.document.querySelector('section[data-testid="stSidebar"]').scrollIntoView({behavior: 'smooth'});
        setTimeout(function() {
            const progressSection = window.parent.document.evaluate(
                "//div[contains(text(), 'Progress & Logs')]",
                window.parent.document,
                null,
                XPathResult.FIRST_ORDERED_NODE_TYPE,
                null
            ).singleNodeValue;
            if (progressSection) {
                progressSection.scrollIntoView({behavior: 'smooth', block: 'start'});
            }
        }, 100);
    </script>
    """, unsafe_allow_html=True)

    st.session_state.processing = True
    st.session_state.logs = []
    st.session_state.report_path = None
    st.session_state.json_path = None
    st.session_state.report_content = None

    # Get selected sources
    sources = [source for source, selected in selected_sources.items() if selected]

    if not sources:
        st.error("⚠️ Please select at least one source")
        st.session_state.processing = False
        st.stop()

    add_log(f"Starting research for: {research_topic}")
    add_log(f"Sources: {', '.join(sources)}")
    add_log(f"Max papers: {max_papers}")

    try:
        # Create output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{report_name}_{timestamp}.md"

        # Initialize progress
        progress_placeholder.progress(0)
        status_placeholder.info("🔄 Initializing research agent...")

        # Create research agent
        add_log("Initializing research agent...")
        logs_text = "\n".join([f"> {log}" for log in st.session_state.logs[-20:]])
        logs_area.code(logs_text, language=None)

        agent = ResearchAgent(max_papers=max_papers)
        progress_placeholder.progress(10)

        # Fetch papers
        status_placeholder.info(f"🔍 Fetching papers from {', '.join(sources)}...")
        add_log(f"Fetching papers from {', '.join(sources)}...")
        logs_text = "\n".join([f"> {log}" for log in st.session_state.logs[-20:]])
        logs_area.code(logs_text, language=None)

        papers = agent.fetch_papers(research_topic, sources=sources)
        progress_placeholder.progress(30)

        if not papers:
            status_placeholder.warning("⚠️ No papers found for the query")
            add_log("No papers found")
            st.session_state.processing = False
            st.stop()

        add_log(f"Found {len(papers)} papers")
        logs_text = "\n".join([f"> {log}" for log in st.session_state.logs[-20:]])
        logs_area.code(logs_text, language=None)

        # Summarize papers
        summarized_papers = []
        for i, paper in enumerate(papers):
            progress = 30 + int((i / len(papers)) * 40)
            progress_placeholder.progress(progress)
            status_placeholder.info(f"📝 Summarizing paper {i+1}/{len(papers)}: {paper['title'][:50]}...")
            add_log(f"Summarizing paper {i+1}/{len(papers)}")
            logs_text = "\n".join([f"> {log}" for log in st.session_state.logs[-20:]])
            logs_area.code(logs_text, language=None)

            summarized = agent.summarize_paper(paper)
            summarized_papers.append(summarized)

        progress_placeholder.progress(70)

        # Generate perspective title
        status_placeholder.info("🎯 Generating perspective title...")
        add_log("Generating perspective title...")
        logs_text = "\n".join([f"> {log}" for log in st.session_state.logs[-20:]])
        logs_area.code(logs_text, language=None)

        perspective_title = agent.generate_perspective_title(research_topic)
        progress_placeholder.progress(80)

        # Synthesize research
        status_placeholder.info("🔬 Synthesizing research insights...")
        add_log("Synthesizing research insights...")
        logs_text = "\n".join([f"> {log}" for log in st.session_state.logs[-20:]])
        logs_area.code(logs_text, language=None)

        synthesis = agent.synthesize_research(summarized_papers, research_topic)
        progress_placeholder.progress(90)

        # Generate report
        status_placeholder.info("📄 Generating final report...")
        add_log("Generating final report...")
        logs_text = "\n".join([f"> {log}" for log in st.session_state.logs[-20:]])
        logs_area.code(logs_text, language=None)

        report = agent.report_generator.generate_markdown_report(
            query=research_topic,
            perspective_title=perspective_title,
            papers=summarized_papers,
            executive_summary=synthesis['executive_summary'],
            key_themes=synthesis['key_themes'],
            recommendations=synthesis['recommendations'],
            conclusion=synthesis['conclusion']
        )

        # Save report
        os.makedirs("./data", exist_ok=True)
        report_path = os.path.join("./data", output_filename)
        json_path = report_path.replace('.md', '.json')

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        # Save JSON data
        json_data = {
            'query': research_topic,
            'perspective_title': perspective_title,
            'generated_at': datetime.now().isoformat(),
            'total_papers': len(summarized_papers),
            'sources': sources,
            'papers': summarized_papers,
            'synthesis': synthesis
        }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        progress_placeholder.progress(100)
        status_placeholder.success("✅ Report generated successfully! You can scroll down to preview and download the ")
        add_log(f"Report saved to: {report_path}")
        add_log(f"JSON data saved to: {json_path}")

        # Store in session state
        st.session_state.report_path = report_path
        st.session_state.json_path = json_path
        st.session_state.report_content = report

        # Add to chat history
        add_to_chat_history(research_topic, report_path)

        logs_text = "\n".join([f"> {log}" for log in st.session_state.logs[-20:]])
        logs_area.code(logs_text, language=None)

    except Exception as e:
        status_placeholder.error(f"❌ Error: {str(e)}")
        add_log(f"Error: {str(e)}")
        logs_text = "\n".join([f"> {log}" for log in st.session_state.logs[-20:]])
        logs_area.code(logs_text, language=None)
        import traceback
        st.exception(e)

    finally:
        st.session_state.processing = False

# Results section
if st.session_state.report_path and st.session_state.report_content:
    st.write("---")
    st.write("### 📊 Results")

    # Download buttons
    download_col1, download_col2 = st.columns(2)

    with download_col1:
        st.download_button(
            label="📥 Download Markdown Report",
            data=st.session_state.report_content,
            file_name=os.path.basename(st.session_state.report_path),
            mime="text/markdown",
            use_container_width=True
        )

    with download_col2:
        if st.session_state.json_path and os.path.exists(st.session_state.json_path):
            with open(st.session_state.json_path, 'r', encoding='utf-8') as f:
                json_content = f.read()

            st.download_button(
                label="📥 Download JSON Data",
                data=json_content,
                file_name=os.path.basename(st.session_state.json_path),
                mime="application/json",
                use_container_width=True
            )

    # Preview
    st.write("**Preview:**")
    with st.expander("📄 View Report", expanded=True):
        st.markdown(st.session_state.report_content)

# Sidebar with chat history
with st.sidebar:
    st.write("### 💬 Chat History")

    if st.session_state.chat_history:
        for idx, entry in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"🔍 {entry['topic'][:40]}...", expanded=False):
                st.caption(f"📅 {entry['timestamp']}")
                st.caption(f"📄 {os.path.basename(entry['report_path'])}")

                # Create two columns for Load and Delete buttons
                btn_col1, btn_col2 = st.columns(2)

                with btn_col1:
                    if st.button(f"Load", key=f"load_{idx}", use_container_width=True):
                        if os.path.exists(entry['report_path']):
                            with open(entry['report_path'], 'r', encoding='utf-8') as f:
                                st.session_state.report_content = f.read()
                            st.session_state.report_path = entry['report_path']
                            json_path = entry['report_path'].replace('.md', '.json')
                            if os.path.exists(json_path):
                                st.session_state.json_path = json_path
                            st.rerun()

                with btn_col2:
                    if st.button(f"🗑️", key=f"delete_{idx}", use_container_width=True, type="secondary"):
                        # Get the actual index in the original list (not reversed)
                        actual_idx = len(st.session_state.chat_history) - 1 - idx
                        st.session_state.chat_history.pop(actual_idx)
                        st.rerun()
    else:
        st.info("No research history yet. Generate your first report!")

    st.write("---")

    st.write("### 📚 Tips")
    st.markdown("""
    - Use specific research queries for better results
    - Select multiple sources for comprehensive coverage
    - Start with 5-10 papers for faster processing
    - Check the logs for detailed progress
    """)

    st.write("---")
    st.caption("Powered by AWS Bedrock & Agno Framework")


