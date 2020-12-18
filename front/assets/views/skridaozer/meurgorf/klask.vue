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
          <base-material-card title="Klask pennger">
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
          </base-material-card>
        </v-col>
      </v-row>
      <v-row
        align="center"
        justify="center"
      >
        <v-col
          cols="12"
          sm="10"
          md="8"
        >
          <base-material-card
            v-if="termsData"
          >
            <template
              class="display-2 font-weight-light px-3 py-1"
              v-slot:heading
            >
              Disoc’h : {{ (current_page - 1) * 20 + 1 }}-{{ total_on_page }} - Page {{ current_page }}/{{ total_pages }}
              <v-pagination
                v-model="current_page"
                :length="total_pages"
                :total-visible="8"
                light
              ></v-pagination>
            </template>
            <v-card-text>
              <v-container
                class="pa-0"
                fluid
              >
                <v-row
                  v-for="(t, i) in termsData.results"
                  :key="i"
                  align="center"
                >
                  <v-col
                    cols="1"
                    md="3"
                  >
                    <router-link
                      v-text="t.canonic_form"
                      tag="span"
                      class="term-link"
                      :to="{ name: 'SkridaozerMeurgorfEtrefasId', params: { id: t.id }}"
                    />
                  </v-col>
                  <v-col cols="8">
                    <router-link
                      v-text="t.grammatical_category.title"
                      tag="span"
                      :to="{ name: 'SkridaozerMeurgorfPennger', params: { id: t.id }}"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
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
          term: '',
          occurrence_historique: '',
          category: '',
          book: '',
          search_type: 'exact',
        },
        current_page: 1,
        search: '',
      }
    },
    computed: {
      ...mapState('terms', {'termsData': 'getInfoData'}),
      ...mapState('books', { 'booksData': 'getInfoData' }),
      ...mapState('categories', { 'categoriesData': 'getInfoData' }),
      total_pages () {
        return this.termsData ? Math.ceil(this.termsData.count / 20) : 0
      },
      total_on_page () {
        return this.termsData ? (this.current_page - 1) * 20 + this.termsData.results.length : 0
      },
      schema () {
        if (!this.categoriesData || !this.booksData) {
            return {}
        }
        return {
          term: { type: 'text', label: 'Pennger', filled: true },
          historical_occurrence: { type: 'text', label: 'Stumm istorel', filled: true },
          category: {
            type: 'select',
            label: 'Rummenn-ger',
            col: 2,
            items: this.categoriesData.map(category => category.title),
            filled: true
          },
          bool: {
            type: 'select',
            label: 'Oberenn',
            col: 4,
            items: this.booksData.map(book => book.title),
            filled: true
          },
          search_type: {
            type: 'radio',
            row: true,
            options: [
              {'label': 'Darn eus ar ger', 'value': 'contains'},
              {'label': 'ger a-bezh', 'value': 'exact'},
              {'label': 'Deroù ar ger', 'value': 'startswith'},
              {'label': 'Dibenn ar ger', 'value': 'endswith'}
            ]
          },
        }
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

          this.$store.dispatch('terms/searchTerms', { search: this.search })
      }
    },
    mounted () {
      this.$store.dispatch('categories/getAllCategories')
      this.$store.dispatch('books/getAllBooks')
      window.addEventListener('keydown', e => {
        if (e.keyCode == "13") {
          this.onSearch()
        }
      })
    },
    watch: {
      current_page (page) {
        this.$store.dispatch('terms/searchTerms', { search: `${this.search}&page=${page}` })
      }
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
