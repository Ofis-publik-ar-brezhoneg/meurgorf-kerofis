<template>
  <span>
    <v-simple-table>
      <template v-slot:default>
        <tbody v-if="termsData">
          <tr
            v-for="item in termsData.historical_occurrences"
            :key="item.id"
          >
            <td>
              {{ item.year }}
            </td>
            <td>
              {{ item.occurence }}
            </td>
            <td>
              {{ item.book.abbreviation }}
            </td>
            <td>
              {{ item.reference }}
            </td>
            <td>
              <v-btn
                icon
                @click="edit_historical_occurrence(item)"
              >
                <v-icon>
                  mdi-pencil
                </v-icon>
              </v-btn>
              <v-btn
                icon
                @click="delete_historical_occurrence(item)"
              >
                <v-icon>
                  mdi-delete
                </v-icon>
              </v-btn>
            </td>
          </tr>
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
  import VFormBase from 'vuetify-form-base'

  export default {
    name: 'Home',
    components: { VFormBase },
    data () {
      return {
        model: {
            "occurence": '',
            "litteral_year": '',
            "year": '',
            "reference": '',
            "book": '',
        },
      }
    },
    computed: {
      ...mapState('books', { 'booksData': 'getInfoData' }),
      ...mapState('terms', { 'termsData': 'getInfoData' }),
      schema () {
        if (!this.booksData) {
            return {}
        }
        return {
          "id": {
            "type": "text",
            "hidden": true
          },
          "occurence": {
            "type": "text",
            "label": "Stumm",
          },
          "litteral_year": {
            "type": "text",
            "label": "Bloavezh lizherennek"
          },
          "year": {
            "type": "text",
            "label": "Bloavezh niverel"
          },
          "reference": {
            "type": "text",
            "label": "Daveenn",
          },
          "book": {
            "type": "select",
            "label": "Berradur",
            "items": this.booksData.map(book => book.abbrevation),
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
      },
    },
    methods: {
      getBook (value, get_attr='abbrevation', return_attr='id') {
        let book = this.booksData.filter(book => book[get_attr] == value).pop()
        return book ? book[return_attr] : ''
      },
      log (val) {
        let { key } = val
        if (key == 'add') {
          this.save()
        }
        if (key == 'reset') {
          this.reset()
        }
      },
      reset () {
        this.model.id = ''
        this.model.occurence = ''
        this.model.litteral_year = ''
        this.model.year = ''
        this.model.reference = ''
        this.model.book = ''
        this.schema.add.label = 'Kas'
        this.schema.reset.hidden = true
      },
      save () {
        let data = { "historical_occurrences": [JSON.parse(JSON.stringify(this.model)), ] }
        data.historical_occurrences[0].book = this.getBook(data.historical_occurrences[0].book)
        const term_id = this.$route.params.id
        this.$store.dispatch('terms/updateTerm', { term_id, data }).then(() => {
          this.reset()
        })
      },
      edit_historical_occurrence(historical_occurrence) {
        this.model.id = historical_occurrence.id
        this.model.occurence = historical_occurrence.occurence
        this.model.litteral_year = historical_occurrence.litteral_year
        this.model.year = historical_occurrence.year
        this.model.reference = historical_occurrence.reference
        this.model.book = this.getBook(historical_occurrence.book, 'id', 'abbrevation')
        this.schema.add.label = 'Enrollañ'
        this.schema.reset.hidden = false
      },
      delete_historical_occurrence (historical_occurrence) {
        this.$store.dispatch('historicalOccurrences/deleteHistoricalOccurrence', { historical_occurrence_id: historical_occurrence.id }).then(() => {
          this.$store.dispatch('terms/getTerm', this.$route.params.id)
        })
      }
    },
  }
</script>
