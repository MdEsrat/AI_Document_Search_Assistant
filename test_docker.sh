#!/bin/bash
# Quick test script for Docker deployment

echo "🐳 Building Docker image..."
docker build -t doc-search-assistant .

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "🚀 Starting container on port 7860..."
    echo "   Access at: http://localhost:7860"
    echo ""
    echo "Press Ctrl+C to stop"
    echo ""
    docker run -p 7860:7860 --rm doc-search-assistant
else
    echo "❌ Build failed. Check the error messages above."
    exit 1
fi
