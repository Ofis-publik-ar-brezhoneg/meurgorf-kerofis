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
          <base-material-card title="Titourer">
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
                  color="teal lighten-3"
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
        v-if="!$route.params.id"
      >
      <v-card-text>
        <v-container
          class="pa-0"
          fluid
          v-if="!getInfoPending"
        >
          <v-row
            align="center"
          >
            <v-col
              cols="1"
              md="2"
            >
              nTitourer
            </v-col>
            <v-col
              cols="1"
              md="2"
            >
              Anv Enklasker
            </v-col>
            <v-col
              cols="1"
              md="2"
            >
              Anv Bihan Titourer
            </v-col>
            <v-col
              cols="1"
              md="2"
            >
              Anv Titourer
            </v-col>
            <v-col
              cols="1"
              md="2"
            >
              Kumun titouret
            </v-col>
          </v-row>
          <v-row
            v-for="(t, i) in getInfoData"
            :key="i"
            align="center"
          >
            <v-col
              cols="1"
              md="2"
            >
              <router-link
                :to="{name:'SkridaozerKerofisTitourerId', params: {id: t.id}}"
                class="abbrevation"
                v-text="t.id"
                tag="span"
              />
            </v-col>
            <v-col
              cols="1"
              md="2"
            >
              <router-link
                :to="{name:'SkridaozerKerofisTitourerId', params: {id: t.id}}"
                class="abbrevation"
                v-text="t.interviewed_by"
                tag="span"
              />
            </v-col>
            <v-col
              cols="1"
              md="2"
            >
              <router-link
                :to="{name:'SkridaozerKerofisTitourerId', params: {id: t.id}}"
                class="abbrevation"
                v-text="t.first_name"
                tag="span"
              />
            </v-col>
            <v-col
              cols="1"
              md="2"
            >
              <router-link
                :to="{name:'SkridaozerKerofisTitourerId', params: {id: t.id}}"
                class="abbrevation"
                v-text="t.last_name"
                tag="span"
              />
            </v-col>
            <v-col
              cols="1"
              md="2"
            >
              <router-link
                :to="{name:'SkridaozerKerofisTitourerId', params: {id: t.id}}"
                class="abbrevation"
                v-text="t.cities"
                tag="span"
              />
            </v-col>
          </v-row>
        </v-container>
        </v-card-text>
      </base-material-card>
      <error-snack
        prefix="informant"
        :messages="messages"
      />
    </v-container>
  </base-app>
</template>

<script>
  import { mapState } from 'vuex'
  import ErrorSnack from '../../../components/base/ErrorSnack.vue'
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
          first_name: '',
          last_name: '',
          surname: '',
          occupation: '',
          birthdate: '',
          birthplace: '',
          cities: '',
          arrival_date: '',
          notes: '',
          contact: ''
        },
        schema: {
          first_name: { type: 'text', label: 'Anv Bihan Titourer', filled: true },
          last_name: { type: 'text', label: 'Anv Titourer', filled: true },
          surname: { type: 'text', label: 'Lesanv', filled: true },
          occupation: { type: 'text', label: 'Micher', filled: true },
          birthdate: { type: 'text', label: 'Bloavezh ganedigezh', filled: true },
          birthplace: { type: 'text', label: 'Lec’h ganedigezh', filled: true },
          cities: { type: 'text', label: 'Kumun titouret', filled: true },
          arrival_date: { type: 'text', label: 'Abaoe pegoulz er gumun', filled: true },
          notes: { type: 'text', label: 'Notennoù', filled: true },
          contact: { type: 'text', label: 'Darempred', filled: true }
        },
        typography: {
          '': ['Paragraph', 'leader'],
        },
      }
    },
    computed: {
      ...mapState('informants', ['getInfoPending', 'getInfoData']),
      ...mapState('informants', ['postInfoData']),
      action () {
        return this.$route.params.id ? 'Entrenañ' : 'Kemmañ'
      }
    },
    methods: {
      Submit () {
        if (this.$route.params.id) {
          this.$store.dispatch('informants/UpdateInformant', { 'informant_id': this.$route.params.id, 'data': this.model }).catch(() => {
            if (this.postInfoData) {
              this.messages = Object.assign({}, this.postInfoData)
            }
          })
        } else {
          this.$store.dispatch('informants/AddNewInformant', this.model).catch(() => {
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
            this.$store.dispatch('informants/getInformant', val).then(() => {
              this.model.first_name = this.getInfoData.first_name,
              this.model.last_name = this.getInfoData.last_name,
              this.model.surname = this.getInfoData.surname,
              this.model.occupation = this.getInfoData.occupation,
              this.model.birthdate = this.getInfoData.birthdate,
              this.model.birthplace = this.getInfoData.birthplace,
              this.model.cities = this.getInfoData.cities,
              this.model.arrival_date = this.getInfoData.arrival_date,
              this.model.notes = this.getInfoData.notes,
              this.model.contact = this.getInfoData.contact
            })
          } else {
            this.$store.dispatch('informants/getAllInformants')
            this.model.first_name = '',
            this.model.last_name = '',
            this.model.surname = '',
            this.model.occupation = '',
            this.model.birthdate = '',
            this.model.birthplace = '',
            this.model.cities = '',
            this.model.arrival_date = '',
            this.model.notes = '',
            this.model.contact = ''
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
