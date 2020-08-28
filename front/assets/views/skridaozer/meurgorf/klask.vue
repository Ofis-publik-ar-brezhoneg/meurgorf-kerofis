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
          sm="10"
          md="5"
        >
          <base-material-card>
            <template v-slot:heading>
              <div class="display-2 font-weight-light">
                Klask pennger
              </div>
            </template>
            <v-form>
              <v-form-base
                :model="model"
                :schema="schema"
                class="title br-8 mx-2 pa-2"
              >
              </v-form-base>
              <v-btn
                color="green"
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
          sm="8"
          md="4"
        >
          <base-material-card
            icon="mdi-book"
            v-if="termsData"
          >
            <template
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
        current_page: 1,
        search: '',
      }
    },
    computed: {
      ...mapState('terms', {'termsData': 'getInfoData'}),
      total_pages () {
        return this.termsData ? Math.ceil(this.termsData.count / 20) : 0
      },
      total_on_page () {
        return this.termsData ? (this.current_page - 1) * 20 + this.termsData.results.length : 0
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
    watch: {
      current_page (page) {
        this.$store.dispatch('terms/searchTerms', { search: `${this.search}&page=${page}` })
      }
    }
  }
</script>
