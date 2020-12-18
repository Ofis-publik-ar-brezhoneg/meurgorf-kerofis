<template>
  <v-navigation-drawer
    id="core-navigation-drawer"
    v-model="drawer"
    :dark="barColor !== 'rgba(228, 226, 226, 1), rgba(255, 255, 255, 0.7)'"
    :expand-on-hover="expandOnHover"
    :right="$vuetify.rtl"
    :src="barImage"
    mobile-breakpoint="960"
    app
    width="260"
    v-bind="$attrs"
  >
    <template v-slot:img="props">
      <v-img
        :gradient="`to bottom, ${barColor}`"
        v-bind="props"
      />
    </template>

    <v-divider class="mb-1" />

    <v-list
      dense
      nav
    >
      <v-list-item>
        <v-list-item-avatar
          class="align-self-center"
          color="white"
          contain
        >
          <v-img
            src="/static/commun/logo.png"
            max-height="30"
          />
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title
            class="display-1"
            style="font-size: 15px !important;"
            v-text="profile.title"
          />
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <v-divider class="mb-2" />

    <v-list
      expand
      nav
    >
      <div />

      <template v-for="(item, i) in computedItems">
        <base-item-group
          v-if="item.children"
          :key="`group-${i}`"
          :item="item"
        >
        </base-item-group>

        <base-item
          v-else
          :key="`item-${i}`"
          :item="item"
        />
      </template>

      <div />
    </v-list>
  </v-navigation-drawer>
</template>

<script>
  // Utilities
  import {
    mapState,
  } from 'vuex'

  export default {
    name: 'DashboardCoreDrawer',

    props: {
      expandOnHover: {
        type: Boolean,
        default: false,
      },
    },

    data: () => ({
      meurgorf_menu: [
        {
          title: 'Meurgorf',
          to: '/meurgorf/klask',
        },
        {
          title: 'Présentation',
          to: '/meurgorf/kinnig',
        },
        {
          title: 'Sources',
          to: '/meurgorf/mammennoù',
        },
        {
          title: 'Abréviations',
          to: '/meurgorf/berradurioù',
        },
        {
          title: 'Termofis',
          href: 'http://www.opab-oplb.org/87-termofis.htm',
        },
        {
          title: 'Kerofis',
          href: 'http://www.opab-oplb.org/91-kerofis.htm',
        },
        {
          title: 'Traducteur',
          href: 'http://www.opab-oplb.org/93-troer-emgefre.htm',
        },
      ],
      kerofis_menu: [
      ],
      skridaozer_menu: [
        {
          title: 'Mammennoù',
          to: '/skridaozer/mammennoù',
        },
        {
          title: 'Meurgorf',
          group: '/skridaozer/meurgorf',
          children: [
            {
              title: 'Klask',
              to: 'klask',
            },
            {
              title: 'Stadegoù',
              to: 'stadegoù',
            },
            {
              title: 'Ezporzhiañ',
              to: 'ezporzhiañ',
            },
            {
              title: 'Ouzhpennañ ur pennger',
              to: 'etrefas',
            },
          ],
        },
        {
          title: 'Kerofis',
          group: '/skridaozer/kerofis',
          children: [
            {
              title: 'Klask',
              to: 'klask',
            },
            {
              title: 'Titourer',
              to: 'titourer',
            },
            {
              title: 'Stadegoù',
              to: 'stadegoù',
            },
            {
              title: 'Levrigoù',
              to: 'levrigoù',
            },
            {
              title: 'Ezporzhiañ',
              to: 'ezporzhiañ',
            },
          ],
        },
      ],
    }),

    computed: {
      ...mapState(['barColor', 'barImage']),
      drawer: {
        get () {
          return this.$store.state.drawer
        },
        set (val) {
          this.$store.commit('SET_DRAWER', val)
        },
      },
      computedItems () {
        if (this.$route.path.startsWith('/meurgorf')) {
          return this.meurgorf_menu.map(this.mapItem)
        } else if (this.$route.path.startsWith('/kerofis')) {
          return this.kerofis_menu.map(this.mapItem)
        } else {
          return this.skridaozer_menu.map(this.mapItem)
        }
      },
      profile () {
        if (this.$route.path.startsWith('/meurgorf')) {
          return {
            avatar: true,
            title: 'Meurgorf',
          }
        } else if (this.$route.path.startsWith('/kerofis')) {
          return {
            avatar: true,
            title: 'Kerofis',
          }
        } else {
          return {
            avatar: true,
            title: 'Skridaozer',
          }
        }
      },
    },

    methods: {
      mapItem (item) {
        return {
          ...item,
          children: item.children ? item.children.map(this.mapItem) : undefined,
          title: this.$t(item.title),
        }
      },
    },
  }
</script>

<style lang="sass">
  @import '~vuetify/src/styles/tools/_rtl.sass'

  #core-navigation-drawer
    .v-list-group__header.v-list-item--active:before
      opacity: .24

    .v-list-item
      &__icon--text,
      &__icon:first-child
        justify-content: center
        text-align: center
        width: 20px

        +ltr()
          margin-right: 24px
          margin-left: 12px !important

        +rtl()
          margin-left: 24px
          margin-right: 12px !important

    .v-list--dense
      .v-list-item
        &__icon--text,
        &__icon:first-child
          margin-top: 10px

    .v-list-group--sub-group
      .v-list-item
        +ltr()
          padding-left: 8px

        +rtl()
          padding-right: 8px

      .v-list-group__header
        +ltr()
          padding-right: 0

        +rtl()
          padding-right: 0

        .v-list-item__icon--text
          margin-top: 19px
          order: 0

        .v-list-group__header__prepend-icon
          order: 2

          +ltr()
            margin-right: 8px

          +rtl()
            margin-left: 8px
</style>
