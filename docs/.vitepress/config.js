import { defineConfig } from 'vitepress'
import { tooltipPlugin } from './plugins/tooltip-plugin.js'

export default defineConfig({
  title: 'SenseTable',
  description: 'Your AI data explorer',
  
  // Base URL for GitHub Pages deployment
  base: '/sense-table',
  
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
}) 