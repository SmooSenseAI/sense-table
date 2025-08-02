<template>
  <img 
    :src="currentImageSrc" 
    :alt="alt" 
    :class="imageClass"
    @load="onImageLoad"
    @error="onImageError"
  />
</template>

<script setup>
import { computed, ref } from 'vue'
import { useData } from 'vitepress'

const props = defineProps({
  src: {
    type: String,
    required: true
  },
  alt: {
    type: String,
    default: ''
  },
  imageClass: {
    type: String,
    default: ''
  }
})

const { isDark, site } = useData()
const imageLoaded = ref(false)
const imageError = ref(false)

// Function to get the appropriate image source based on theme
const getThemedImageSrc = (baseSrc, isDarkMode) => {
  if (!baseSrc) return ''
  
  // If the image already has a theme suffix, replace it
  if (baseSrc.includes('_dark.jpg')) {
    const result = isDarkMode ? baseSrc : baseSrc.replace('_dark.jpg', '_light.jpg')
    return result
  }
  
  if (baseSrc.includes('_light.jpg')) {
    const result = isDarkMode ? baseSrc.replace('_light.jpg', '_dark.jpg') : baseSrc
    return result
  }
  
  // If no theme suffix, add one based on current mode
  const basePath = baseSrc.replace(/\.(jpg|jpeg|png|gif|webp)$/i, '')
  const extension = baseSrc.match(/\.(jpg|jpeg|png|gif|webp)$/i)?.[0] || '.jpg'
  const result = `${basePath}_${isDarkMode ? 'dark' : 'light'}${extension}`
  return result
}

// Function to add base URL to image path
const addBaseUrl = (imagePath) => {
  const base = site.value?.base || ''
  
  // Ensure imagePath starts with / (but don't add if it already has one)
  const normalizedPath = imagePath.startsWith('/') ? imagePath : `/${imagePath}`
  
  // Remove trailing slash from base if it exists
  const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base
  
  // Combine base and path
  const result = `${cleanBase}${normalizedPath}`
  return result
}

// Computed property for current image source
const currentImageSrc = computed(() => {
  const themedSrc = getThemedImageSrc(props.src, isDark.value)
  const finalSrc = addBaseUrl(themedSrc)
  return finalSrc
})

const onImageLoad = () => {
  imageLoaded.value = true
  imageError.value = false
}

const onImageError = () => {
  imageError.value = true
  console.error(`❌ Failed to load themed image: ${currentImageSrc.value}`)
  console.error(`Original src: ${props.src}, isDark: ${isDark.value}`)
}
</script>

<style scoped>
img {
  transition: opacity 0.3s ease;
}
</style> 