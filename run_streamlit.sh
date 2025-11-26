#!/bin/bash
# Script to run the Streamlit frontend for AI-Powered Research Agent

echo "================================================"
echo "AI-Powered Research Agent - Streamlit Frontend"
echo "================================================"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "⚠️  Streamlit is not installed."
    echo "Installing Streamlit..."
    pip install streamlit>=1.28.0
    echo ""
fi

# Check for required environment variables
if [ -z "$BEDROCK_MODEL_ID" ]; then
    echo "⚠️  Warning: BEDROCK_MODEL_ID is not set"
    echo "Please set the following environment variables:"
    echo ""
    echo "  export BEDROCK_MODEL_ID=\"your-model-id\""
    echo "  export AWS_REGION=\"us-east-1\""
    echo "  export AWS_ACCESS_KEY_ID=\"your-access-key\""
    echo "  export AWS_SECRET_ACCESS_KEY=\"your-secret-key\""
    echo ""
    echo "Or create a .env file with these variables."
    echo ""
fi

# Check if .env file exists
if [ -f .env ]; then
    echo "✅ Found .env file"
    echo ""
fi

echo "🚀 Starting Streamlit app..."
echo "The app will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run streamlit
streamlit run streamlit_app.py

