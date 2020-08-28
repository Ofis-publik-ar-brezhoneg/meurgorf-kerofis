<template>
  <base-material-card>
          <template v-slot:heading>
            <div class="subtitle-1 font-weight-light">
              Dictionnaire historique Meurgorf
            </div>
          </template>
          <v-form
            v-model="valid"
          >
            <v-container>
              <v-row>
                <v-col
                  cols="12"
                  md="8"
                >
                  <v-menu
                    v-model="term_complete"
                    :close-on-click="true"
                    :close-on-content-click="true"
                    nudge-bottom="50"
                  >
                    <template v-slot:activator="{ on }">
                      <v-text-field
                        v-model="term"
                        label="Terme recherché"
                        :rules="rules"
                        required
                        @click="onTermClick"
                      >
                      </v-text-field>
                    </template>
                    <v-list
                      v-if="isAutoComplete && termsData"
                    >
                      <v-list-item
                        v-for="(item, index) in termsData.results"
                        :to="{name: 'MeurgorfKlaskId', params: {id: item.id}}"
                        :key="index"
                      >
                        <v-list-item-title>
                          {{ item.canonic_form }}
                        </v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-menu>
                 </v-col>
              </v-row>
              <v-row>
                <v-col
                  cols="12"
                  md="16"
                >
                <v-row>
                  <v-col
                    md="8">
                    <v-row>
                      <v-col>
                        <v-select
                          v-model="category"
                          :items="categoriesData"
                          item-text="title"
                          item-value="id"
                          no-data-text="Aucune catégorie"
                          label="Catégorie"
                          clearable
                        ></v-select>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <v-select
                          v-model="book"
                          :items="booksData"
                          item-text="abbrevation"
                          item-value="id"
                          no-data-text="Aucune source"
                          label="Sources"
                          clearable
                        ></v-select>
                      </v-col>
                    </v-row>
                  </v-col>
                  <v-col>
                    <v-checkbox
                      v-model="search_position"
                      value="contains"
                      label="Partie de mot"
                    ></v-checkbox>
                    <v-checkbox
                      v-model="search_position"
                      value="startswith"
                      label="Début de mot"
                    ></v-checkbox>
                    <v-checkbox
                      v-model="search_position"
                      value="endswith"
                      label="Fin de mot"
                    ></v-checkbox>
                  </v-col>
                </v-row>
                </v-col>
              </v-row>
              <div>
                <v-btn large
                  :color="button_color"
                  @click="OnSearchClick"
                >
                  Rechercher
                </v-btn>
              </div>
            </v-container>
          </v-form>
        </base-material-card>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    name: 'index',
    data () {
      return {
        valid: false,
        term: '',
        rules: [
          value => !!value || 'Obligatoire.'
        ],
        term_complete: false,
        search_position: '',
        category: null,
        book: null,
      }
    },
    computed: {
      ...mapState('books', { 'booksData': 'getInfoData' }),
      ...mapState('categories', { 'categoriesData': 'getInfoData' }),
      ...mapState('terms', { 'termsData': 'getInfoData', 'isAutoComplete': 'isAutoComplete' }),
      button_color () {
        return this.valid ? 'green' : 'white'
      },
    },
    methods: {
      OnSearchClick () {
        if (this.valid) {
          var search = '';
          if (this.category) {
            search += `grammatical_category=${this.category}&`
          }
          if (this.book) {
            search += `historical_occurrences__book=${this.book}&`
          }
          search += `term_${this.search_position}=${this.term}`
          this.$emit('search', { search })
        }
      },
      onTermClick () {
        if (!this.search_position && this.termsData && this.termsData.count) {
          this.term_complete = true
        }
      }
    },
    mounted () {
      this.$store.dispatch('books/getAllBooks')
      this.$store.dispatch('categories/getAllCategories')
    },
    watch: {
      term (val) {
        if(!this.search_position) {
          this.$emit('search', {
            search: `term_contains=${val}&autocomplete=1`,
            isAutoComplete: true
          })
        }
      },
      termsData () {
        if (!this.search_position && this.termsData && this.termsData.count) {
          this.term_complete = true
        }
      },
    },
  }
</script>
