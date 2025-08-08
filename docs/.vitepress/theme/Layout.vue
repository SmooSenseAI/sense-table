<template>
  <Layout>
    <template #home-features-after>
      <VideoFeatures v-if="frontmatter.features" :features="frontmatter.features" />
    </template>
    <template #layout-bottom>
      <CustomFooter />
    </template>
  </Layout>
</template>

<script setup>
import { useData } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import VideoFeatures from './components/VideoFeatures.vue'
import CustomFooter from './components/CustomFooter.vue'

const Layout = DefaultTheme.Layout
const { frontmatter } = useData()
</script>