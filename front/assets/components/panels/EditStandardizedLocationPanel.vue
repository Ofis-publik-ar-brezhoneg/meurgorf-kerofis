<template>
  <span>
    <v-simple-table>
      <template v-slot:default>
        <tbody>
          <draggable v-model="standardized_forms">
            <tr
              v-for="item in standardized_forms"
              :key="item.id"
            >
              <td>
                {{ item.standardized_form }}
              </td>
              <td>
                {{ formatDate(item.date) }}
              </td>
              <td>
                <v-btn
                  icon
                  @click="edit_standardized_form(item)"
                >
                  <v-icon>
                    mdi-pencil
                  </v-icon>
                </v-btn>
                <v-btn
                  icon
                  @click="delete_standardized_form(item)"
                >
                  <v-icon>
                    mdi-delete
                  </v-icon>
                </v-btn>
              </td>
            </tr>
          </draggable>
        </tbody>
      </template>
    </v-simple-table>
    <v-form-base
      id="location"
      :model="model"
      :schema="schema"
      @change:location="log"
    >
    </v-form-base>
  </span>
</template>

<script>
  import { mapState } from 'vuex'
  import draggable from 'vuedraggable'
  import VFormBase from 'vuetify-form-base'

  export default {
    name: 'Home',
    components: { draggable, VFormBase },
    data () {
      return {
        model: {
            standardized_form: '',
            date: ''
        },
        schema: {
          "id": {
            "type": "text",
            "hidden": true
          },
          "standardized_form": {
            "type": "text",
            "label": "Anv",
          },
          "date": {
            "type": "text",
            "ext": "date",
            "label": "Deiziad degemer",
          },
          "add": {
            "type": "btn",
            "label": "Kas",
            "dark": true,
            "color": "green"
          },
          "reset": {
            "type": "btn",
            "label": "X",
            "hidden": true,
            "color": "grey"
          }
        }
      }
    },
    computed: {
      ...mapState('locations', { 'locationsData': 'getInfoData' }),
      standardized_forms: {
        get() {
          return (this.locationsData && this.locationsData.standardized_forms) ? this.locationsData.standardized_forms : []
        },
        set(value) {
          let changed_forms = JSON.parse(JSON.stringify(value))
          changed_forms.forEach((item, index) => {
            item.order = index + 1
          })
          const location_id = this.$route.params.id
          this.$store.dispatch('locations/updateLocations', { location_id, data: { "standardized_forms": changed_forms }})
        }
      }
    },
    methods: {
      formatDate (date) {
        if (!date) return null

        const [year, month, day] = date.split('-')
        return `${day}/${month}/${year}`
      },
      log (val) {
        let { key } = val
        if (key == 'add') {
          this.save()
        }
        if (key == 'reset') {
          this.model.id = ''
          this.model.standardized_form = ''
          this.model.date = ''
          this.schema.add.label = 'Kas'
          this.schema.reset.hidden = true
        }
      },
      save () {
        let data = { "standardized_forms": [this.model, ] }
        const location_id = this.$route.params.id
        this.$store.dispatch('locations/updateLocation', { location_id, data }).then(() => {
          this.model.id = ''
          this.model.standardized_form = ''
          this.model.date = ''
          this.schema.add.label = 'Kas'
          this.schema.reset.hidden = true
        })
      },
      edit_standardized_form(standardized_form) {
        this.model.id = standardized_form.id
        this.model.standardized_form = standardized_form.standardized_form
        this.model.date = standardized_form.date
        this.schema.add.label = 'Enrollañ'
        this.schema.reset.hidden = false
      },
      delete_standardized_form (standardized_form) {
        this.$store.dispatch(
          'locations/deleteStandardizedForm', { standardized_form_id: standardized_form.id }
        ).then(() => {
          this.$store.dispatch('locations/getLocation', this.$route.params.id)
        })
      }
    },
  }
</script>
