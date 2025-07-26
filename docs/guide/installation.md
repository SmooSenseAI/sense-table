# Installation

This page covers how to set up and customize your VitePress documentation site.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** version 18 or higher
- **npm** or **yarn** package manager

## Initial Setup

### 1. Clone or Download

If you're starting from this template:

```bash
git clone https://github.com/SmooSenseAI/sense-table-doc.git
cd sense-table-doc
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start Development Server

```bash
npm run docs:dev
```

Your site will be available at `http://localhost:5173`

## Project Structure

Here's the recommended file structure for your documentation:

```
sense-table-doc/
├── .vitepress/
│   ├── config.js          # Site configuration
│   └── dist/              # Built files (auto-generated)
├── guide/
│   ├── index.md           # Guide homepage
│   ├── installation.md    # This page
│   └── configuration.md   # Configuration guide
├── api/
│   ├── index.md           # API overview
│   └── methods.md         # API methods
├── index.md               # Site homepage
└── package.json           # Dependencies and scripts
```

## Adding Content

### Creating New Pages

1. Create a new `.md` file in the appropriate directory
2. Add frontmatter if needed:

```markdown
---
title: Page Title
description: Page description
---

# Your Content Here
```

3. Update the navigation in `.vitepress/config.js` if needed

### Adding Images

Place images in a `public` directory at the root:

```
public/
├── images/
│   └── screenshot.png
└── logo.svg
```

Reference them in Markdown:

```markdown
![Screenshot](/images/screenshot.png)
```

## Customization

### Updating Site Information

Edit `.vitepress/config.js` to update:

- Site title and description
- Navigation menu
- Social links
- Footer information

### Styling

You can customize the appearance by:

1. Overriding CSS variables
2. Adding custom CSS
3. Using custom Vue components

See the [Configuration Guide](/guide/configuration) for detailed customization options. 