<template>
  <base-app>
    <v-container
      fluid
    >
      <v-row
        justify="center"
      >
        <v-col
          cols="12"
          sm="8"
          md="4"
        >
          <base-material-card
            icon="mdi-finance"
            v-if="statsData"
          >
            <v-card-text>
              <v-container
                class="pa-0"
                fluid
              >
                <v-row
                  v-for="(t, i) in statsCols"
                  :key="i"
                  align="center"
                >
                  <v-col
                    cols="8"
                  >
                    <span
                      class="tim-note"
                      v-text="t.title"
                    />
                  </v-col>
                  <v-col cols="4">
                    <span
                      v-text="`${ statsData[t.k] }`"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </base-material-card>
        </v-col>
        <v-col
          cols="12"
          sm="8"
          md="4"
        >
          <base-material-card
            icon="mdi-poll-box"
            v-if="statsData"
          >
            <v-card-text>
              <v-container
                class="pa-0"
                fluid
              >
                <v-row
                  v-for="(t, i) in statsData.grammatical_categories"
                  :key="i"
                  align="center"
                >
                  <v-col
                    cols="8"
                  >
                    <span
                      class="tim-note"
                      v-text="t.title"
                    />
                  </v-col>
                  <v-col cols="2">
                    <span
                      v-text="t.terms_count"
                    />
                  </v-col>
                  <v-col cols="2">
                    <span
                      v-text="`${ ((t.terms_count / statsData.terms) * 100).toFixed(2) } %`"
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

  export default {
    name: 'Home',
    data () {
      return {
        statsCols: [
          {title: 'Pennger en diaz', k: 'terms'},
          {title: 'Stumm istorel testeniekaet', k: 'historical_occurences'},
          {title: 'Adpennger', k: 'variants'},
          {title: 'Stumm deveret skouer', k: 'derived_forms'},
          {title: 'Stumm deveret all', k: 'principal_derived_forms'},
          {title: 'Termenadur', k: 'definitions'},
          {title: 'Displegadur gerdarzhel', k: 'etymologies'},
          {title: 'Notenn studiañ', k: 'study_notes'},
          {title: 'Distagadur', k: 'phonetic_forms'},
          {title: 'Distagadur enrolladenn', k: 'phonetic_links'},
          {title: 'Reket', k: 'searchs'},
        ],
      }
    },
    computed: {
      ...mapState('stats', {'statsData': 'getInfoData'}),
    },
    mounted () {
      this.$store.dispatch('users/getCurrentUser')
      this.$store.dispatch('stats/getStats', 'meurgorf')
    }
  }
</script>
