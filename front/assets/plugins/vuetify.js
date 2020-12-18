import Vue from 'vue'
import i18n from '../i18n'
import '../sass/overrides.sass'
import Vuetify, { VAutocomplete, VBtn, VCombobox, VCol, VCheckbox, VDatePicker, VExpansionPanel, VFileInput, VIcon,
  VTextField, VSelect, VSimpleTable, VRow, VTooltip, VRadioGroup, VRadio, VHover, VTextarea, } from 'vuetify/lib'
import { Touch, Intersect, Resize } from 'vuetify/lib/directives'

Vue.use(Vuetify,{
  components: {
    VAutocomplete,
    VBtn,
    VCombobox,
    VCheckbox,
    VCol,
    VDatePicker,
    VFileInput,
    VIcon,
    VSelect,
    VSimpleTable,
    VTextField,
    VRow,
    VTooltip,
    VRadioGroup,
    VRadio,
    VHover,
    VTextarea
  },
  directives: {
    Touch,
    Intersect,
    Resize,
  }
})

const theme = {
  primary: '#4CAF50',
  secondary: '#9C27b0',
  accent: '#9C27b0',
  info: '#00CAE3',
}

const opts = {
  lang: {
    t: (key, ...params) => i18n.t(key, params),
  },
  theme: {
    ...theme,
    dark: true
  }
}

export default new Vuetify(opts)
