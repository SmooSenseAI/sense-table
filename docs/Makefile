# Documentation Site Makefile
# Commands for building and deploying VitePress documentation

.PHONY: help install dev build preview clean deploy deploy-force

# Default target
help:
	@echo "Documentation Site - Available Commands:"
	@echo ""
	@echo "  make install      - Install dependencies"
	@echo "  make dev          - Start development server"
	@echo "  make build        - Build static site for production"
	@echo "  make preview      - Preview built site locally"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make deploy       - Build and deploy to GitHub Pages"
	@echo "  make deploy-force - Force deploy to GitHub Pages (overwrites)"
	@echo "  make help         - Show this help message"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	npm install

# Start development server
dev:
	@echo "🚀 Starting development server..."
	npm run docs:dev

# Build static site
build:
	@echo "🔨 Building documentation..."
	npm run docs:build

# Preview built site
preview: build
	@echo "👀 Previewing built site..."
	npm run docs:preview

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf .vitepress/dist
	rm -rf .vitepress/cache
	rm -rf node_modules/.cache

# Deploy to GitHub Pages
deploy: build
	@echo "🚀 Deploying to GitHub Pages..."
	@if [ ! -d ".vitepress/dist" ]; then \
		echo "❌ Build directory not found. Run 'make build' first."; \
		exit 1; \
	fi
	@echo "📁 Switching to dist directory..."
	cd .vitepress/dist && \
	git init && \
	git add -A && \
	git commit -m "Deploy documentation - $$(date '+%Y-%m-%d %H:%M:%S')" && \
	git branch -M gh-pages && \
	git remote remove origin 2>/dev/null || true && \
	git remote add origin $$(git -C ../.. config --get remote.origin.url) && \
	git push -f origin gh-pages
	@echo "✅ Deployment complete! Visit: https://$$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1.github.io\/\2/')"

# Force deploy (useful if you need to overwrite)
deploy-force: clean build
	@echo "⚡ Force deploying to GitHub Pages..."
	cd .vitepress/dist && \
	git init && \
	git add -A && \
	git commit -m "Force deploy documentation - $$(date '+%Y-%m-%d %H:%M:%S')" && \
	git branch -M gh-pages && \
	git remote remove origin 2>/dev/null || true && \
	git remote add origin $$(git -C ../.. config --get remote.origin.url) && \
	git push -f origin gh-pages
	@echo "✅ Force deployment complete!"

# Setup GitHub Pages (run once)
setup-pages:
	@echo "⚙️  Setting up GitHub Pages..."
	@echo "1. Go to your GitHub repository settings"
	@echo "2. Navigate to 'Pages' section"
	@echo "3. Set source to 'Deploy from a branch'"
	@echo "4. Select 'gh-pages' branch and '/ (root)' folder"
	@echo "5. Save settings"
	@echo "6. Run 'make deploy' to deploy your site"

# Quick development workflow
quick: clean install build
	@echo "✅ Quick setup complete! Run 'make dev' to start development."
