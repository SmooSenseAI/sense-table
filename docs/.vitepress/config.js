import { defineConfig } from 'vitepress'
import { tooltipPlugin } from './plugins/tooltip-plugin.js'
import { withMermaid } from 'vitepress-plugin-mermaid'


export default withMermaid(defineConfig({
  title: 'SenseTable',
  description: 'Your AI data explorer',
  
  // Base URL for GitHub Pages deployment
  base: '/sense-table',
  
  // Google Analytics
  head: [
    [
      'script',
      {
        async: true,
        src: 'https://www.googletagmanager.com/gtag/js?id=G-XSNBTBWZC4'
      }
    ],
    [
      'script',
      {},
      `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-XSNBTBWZC4');
      `
    ]
  ],
  
  // Markdown configuration
  markdown: {
    config: (md) => {
      tooltipPlugin(md)
    }
  },
  
  themeConfig: {
    // Navigation menu
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/' },
      { text: 'Blog', link: '/blog/' }
    ],

    // Sidebar navigation
    sidebar: {
      '/guide/': [
        {
          text: 'Guide',
          items: [
            { text: 'Introduction', link: '/guide/' },
            { text: 'Start', link: '/guide/start' },
            { text: 'Folder Browser', link: '/guide/folder-browser' },
            { text: 'Tabular slice-n-dice', link: '/guide/tabular-slice-n-dice' },
            { text: 'Graphical slice-n-dice', link: '/guide/graphical-slice-n-dice' },
            { text: 'Serving images', link: '/guide/serve-images' },
            { text: 'CV visualization', link: '/guide/cv-visualization' },
            { text: 'Configuration', link: '/guide/configuration' },
          ]
        }
      ],
      '/blog/': [
        {
          text: 'Blog',
          items: [
            { text: 'Overview', link: '/blog/' },
            { text: 'Methods', link: '/blog/methods' }
          ]
        }
      ]
    },

    // Social links
    socialLinks: [
      { icon: 'github', link: 'https://github.com/SmooSenseAI/sense-table' }
    ],



    // Enable search
    search: {
      provider: 'local'
    }
  },

  // Clean URLs (remove .html)
  cleanUrls: true,

  // Last updated
  lastUpdated: true
})) 