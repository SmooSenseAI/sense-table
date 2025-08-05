// Simple test for ThemedVideo component logic
// This tests the getThemedVideoSrc function logic

function getThemedVideoSrc(baseSrc, isDarkMode) {
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

// Test cases
console.log('Testing ThemedVideo component logic:')

// Test 1: Base path with webm extension
console.log('Test 1:', getThemedVideoSrc('/videos/preview_parquet.webm', true)) // Should return: /videos/preview_parquet_dark.webm
console.log('Test 1:', getThemedVideoSrc('/videos/preview_parquet.webm', false)) // Should return: /videos/preview_parquet_light.webm

// Test 2: Already has dark suffix
console.log('Test 2:', getThemedVideoSrc('/videos/preview_parquet_dark.webm', true)) // Should return: /videos/preview_parquet_dark.webm
console.log('Test 2:', getThemedVideoSrc('/videos/preview_parquet_dark.webm', false)) // Should return: /videos/preview_parquet_light.webm

// Test 3: Already has light suffix
console.log('Test 3:', getThemedVideoSrc('/videos/preview_parquet_light.webm', true)) // Should return: /videos/preview_parquet_dark.webm
console.log('Test 3:', getThemedVideoSrc('/videos/preview_parquet_light.webm', false)) // Should return: /videos/preview_parquet_light.webm

// Test 4: MP4 format
console.log('Test 4:', getThemedVideoSrc('/videos/demo.mp4', true)) // Should return: /videos/demo_dark.mp4
console.log('Test 4:', getThemedVideoSrc('/videos/demo.mp4', false)) // Should return: /videos/demo_light.mp4

console.log('Tests completed!') 