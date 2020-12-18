import Vue from 'vue'
import VueRouter from 'vue-router'

import SkridaozerIndex from './views/skridaozer/index.vue'

import SkridaozerMammennoù from './views/skridaozer/mammennoù.vue'

import SkridaozerMeurgorfKlask from './views/skridaozer/meurgorf/klask.vue'
import SkridaozerMeurgorfEtrefas from './views/skridaozer/meurgorf/etrefas.vue'
import SkridaozerMeurgorfStadegoù from './views/skridaozer/meurgorf/stadegoù.vue'
import SkridaozerMeurgorfEzporzhiañ from './views/skridaozer/meurgorf/ezporzhiañ.vue'

import SkridaozerKerofisKlask from './views/skridaozer/kerofis/klask.vue'
import SkridaozerKerofisTitourer from './views/skridaozer/kerofis/titourer.vue'
import SkridaozerKerofisStadegoù from './views/skridaozer/kerofis/stadegoù.vue'
import SkridaozerKerofisLevrigoù from './views/skridaozer/kerofis/levrigoù.vue'
import SkridaozerKerofisEtrefas from './views/skridaozer/kerofis/etrefas.vue'
import SkridaozerKerofisEzporzhiañ from './views/skridaozer/kerofis/ezporzhiañ.vue'


const routes = [
  { path: '/skridaozer/', name: 'Skridaozer', component: SkridaozerIndex },

  { path: '/skridaozer/mammennoù', name: 'SkridaozerMammennoù', component: SkridaozerMammennoù},
  { path: '/skridaozer/mammennoù/:id', name: 'SkridaozerMammennoùId', component: SkridaozerMammennoù},

  { path: '/skridaozer/meurgorf/klask', name: 'SkridaozerMeurgorfKlask', component: SkridaozerMeurgorfKlask},
  { path: '/skridaozer/meurgorf/etrefas', name: 'SkridaozerMeurgorfEtrefas', component: SkridaozerMeurgorfEtrefas},
  { path: '/skridaozer/meurgorf/etrefas/:id', name: 'SkridaozerMeurgorfEtrefasId', component: SkridaozerMeurgorfEtrefas},
  { path: '/skridaozer/meurgorf/stadegoù', name: 'SkridaozerMeurgorfStadegoù', component: SkridaozerMeurgorfStadegoù},
  { path: '/skridaozer/meurgorf/ezporzhiañ', name: 'SkridaozerMeurgorfEzporzhiañ', component: SkridaozerMeurgorfEzporzhiañ},

  { path: '/skridaozer/kerofis/klask', name: 'SkridaozerKerofisKlask', component: SkridaozerKerofisKlask},
  { path: '/skridaozer/kerofis/titourer', name: 'SkridaozerKerofisTitourer', component: SkridaozerKerofisTitourer},
  { path: '/skridaozer/kerofis/titourer/:id', name: 'SkridaozerKerofisTitourerId', component: SkridaozerKerofisTitourer},
  { path: '/skridaozer/kerofis/stadegoù', name: 'SkridaozerKerofisStadegoù', component: SkridaozerKerofisStadegoù},
  { path: '/skridaozer/kerofis/Levrigoù', name: 'SkridaozerKerofisLevrigoù', component: SkridaozerKerofisLevrigoù},
  { path: '/skridaozer/kerofis/etrefas/:id', name: 'SkridaozerKerofisEtrefas', component: SkridaozerKerofisEtrefas},
  { path: '/skridaozer/kerofis/ezporzhiañ', name: 'SkridaozerKerofisEzporzhiañ', component: SkridaozerKerofisEzporzhiañ},

]

Vue.use(VueRouter)

const router = new VueRouter({
  scrollBehavior (to, from, savedPosition) { return {x: 0, y: 0} },
  mode: 'history',
  routes,
})

export default router
