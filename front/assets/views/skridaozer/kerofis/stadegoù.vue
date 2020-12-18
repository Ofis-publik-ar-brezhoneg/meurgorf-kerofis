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
                  align="center"
                >
                  <v-col
                    cols="2"
                  >
                    {{ statsData.locations }}
                  </v-col>
                  <v-col
                    cols="8"
                  >
                    enrolladenn  en  diaz.
                  </v-col>
                </v-row>
                <v-row
                  align="center"
                >
                  <v-col
                    cols="2"
                  >
                    {{ statsData.phonetic_transcription }}
                  </v-col>
                  <v-col
                    cols="8"
                  >
                    distagadur evit
                  </v-col>
                  <v-col
                    cols="2"
                  >
                    {{ statsData.locations_with_phonetic }}
                    anv-lec'h
                  </v-col>
                </v-row>
                <v-row
                  align="center"
                >
                  <v-col
                    cols="2"
                  >
                    {{ statsData.normalized_forms }}
                  </v-col>
                  <v-col
                    cols="8"
                  >
                    stumm  skoueriekaet
                  </v-col>
                  <v-col
                    cols="2"
                  >
                    {{ ((statsData.normalized_forms / statsData.locations) * 100).toFixed(2) }}
                    %
                  </v-col>
                </v-row>
                <v-row
                  align="center"
                >
                  <v-col
                    cols="2"
                  >

                  </v-col>
                  <v-col
                    cols="8"
                  >
                    Aotre da embann
                  </v-col>
                  <v-col
                    cols="2"
                  >

                  </v-col>
                </v-row>
                <v-row
                  align="center"
                >
                  <v-col
                    cols="2"
                  >
                    {{ statsData.public_locations }}
                  </v-col>
                  <v-col
                    cols="8"
                  >
                    Lec'hanvadurezh
                  </v-col>
                  <v-col
                    cols="2"
                  >
                    {{ ((statsData.public_locations / statsData.locations) * 100).toFixed(2) }}
                    %
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
                  <v-col cols="4">
                    <span
                      v-text="`${ statsData[t.k] }`"
                    />
                  </v-col>
                  <v-col
                    cols="8"
                  >
                    <span
                      class="tim-note"
                      v-text="t.title"
                    />
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </base-material-card>
        </v-col>
      </v-row>
      <v-row
        justify="center"
      >
      <v-col
          cols="12"
          sm="8"
          md="4"
        >
          <base-material-card
            icon="mdi-poll-box"
            v-if="statsData.by_department"
          >
            <v-card-text>
              <v-container
                class="pa-0"
                fluid
              >
                <v-row
                  v-for="(t, i) in statsData.by_department"
                  :key="i"
                  align="center"
                >
                  <v-col
                    cols="8"
                  >
                    <span
                      class="tim-note"
                      v-text="t.department__name_bre"
                    />
                  </v-col>
                  <v-col cols="2">
                    <span
                      v-text="t.locations_count"
                    />
                  </v-col>
                  <v-col cols="2">
                    <span
                      v-text="`${ ((t.locations_count / statsData.locations) * 100).toFixed(2) } %`"
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
                  v-for="(t, i) in statsData.categories"
                  :key="i"
                  align="center"
                >
                  <v-col
                    cols="8"
                  >
                    <span
                      class="tim-note"
                      v-text="t.name"
                    />
                  </v-col>
                  <v-col cols="2">
                    <span
                      v-text="t.locations_count"
                    />
                  </v-col>
                  <v-col cols="2">
                    <span
                      v-text="`${ ((t.locations_count / statsData.locations) * 100).toFixed(2) } %`"
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
          {title: 'stumm kozh testeniekaet', k: 'old_forms'},
          {title: 'stumm  brezhoneg  testeniekaet', k: 'attested_forms'},
          {title: 'stumm all implijet', k: 'other_forms'},
          {title: 'daveenn douaroniel', k: 'has_coordinates'},
          {title: 'deiziad ofisielisaet', k: 'has_formalized_date'},
          {title: 'ign', k: 'is_on_ign'},
          {title: 'gerdarzh fra', k: 'etymological_note_fra'},
          {title: 'gerdarzh bre', k: 'etymological_note_bre'},
          {title: 'goulenn', k: 'nb_query'},
          {title: 'distagadur skouer', k: 'standard_phonetic'},
          {title: 'distagadur enrolladenn', k: 'phonetic_links'},
        ],
      }
    },
    computed: {
      ...mapState('stats', {'statsData': 'getInfoData'}),
    },
    mounted () {
      this.$store.dispatch('users/getCurrentUser')
      this.$store.dispatch('stats/getStats', 'kerofis')
    }
  }
</script>
