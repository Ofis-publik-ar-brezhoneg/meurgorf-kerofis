import Vue from 'vue'
import VueI18n from 'vue-i18n'

import fr from 'vuetify/lib/locale/fr'

Vue.use(VueI18n)

const messages = {
  fr: {
    ...require('./locales/fr.json'),
    $vuetify: fr,
  },
  br: {
    ...require('./locales/br.json'),
    $vuetify: fr,
  },
}

export default new VueI18n({
  locale: 'br',
  fallbackLocale: process.env.VUE_APP_I18N_FALLBACK_LOCALE || 'br',
  messages,
})
