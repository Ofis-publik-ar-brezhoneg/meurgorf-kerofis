<template>
  <v-snackbar
    v-model="snackbar"
    color="error"
    multi-line
  >
    <v-list
      two-line
      color="error"
    >
      <v-list-item-group>
        <v-list-item
          v-for="(value, key) in messages"
          :key="key"
        >
          <v-list-item-content
            color="error"
          >
            <v-list-item-title>
              {{ $t(`${prefix}_${key}`) }}
            </v-list-item-title>
            <v-list-item-subtitle>
              <p
                v-for="(text, i) in value"
                :key="i"
                v-text="text"
              />
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <template v-slot:action="{ attrs }">
      <v-btn
        color="white"
        text
        v-bind="attrs"
        @click="snackbar = false"
      >
        Fermer
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
  export default {
    name: 'ErrorSnack',
    props: ['messages', 'prefix'],
    data () {
      return {
        snackbar: false
      }
    },
    watch: {
      messages (val) {
        if (val) {
          this.snackbar = true
        }
      },
    },
  }
</script>
