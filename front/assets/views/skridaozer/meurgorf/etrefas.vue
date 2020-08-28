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
          <base-material-card
            icon="mdi-database-plus"
          >
            <v-card-text>
              <v-row
                align="center"
                justify="center"
              >
                <v-col
                  cols="12"
                >
                  <v-expansion-panels
                    inset
                    multiple
                    :value="panels"
                  >
                    <v-expansion-panel
                      :readonly="true"
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Pennger
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-term-panel :isNew="!$route.params.id" />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                      v-if="$route.params.id"
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Adpennger
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-term-variants-panel />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                      v-if="$route.params.id"
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Termenadur
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-term-definition-panel />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                      v-if="$route.params.id"
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Stummoù deveret
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-term-derived-form-panel />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                      v-if="$route.params.id"
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Stummoù istorel testeniekaet
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-term-historical-occurrence-panel />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                      v-if="$route.params.id"
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Notennoù studiañ
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-term-study-note-panel />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                      v-if="$route.params.id"
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Gerdarzh
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-term-etymology-panel />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                      v-if="$route.params.id"
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Penngerioù kar
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-term-parent-panel />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </v-col>
              </v-row>
            </v-card-text>
          </base-material-card>
        </v-col>
      </v-row>
    </v-container>
  </base-app>
</template>

<script>
  import { mapState } from 'vuex'

  export default {
    name: 'Home',
    data () {
      return {
        panels: [0],
      }
    },
    components: {
      EditTermPanel: () => import('../../../components/panels/EditTermPanel.vue'),
      EditTermVariantsPanel: () => import('../../../components/panels/EditTermVariantsPanel.vue'),
      EditTermDefinitionPanel: () => import('../../../components/panels/EditTermDefinitionPanel.vue'),
      EditTermDerivedFormPanel: () => import('../../../components/panels/EditTermDerivedFormPanel.vue'),
      EditTermHistoricalOccurrencePanel: () => import('../../../components/panels/EditTermHistoricalOccurrencePanel.vue'),
      EditTermStudyNotePanel: () => import('../../../components/panels/EditTermStudyNotePanel.vue'),
      EditTermEtymologyPanel: () => import('../../../components/panels/EditTermEtymologyPanel.vue'),
      EditTermParentPanel: () => import('../../../components/panels/EditTermParentPanel.vue'),
    },
    computed: {
      ...mapState('terms', { 'newTermsData': 'postInfoData' }),
    },
    mounted () {
      this.$store.dispatch('users/getCurrentUser')
      this.$store.dispatch('books/getAllBooks')
      this.$store.dispatch('categories/getAllCategories')
    },
    watch: {
      newTermsData (val) {
        if (!this.$route.params.id) {
          this.$router.push({name: 'SkridaozerMeurgorfEtrefasId', params: { id: val.id }})
        }
      },
      '$route.params.id': {
        handler (val) {
          if (val) {
            this.$store.dispatch('terms/getTerm', val)
          } else {
            this.$store.dispatch('terms/reset')
          }
        },
        immediate: true
      }
    },
  }
</script>
