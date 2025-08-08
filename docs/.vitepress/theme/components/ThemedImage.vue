<template>
  <img 
    :src="currentImageSrc" 
    :alt="alt" 
    :class="[imageClass, { 'clickable-image': !isInlineImage }]"
    @load="onImageLoad"
    @error="onImageError"
    @click="handleImageClick"
  />

  <!-- Modal for full-size image -->
  <div v-if="showModal" class="modal-overlay" @click="closeModal">
    <div class="modal-content">
      <button class="modal-close" @click="closeModal">&times;</button>
      <img 
        :src="currentImageSrc"
        :alt="alt"
        class="modal-image"
        @click.stop
      />
      <div v-if="alt" class="modal-caption" @click.stop>{{ alt }}</div>
    </div>
  </div>
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
const showModal = ref(false)

// Check if image is inline
const isInlineImage = computed(() => {
  return props.imageClass.includes('inline')
})

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

const handleImageClick = () => {
  if (!isInlineImage.value) {
    openModal()
  }
}

const openModal = () => {
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  showModal.value = false
  document.body.style.overflow = ''
}
</script>

<style scoped>
img {
  transition: opacity 0.3s ease;
}

/* Clickable image cursor */
.clickable-image {
  cursor: pointer;
  transition: all 0.3s ease;
}

.clickable-image:hover {
  opacity: 0.8;
  transform: scale(1.02);
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 0;
  backdrop-filter: blur(4px);
}

.modal-content {
  position: relative;
  width: 100vw;
  height: 100vh;
  background: transparent;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.modal-close {
  position: absolute;
  top: 24px;
  right: 24px;
  width: 48px;
  height: 48px;
  border: none;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  z-index: 1001;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  backdrop-filter: blur(8px);
  pointer-events: auto;
}

.modal-close:hover {
  background: rgba(0, 0, 0, 0.9);
  transform: scale(1.1);
}

.modal-close:focus {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 2px;
}

.modal-image {
  max-width: 100vw;
  max-height: calc(100vh - 80px);
  width: auto;
  height: auto;
  display: block;
  object-fit: contain;
  pointer-events: auto;
}

.modal-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 24px;
  font-size: 18px;
  font-weight: 500;
  color: white;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  text-align: center;
  backdrop-filter: blur(8px);
  pointer-events: auto;
}
</style> 