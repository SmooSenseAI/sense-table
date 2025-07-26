import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'SenseTable',
  description: 'Your AI data explorer',
  
  // Base URL for GitHub Pages deployment
  base: '/sense-table',
  
 
  
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
            { text: 'Getting Started', link: '/guide/' },
            { text: 'Installation', link: '/guide/installation' },
            { text: 'Configuration', link: '/guide/configuration' }
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