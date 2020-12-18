<template>
  <base-app>
    <v-container
      fluid
    >
      <v-row
        align="center"
        justify="center"
      >
        <v-col
          cols="12"
        >
          <base-material-card>
            <v-form>
              <v-form-base
                :model="model"
                :schema="schema"
                class="title br-8 mx-2 pa-2"
              >
              </v-form-base>
              <v-btn
                color="teal lighten-3"
                @click="onSearch"
              >
                Krouiñ
              </v-btn>
            </v-form>
          </base-material-card>
        </v-col>
      </v-row>
    </v-container>
  </base-app>
</template>

<script>
  import { mapState } from 'vuex'
  import VFormBase from 'vuetify-form-base'

  export default {
    name: 'Klask',
    components: { VFormBase },
    data () {
      return {
        model: {
          type: '',
          city: '',
        },
      }
    },
    computed: {
      ...mapState('cities', {'citiesData': 'getInfoData'}),
      ...mapState('locations', {'locationsData': 'getInfoData'}),
      schema () {
        if (!this.citiesData) {
            return {}
        }
        return {
          type: {
            type: 'select',
            label: 'Seurt levrig',
            col: 2,
            items: ['raklevrig', 'Levrig echu']
          },
          city: {
            type: 'select',
            label: 'Kumun',
            col: 2,
            itemText: "name_bre",
            returnObject: true,
            items: this.citiesData,
            filled: true
          }
        }
      },
      fields () {
        if (this.model.type == 'raklevrig') {
          return [
            {'text': 'Stagadenn', 'keys': ['generic_name', 'name'] },
            {'text': 'Distagadur(-ioù)', 'key': 'phonetic_transcriptions_list' },
            {'text': 'Stummoù all', 'obj': 'other_forms', 'keys': ['usage_form', 'litteral_year', 'book', 'reference'] },
            {'text': 'Stummoù kozhtesteniekaet', 'obj': 'attested_forms', 'keys': ['attested_form', 'litteral_year', 'book', 'reference']},
            {'text': 'Notennoù studiañ', 'key': 'notes' },
            {'text': 'Displegadennoù', 'key': 'etymological_note_fra' },
            {'text': 'Displegadennoù br', 'key': 'etymological_note_bre' },
            {'text': 'Kinnig OPLB', 'key': 'formalized_proposal' },
          ]
        } else {
          return [
            {'text': 'Kinnig OPLB', 'key': 'formalized_proposal' },
            {'text': 'Stagadenn', 'keys': ['generic_name', 'name'] },
            {'text': 'Distagadur(-ioù)', 'key': 'phonetic_transcriptions' },
            {'text': 'Stummoù kozhtesteniekaet', 'obj': 'attested_forms', 'keys': ['attested_form', 'litteral_year', 'book', 'reference']},
            {'text': 'Stummoù all', 'obj': 'other_forms', 'keys': ['usage_form', 'litteral_year', 'book', 'reference'] },
          ]
        }
      }
    },
    methods: {
      onSearch () {
        var search = ''
        if (this.model.city) {
          search += `city=${this.model.city.id}&`
        }

        this.$store.dispatch('locations/searchLocations', { search }).then(() => {
          let content = "data:text/csv;charset=utf-8,"
          this.fields.forEach(field => {
            content += field.text + ";"
          })
          content += "\r\n"
          for (let i = 0; i < this.locationsData.results.length; i++) {
            content += this.formatRow(this.locationsData.results[i]).join(";") + "\r\n"
          }
          const encodedUri = encodeURI(content)
          const link = document.createElement("a")
          link.setAttribute("href", encodedUri)
          link.setAttribute("download", "levrigoù.csv")
          document.body.appendChild(link)
          link.click();
        })
      },
      formatRow(line) {
        return this.fields.map(field => {
          if (field.obj) {
            if (field.obj) {
              return line[field.obj].map(res => { return field.keys.map(key => res[key]).join(' ') }).join(', ')
            }
          } else if (field.keys) {
            return field.keys.map(key => line[key]).join(' ')
          } else {
            return line[field.key]
          }
        })
      }
    },
    mounted () {
      this.$store.dispatch('cities/getAllCities')
      window.addEventListener('keydown', e => {
        if (e.keyCode == "13") {
          this.onSearch()
        }
      })
    }
  }
</script>

<style lang="sass">
.term-link
  font-size: 1rem !important
  font-weight: 400
  line-height: 1.75rem
  letter-spacing: .009375em !important
  font-family: Roboto,sans-serif !important
  border-bottom: 1px dotted #fff
  border-style: none none dotted
  cursor: pointer
</style>
