# Getting Started

Welcome to SenseTable! This guide will help you get up and running quickly.


## Quick Start

SenseTable provides CLI, Python package and MacOS app (coming). You can choose anyone that you prefer.

### CLI (Homebrew - Recommended)

```bash
brew tap SmooSenseAI/tap
brew install sense-table
```

After installation, start SenseTable:

```bash
sense-table --port 8000
```

### Python package

```bash
pip install sense-table
```

After installation, start SenseTable:

```bash
sense-table --port 8000
```

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