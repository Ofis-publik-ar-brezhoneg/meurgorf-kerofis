<template>
  <v-dialog
    v-model="dialog"
    max-width="290"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        icon
        dark
        v-bind="attrs"
        v-on="on"
      >
        <v-icon>mdi-play</v-icon>
      </v-btn>
    </template>
    <vuetify-audio :file="file" color="white" autoPlay :ended="close" v-if="dialog"></vuetify-audio>
  </v-dialog>
</template>


<script>
  export default {
    name: 'AudioDialog',
    components: {
        VuetifyAudio: () => import('./vuetifyaudio.vue'),
    },
    props: ['openDialog', 'file'],
    data () {
      return {
        dialog: false,
      }
    },
    methods: {
      close () {
        this.dialog = false
      }
    },
    watch: {
      'openDialog': {
        handler (val) {
          if (val) {
            this.dialog = true
          }
        },
        immediate: true,
      }
    },
  }
</script>
