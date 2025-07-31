#!/bin/bash

# Script to install git hooks for the SenseTable project
# This script copies the hooks from .git/hooks to make them available for all developers

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"

echo "🔧 Installing git hooks for SenseTable..."

# Check if we're in the right directory
if [ ! -f "$PROJECT_ROOT/Makefile" ]; then
    echo "❌ Error: Makefile not found. Please run this script from the project root."
    exit 1
fi

# Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_DIR"

# Copy hooks and make them executable
echo "📋 Installing pre-commit hook..."
cp "$SCRIPT_DIR/../.git/hooks/pre-commit" "$HOOKS_DIR/pre-commit"
chmod +x "$HOOKS_DIR/pre-commit"

echo "📋 Installing pre-push hook..."
cp "$SCRIPT_DIR/../.git/hooks/pre-push" "$HOOKS_DIR/pre-push"
chmod +x "$HOOKS_DIR/pre-push"

echo "✅ Git hooks installed successfully!"
echo ""
echo "The following hooks are now active:"
echo "  • pre-commit: Runs basic checks before each commit"
echo "  • pre-push: Runs tests and ensures clean git tree before push"
echo ""
echo "To skip hooks in emergency situations, use:"
echo "  git commit --no-verify  # Skip pre-commit hook"
echo "  git push --no-verify    # Skip pre-push hook" 