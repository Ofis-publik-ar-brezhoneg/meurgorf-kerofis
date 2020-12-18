<template>
  <span>
    <v-simple-table>
      <template v-slot:default>
        <tbody>
          <draggable v-model="phonetic_forms">
            <tr
              v-for="item in phonetic_forms"
              :key="item.id"
            >
              <td>
                {{ item.phonetic_form }}
              </td>
              <td>
                <span v-if="item.phonetic_file">
                  <audio-dialog :file="`/media/${item.phonetic_file}`" />
                </span>
              </td>
              <td>
                <v-btn
                  icon
                  @click="edit_phonetic_form(item)"
                >
                  <v-icon>
                    mdi-pencil
                  </v-icon>
                </v-btn>
                <v-btn
                  icon
                  @click="delete_phonetic_form(item)"
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
      id="term"
      :model="model"
      :schema="schema"
      @change:term="log"
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
            phonetic_form: '',
            phonetic_file: null
        },
        has_file: false,
        schema: {
          "id": {
            "type": "text",
            "hidden": true
          },
          "phonetic_form": {
            "type": "text",
            "label": "Distagadur",
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
    computed: {
      ...mapState('terms', { 'termsData': 'getInfoData' }),
      phonetic_forms: {
        get() {
          return (this.termsData && this.termsData.phonetic_forms) ? this.termsData.phonetic_forms : []
        },
        set(value) {
          let changed_forms = JSON.parse(JSON.stringify(value))
          changed_forms.forEach((item, index) => {
            item.order = index + 1
          })
          const term_id = this.$route.params.id
          this.$store.dispatch('terms/updateTerms', { term_id, data: { "phonetic_forms": changed_forms }})
        }
      },
    },
    methods: {
      log (val) {
        let { key } = val
        if (key == 'add') {
          this.save()
        }
        if (key == 'reset') {
          this.model.phonetic_form = ''
          this.model.link = ''
          this.schema.add.label = 'Kas'
          this.schema.reset.hidden = true
        }
      },
      save () {
        let data = { "phonetic_forms": [this.model, ] }
        toBase64(this.model.link).then(file => {
          data.phonetic_forms[0].link = file
          const term_id = this.$route.params.id
          this.$store.dispatch('terms/updateTerm', { term_id, data }).then(() => {
            this.model.id = ''
            this.model.phonetic_form = ''
            this.model.phonetic_file = ''
            this.schema.add.label = 'Kas'
            this.schema.reset.hidden = true
          })
        })
      },
      edit_phonetic_form(phonetic_form) {
        this.model.id = phonetic_form.id
        this.model.phonetic_form = phonetic_form.phonetic_form
        this.has_file = phonetic_form.phonetic_file
        this.schema.add.label = 'Enrollañ'
        this.schema.reset.hidden = false
      },
      delete_phonetic_form(phonetic_form) {
        this.$store.dispatch(
          'terms/deletePhoneticTranscription', { phonetic_form_id: phonetic_form.id }
        ).then(() => {
          this.$store.dispatch('terms/getTerm', this.$route.params.id)
        })
      },
    },
  }
</script>
