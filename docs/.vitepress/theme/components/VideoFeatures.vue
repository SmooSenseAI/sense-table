<template>
  <div class="VPFeatures">
    <div class="container">
      <div class="items">
        <div 
          v-for="(feature, index) in features" 
          :key="index" 
          class="item"
        >
          <article class="box">
            <!-- Video mode -->
            <div v-if="feature.video" class="video-container" @click="openModal(feature, index)">
              <video 
                :src="getThemedVideoSrc(feature.video)"
                autoplay
                loop
                muted
                playsinline
                class="preview-video"
              >
                <source :src="getThemedVideoSrc(feature.video)" type="video/webm" />
                Your browser does not support the video tag.
              </video>
              <div class="play-overlay">
                <svg class="play-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </div>
            </div>
            
            <!-- Image album mode -->
            <div v-else-if="feature.images && feature.images.length" class="album-container" @click="openModal(feature, index)">
              <div class="album-viewport">
                <div 
                  class="album-track"
                  :style="{ transform: `translateX(-${currentImageIndex[index] * 100}%)` }"
                >
                  <div 
                    v-for="(image, imgIndex) in feature.images" 
                    :key="imgIndex"
                    class="album-slide"
                  >
                    <img 
                      :src="getThemedImageSrc(image)"
                      :alt="`${feature.title} - Image ${imgIndex + 1}`"
                      class="preview-image"
                    />
                  </div>
                </div>
              </div>
              <div class="album-indicators">
                <span 
                  v-for="(image, imgIndex) in feature.images"
                  :key="imgIndex"
                  class="indicator"
                  :class="{ active: currentImageIndex[index] === imgIndex }"
                ></span>
              </div>
              <div class="album-overlay">
                <svg class="album-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z"/>
                </svg>
              </div>
            </div>
            
            <h2 class="title" v-html="feature.title"></h2>
          </article>
        </div>
      </div>
    </div>

    <!-- Modal for full-size content -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeModal">&times;</button>
        
        <!-- Video modal -->
        <div v-if="modalContent.video" class="modal-video-container">
          <video 
            :src="getThemedVideoSrc(modalContent.video)"
            autoplay
            loop
            muted
            playsinline
            controls
            class="modal-video"
          >
            <source :src="getThemedVideoSrc(modalContent.video)" type="video/webm" />
            Your browser does not support the video tag.
          </video>
        </div>
        
        <!-- Image album modal -->
        <div v-else-if="modalContent.images && modalContent.images.length" class="modal-album-container">
          <button 
            v-if="modalContent.images.length > 1"
            class="modal-nav modal-prev" 
            @click="prevModalImage"
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
            </svg>
          </button>
          
          <img 
            :src="getThemedImageSrc(modalContent.images[modalImageIndex])"
            :alt="`${modalContent.title} - Image ${modalImageIndex + 1}`"
            class="modal-image"
          />
          
          <button 
            v-if="modalContent.images.length > 1"
            class="modal-nav modal-next" 
            @click="nextModalImage"
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
            </svg>
          </button>
          
          <div v-if="modalContent.images.length > 1" class="modal-indicators">
            <span 
              v-for="(image, imgIndex) in modalContent.images"
              :key="imgIndex"
              class="modal-indicator"
              :class="{ active: modalImageIndex === imgIndex }"
              @click="modalImageIndex = imgIndex"
            ></span>
          </div>
        </div>
        
        <div class="modal-caption" v-html="modalContent.title"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useData } from 'vitepress'

const props = defineProps({
  features: {
    type: Array,
    required: true
  }
})

const { isDark, site } = useData()
const showModal = ref(false)
const modalContent = ref({})
const modalImageIndex = ref(0)

// Track current image for each album
const currentImageIndex = ref({})
const albumIntervals = ref({})

// Initialize image indices for albums
onMounted(() => {
  props.features.forEach((feature, index) => {
    if (feature.images && feature.images.length > 0) {
      currentImageIndex.value[index] = 0
      startAlbumAutoSlide(index, feature.images.length)
    }
  })
})

// Cleanup intervals on unmount
onUnmounted(() => {
  Object.values(albumIntervals.value).forEach(interval => {
    if (interval) clearInterval(interval)
  })
})

// Start auto-slide for album
const startAlbumAutoSlide = (featureIndex, imageCount) => {
  if (imageCount <= 1) return
  
  albumIntervals.value[featureIndex] = setInterval(() => {
    currentImageIndex.value[featureIndex] = 
      (currentImageIndex.value[featureIndex] + 1) % imageCount
  }, 3000) // 3 seconds
}

