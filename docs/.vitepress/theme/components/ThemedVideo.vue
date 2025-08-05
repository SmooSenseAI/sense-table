<template>
  <video 
    :src="currentVideoSrc" 
    :autoplay="autoplay"
    :loop="loop"
    :muted="muted"
    :playsinline="playsinline"
    :controls="controls"
    :class="videoClass"
    @loadstart="onVideoLoadStart"
    @error="onVideoError"
  >
    <source :src="currentVideoSrc" :type="videoType" />
    Your browser does not support the video tag.
  </video>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useData } from 'vitepress'

const props = defineProps({
  src: {
    type: String,
    required: true
  },
  autoplay: {
    type: Boolean,
    default: true
  },
  loop: {
    type: Boolean,
    default: true
  },
  muted: {
    type: Boolean,
    default: true
  },
  playsinline: {
    type: Boolean,
    default: true
  },
  controls: {
    type: Boolean,
    default: true
  },
  videoClass: {
    type: String,
    default: ''
  },
  videoType: {
    type: String,
    default: 'video/webm'
  }
})

const { isDark, site } = useData()
const videoLoaded = ref(false)
const videoError = ref(false)

// Function to get the appropriate video source based on theme
const getThemedVideoSrc = (baseSrc, isDarkMode) => {
  if (!baseSrc) return ''
  
  // If the video already has a theme suffix, replace it
  if (baseSrc.includes('_dark.webm')) {
    const result = isDarkMode ? baseSrc : baseSrc.replace('_dark.webm', '_light.webm')
    return result
  }
  
  if (baseSrc.includes('_light.webm')) {
    const result = isDarkMode ? baseSrc.replace('_light.webm', '_dark.webm') : baseSrc
    return result
  }
  
  if (baseSrc.includes('_dark.mp4')) {
    const result = isDarkMode ? baseSrc : baseSrc.replace('_dark.mp4', '_light.mp4')
    return result
  }
  
  if (baseSrc.includes('_light.mp4')) {
    const result = isDarkMode ? baseSrc.replace('_light.mp4', '_dark.mp4') : baseSrc
    return result
  }
  
  // If no theme suffix, add one based on current mode
  const basePath = baseSrc.replace(/\.(webm|mp4|avi|mov)$/i, '')
  const extension = baseSrc.match(/\.(webm|mp4|avi|mov)$/i)?.[0] || '.webm'
  const result = `${basePath}_${isDarkMode ? 'dark' : 'light'}${extension}`
  return result
}

// Function to add base URL to video path
const addBaseUrl = (videoPath) => {
  const base = site.value?.base || ''
  
  // Ensure videoPath starts with / (but don't add if it already has one)
  const normalizedPath = videoPath.startsWith('/') ? videoPath : `/${videoPath}`
  
  // Remove trailing slash from base if it exists
  const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base
  
  // Combine base and path
  const result = `${cleanBase}${normalizedPath}`
  return result
}

// Computed property for current video source
const currentVideoSrc = computed(() => {
  const themedSrc = getThemedVideoSrc(props.src, isDark.value)
  const finalSrc = addBaseUrl(themedSrc)
  return finalSrc
})

const onVideoLoadStart = () => {
  videoLoaded.value = true
  videoError.value = false
}

const onVideoError = () => {
  videoError.value = true
  console.error(`❌ Failed to load themed video: ${currentVideoSrc.value}`)
  console.error(`Original src: ${props.src}, isDark: ${isDark.value}`)
}
</script>

<style scoped>
video {
  transition: opacity 0.3s ease;
  max-width: 100%;
  height: auto;
}
</style> 