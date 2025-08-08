# CV Visualization


We provide built-in visualization for common Computer Vision algorithms.

It is worth mentioning that the visualization web apps are static web pages that can be
used beyond SenseTable. They are open source and released under MIT license, free for all use cases.


<script setup>

const baseUrl = 'https://stcdn.smoosense.ai/viz-bbox.html'
const imageUrl = 'https://stcdn.smoosense.ai/000000130579.jpg'
const bboxes = '[{"bbox":[176,187,64,57],"label":"GT"},{"bbox":[162,183,107,68],"label":"pred"}]'
const name = 'baseball glove'
const urlFull = `${baseUrl}?image=${encodeURIComponent(imageUrl)}&bboxes=${encodeURIComponent(bboxes)}&name=${encodeURIComponent(name)}`
const urlAutoRange = `${urlFull}&autorange=true`
const urlNoAutoRange = `${urlFull}&autorange=false`
</script>




### Bounding box overlaid on image




Base url: `{{ baseUrl }}`

Parameters:
  - `image`: URL of the background image. Note that users need to set the CORS policy on the image server side. E.g. `{{ imageUrl }}`
  - `bboxes`: Strinfied json list of bbox dict. E.g. `{{ bboxes }}`
  - `autorange`: when set to `true`, the plot will intially automatically set range to the bounding box.

The <a :href="urlAutoRange" target="_blank">full URL</a> can be embeded into almost any web app with `iframe`, and it will automatically adjust behavior based on the available width and height.

- Small view with no interaction. It is suitable when you want to display a bunch of visualizations within limited space, such as inside table cells.
<iframe :src="urlAutoRange" width=64 height=64></iframe>

- Medium view to be displayed in gallery. Try to hover, double click and drag-move the image.
<iframe :src="urlAutoRange" width=200 height=200></iframe>

Full size view with full interactivity. Beside aforementioned ones, you can also scroll to zoom in/out.
<iframe :src="urlNoAutoRange" width=600 height=600></iframe>

### 2D skeleton overlaid on image
Coming ...

### 3D skeleton
Coming ...

### 3D mesh
Coming ...
