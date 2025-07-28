// Markdown-it plugin for tooltip links with @[text](/image) syntax
export function tooltipPlugin(md) {
  // Custom rule for tooltip links
  const tooltipRule = (state, startLine, endLine, silent) => {
    const start = state.pos
    const max = state.posMax

    // Ensure we have a valid source string
    if (typeof state.src !== 'string') return false

    // Look for the pattern: @[text](/path/to/image.jpg)
    const atMarker = state.src.charCodeAt(start)
    if (atMarker !== 0x40/* @ */) return false

    const bracketStart = start + 1
    if (bracketStart >= max) return false

    const bracketMarker = state.src.charCodeAt(bracketStart)
    if (bracketMarker !== 0x5B/* [ */) return false

    // Find the closing bracket
    let labelEnd = -1
    for (let i = bracketStart + 1; i < max; i++) {
      if (state.src.charCodeAt(i) === 0x5D/* ] */) {
        labelEnd = i
        break
      }
    }
    if (labelEnd === -1) return false

    const pos = labelEnd + 1
    if (pos >= max) return false

    // Check for opening parenthesis
    if (state.src.charCodeAt(pos) !== 0x28/* ( */) return false

    // Find the closing parenthesis
    let urlEnd = -1
    for (let i = pos + 1; i < max; i++) {
      if (state.src.charCodeAt(i) === 0x29/* ) */) {
        urlEnd = i
        break
      }
    }
    if (urlEnd === -1) return false

    if (silent) return true

    // Extract text and URL
    const text = state.src.slice(bracketStart + 1, labelEnd)
    let url = state.src.slice(pos + 1, urlEnd)

    // Check if URL points to an image (common image extensions)
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
    const isImage = imageExtensions.some(ext => url.toLowerCase().endsWith(ext))

    if (!isImage) {
      // If not an image, treat as regular link
      return false
    }

    // Prepend base path if URL starts with '/'
    if (url.startsWith('/')) {
      url = '/sense-table' + url
    }

    // Create token
    const token = state.push('tooltip_link', '', 0)
    token.content = text
    token.attrs = [
      ['text', text],
      ['href', url],
      ['imageSrc', url]
    ]

    state.pos = urlEnd + 1
    return true
  }

  // Renderer for tooltip links
  const tooltipRenderer = (tokens, idx) => {
    const token = tokens[idx]
    const text = token.attrs.find(attr => attr[0] === 'text')[1]
    const href = token.attrs.find(attr => attr[0] === 'href')[1]
    const imageSrc = token.attrs.find(attr => attr[0] === 'imageSrc')[1]

    return `<TooltipLink text="${text}" href="${href}" image-src="${imageSrc}" />`
  }

  // Register the rule
  md.inline.ruler.before('link', 'tooltip_link', tooltipRule)
  
  // Register the renderer
  md.renderer.rules.tooltip_link = tooltipRenderer
} 