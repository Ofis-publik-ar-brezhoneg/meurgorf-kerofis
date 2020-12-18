<template>
  <span>
    <v-simple-table>
      <template v-slot:default>
        <tbody>
          <tr
            v-for="item in termsData.parents"
            :key="item.id"
          >
            <td>
              {{ item.canonic_form }}
            </td>
            <td>
              <span
                v-if="item.grammatical_category"
              >
                {{ item.grammatical_category.title }}
              </span>
            </td>
            <td>
              <v-btn
                icon
                @click="delete_parent(item)"
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
    <v-dialog
      v-model="dialog"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="teal lighten-3"
          dark
          v-bind="attrs"
          v-on="on"
        >
          Kas
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="headline grey lighten-2">
          Penngerioù kar
        </v-card-title>

        <v-card-text>
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
              Klask
            </v-btn>
          </v-form>
          <v-simple-table
            v-if="parentsData"
          >
            <template v-slot:default>
              <tbody>
                <tr
                  v-for="item in parents"
                  :key="item.id"
                >
                  <td>
                    {{ item.canonic_form }}
                  </td>
                  <td
                    v-if="!item.is_parent"
                  >
                    <v-btn
                      icon
                      @click="add_parent(item)"
                    >
                      <v-icon>
                        mdi-plus
                      </v-icon>
                    </v-btn>
                  </td>
                  <td
                    v-else
                  >
                    <v-btn
                      icon
                      color="teal lighten-3"
                    >
                      <v-icon>
                        mdi-check
                      </v-icon>
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="dialog = false"
          >
            Ok
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
        dialog: false,
        model: {
          term: '',
          occurrence_historique: '',
          category: '',
          book: '',
          search_type: '',
        },
        schema: {
          term: { type: 'text', label: 'Pennger' },
          historical_occurrence: { type: 'text', label: 'Stumm istorel' },
          category: { type: 'text', label: 'Rummenn-ger' },
          book: { type: 'text', label: 'Oberenn' },
          search_type: {
            type: 'radio',
            row: true,
            options: [
              {'label': 'Darn eus ar ger', 'value': 'contains'},
              {'label': 'Ger-bezh', 'value': 'exact'},
              {'label': 'Deroù ar ger', 'value': 'startswith'},
              {'label': 'Dibenn ar ger', 'value': 'endswith'}
            ]
          },
        },
      }
    },
    computed: {
      ...mapState('categories', { 'categoriesData': 'getInfoData' }),
      ...mapState('terms', { 'termsData': 'getInfoData', 'parentsData': 'fpInfoData' }),
      parents () {
        let inTermParents = []
        if(this.termsData && this.termsData.parents) {
          this.termsData.parents.forEach((parent) => {
            inTermParents.push(parent.id)
          })
        }
        if(this.parentsData && this.parentsData.results) {
          return this.parentsData.results.map((term) => {
            return {
              ...term,
              is_parent: inTermParents.includes(term.id)
            }
          })
        }
        return []
      }
    },
    methods: {
      onSearch () {
        this.search = ''
        var search_type = 'contains'
        if (this.model.category) {
          this.search += `grammatical_category=${this.model.category}&`
        }
        if (this.model.book) {
          this.search += `historical_occurrences__book=${this.model.book}&`
        }
        if (this.model.term) {
          this.search += `term_${this.model.search_type}=${this.model.term}&`
        }
        if (this.model.historical_occurrence) {
          this.search += `historical_occurrence_${this.model.search_type}=${this.model.historical_occurrence}`
        }

        this.$store.dispatch('terms/searchTerms', { search: this.search, isForParent: true })
      },
      add_parent (term) {
        let data = { "parents": this.termsData.parents }
        data.parents.push({'id': term.id})
        const term_id = this.$route.params.id
        this.$store.dispatch('terms/updateTerm', { term_id, data })
      },
      delete_parent (term) {
        let data = { "parents": this.termsData.parents.filter(parent => parent.id != term.id) }
        const term_id = this.$route.params.id
        this.$store.dispatch('terms/updateTerm', { term_id, data })
      }
    },
  }
</script>
