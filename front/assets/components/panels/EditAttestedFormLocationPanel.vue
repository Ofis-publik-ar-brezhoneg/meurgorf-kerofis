<template>
  <span>
    <v-simple-table>
      <template v-slot:default>
        <tbody>
          <draggable v-model="attested_forms">
            <tr
              v-for="item in attested_forms"
              :key="item.id"
            >
              <td>
                {{ item.attested_form }}
              </td>
              <td>
                <v-checkbox
                  v-model="item.is_labeled"
                  readonly
                />
              </td>
              <td>
                {{ item.litteral_year }}
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
                  @click="edit_attested_form(item)"
                >
                  <v-icon>
                    mdi-pencil
                  </v-icon>
                </v-btn>
                <v-btn
                  icon
                  @click="delete_attested_form(item)"
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
            attested_form: '',
            is_labeled: false,
            litteral_year: '',
            book: '',
            reference: '',
        },

      }
    },
    computed: {
      ...mapState('locations', { 'locationsData': 'getInfoData' }),
      ...mapState('books', { 'booksData': 'getInfoData' }),
      attested_forms: {
        get() {
          return (this.locationsData && this.locationsData.attested_forms) ? this.locationsData.attested_forms : []
        },
        set(value) {
          let changed_forms = JSON.parse(JSON.stringify(value))
          changed_forms.forEach((item, index) => {
            item.order = index + 1
          })
          const location_id = this.$route.params.id
          this.$store.dispatch('locations/updateLocations', { location_id, data: { "attested_forms": changed_forms }})
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
          "attested_form": {
            "type": "text",
            "label": "Stumm",
          },
          "is_labeled": {
            "type": "checkbox"
          },
          "litteral_year": {
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
          this.model.attested_form = ''
          this.model.is_labeled = ''
          this.model.litteral_year = ''
          this.model.book = ''
          this.model.reference = ''
          this.schema.add.label = 'Kas'
          this.schema.reset.hidden = true
        }
      },
      save () {
        let data = { "attested_forms": [this.model, ] }
        data["attested_forms"][0]["book"] = this.model.book.id
        data["attested_forms"][0]["is_labeled"] = this.model.is_labeled == true
        const location_id = this.$route.params.id
        this.$store.dispatch('locations/updateLocation', { location_id, data }).then(() => {
          this.model.attested_form = ''
          this.model.is_labeled = ''
          this.model.litteral_year = ''
          this.model.book = ''
          this.model.reference = ''
          this.schema.add.label = 'Kas'
          this.schema.reset.hidden = true
        })
      },
      edit_attested_form(attested_form) {
        this.model.id = attested_form.id
        this.model.attested_form = attested_form.attested_form
        this.model.is_labeled = attested_form.is_labeled
        this.model.litteral_year = attested_form.litteral_year
        this.model.book = this.getBook(attested_form.book, 'id', null)
        this.model.reference = attested_form.reference
        this.schema.add.label = 'Enrollañ'
        this.schema.reset.hidden = false
      },
      delete_attested_form(attested_form) {
        this.$store.dispatch(
          'locations/deleteAttestedForm', { attested_form_id: attested_form.id }
        ).then(() => {
          this.$store.dispatch('locations/getLocation', this.$route.params.id)
        })
      }
    },
  }
</script>
