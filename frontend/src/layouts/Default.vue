<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer" app right>
      <v-list dense>
        <v-list-item link @click="logout">
          <v-list-item-action>
            <v-icon>mdi-exit-run</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Выход</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar app color="primary" dark>
      <v-spacer />
      <v-toolbar-title>Frontend application</v-toolbar-title>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
    </v-app-bar>
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col class="text-center">
            <slot />
          </v-col>
        </v-row>
      </v-container>
    </v-content>
    <v-footer color="primary" app>
      <v-spacer />
      <span class="white--text">&copy; 2019</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      drawer: false
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('logout').then(() =>
        this.$router.push({
          name: 'Login'
        })
      )
    }
  }
}
</script>

<style lang="css" scoped></style>
