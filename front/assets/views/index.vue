<template>
  <v-app id="inspire">
    <v-main>
      <v-container
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="12"
          >
            <p>
              <router-link :to="{ name: 'MeurgorfKlask' }">Meurgorf</router-link>
            </p>
            <p>
              <router-link :to="{ name: 'Kerofis' }">Kerofis</router-link>
            </p>
            <p>
              <a href="/skridaozer">SKridaozer</a>
            </p>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
  export default {
    name: 'Home',
  }
</script>
