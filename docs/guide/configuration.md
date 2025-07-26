# Configuration

Learn how to configure and customize your VitePress documentation site.

## Basic Configuration

The main configuration file is located at `.vitepress/config.js`. Here are the key sections:

### Site Metadata

```javascript
export default defineConfig({
  title: 'Your Site Title',
  description: 'Your site description',
  // ... other options
})
```

### Theme Configuration

```javascript
themeConfig: {
  // Site logo
  logo: '/logo.svg',
  
  // Navigation
  nav: [
    { text: 'Home', link: '/' },
    { text: 'Guide', link: '/guide/' }
  ],
  
  // Sidebar
  sidebar: {
    '/guide/': [
      { text: 'Getting Started', link: '/guide/' }
    ]
  }
}
```

## Navigation

### Top Navigation

Add items to the top navigation bar:

```javascript
nav: [
  { text: 'Home', link: '/' },
  { text: 'Guide', link: '/guide/' },
  { 
    text: 'Dropdown',
    items: [
      { text: 'Option 1', link: '/option1' },
      { text: 'Option 2', link: '/option2' }
    ]
  }
]
```

### Sidebar Navigation

Configure sidebar navigation for different sections:

```javascript
sidebar: {
  '/guide/': [
    {
      text: 'Getting Started',
      collapsed: false,
      items: [
        { text: 'Introduction', link: '/guide/' },
        { text: 'Installation', link: '/guide/installation' }
      ]
    }
  ]
}
```

## Advanced Features

### Search

Enable local search:

```javascript
themeConfig: {
  search: {
    provider: 'local',
    options: {
      locales: {
        zh: {
          translations: {
            button: {
              buttonText: '搜索文档',
              buttonAriaLabel: '搜索文档'
            }
          }
        }
      }
    }
  }
}
```

### Social Links

Add social media links:

```javascript
socialLinks: [
  { icon: 'github', link: 'https://github.com/your-repo' },
  { icon: 'twitter', link: 'https://twitter.com/your-handle' },
  { icon: 'discord', link: 'https://discord.gg/your-server' }
]
```

### Custom CSS

Create `.vitepress/theme/style.css` to add custom styles:

```css
:root {
  --vp-c-brand-1: #646cff;
  --vp-c-brand-2: #747bff;
}

.custom-block {
  padding: 16px;
  border-radius: 8px;
}
```

### Custom Components

You can use Vue components in your Markdown:

1. Create `.vitepress/theme/index.js`:

```javascript
import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import CustomComponent from './CustomComponent.vue'

export default {
  extends: DefaultTheme,
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      // Slot content
    })
  },
  enhanceApp({ app, router, siteData }) {
    app.component('CustomComponent', CustomComponent)
  }
}
```

2. Use in Markdown:

```markdown
<CustomComponent />
```

## Build Configuration

### Output Directory

Change the build output directory:

```javascript
export default defineConfig({
  outDir: '../dist',
  // ...
})
```

### Base URL

If deploying to a subdirectory:

```javascript
export default defineConfig({
  base: '/my-docs/',
  // ...
})
```

## Deployment

### GitHub Pages

Add a workflow file `.github/workflows/deploy.yml`:

```yaml
name: Deploy VitePress site to Pages

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm run docs:build
      - uses: actions/upload-pages-artifact@v2
        with:
          path: .vitepress/dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v2
        id: deployment
```

### Netlify

Add `netlify.toml`:

```toml
[build]
  publish = ".vitepress/dist"
  command = "npm run docs:build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
``` 