<template>
  <span>
    <v-simple-table>
      <template v-slot:default>
        <tbody>
          <draggable v-model="phonetic_transcriptions">
            <tr
              v-for="item in phonetic_transcriptions"
              :key="item.id"
            >
              <td>
                {{ item.phonetic_transcription }}
              </td>
              <td>
                <v-checkbox
                  :value="item.is_standard"
                />
              </td>
              <td>
                {{ item.created_at }}
              </td>
              <td>
                {{ item.informant }}
              </td>
              <td>
                <span v-if="item.links && item.links.length">
                  <audio-dialog :file="`/media/${item.links[0].link}`" />
                </span>
              </td>
              <td>
                <v-btn
                  icon
                  @click="edit_phonetic_transcription(item)"
                >
                  <v-icon>
                    mdi-pencil
                  </v-icon>
                </v-btn>
                <v-btn
                  icon
                  @click="delete_phonetic_transcription(item)"
                >
                  <v-icon>
                    mdi-delete
                  </v-icon>
                </v-btn>
              </td>
            </tr>
          </draggable>
        </tbody>
      </template>
    </v-simple-table>
    <v-form-base
      id="location"
      :model="model"
      :schema="schema"
      @change:location="log"
    >
    </v-form-base>
  </span>
</template>

<script>
  import { mapState } from 'vuex'
  import draggable from 'vuedraggable'
  import VFormBase from 'vuetify-form-base'
  import AudioDialog from '../../components/base/AudioDialog.vue'

  const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });

  export default {
    name: 'Home',
    components: { draggable, VFormBase, AudioDialog },
    data () {
      return {
        model: {
            phonetic_transcription: '',
            is_standard: false,
            created_at: '',
            informant: '',
            link: ''
        },
        has_file: false
      }
    },
    computed: {
      ...mapState('locations', { 'locationsData': 'getInfoData' }),
      ...mapState('informants', { 'informantsData': 'getInfoData' }),
      phonetic_transcriptions: {
        get() {
          return (this.locationsData && this.locationsData.phonetic_transcriptions) ? this.locationsData.phonetic_transcriptions : []
        },
        set(value) {
          let changed_forms = JSON.parse(JSON.stringify(value))
          changed_forms.forEach((item, index) => {
            item.order = index + 1
          })
          const location_id = this.$route.params.id
          this.$store.dispatch('locations/updateLocations', { location_id, data: { "phonetic_transcriptions": changed_forms }})
        }
      },
      schema() {
        if (!this.informantsData) {
          return {}
        }

        return {
          "id": {
            "type": "text",
            "hidden": true
          },
          "phonetic_transcription": {
            "type": "text",
            "label": "Distagadur",
          },
          "is_standard": {
            "type": "checkbox"
          },
          "created_at": {
            "type": "text",
            "ext": "date",
            "label": "Deiziad degemer",
          },
          "informant": {
            "type": "autocomplete",
            "label": "Orin",
            items: this.informantsData.map(informant => `${informant.first_name} ${informant.last_name}`)
          },
          "link": {
            "type": "file",
            "accept": "audio/*",
            "label": "fichier",
            disabled: this.has_file,
            col: 4
          },
          "add": {
            "type": "btn",
            "label": "Kas",
            "dark": true,
            "color": "green"
          },
          "reset": {
            "type": "btn",
            "label": "X",
            "hidden": true,
            "color": "grey"
          }
        }
      }
    },
    methods: {
      log (val) {
        let { key } = val
        if (key == 'add') {
          this.save()
        }
        if (key == 'reset') {
          this.model.phonetic_transcription = ''
          this.model.is_standard = false
          this.model.created_at = ''
          this.model.informant = ''
          this.schema.add.label = 'Kas'
          this.schema.reset.hidden = true
        }
      },
      save () {
        let data = { "phonetic_transcriptions": [this.model, ] }
        toBase64(this.model.link).then(file => {
          data.phonetic_transcriptions[0].link = file
          const location_id = this.$route.params.id
          this.$store.dispatch('locations/updateLocation', { location_id, data }).then(() => {
            this.model.id = ''
            this.model.phonetic_transcription = ''
            this.model.created_at = ''
            this.model.informant = ''
            this.model.link = ''
            this.schema.add.label = 'Kas'
            this.schema.reset.hidden = true
          })
        })
      },
      edit_phonetic_transcription(phonetic_transcription) {
        this.model.id = phonetic_transcription.id
        this.model.phonetic_transcription = phonetic_transcription.phonetic_transcription
        this.model.created_at = phonetic_transcription.created_at
        this.model.informant = phonetic_transcription.informant
        this.has_file = phonetic_transcription.links && phonetic_transcription.links.length
        this.schema.add.label = 'Enrollañ'
        this.schema.reset.hidden = false
      },
      delete_phonetic_transcription(phonetic_transcription) {
        this.$store.dispatch(
          'locations/deletePhoneticTranscription', { phonetic_transcription_id: phonetic_transcription.id }
        ).then(() => {
          this.$store.dispatch('locations/getLocation', this.$route.params.id)
        })
      },
    },
  }
</script>
