<template>
  <span>
    <v-form-base
      id="term"
      :model="model"
      :schema="schema"
    >
    </v-form-base>
    <v-btn
      color="teal lighten-3"
      @click="save"
    >
      Enrollañ
    </v-btn>
    <v-btn
      color="red"
      @click="confirm_dialog=true"
      v-if="!isNew"
    >
      Dilemel
    </v-btn>
    <confirm-dialog
      :openDialog="confirm_dialog"
      @agree="delete_term"
      @disagree="confirm_dialog=false"
    />
  </span>
</template>

<script>
  import { mapState } from 'vuex'
  import VFormBase from 'vuetify-form-base'
  import ConfirmDialog from '../../components/base/ConfirmDialog.vue'

  export default {
    name: 'Home',
    props: {
      isNew: {
        type: Boolean,
      }
    },
    components: { VFormBase, ConfirmDialog },
    data () {
      return {
        model: {
            canonic_form: '',
            grammatical_category: '',
        },
        confirm_dialog: false,
      }
    },
    computed: {
      ...mapState('categories', { 'categoriesData': 'getInfoData' }),
      ...mapState('terms', { 'termsData': 'getInfoData' }),
      action () {
        return this.isNew ? "Enrollañ": "Etrenan"
      },
      schema () {
        if (!this.categoriesData) {
            return {}
        }
        return {
          canonic_form: {
            type: 'text',
            label: 'Pennger',
            col: 4,
          },
          grammatical_category: {
            type: 'autocomplete',
            label: 'Rummenn ger',
            col: 4,
            items: this.categoriesData.map(category => category.title)
          },
        }
      },
    },
    methods: {
      getCategory (title) {
        return this.categoriesData.filter(category => category.title == title).pop()
      },
      save () {
        if (this.isNew) {
          let data = JSON.parse(JSON.stringify(this.model))
          data.grammatical_category = this.getCategory(data.grammatical_category)
          this.$store.dispatch('terms/addNewTerm', data)
        }
      },
      delete_term () {
        this.confirm_dialog = false
        this.$store.dispatch('terms/deleteTerm', this.$route.params.id).then(() => {
          this.$router.push({name: 'SkridaozerMeurgorfEtrefas'})
        })
      },
    },
    watch: {
      termsData: {
        handler (val) {
          if (val && val.id) {
            this.model.canonic_form = val.canonic_form
            this.model.grammatical_category = val.grammatical_category.title
          }
        },
        immediate: true,
      },
    }
  }
</script>
