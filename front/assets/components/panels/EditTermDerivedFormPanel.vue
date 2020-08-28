<template>
  <span>
    <v-simple-table>
      <template v-slot:default>
        <tbody>
          <draggable v-model="derived_forms">
            <tr
              v-for="item in derived_forms"
              :key="item.id"
            >
              <td>
                {{ item.form }}
              </td>
              <td>
                <v-btn
                  icon
                  @click="edit_derived_form(item)"
                >
                  <v-icon>
                    mdi-pencil
                  </v-icon>
                </v-btn>
                <v-btn
                  icon
                  @click="delete_derived_form(item)"
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
      id="term"
      :model="model"
      :schema="schema"
      @change:term="log"
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
            form: '',
        },
        schema: {
          "id": {
            "type": "text",
            "hidden": true
          },
          "form": {
            "type": "text",
            "label": "Stumm skouer",
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
      ...mapState('terms', { 'termsData': 'getInfoData' }),
      derived_forms: {
        get() {
          return (this.termsData && this.termsData.derived_forms) ? this.termsData.derived_forms : []
        },
        set(value) {
          let changed_forms = JSON.parse(JSON.stringify(value))
          changed_forms.forEach((item, index) => {
            item.order = index + 1
          })
          const term_id = this.$route.params.id
          this.$store.dispatch('terms/updateTerm', { term_id, data: { "derived_forms": changed_forms }})
        }
      }
    },
    methods: {
      log (val) {
        let { key } = val
        if (key == 'add') {
          this.save()
        }
        if (key == 'reset') {
          this.model.id = ''
          this.model.form = ''
          this.schema.add.label = 'Kas'
          this.schema.reset.hidden = true
        }
      },
      save () {
        let data = { "derived_forms": [this.model, ] }
        const term_id = this.$route.params.id
        this.$store.dispatch('terms/updateTerm', { term_id, data }).then(() => {
          this.model.id = ''
          this.model.form = ''
          this.schema.add.label = 'Kas'
          this.schema.reset.hidden = true
        })
      },
      edit_derived_form(derived_form) {
        this.model.id = derived_form.id
        this.model.form = derived_form.form
        this.schema.add.label = 'Enrollañ'
        this.schema.reset.hidden = false
      },
      delete_derived_form (derived_form) {
        this.$store.dispatch('derivedForms/deleteDerivedForm', { derived_form_id: derived_form.id }).then(() => {
          this.$store.dispatch('terms/getTerm', this.$route.params.id)
        })
      }
    },
  }
</script>
