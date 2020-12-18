<template>
  <span>
    <v-form-base
      id="location"
      :model="model"
      :schema="schema"
    >
    </v-form-base>
    <v-btn
      color="teal lighten-3"
      @click="save"
    >
      Enrollañ
    </v-btn>
  </span>
</template>

<script>
  import { mapState } from 'vuex'
  import VFormBase from 'vuetify-form-base'
  import ConfirmDialog from '../../components/base/ConfirmDialog.vue'

  export default {
    name: 'Home',
    props: {
      isNew: {
        type: Boolean,
      }
    },
    components: { VFormBase, ConfirmDialog },
    data () {
      return {
        model: {
            proposal_author: '',
            reference: '',
            notes: '',
            etymological_note_fra: '',
            etymological_note_bre: '',
            formalized_proposal: '',
            is_public: false,
            is_name_of_day: false
        },
        schema: {
          proposal_author: {
            type: 'text',
            label: 'Goulenner',
            col: 6
          },
          reference: {
            type: 'text',
            label: 'Daveenn',
            col: 6
          },
          notes: {
            type: 'textarea',
            label: 'Notennoù studiañ',
            col: 4
          },
          etymological_note_fra: {
            type: 'textarea',
            label: 'Gerdarzh ha displegadenn e galleg',
            col: 4
          },
          etymological_note_bre: {
            type: 'textarea',
            label: 'Gerdarzh ha displegadenn e brezhoneg',
            col: 4
          },
          formalized_proposal: {
            type: 'text',
            label: 'Kinnig skoueriekaat'
          },
          is_public: {
            type: 'checkbox',
            label: 'Aotre da embann'
          },
          is_name_of_day: {
            type: 'checkbox',
            label: 'Anv an deiz'
          }
        }
      }
    },
    computed: {
      ...mapState('locations', { 'locationsData': 'getInfoData' }),
      action () {
        return this.isNew ? "Enrollañ": "Etrenan"
      },
    },
    methods: {
      save () {
        let data = JSON.parse(JSON.stringify(this.model))
        const location_id = this.$route.params.id
        this.$store.dispatch('locations/updateLocation', { location_id, data })
      },
    },
    watch: {
      locationsData: {
        handler (val) {
          if (val && val.id) {
            if (val.city) {
              this.model.proposal_author = val.proposal_author
              this.model.reference = val.reference
              this.model.notes = val.notes
              this.model.etymological_note_fra = val.etymological_note_fra
              this.model.etymological_note_bre = val.etymological_note_bre
              this.model.formalized_proposal = val.formalized_proposal
              this.model.is_public = val.is_public
              this.model.is_name_of_day = val.is_name_of_day
            }
          }
        },
        immediate: true,
      },
    }
  }
</script>
