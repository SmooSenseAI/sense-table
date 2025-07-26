<template>
  <footer class="VPFooter custom-footer">
    <div class="container">
      <p class="message">
        Made with 
        <span 
          class="tooltip-trigger"
          @mouseenter="showTooltip = true"
          @mouseleave="showTooltip = false"
          @focus="showTooltip = true"
          @blur="showTooltip = false"
          tabindex="0"
        >
          care and love
          <div v-if="showTooltip" class="tooltip">
            <div class="tooltip-content">
              <p>
                <strong>✨ 
                Make something wonderful
                </strong>
              </p>
              <p>
                There’s lots of ways to be, as a person. And some people express their deep appreciation in different ways. But one of the ways that I believe people express their appreciation to the rest of humanity is to make something wonderful and put it out there.
              </p>
              <p>
                And you never meet the people. You never shake their hands. You never hear their story or tell yours. But somehow, in the act of making something with a great deal of care and love, something’s transmitted there. And it’s a way of expressing to the rest of our species our deep appreciation. So we need to be true to who we are and remember what’s really important to us.
              </p>
              <p>
                --- Steve Jobs, 2007
              </p>
            </div>
          </div>
        </span>
         by SmooSense AI
      </p>
      <p class="copyright">Copyright © 2025</p>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'

const showTooltip = ref(false)
</script>

<style scoped>
.custom-footer {
  margin-top: 64px;
  border-top: 1px solid var(--vp-c-divider);
  padding: 32px 24px;
  text-align: center;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg);
}

.container {
  max-width: 1152px;
  margin: 0 auto;
}

.message {
  margin: 0 0 8px;
  font-size: 14px;
  font-weight: 500;
  line-height: 24px;
}

.copyright {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  line-height: 24px;
}

.tooltip-trigger {
  position: relative;
  cursor: help;
  color: var(--vp-c-brand-1);
  text-decoration: underline;
  text-decoration-style: dotted;
  text-underline-offset: 3px;
  transition: all 0.2s ease;
  border-radius: 3px;
  padding: 2px;
  outline: none;
}

.tooltip-trigger:hover,
.tooltip-trigger:focus {
  color: var(--vp-c-brand-2);
  background: var(--vp-c-brand-soft);
}

.tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 8px;
  z-index: 1000;
  animation: tooltipFadeIn 0.2s ease-out;
}

.tooltip-content {
  background: var(--vp-c-bg-elv);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 16px;
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.1),
    0 2px 4px rgba(0, 0, 0, 0.06);
  min-width: 280px;
  max-width: 320px;
  text-align: left;
  position: relative;
}

.tooltip-content::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: var(--vp-c-bg-elv);
}

.tooltip-content::before {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 7px solid transparent;
  border-top-color: var(--vp-c-divider);
  z-index: -1;
}

.tooltip-content p {
  margin: 0 0 12px;
  font-size: 13px;
  line-height: 1.5;
  color: var(--vp-c-text-1);
}

.tooltip-content p:last-child {
  margin-bottom: 0;
}

.tooltip-content strong {
  color: var(--vp-c-brand-1);
  font-weight: 600;
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* Dark mode adjustments */
.dark .tooltip-content {
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.3),
    0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .tooltip-content {
    min-width: 240px;
    max-width: 280px;
    padding: 14px;
    font-size: 12px;
  }
  
  .tooltip {
    left: 50%;
    right: auto;
    transform: translateX(-50%);
  }
}

/* Ensure tooltip doesn't get cut off */
@media (max-width: 350px) {
  .tooltip {
    left: 16px;
    right: 16px;
    transform: none;
  }
  
  .tooltip-content::after,
  .tooltip-content::before {
    left: 50%;
  }
}
</style> 