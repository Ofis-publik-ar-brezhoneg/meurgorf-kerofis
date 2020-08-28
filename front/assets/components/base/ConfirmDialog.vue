<template>
  <v-dialog
      v-model="dialog"
      max-width="290"
    >
    <v-card>
      <v-card-title class="headline"></v-card-title>

      <v-card-text>
        Kadarnait an dilemel mar plij
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn
          color="green darken-1"
          text
          @click="agree"
        >
          Ya
        </v-btn>

        <v-btn
          color="green darken-1"
          text
          @click="disagree"
        >
          Ket
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>


<script>
  export default {
    name: 'ConfirmDialog',
    props: ['openDialog'],
    data () {
      return {
        dialog: false,
      }
    },
    methods: {
      agree () {
        this.dialog = false
        this.$emit('agree')
      },
      disagree () {
        this.dialog = false
        this.$emit('disagree')
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