// Stop auto-slide for album
const stopAlbumAutoSlide = (featureIndex) => {
  if (albumIntervals.value[featureIndex]) {
    clearInterval(albumIntervals.value[featureIndex])
    albumIntervals.value[featureIndex] = null
  }
}

// Function to get the appropriate video source based on theme
const getThemedVideoSrc = (baseSrc) => {
  if (!baseSrc) return ''
  
  // If the video already has a theme suffix, replace it
  if (baseSrc.includes('_dark.webm')) {
    const themedSrc = isDark.value ? baseSrc : baseSrc.replace('_dark.webm', '_light.webm')
    return addBaseUrl(themedSrc)
  }
  
  if (baseSrc.includes('_light.webm')) {
    const themedSrc = isDark.value ? baseSrc.replace('_light.webm', '_dark.webm') : baseSrc
    return addBaseUrl(themedSrc)
  }
  
  if (baseSrc.includes('_dark.mp4')) {
    const themedSrc = isDark.value ? baseSrc : baseSrc.replace('_dark.mp4', '_light.mp4')
    return addBaseUrl(themedSrc)
  }
  
  if (baseSrc.includes('_light.mp4')) {
    const themedSrc = isDark.value ? baseSrc.replace('_light.mp4', '_dark.mp4') : baseSrc
    return addBaseUrl(themedSrc)
  }
  
  // If no theme suffix, add one based on current mode
  const basePath = baseSrc.replace(/\.(webm|mp4|avi|mov)$/i, '')
  const extension = baseSrc.match(/\.(webm|mp4|avi|mov)$/i)?.[0] || '.webm'
  const themedSrc = `${basePath}_${isDark.value ? 'dark' : 'light'}${extension}`
  return addBaseUrl(themedSrc)
}

// Function to get the appropriate image source based on theme
const getThemedImageSrc = (baseSrc) => {
  if (!baseSrc) return ''
  
  // If the image already has a theme suffix, replace it
  if (baseSrc.includes('_dark.')) {
    const themedSrc = isDark.value ? baseSrc : baseSrc.replace('_dark.', '_light.')
    return addBaseUrl(themedSrc)
  }
  
  if (baseSrc.includes('_light.')) {
    const themedSrc = isDark.value ? baseSrc.replace('_light.', '_dark.') : baseSrc
    return addBaseUrl(themedSrc)
  }
  
  // If no theme suffix, add one based on current mode
  const basePath = baseSrc.replace(/\.(jpg|jpeg|png|gif|webp|svg)$/i, '')
  const extension = baseSrc.match(/\.(jpg|jpeg|png|gif|webp|svg)$/i)?.[0] || '.jpg'
  const themedSrc = `${basePath}_${isDark.value ? 'dark' : 'light'}${extension}`
  return addBaseUrl(themedSrc)
}

// Function to add base URL to media path
const addBaseUrl = (mediaPath) => {
  const base = site.value?.base || ''
  
  // Ensure mediaPath starts with / (but don't add if it already has one)
  const normalizedPath = mediaPath.startsWith('/') ? mediaPath : `/${mediaPath}`
  
  // Remove trailing slash from base if it exists
  const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base
  
  // Combine base and path
  const result = `${cleanBase}${normalizedPath}`
  return result
}

const openModal = (feature, featureIndex) => {
  modalContent.value = feature
  modalImageIndex.value = 0
  showModal.value = true
  document.body.style.overflow = 'hidden'
  
  // Stop auto-slide when modal opens
  if (feature.images) {
    stopAlbumAutoSlide(featureIndex)
  }
}

const closeModal = () => {
  showModal.value = false
  const oldContent = modalContent.value
  modalContent.value = {}
  modalImageIndex.value = 0
  document.body.style.overflow = ''
  
  // Restart auto-slide for albums
  props.features.forEach((feature, index) => {
    if (feature.images && feature.images.length > 1) {
      startAlbumAutoSlide(index, feature.images.length)
    }
  })
}

const nextModalImage = () => {
  if (modalContent.value.images && modalContent.value.images.length > 1) {
    modalImageIndex.value = (modalImageIndex.value + 1) % modalContent.value.images.length
  }
}

const prevModalImage = () => {
  if (modalContent.value.images && modalContent.value.images.length > 1) {
    modalImageIndex.value = modalImageIndex.value === 0 
      ? modalContent.value.images.length - 1 
      : modalImageIndex.value - 1
  }
}
</script>

