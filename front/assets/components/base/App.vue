<template>
  <v-app>
    <dashboard-core-app-bar />
    <dashboard-core-drawer />
    <v-main>
      <slot />
    </v-main>
  </v-app>
</template>

<script>
  export default {
    name: 'DashboardIndex',

    components: {
      DashboardCoreAppBar: () => import('../core/AppBar.vue'),
      DashboardCoreDrawer: () => import('../core/Drawer.vue'),
    },

    data: () => ({
      expandOnHover: false,
    }),

    mounted () {
      // this.$store.dispatch('users/getCurrentUser');
    }
  }
</script>
