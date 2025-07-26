# SenseTable

A modern, fast documentation website built with VitePress. Write your documentation in Markdown and automatically compile it to a beautiful static site.

## ✨ Features

- 📝 **Markdown-powered** - Write docs in simple Markdown format
- ⚡ **Lightning fast** - Powered by Vite for instant hot-reload
- 🎨 **Beautiful themes** - Professional, responsive design out of the box
- 🔍 **Built-in search** - Full-text search functionality
- 📱 **Mobile-friendly** - Works perfectly on all devices
- 🚀 **Easy deployment** - Deploy anywhere as static files

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Development

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run docs:dev
   ```
   
   Your site will be available at `http://localhost:5173`

3. **Build for production**:
   ```bash
   npm run docs:build
   ```
   
   Static files will be generated in `.vitepress/dist`

4. **Preview production build**:
   ```bash
   npm run docs:preview
   ```

## 📁 Project Structure

```
├── .vitepress/
│   ├── config.js          # Site configuration
│   └── dist/              # Built files (auto-generated)
├── guide/                 # Guide documentation
│   ├── index.md          # Getting started
│   ├── installation.md   # Installation guide
│   └── configuration.md  # Configuration options
├── api/                   # API documentation
│   ├── index.md          # API overview
│   └── methods.md        # Method references
├── public/               # Static assets
│   └── logo.svg         # Site logo
├── index.md             # Homepage
└── package.json         # Dependencies
```

## ✍️ Writing Documentation

### Creating Pages

1. Create `.md` files in the appropriate directory
2. Add frontmatter if needed:
   ```markdown
   ---
   title: Page Title
   description: Page description
   ---
   
   # Your content here
   ```

3. Update navigation in `.vitepress/config.js`

### Markdown Features

VitePress supports extended Markdown features:

#### Code Blocks
\`\`\`javascript
function hello() {
  console.log('Hello, VitePress!')
}
\`\`\`

#### Custom Containers
::: tip
This is a helpful tip
:::

::: warning
This is a warning
:::

::: danger
This is important information
:::

#### Tables
| Feature | Status |
|---------|--------|
| Fast | ✅ |
| SEO-friendly | ✅ |
| Mobile responsive | ✅ |

### Adding Images

Place images in the `public/` directory:

```markdown
![Description](/images/screenshot.png)
```

## ⚙️ Configuration

Edit `.vitepress/config.js` to customize:

- **Site metadata** (title, description)
- **Navigation menu** (header and sidebar)
- **Theme settings** (colors, layout)
- **Social links** (GitHub, Twitter, etc.)

See the [Configuration Guide](./guide/configuration.md) for detailed options.

## 🎨 Customization

### Styling

Override CSS variables in `.vitepress/theme/style.css`:

```css
:root {
  --vp-c-brand-1: #your-color;
  --vp-c-brand-2: #your-color;
}
```

### Custom Components

Add Vue components in `.vitepress/theme/` and use them in Markdown:

```markdown
<CustomComponent />
```

## 🚀 Deployment

### GitHub Pages

1. Enable GitHub Pages in repository settings
2. Add deployment workflow (see [Configuration Guide](./guide/configuration.md))
3. Push to main branch to trigger deployment

### Netlify

1. Connect your repository to Netlify
2. Set build command: `npm run docs:build`
3. Set publish directory: `.vitepress/dist`

### Vercel

1. Import project to Vercel
2. Vercel will auto-detect VitePress settings
3. Deploy with one click

### Other Platforms

Since VitePress generates static files, you can deploy to:
- AWS S3 + CloudFront
- Google Cloud Storage
- Azure Static Web Apps
- Any static hosting service

## 📚 Learn More

- [VitePress Documentation](https://vitepress.dev/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Vue.js Documentation](https://vuejs.org/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

- **Documentation**: Browse the [Guide](./guide/) section
- **Issues**: [GitHub Issues](https://github.com/SmooSenseAI/sense-table/issues)
- **Discussions**: [GitHub Discussions](https://github.com/SmooSenseAI/sense-table/discussions)

---

**Happy documenting!** 🎉 