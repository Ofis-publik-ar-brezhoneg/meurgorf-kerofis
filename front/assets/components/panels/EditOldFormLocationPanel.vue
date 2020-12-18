<template>
  <span>
    <v-simple-table>
      <template v-slot:default>
        <tbody>
          <draggable v-model="old_forms">
            <tr
              v-for="item in old_forms"
              :key="item.id"
            >
              <td>
                {{ item.old_form }}
              </td>
              <td>
                {{ item.litteral_year }}
              </td>
              <td>
                {{ item.year }}
              </td>
              <td>
                {{ getBook(item.book) }}
              </td>
              <td>
                {{ item.reference }}
              </td>
              <td>
                <v-btn
                  icon
                  @click="edit_old_form(item)"
                >
                  <v-icon>
                    mdi-pencil
                  </v-icon>
                </v-btn>
                <v-btn
                  icon
                  @click="delete_old_form(item)"
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
            old_form: '',
            litteral_year: '',
            year: '',
            book: '',
            reference: '',
        },

      }
    },
    computed: {
      ...mapState('locations', { 'locationsData': 'getInfoData' }),
      ...mapState('books', { 'booksData': 'getInfoData' }),
      old_forms: {
        get() {
          return (this.locationsData && this.locationsData.old_forms) ? this.locationsData.old_forms : []
        },
        set(value) {
          let changed_forms = JSON.parse(JSON.stringify(value))
          changed_forms.forEach((item, index) => {
            item.order = index + 1
          })
          const location_id = this.$route.params.id
          this.$store.dispatch('locations/updateLocations', { location_id, data: { "old_forms": changed_forms }})
        }
      },
      schema() {
        if (!this.booksData) {
          return {}
        }

        return {
          "id": {
            "type": "text",
            "hidden": true
          },
          "old_form": {
            "type": "text",
            "label": "Anv",
          },
          "litteral_year": {
            "type": "text",
            "label": "Bloavezh niverel"
          },
          "year": {
            "type": "text",
            "label": "Bloavezh",
          },
          "book": {
            "type": "autocomplete",
            "label": "Berradur",
            "items": this.booksData,
            "itemText": "abbrevation",
            "returnObject": true,
          },
          "reference": {
            "type": "text",
            "label": "Daveenn",
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
    methods: {
      getBook (value, get_attr='id', return_attr='abbrevation') {
        if (!this.booksData) {
          return ''
        }
        let book = this.booksData.filter(book => book[get_attr] == value).pop()
        return return_attr ? (book ? book[return_attr] : '') : book
      },
      log (val) {
        let { key } = val
        if (key == 'add') {
          this.save()
        }
        if (key == 'reset') {
          this.model.phonetic_transcription = ''
          this.model.is_standard = false
          this.model.created_at = ''
          this.model.informant = ''
          this.schema.add.label = 'Kas'
          this.schema.reset.hidden = true
        }
      },
      save () {
        let data = { "old_forms": [this.model, ] }
        data["old_forms"][0]["book"] = this.model.book.id
        const location_id = this.$route.params.id
        this.$store.dispatch('locations/updateLocation', { location_id, data }).then(() => {
          this.model.old_form = ''
          this.model.litteral_year = ''
          this.model.year = ''
          this.model.book = ''
          this.model.reference = ''
          this.schema.add.label = 'Kas'
          this.schema.reset.hidden = true
        })
      },
      edit_old_form(old_form) {
        this.model.id = old_form.id
        this.model.old_form = old_form.old_form
        this.model.litteral_year = old_form.litteral_year
        this.model.year = old_form.year
        this.model.book = this.getBook(old_form.book, 'id', null)
        this.model.reference = old_form.reference
        this.schema.add.label = 'Enrollañ'
        this.schema.reset.hidden = false
      },
      delete_old_form(old_form) {
        this.$store.dispatch(
          'locations/deleteOldForm', { old_form_id: old_form.id }
        ).then(() => {
          this.$store.dispatch('locations/getLocation', this.$route.params.id)
        })
      }
    },
  }
</script>
