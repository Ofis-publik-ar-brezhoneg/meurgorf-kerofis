<template>
  <span
    v-if="!isAutoComplete"
  >
    <span
      class="px-5 py-3 text-center"
      v-if="terms_length == 0"
    >
      <h2>Mot inconnu</h2>
    </span>
    <base-material-card
      class="px-5 py-3"
      v-else-if="terms_length < 6"
    >
      <template
        v-slot:heading
      >
        <v-tabs
          v-model="tabs"
          background-color="transparent"
          slider-color="white"
        >
          <span
            class="subheading font-weight-light mx-3"
            style="align-self: center"
          >
            Resultats :
          </span>
          <v-tab
            class="mr-3"
            v-for="term in termsData.results"
            :key="term.id"
          >
            {{ term.canonic_form }} ({{ term.grammatical_category.title }})
          </v-tab>
        </v-tabs>
      </template>

      <v-tabs-items
        v-model="tabs"
        class="transparent"
      >
        <v-tab-item
          v-for="term in termsData.results"
          :key="term.id"
        >
          <v-card-text>
            <v-expansion-panels
              v-model="panel"
              :inset="true"
            >
              <v-expansion-panel
                v-if="term.grammatical_category"
              >
                <v-expansion-panel-header
                  expand-icon=""
                >
                  <strong>
                    {{ term.grammatical_category.title }}
                  </strong>
                </v-expansion-panel-header>
              </v-expansion-panel>
              <v-expansion-panel>
                <v-expansion-panel-header>
                  <strong>
                    Prononciation
                  </strong>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                </v-expansion-panel-content>
              </v-expansion-panel>
              <v-expansion-panel>
                <v-expansion-panel-header
                  expand-icon=""
                >
                  <span>
                    <strong>
                      Emploi :
                    </strong>
                    {{ term.usage }}
                  </span>
                </v-expansion-panel-header>
              </v-expansion-panel>
              <v-expansion-panel
                v-if="term.variants && term.variants.length"
              >
                <v-expansion-panel-header>
                  <strong>
                    Variantes historiques ou dialectales attestées
                  </strong>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <p v-for="variant in term.variants" :key="variant.id">
                    {{ variant.variant }}
                  </p>
                </v-expansion-panel-content>
              </v-expansion-panel>
              <v-expansion-panel
                v-if="term.parents && term.parents.length"
              >
                <v-expansion-panel-header
                  expand-icon=""
                >
                  <span>
                    <strong>
                      Mots parents
                    </strong>
                    <v-btn
                      v-for="parent in term.parents"
                      key="parent.id"
                      :to="{'name': 'MeurgorfKlaskId', params: {id: parent.id}}"
                    >
                      {{ parent.canonic_form }}
                    </v-btn>
                  </span>
                </v-expansion-panel-header>
              </v-expansion-panel>
              <v-expansion-panel>
                <v-expansion-panel-header>
                  <strong>
                    Définition
                  </strong>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <pre>{{ term.definition }}</pre>
                </v-expansion-panel-content>
              </v-expansion-panel>
              <v-expansion-panel
                v-if="term.derived_forms && term.derived_forms.length"
              >
                <v-expansion-panel-header>
                  <strong>
                    Formes fléchies ({{ term.derived_forms.length }})
                  </strong>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-btn color="primary">
                    <v-icon left>mdi-cloud</v-icon>
                    Exporter les formes fléchies
                  </v-btn>
                  <p>{{ term.derived_forms.map(f => f.form).join(', ') }}</p>
                </v-expansion-panel-content>
              </v-expansion-panel>
              <v-expansion-panel
                v-if="term.historical_occurrences && term.historical_occurrences.length"
              >
                <v-expansion-panel-header>
                  <strong>
                    Exemples historiques ({{ term.historical_occurrences.length }})
                  </strong>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <v-timeline>
                    <v-timeline-item
                      v-for="(occurrence, n) in term.historical_occurrences"
                      :key="n"
                      icon="mdi-star"
                      color="teal lighten-3"
                      small
                    >
                      <span slot="opposite">{{ occurrence.year }}</span>
                      <v-card class="elevation-2">
                        <v-card-title class="headline">
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <span v-bind="attrs" v-on="on">{{ occurrence.book.abbrevation }} {{ occurrence.reference }}</span>
                            </template>
                            <span>{{ occurrence.book.title }}</span>
                          </v-tooltip>
                        </v-card-title>
                        <v-card-text>
                          <pre>
                            {{ occurrence.occurence }}
                          </pre>
                        </v-card-text>
                      </v-card>
                    </v-timeline-item>
                  </v-timeline>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
            <div class="copy-clipboard">
              <v-btn
                color="primary"
                v-clipboard:copy="link_from_term_id(term.id)"
              >
                <v-icon left>mdi-clipboard</v-icon>
                Copier le lien
              </v-btn>
            </div>
          </v-card-text>
        </v-tab-item>
      </v-tabs-items>
    </base-material-card>
    <base-material-card
      v-else-if="terms_length >= 6"
    >
      <template
        v-slot:heading
      >
        Résultat {{ (current_page - 1) * 20 + 1 }}-{{ total_on_page }} sur {{ termsData.count }} - Page {{ current_page + 1 }}/{{ total_pages }}
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
            v-for="(term, i) in termsData.results"
            :key="i"
            align="center"
          >
            <v-col
              cols="1"
              md="3"
            >
              <router-link
                :to="{name: 'MeurgorfKlaskId', params: {id: term.id}}"
                class="tim-note"
                v-text="term.canonic_form"
                tag="span"
              />
            </v-col>
            <v-col cols="8">
              <router-link
                :to="{name: 'MeurgorfKlaskId', params: {id: term.id}}"
                class="tim-note"
                v-text="term.grammatical_category.title"
                tag="span"
              />
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </base-material-card>
  </span>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    name: 'index',
    computed: {
      ...mapState('terms', { 'termsData': 'getInfoData', 'isAutoComplete': 'isAutoComplete' }),
      terms_length () {
        return this.termsData && !this.isAutoComplete ? this.termsData.count : 0
      },
      total_pages () {
        return this.termsData && !this.isAutoComplete ? Math.ceil(this.termsData.count / 20) : 0
      },
      total_on_page () {
        return this.termsData && !this.isAutoComplete ? (this.current_page - 1) * 20 + this.termsData.results.length : 0
      }
    },
    data () {
      return {
        current_page: 1,
        panel: [],
        tabs: 0
      }
    },
    methods: {
      link_from_term_id (term_id) {
        var url = new URL(window.location.href);
        url.pathname = this.$router.resolve({ name: 'MeurgorfKlaskId', params: { id: term_id }}).href
        return url.href
      }
    },
    watch: {
      current_page (val) {
        this.$emit('change_page', val)
      },
    }
  }
</script>

<style lang="sass">
.copy-clipboard
  margin-top: 1em
pre
 white-space: pre-wrap
 white-space: -moz-pre-wrap
 white-space: -pre-wrap
 white-space: -o-pre-wrap
 word-wrap: break-word

</style>
