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
          <base-material-card>
            <template v-slot:heading>
              <div class="display-2 font-weight-light">
                Mammennoù
              </div>
            </template>
            <v-card-text>
              <v-container
                class="pa-0"
                fluid
                v-if="!getInfoPending"
              >
              <v-form>
                <v-form-base
                  :model="model"
                  :schema="schema"
                >
                </v-form-base>
                <v-btn
                  large
                  color="green"
                  @click="Submit"
                  v-text="action"
                />
              </v-form>
              </v-container>
            </v-card-text>
          </base-material-card>
        </v-col>
      </v-row>
      <base-material-card
        icon="mdi-book"
        v-if="!$route.params.id"
      >
      <v-card-text>
        <v-container
          class="pa-0"
          fluid
          v-if="!getInfoPending"
        >
          <v-row
            v-for="(t, i) in getInfoData"
            :key="i"
            align="center"
          >
            <v-col
              cols="1"
              md="3"
            >
              <router-link
                :to="{name:'SkridaozerMammennoùId', params: {id: t.id}}"
                class="abbrevation"
                v-text="t.abbrevation"
                tag="span"
              />
            </v-col>
            <v-col cols="8">
              <router-link
                :to="{name:'SkridaozerMammennoùId', params: {id: t.id}}"
                tag="p"
              >
                {{ t.title }} ; {{ t.author }}
                <br />
                {{ t.description }}
              </router-link>
            </v-col>
          </v-row>
        </v-container>
        </v-card-text>
      </base-material-card>
      <error-snack
        prefix="book"
        :messages="messages"
      />
    </v-container>
  </base-app>
</template>

<script>
  import { mapState } from 'vuex'
  import ErrorSnack from '../../components/base/ErrorSnack.vue'
  import VFormBase from 'vuetify-form-base'

  export default {
    name: 'Index',
    components: {
      VFormBase,
      ErrorSnack
    },
    data () {
      return {
        messages: [],
        model: {
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
        schema: {
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
    computed: {
      ...mapState('books', ['getInfoPending', 'getInfoData']),
      ...mapState('books', ['postInfoData']),
      action () {
        return this.$route.params.id ? 'Entrenañ' : 'Kas'
      }
    },
    methods: {
      Submit () {
        if (this.$route.params.id) {
          this.$store.dispatch('books/UpdateBook', { 'book_id': this.$route.params.id, 'data': this.model }).catch(() => {
            if (this.postInfoData) {
              this.messages = Object.assign({}, this.postInfoData)
            }
          })
        } else {
          this.$store.dispatch('books/AddNewBook', this.model).catch(() => {
            if (this.postInfoData) {
              this.messages = Object.assign({}, this.postInfoData)
            }
          })
        }
      }
    },
    watch: {
      '$route.params.id': {
        handler (val) {
          if (val) {
            this.$store.dispatch('books/getBook', val).then(() => {
              this.model.is_active = this.getInfoData.is_active
              this.model.abbrevation = this.getInfoData.abbrevation
              this.model.title = this.getInfoData.title
              this.model.description = this.getInfoData.description
              this.model.author = this.getInfoData.author
              this.model.is_kerofis_old = this.getInfoData.is_kerofis_old
              this.model.is_kerofis_other = this.getInfoData.is_kerofis_other
              this.model.is_kerofis_attested = this.getInfoData.is_kerofis_attested
              this.model.is_meurgorf = this.getInfoData.is_meurgorf
            })
          } else {
            this.$store.dispatch('books/getAllBooks')
            this.model.is_active = true
            this.model.abbrevation = ''
            this.model.title = ''
            this.model.description = ''
            this.model.author = ''
            this.model.is_kerofis_old = false
            this.model.is_kerofis_other = false
            this.model.is_kerofis_attested = false
            this.model.is_meurgorf = false
          }
        },
        immediate: true
      }
    },
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
