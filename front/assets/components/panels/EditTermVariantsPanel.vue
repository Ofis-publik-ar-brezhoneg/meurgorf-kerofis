<template>
  <span>
    <v-simple-table>
      <template v-slot:default>
        <tbody>
          <tr
            v-for="item in termsData.variants"
            :key="item.id"
          >
            <td>
              {{ item.variant }}
            </td>
            <td>
              <v-btn
                icon
                @click="edit_variant(item)"
              >
                <v-icon>
                  mdi-pencil
                </v-icon>
              </v-btn>
              <v-btn
                icon
                @click="delete_variant(item)"
              >
                <v-icon>
                  mdi-delete
                </v-icon>
              </v-btn>
            </td>
          </tr>
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
  import VFormBase from 'vuetify-form-base'

  export default {
    name: 'Home',
    components: { VFormBase },
    data () {
      return {
        model: {
            variant: '',
        },
        schema: {
          "id": {
            "type": "text",
            "hidden": true
          },
          "variant": {
            "type": "text",
            "label": "Adpennger"
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
        },
        variants: [
        ],
      }
    },
    computed: {
      ...mapState('terms', { 'termsData': 'getInfoData' }),
    },
    methods: {
      save () {
        let data = { "variants": [this.model, ] }
        const term_id = this.$route.params.id
        this.$store.dispatch('terms/updateTerm', { term_id, data }).then(() => {
          this.model.id = ''
          this.model.variant = ''
          this.schema.add.label = 'Kas'
          this.schema.reset.hidden = true
        })
      },
      log (val) {
        let { key } = val
        if (key == 'add') {
          this.save()
        }
        if (key == 'reset') {
          this.model.id = ''
          this.model.variant = ''
          this.schema.add.label = 'Kas'
          this.schema.reset.hidden = true
        }
      },
      edit_variant (variant) {
        this.model.id = variant.id
        this.model.variant = variant.variant
        this.schema.add.label = 'Enrollañ'
        this.schema.reset.hidden = false
      },
      delete_variant (variant) {
        this.$store.dispatch('variants/deleteVariant', { variant_id: variant.id }).then(() => {
          this.$store.dispatch('terms/getTerm', this.$route.params.id)
        })
      }
    },
  }
</script>
