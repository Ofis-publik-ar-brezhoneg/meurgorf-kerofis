<template>
  <base-app>
    <v-container
        id="typography"
        fluid
        tag="section"
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col cols="12">
            <base-material-card
              icon="mdi-book"
            >
              <v-card-text>
                <p>
                  Meurgorf est un dictionnaire historique. Le lecteur y trouvera des exemples d'emploi tirés d'oeuvres variées
                  depuis l'époque du moyen breton jusqu'à nos jours. Tous les exemples sont référencés. Cette page propose la liste
                  des sources utilisées dans le dictionnaire. Comme le dictionnare, elle est actualisée en continu.
                </p>
                <v-container
                  class="pa-0"
                  fluid
                  v-if="!booksPending"
                >
                  <v-row
                    v-for="(t, i) in booksData"
                    :key="i"
                    align="center"
                  >
                    <v-col
                      cols="1"
                      md="3"
                    >
                      <span
                        class="abbrevation"
                        v-text="t.abbrevation"
                      />
                    </v-col>
                    <v-col cols="8">
                      <p>
                        {{ t.title }} ; {{ t.author }}
                        <br />
                        {{ t.description }}
                      </p>
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
    name: 'Index',
    components: {
      VFormBase
    },
    data () {
      return {
        myModel: {
          is_active: true,
          abbrevation: '',
          title: '',
          description: '',
          author: '',
          is_kerofis_old: false,
          is_kerofis_other: false,
          is_kerofis_attested: false,
          is_meurgorf: false
        },
        mySchema: {
          is_active: { type: 'checkbox', label: 'Bev' },
          abbrevation: { type: 'text', label: 'Berradur' },
          title: { type: 'text', label: 'Levr' },
          description: { type: 'text', label: 'Deskrivadur' },
          author: { type: 'text', label: 'Aozer' },

          is_kerofis_old: { type: 'checkbox', label: 'Stummoù kozh' },
          is_kerofis_other: { type: 'checkbox', label: 'Stummoù all' },
          is_kerofis_attested: { type: 'checkbox', label: 'Stummoù testeniekaet' },
          is_meurgorf: { type: 'checkbox', label: 'Meurgorf' },
        },
        typography: {
          '': ['Paragraph', 'leader'],
        },
      }
    },
    mounted () {
      this.$store.dispatch('books/getAllBooks')
    },
    computed: {
      ...mapState('books', {
        'booksPending': 'getInfoPending',
        'booksData': 'getInfoData'
      }),
    },
    methods: {
      Submit () {
        this.$store.dispatch('books/AddNewBook', this.myModel)
      }
    }
  }
</script>

<style lang="scss" scoped>
  .abbrevation {
    bottom: 10px;
    display: block;
    font-weight: 400;
    font-size: 15px;
    line-height: 13px;
    left: 0;
    margin-left: 20px;
    width: 260px;
  }
</style>
