<template>
  <span>
    <v-form-base
      id="term"
      :model="model"
      :schema="schema"
    >
    </v-form-base>
    <v-btn
      color="green"
      @click="save"
    >
      Enrollañ
    </v-btn>
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
            study_notes: '',
        },
        schema: {
          study_notes: {
            type: "textarea",
            col: 4,
          },
        }
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
    watch: {
      termsData: {
        handler (val) {
          if (val && val.id) {
            this.model.study_notes = val.study_notes
          }
        },
        immediate: true,
      },
    }
  }
</script>
