<template>
  <div class="VPFeatures">
    <div class="container">
      <div class="items">
        <div 
          v-for="(feature, index) in features" 
          :key="index" 
          class="item"
          @click="openModal(feature.video, feature.title)"
        >
          <article class="box">
            <div class="video-container">
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
            <h2 class="title">{{ feature.title }}</h2>
          </article>
        </div>
      </div>
    </div>

    <!-- Modal for full-size video -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeModal">&times;</button>
        <video 
          :src="getThemedVideoSrc(modalVideo)"
          autoplay
          loop
          muted
          playsinline
          controls
          class="modal-video"
        >
          <source :src="getThemedVideoSrc(modalVideo)" type="video/webm" />
          Your browser does not support the video tag.
        </video>
        <div class="modal-caption">{{ modalTitle }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useData } from 'vitepress'

const props = defineProps({
  features: {
    type: Array,
    required: true
  }
})

const { isDark, site } = useData()
const showModal = ref(false)
const modalVideo = ref('')
const modalTitle = ref('')

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

const openModal = (video, title) => {
  modalVideo.value = video
  modalTitle.value = title
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  showModal.value = false
  modalVideo.value = ''
  modalTitle.value = ''
  document.body.style.overflow = ''
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
  cursor: pointer;
  transition: transform 0.2s ease;
}

.item:hover {
  transform: translateY(-2px);
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

.video-container {
  position: relative;
  margin-bottom: 16px;
  border-radius: 8px;
  overflow: hidden;
  background: var(--vp-c-bg);
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

.title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
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

.modal-video {
  max-width: 100vw;
  max-height: calc(100vh - 80px);
  width: auto;
  height: auto;
  display: block;
  object-fit: contain;
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
}

/* Dark mode adjustments */
.dark .box {
  background: var(--vp-c-bg-soft);
}

.dark .modal-content {
  background: var(--vp-c-bg);
}
</style>