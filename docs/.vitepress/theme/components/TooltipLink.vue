<template>
  <span class="tooltip-container">
    <a :href="href" class="tooltip-link" @mouseenter="showTooltip" @mouseleave="hideTooltip" @click.prevent="showPopup">{{ text }}</a>
    <div v-if="isVisible" class="tooltip" :style="tooltipStyle">
      <img :src="imageSrc" :alt="text" class="tooltip-image" />
    </div>
    
    <!-- Modal popup for larger image view -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeModal">&times;</button>
        <img :src="imageSrc" :alt="text" class="modal-image" />
        <div class="modal-caption">{{ text }}</div>
      </div>
    </div>
  </span>
</template>

<script>
export default {
  name: 'TooltipLink',
  props: {
    text: {
      type: String,
      required: true
    },
    href: {
      type: String,
      required: true
    },
    imageSrc: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      isVisible: false,
      showModal: false,
      tooltipStyle: {}
    }
  },
  methods: {
    showTooltip(event) {
      this.isVisible = true
      this.$nextTick(() => {
        this.positionTooltip(event)
      })
    },
    hideTooltip() {
      this.isVisible = false
    },
    showPopup() {
      this.showModal = true
      // Prevent body scroll when modal is open
      document.body.style.overflow = 'hidden'
      // Add keyboard event listener for Escape key
      document.addEventListener('keydown', this.handleKeydown)
    },
    closeModal() {
      this.showModal = false
      // Restore body scroll
      document.body.style.overflow = ''
      // Remove keyboard event listener
      document.removeEventListener('keydown', this.handleKeydown)
    },
    handleKeydown(event) {
      if (event.key === 'Escape') {
        this.closeModal()
      }
    },
    positionTooltip(event) {
      const tooltip = this.$el.querySelector('.tooltip')
      if (!tooltip) return

      const rect = event.target.getBoundingClientRect()
      const tooltipRect = tooltip.getBoundingClientRect()
      const viewportWidth = window.innerWidth
      const viewportHeight = window.innerHeight

      // Default position (below the link)
      let top = rect.bottom + 10
      let left = rect.left

      // Adjust if tooltip would go off the right edge
      if (left + tooltipRect.width > viewportWidth) {
        left = viewportWidth - tooltipRect.width - 10
      }

      // Adjust if tooltip would go off the bottom edge
      if (top + tooltipRect.height > viewportHeight) {
        top = rect.top - tooltipRect.height - 10
      }

      // Ensure tooltip doesn't go off the left edge
      if (left < 10) {
        left = 10
      }

      // Ensure tooltip doesn't go off the top edge
      if (top < 10) {
        top = rect.bottom + 10
      }

      this.tooltipStyle = {
        position: 'fixed',
        top: `${top}px`,
        left: `${left}px`,
        zIndex: 1000
      }
    }
  },
  beforeUnmount() {
    // Clean up body scroll when component is destroyed
    document.body.style.overflow = ''
  }
}
</script>

<style scoped>
.tooltip-container {
  position: relative;
  display: inline;
}

.tooltip-link {
  color: #3b82f6;
  text-decoration: underline;
  cursor: pointer;
}

.tooltip-link:hover {
  color: #1d4ed8;
}

.tooltip {
  position: fixed;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  padding: 8px;
  max-width: 300px;
  max-height: 300px;
  overflow: hidden;
  z-index: 1000;
}

.tooltip-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 4px;
  display: block;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: modalFadeIn 0.3s ease-out;
}

.modal-content {
  position: relative;
  background: white;
  border-radius: 12px;
  padding: 20px;
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 15px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: background-color 0.2s;
}

.modal-close:hover {
  background: rgba(0, 0, 0, 0.7);
}

.modal-image {
  max-width: 100%;
  max-height: calc(90vh - 80px);
  object-fit: contain;
  border-radius: 8px;
  display: block;
}

.modal-caption {
  margin-top: 15px;
  text-align: center;
  font-weight: 500;
  color: #374151;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .tooltip {
    background: #1f2937;
    border-color: #374151;
    color: #f9fafb;
  }
  
  .modal-content {
    background: #1f2937;
    color: #f9fafb;
  }
  
  .modal-caption {
    color: #d1d5db;
  }
}

/* Animations */
.tooltip {
  animation: tooltipFadeIn 0.2s ease-out;
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .modal-content {
    margin: 20px;
    padding: 15px;
  }
  
  .modal-image {
    max-height: calc(90vh - 60px);
  }
  
  .modal-close {
    top: 5px;
    right: 10px;
    width: 25px;
    height: 25px;
    font-size: 16px;
  }
}
</style> 