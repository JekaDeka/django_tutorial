<template>
  <blog-post-table />
</template>

<script>
// @ is an alias to /src
import BlogPostTable from '@/components/BlogPostTable.vue'

export default {
  name: 'Home',
  components: {
    BlogPostTable
  }
}
</script>
