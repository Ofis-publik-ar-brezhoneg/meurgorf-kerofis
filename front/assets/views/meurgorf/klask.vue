<template>
  <base-app>
    <v-row justify="center">
      <v-col
        cols="12"
        md="4"
      >
        <search-term-panel
          @search="OnSearch"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col
        cols="12"
        md="12"
      >
        <result-term-panel
          @change_page="onChangePage"
        />
      </v-col>
    </v-row>
  </base-app>
</template>

<script>
  export default {
    name: 'index',
    data () {
      return {
        current_search: ''
      }
    },
    components: {
      SearchTermPanel: () => import('../../components/panels/SearchTermPanel.vue'),
      ResultTermPanel: () => import('../../components/panels/ResultTermPanel.vue'),
    },
    watch: {
      '$route.params.id': {
        handler (val) {
          this.$store.dispatch('terms/searchTerms', { search: `id=${val}` })
        },
        immediate: true
      }
    },
    methods: {
      onChangePage (val) {
        this.OnSearch({ search: `${this.current_search}&page=${val}` })
      },
      OnSearch ({ search, isAutoComplete = false }) {
        this.current_search = search
        this.$store.dispatch('terms/searchTerms', { search, isAutoComplete })
      }
    },
  }
</script>