<style scoped>
.VPFeatures {
  position: relative;
  padding: 0 24px;
}

.container {
  margin: 0 auto;
  max-width: 1152px;
}

.items {
  display: flex;
  flex-wrap: wrap;
  margin: -8px;
}

.item {
  padding: 8px;
  width: 100%;
}

@media (min-width: 640px) {
  .item {
    width: 50%;
  }
}

@media (min-width: 960px) {
  .item {
    width: 33.333333%;
  }
}

.box {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 24px;
  height: 100%;
  transition: border-color 0.25s, box-shadow 0.25s;
}

.box:hover {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

/* Video container styles */
.video-container {
  position: relative;
  margin-bottom: 16px;
  border-radius: 8px;
  overflow: hidden;
  background: var(--vp-c-bg);
  cursor: pointer;
  transition: transform 0.2s ease;
}

.video-container:hover {
  transform: translateY(-2px);
}

.preview-video {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 48px;
  height: 48px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.item:hover .play-overlay {
  opacity: 1;
}

.play-icon {
  width: 20px;
  height: 20px;
  margin-left: 2px; /* Slightly offset to center visually */
}

/* Album container styles */
.album-container {
  position: relative;
  margin-bottom: 16px;
  border-radius: 8px;
  overflow: hidden;
  background: var(--vp-c-bg);
  cursor: pointer;
  transition: transform 0.2s ease;
}

.album-container:hover {
  transform: translateY(-2px);
}

.album-viewport {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.album-track {
  display: flex;
  width: 100%;
  height: 100%;
  transition: transform 0.5s ease-in-out;
}

.album-slide {
  flex: 0 0 100%;
  width: 100%;
  height: 100%;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.album-indicators {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 6px;
  z-index: 10;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  transition: background-color 0.3s ease;
}

.indicator.active {
  background: rgba(255, 255, 255, 0.9);
}

.album-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 48px;
  height: 48px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.item:hover .album-overlay {
  opacity: 1;
}

.album-icon {
  width: 20px;
  height: 20px;
}

.title {
  margin: 0;
  font-size: 18px;
  font-weight: 400;
  color: var(--vp-c-text-1);
  line-height: 1.4;
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
}

.modal-content {
  position: relative;
  width: 100vw;
  height: 100vh;
  background: black;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
  transition: background-color 0.2s ease;
  backdrop-filter: blur(8px);
}

.modal-close:hover {
  background: rgba(0, 0, 0, 0.9);
  transform: scale(1.1);
}

/* Video modal styles */
.modal-video-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-video {
  max-width: 100vw;
  max-height: calc(100vh - 80px);
  width: auto;
  height: auto;
  display: block;
  object-fit: contain;
}

/* Image album modal styles */
.modal-album-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-image {
  max-width: 100vw;
  max-height: calc(100vh - 80px);
  width: auto;
  height: auto;
  object-fit: contain;
}

.modal-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  border: none;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border-radius: 50%;
  cursor: pointer;
  z-index: 1001;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
  backdrop-filter: blur(8px);
}

.modal-nav:hover {
  background: rgba(0, 0, 0, 0.9);
  transform: translateY(-50%) scale(1.1);
}

.modal-prev {
  left: 24px;
}

.modal-next {
  right: 24px;
}

.modal-nav svg {
  width: 24px;
  height: 24px;
}

.modal-indicators {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 12px;
  z-index: 1001;
}

.modal-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.modal-indicator:hover {
  transform: scale(1.2);
}

.modal-indicator.active {
  background: rgba(255, 255, 255, 0.9);
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
  z-index: 1000;
}

.modal-caption a {
  color: #ffffff;
  text-decoration: underline;
  font-weight: 600;
  transition: all 0.2s ease;
  border-radius: 4px;
  padding: 2px 6px;
  margin: 0 -6px;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.modal-caption a:hover {
  color: var(--vp-c-brand-1);
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-1px);
}

/* Dark mode adjustments */
.dark .box {
  background: var(--vp-c-bg-soft);
}

.dark .modal-content {
  background: var(--vp-c-bg);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .modal-nav {
    width: 40px;
    height: 40px;
  }
  
  .modal-prev {
    left: 12px;
  }
  
  .modal-next {
    right: 12px;
  }
  
  .modal-close {
    top: 12px;
    right: 12px;
    width: 40px;
    height: 40px;
  }
  
  .modal-nav svg {
    width: 20px;
    height: 20px;
  }
}
</style>