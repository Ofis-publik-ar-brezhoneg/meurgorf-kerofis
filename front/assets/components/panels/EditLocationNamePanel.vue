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

  const required = msg => v => !!v || msg
  const rules = {
    requiredName: required('Le nom est obligatoire'),
    requiredGenericName: required('Le générique est obligatoire')
  }

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
            name: '',
            generic_name: ''
        },
        schema: {
          name: {
            type: 'text',
            rules: [rules.requiredName],
            label: 'Stagadenn',
            col: 4,
          },
          generic_name: {
            type: 'text',
            rules: [rules.requiredGenericName],
            label: 'Lec\'hanv',
            col: 4,
          },
        },
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
        if (this.isNew) {

        } else {
          this.$store.dispatch('locations/updateLocation', { location_id, data })
        }
      },
    },
    watch: {
      locationsData: {
        handler (val) {
          if (val && val.id) {
            this.model.name = val.name
            this.model.generic_name = val.generic_name
          }
        },
        immediate: true,
      },
    }
  }
</script>
