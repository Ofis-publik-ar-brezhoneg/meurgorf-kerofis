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
                      v-if="$route.params.id"
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Stumm Kein
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-location-name-panel />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Titouroù hollek
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-location-panel :isNew="!$route.params.id" />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Stumm skoueriekaet
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-standardized-location-panel :isNew="!$route.params.id" />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Distagadur
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-phonetic-location-panel :isNew="!$route.params.id" />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Stumm kozh
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-old-form-location-panel :isNew="!$route.params.id" />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Stumm all en implij
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-other-form-location-panel :isNew="!$route.params.id" />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        Stumm brezhoneg testeniekaet
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-attested-form-location-panel :isNew="!$route.params.id" />
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel
                    >
                      <v-expansion-panel-header
                        expand-icon=""
                      >
                        A bep seurt
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <edit-notes-location-panel :isNew="!$route.params.id" />
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
        panels: [0, 4],
      }
    },
    components: {
      EditLocationPanel: () => import('../../../components/panels/EditLocationPanel.vue'),
      EditLocationNamePanel: () => import('../../../components/panels/EditLocationNamePanel.vue'),
      EditStandardizedLocationPanel: () => import('../../../components/panels/EditStandardizedLocationPanel.vue'),
      EditPhoneticLocationPanel: () => import('../../../components/panels/EditPhoneticLocationPanel.vue'),
      EditOldFormLocationPanel: () => import('../../../components/panels/EditOldFormLocationPanel.vue'),
      EditOtherFormLocationPanel: () => import('../../../components/panels/EditOtherFormLocationPanel.vue'),
      EditAttestedFormLocationPanel: () => import('../../../components/panels/EditAttestedFormLocationPanel.vue'),
      EditNotesLocationPanel: () => import('../../../components/panels/EditNotesLocationPanel.vue'),
    },
    computed: {
      ...mapState('terms', { 'newTermsData': 'postInfoData' }),
    },
    mounted () {
      this.$store.dispatch('users/getCurrentUser')
      this.$store.dispatch('cities/getAllCities')
      this.$store.dispatch('books/getAllBooks')
      this.$store.dispatch('location_categories/getAllCategories')
      this.$store.dispatch('informants/getAllInformants')
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
            this.$store.dispatch('locations/getLocation', val)
          } else {
            this.$store.dispatch('locations/reset')
          }
        },
        immediate: true
      }
    },
  }
</script>
