<template>
  <span>
    <v-form-base
      id="term"
      :model="model"
      :schema="schema"
    >
    </v-form-base>
    <v-card-actions>
      <v-btn
        color="green"
        @click="save"
      >
        Enrollañ
      </v-btn>
    </v-card-actions>
  </span>
</template>

<script>
  import { mapState } from 'vuex'
  import VFormBase from 'vuetify-form-base'

  export default {
    name: 'Home',
    components: { VFormBase },
    data () {
      return {
        model: {
           definition: ''
        },
        schema: {
          "definition": {
            type: "textarea",
            col: 4
          }
        },
      }
    },
    computed: {
      ...mapState('terms', { 'termsData': 'getInfoData' }),
    },
    methods: {
      save () {
        let data = JSON.parse(JSON.stringify(this.model))
        const term_id = this.$route.params.id
        this.$store.dispatch('terms/updateTerm', { term_id, data })
      },
    },
    mounted () {
      if (this.termsData && this.termsData.id) {
        this.model.definition = this.termsData.definition
      }
    },
    watch: {
      termsData: {
        handler (val) {
          if (val && val.id) {
            this.model.definition = val.definition
          }
        },
        immediate: true,
      },
    }
  }
</script>
