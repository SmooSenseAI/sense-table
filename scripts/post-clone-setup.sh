#!/bin/bash

# Post-clone setup script for SenseTable
# This script should be run after cloning the repository to set up the development environment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Setting up SenseTable development environment..."

# Check if we're in the right directory
if [ ! -f "$PROJECT_ROOT/Makefile" ]; then
    echo "❌ Error: Makefile not found. Please run this script from the project root."
    exit 1
fi

# Install git hooks
echo "🔧 Installing git hooks..."
"$SCRIPT_DIR/install-hooks.sh"

# Set up git configuration for this project
echo "⚙️  Configuring git..."
git config core.hooksPath .git/hooks

echo "✅ Development environment setup complete!"
echo ""
echo "Next steps:"
echo "  1. Install dependencies: make env"
echo "  2. Run tests: make test"
echo "  3. Start development: make dev"
echo ""
echo "The git hooks are now active and will:"
echo "  • Run pre-commit checks before each commit"
echo "  • Run tests before each push" 