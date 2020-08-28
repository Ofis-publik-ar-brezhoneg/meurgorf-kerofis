<template>
  <base-app>
  </base-app>
</template>

<script>
  export default {
    name: 'Home',
    mounted () {
      this.$store.dispatch('users/getCurrentUser')
    }
  }
</script>
