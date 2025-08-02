import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import CustomFooter from './components/CustomFooter.vue'
import TooltipLink from './components/TooltipLink.vue'
import ThemedImage from './components/ThemedImage.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    // Register the TooltipLink component globally
    app.component('TooltipLink', TooltipLink)
    // Register the ThemedImage component globally
    app.component('ThemedImage', ThemedImage)
  },
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      // Override the footer slot with our custom component
      'layout-bottom': () => h(CustomFooter)
    })
  }
} 