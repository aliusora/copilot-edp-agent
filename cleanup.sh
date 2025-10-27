#!/bin/bash
# cleanup.sh - Remove old/unused files before deployment

echo "🧹 Starting repository cleanup..."

# Remove old agent directory (Mixtral implementation)
if [ -d "agent" ]; then
    echo "❌ Removing agent/ directory..."
    rm -rf agent/
fi

# Remove old test file
if [ -f "test_local_mixtral.py" ]; then
    echo "❌ Removing test_local_mixtral.py..."
    rm -f test_local_mixtral.py
fi

# Remove VS Code MCP config
if [ -f ".vscode/mcp.json" ]; then
    echo "❌ Removing .vscode/mcp.json..."
    rm -f .vscode/mcp.json
fi

# Remove .vscode directory if empty
if [ -d ".vscode" ] && [ -z "$(ls -A .vscode)" ]; then
    echo "❌ Removing empty .vscode/ directory..."
    rmdir .vscode/
fi

# Remove cache if exists
if [ -d ".doc_cache" ]; then
    echo "❌ Removing .doc_cache/ (will be regenerated on first run)..."
    rm -rf .doc_cache/
fi

# Remove __pycache__ directories
echo "❌ Removing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📋 Remaining files:"
ls -lh

echo ""
echo "🚀 Next steps:"
echo "1. Review changes: git status"
echo "2. Test the app: streamlit run app.py"
echo "3. Commit changes: git add . && git commit -m 'Clean up repository for deployment'"
echo "4. Push to GitHub: git push origin main"
