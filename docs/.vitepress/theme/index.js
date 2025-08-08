import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import CustomFooter from './components/CustomFooter.vue'
import TooltipLink from './components/TooltipLink.vue'
import ThemedImage from './components/ThemedImage.vue'
import ThemedVideo from './components/ThemedVideo.vue'
import VideoFeatures from './components/VideoFeatures.vue'
import Layout from './Layout.vue'
import './style.css'

export default {
  extends: DefaultTheme,
  Layout,
  enhanceApp({ app }) {
    // Register the TooltipLink component globally
    app.component('TooltipLink', TooltipLink)
    // Register the ThemedImage component globally
    app.component('ThemedImage', ThemedImage)
    // Register the ThemedVideo component globally
    app.component('ThemedVideo', ThemedVideo)
    // Register the VideoFeatures component globally
    app.component('VideoFeatures', VideoFeatures)
  }
} 