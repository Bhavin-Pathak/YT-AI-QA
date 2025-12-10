#!/bin/bash
# Start the restructured RAG YouTube Assistant backend

echo "Starting RAG YouTube Assistant (Restructured Version)"
echo "======================================================"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found!"
    echo "Make sure you're in the backend directory."
    exit 1
fi

# Start the server
echo "Starting FastAPI server on http://localhost:8001"
echo "Press Ctrl+C to stop the server"
echo ""

python3 main.py
