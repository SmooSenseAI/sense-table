# Getting Started

Welcome to the documentation site! This guide will help you get up and running quickly.

## What is This?

This is a VitePress-powered documentation site that allows you to:

- ✍️ Write documentation in **Markdown**
- 🏗️ Build static websites automatically
- 🎨 Customize the look and feel
- 🔍 Provide built-in search functionality
- 📱 Ensure mobile-friendly responsive design

## Quick Start

### 1. Development

To start the development server and preview your changes:

```bash
npm run docs:dev
```

This will start a local development server at `http://localhost:5173`

### 2. Building

To build the static site for production:

```bash
npm run docs:build
```

The built files will be generated in the `.vitepress/dist` directory.

### 3. Preview

To preview the built site locally:

```bash
npm run docs:preview
```

## Next Steps

- [Installation Guide](/guide/installation) - Learn how to customize and extend
- [Configuration](/guide/configuration) - Discover configuration options
- [Blog](/blog/) - Read our latest updates and tutorials

## Writing Documentation

All your documentation files should be written in Markdown (`.md`) format. VitePress extends standard Markdown with additional features:

### Code Blocks

\`\`\`javascript
function hello() {
  console.log('Hello, VitePress!')
}
\`\`\`

### Custom Containers

::: tip
This is a tip container
:::

::: warning
This is a warning container
:::

::: danger
This is a danger container
:::

### Tables

| Feature | Description |
|---------|-------------|
| Markdown | Write in simple Markdown |
| Static | Builds to static files |
| Fast | Powered by Vite | 