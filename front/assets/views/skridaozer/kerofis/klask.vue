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
        >
          <base-material-card
            v-if="locationsData"
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
                  align="center"
                >
                  <v-col
                    cols="1"
                  >
                    Stagadenn
                  </v-col>
                  <v-col
                    cols="1"
                  >
                    Lec’hanv
                  </v-col>
                  <v-col
                    cols="1"
                  >
                    Kumun
                  </v-col>
                  <v-col
                    cols="1"
                  >
                    Rummad
                  </v-col>
                  <v-col
                    cols="1"
                  >
                    Departamant
                  </v-col>
                  <v-col
                    cols="1"
                    v-if="model.display_normalized"
                  >
                    Ar stummoù skoueriekaet
                  </v-col>
                  <v-col
                    cols="1"
                    v-if="model.has_coordinated"
                  >
                    Daveennoù douaroniel
                  </v-col>
                  <v-col
                    cols="1"
                    v-if="model.is_on_ign"
                  >
                    Kaset d’an IGN
                  </v-col>
                  <v-col
                    cols="1"
                    v-if="model.is_official"
                  >
                    Bet ofisialisaet
                  </v-col>
                  <v-col
                    cols="1"
                    v-if="model.is_public"
                  >
                    Embannet
                  </v-col>
                </v-row>
                <v-row
                  v-for="(t, i) in locationsData.results"
                  :key="i"
                  align="center"
                >
                  <v-col
                    cols="1"
                  >
                    <router-link
                      v-text="t.generic_name"
                      tag="span"
                      class="term-link"
                      :to="{ name: 'SkridaozerKerofisEtrefas', params: { id: t.id }}"
                    />
                  </v-col>
                  <v-col
                    cols="1"
                  >
                    <router-link
                      v-text="t.name"
                      tag="span"
                      :to="{ name: 'SkridaozerKerofisEtrefas', params: { id: t.id }}"
                    />
                  </v-col>
                  <v-col
                    cols="1"
                  >
                    <span v-if="t.city">
                      <router-link
                        v-text="t.city.name_bre"
                        tag="span"
                        :to="{ name: 'SkridaozerKerofisEtrefas', params: { id: t.id }}"
                      />
                    </span>
                  </v-col>
                  <v-col
                    cols="1"
                  >
                    <span v-if="t.category">
                      <router-link
                        v-text="t.category.name"
                        tag="span"
                        :to="{ name: 'SkridaozerKerofisEtrefas', params: { id: t.id }}"
                      />
                    </span>
                  </v-col>
                  <v-col
                    cols="1"
                  >
                    <span v-if="t.city">
                      <router-link
                        v-text="t.city.department"
                        tag="span"
                        :to="{ name: 'SkridaozerKerofisEtrefas', params: { id: t.id }}"
                      />
                    </span>
                  </v-col>
                  <v-col
                    cols="1"
                    v-if="display_normalized"
                  >
                    <span
                     v-for=standardized_form for t.standardized_forms"
                    >
                      {{ standardized_form }}
                    </span>
                  </v-col>
                  <v-col
                    cols="1"
                    v-if="model.has_coordinated"
                  >
                    <span
                      v-if="t.latitude"
                    >
                      Ya
                    </span>
                  </v-col>
                  <v-col
                    cols="1"
                    v-if="model.is_on_ign"
                  >
                    <span
                      v-if="t.on_ign"
                    >
                      Ya
                    </span>
                    <span
                      v-else
                    >
                      N'eo ket
                    </span>
                  </v-col>
                  <v-col
                    cols="1"
                    v-if="model.is_official"
                  >
                    <span
                      v-if="t.formalized_date"
                    >
                      Ya
                    </span>
                    <span
                      v-else
                    >
                      N'eo ket
                    </span>
                  </v-col>
                  <v-col
                    cols="1"
                    v-if="model.is_public"
                  >
                    <span
                      v-if="t.is_public"
                    >
                      Ya
                    </span>
                    <span
                      v-else
                    >
                      N'eo ket
                    </span>
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
          generic_name: '',
          name: '',
          search_keyword: '',
          city: '',
          department: '',
          category: '',
          search_type: 'exact',
          is_old: false,
          is_normalized: false,
          is_attested: false,
          display_normalized: false,
          has_coordinated: false,
          is_on_ign: false,
          is_official: false,
          is_public: false
        },
        current_page: 1,
        search: '',
      }
    },
    computed: {
      ...mapState('locations', {'locationsData': 'getInfoData'}),
      ...mapState('location_categories', { 'categoriesData': 'getInfoData' }),
      total_pages () {
        return this.locationsData ? Math.ceil(this.locationsData.count / 20) : 0
      },
      total_on_page () {
        return this.locationsData ? (this.current_page - 1) * 20 + this.locationsData.results.length : 0
      },
      schema () {
        if (!this.categoriesData) {
            return {}
        }
        return {
          generic_name: { type: 'text', label: 'Stagadenn', filled: true },
          name: { type: 'text', label: 'Lec’hanv', filled: true },
          search_keyword: { type: 'text', label: 'Gerioù-alc’hwez', filled: true },
          city: { type: 'text', label: 'Kumun', filled: true },
          department: { type: 'text', label: 'Departamant', filled: true },
          category: {
            type: 'select',
            label: 'Rummad',
            col: 2,
            items: this.categoriesData.map(category => category.name),
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
          is_old: { type: 'checkbox', label: 'Er stummoù kozh kepken' },
          is_normalized: { type: 'checkbox', label: 'Er stummoù skoueriekaet hepken' },
          is_standardized: { type: 'checkbox', label: 'Er stummoù testeniekaet hepken' },
          display_normalized: { type: 'checkbox', label: 'Ar stummoù skoueriekaet' },
          has_coordinated: { type: 'checkbox', label: 'Gant daveennoù douaroniel' },
          is_on_ign: { type: 'checkbox', label: 'Kaset d’an IGN' },
          is_official: { type: 'checkbox', label: 'Bet ofisialisaet' },
          is_public: { type: 'checkbox', label: 'Embannet' }
        }
      }
    },
    methods: {
      onSearch () {
          this.search = ''
          if (this.model.category) {
            this.search += `category=${this.model.category}&`
          }
          if (this.model.generic_name) {
            this.search += `generic_name_${this.model.search_type}=${this.model.generic_name}&`
          }
          if (this.model.name) {
            if (this.is_old) {
              this.search += 'old_'
            } else if (this.is_normalized) {
              this.search += 'normalized_'
            } else if (this.is_standardized) {
              this.search += 'standardized_'
            }
            this.search += `name_${this.model.search_type}=${this.model.name}&`
          }
          if (this.model.search_keyword) {
            this.search += `search_keyword_${this.model.search_type}=${this.model.search_keyword}&`
          }
          if (this.model.city) {
            this.search += `city_${this.model.search_type}=${this.model.city}&`
          }
          if (this.model.department) {
            this.search += `department_${this.model.search_type}=${this.model.department}&`
          }

          this.$store.dispatch('locations/searchLocations', { search: this.search })
      }
    },
    mounted () {
      this.$store.dispatch('location_categories/getAllCategories')
      window.addEventListener('keydown', e => {
        if (e.keyCode == "13") {
          this.onSearch()
        }
      })
    },
    watch: {
      current_page (page) {
        this.$store.dispatch('locations/searchLocations', { search: `${this.search}&page=${page}` })
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
