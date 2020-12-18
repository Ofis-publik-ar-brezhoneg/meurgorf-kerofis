<template>
  <span>
    <v-form-base
      id="location"
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
            insee_code: '',
            postal_code: '',
            city: '',
            category: '',
        },
        confirm_dialog: false,
      }
    },
    computed: {
      ...mapState('location_categories', { 'categoriesData': 'getInfoData' }),
      ...mapState('cities', { 'citiesData': 'getInfoData' }),
      ...mapState('locations', { 'locationsData': 'getInfoData' }),
      action () {
        return this.isNew ? "Enrollañ": "Etrenan"
      },
      schema () {
        if (!this.categoriesData || !this.citiesData) {
            return {}
        }
        return {
          insee_code: {
            type: 'text',
            label: 'INSEE',
            col: 4,
          },
          postal_code: {
            type: 'text',
            label: 'Kod post'
          },
          city: {
            type: 'autocomplete',
            label: 'Kumun',
            col: 4,
            items: this.citiesData.map(city => city.name_bre)
          },
          categories: {
            type: 'autocomplete',
            label: 'Rummad',
            col: 4,
            items: this.categoriesData.map(category => category.name)
          },
        }
      },
    },
    methods: {
      getCategory (name) {
        return this.categoriesData.filter(category => category.name == name).pop()
      },
      getCity (name_bre) {
        return this.citiesData.filter(city => city.name_bre == name_bre).pop()
      },
      save () {
        let data = JSON.parse(JSON.stringify(this.model))
        data.category = this.getCategory(data.category)
        data.city = this.getCity(data.city)
        const location_id = this.$route.params.id
        if (this.isNew) {

        } else {
          this.$store.dispatch('locations/updateLocation', { location_id, data })
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
      locationsData: {
        handler (val) {
          if (val && val.id) {
            if (val.city) {
              this.model.insee_code = val.city.insee_code
              this.model.postal_code = val.city.postal_code
              this.model.city = val.city.name_bre
              this.model.category = val.category ? val.category.name : ''
            }
          }
        },
        immediate: true,
      },
    }
  }
</script>
