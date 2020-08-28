import Vue from 'vue'
import VueRouter from 'vue-router'

import Index from './views/index.vue'

import MeurgorfKlask from './views/meurgorf/klask.vue'
import MeurgorfKinnig from './views/meurgorf/kinnig.vue'
import MeurgorfBerradurioù from './views/meurgorf/berradurioù.vue'
import MeurgorfMammennoù from './views/meurgorf/mammennoù.vue'

import KerofisIndex from './views/kerofis/index.vue'

import SkridaozerIndex from './views/skridaozer/index.vue'
import SkridaozerMammennoù from './views/skridaozer/mammennoù.vue'
import SkridaozerMeurgorfKlask from './views/skridaozer/meurgorf/klask.vue'
import SkridaozerMeurgorfEtrefas from './views/skridaozer/meurgorf/etrefas.vue'
import SkridaozerMeurgorfStadegoù from './views/skridaozer/meurgorf/stadegoù.vue'
import SkridaozerMeurgorfEzporzhiañ from './views/skridaozer/meurgorf/ezporzhiañ.vue'


const routes = [
  { path: '/', name: 'Home', component: Index },

  { path: '/meurgorf/klask', name: 'MeurgorfKlask', component: MeurgorfKlask },
  { path: '/meurgorf/klask/:id', name: 'MeurgorfKlaskId', component: MeurgorfKlask },
  { path: '/meurgorf/kinnig', name: 'MeurgorfKinnig', component: MeurgorfKinnig },
  { path: '/meurgorf/mammennoù', name: 'MeurgorfMammennoù', component: MeurgorfMammennoù },
  { path: '/meurgorf/berradurioù', name: 'MeurgorfBerradurioù', component: MeurgorfBerradurioù },
  { path: '/meurgorf/berradurioù/*', name: 'MeurgorfBerradurioùBis', component: MeurgorfBerradurioù },

  { path: '/kerofis/', name: 'Kerofis', component: KerofisIndex },

  { path: '/skridaozer/', name: 'Skridaozer', component: SkridaozerIndex },
  { path: '/skridaozer/mammennoù', name: 'SkridaozerMammennoù', component: SkridaozerMammennoù},
  { path: '/skridaozer/mammennoù/:id', name: 'SkridaozerMammennoùId', component: SkridaozerMammennoù},
  { path: '/skridaozer/meurgorf/klask', name: 'SkridaozerMeurgorfKlask', component: SkridaozerMeurgorfKlask},
  { path: '/skridaozer/meurgorf/etrefas', name: 'SkridaozerMeurgorfEtrefas', component: SkridaozerMeurgorfEtrefas},
  { path: '/skridaozer/meurgorf/etrefas/:id', name: 'SkridaozerMeurgorfEtrefasId', component: SkridaozerMeurgorfEtrefas},
  { path: '/skridaozer/meurgorf/stadegoù', name: 'SkridaozerMeurgorfStadegoù', component: SkridaozerMeurgorfStadegoù},
  { path: '/skridaozer/meurgorf/ezporzhiañ', name: 'SkridaozerMeurgorfEzporzhiañ', component: SkridaozerMeurgorfEzporzhiañ},
]

Vue.use(VueRouter)

const router = new VueRouter({
  scrollBehavior (to, from, savedPosition) { return {x: 0, y: 0} },
  mode: 'history',
  routes,
})

export default router
