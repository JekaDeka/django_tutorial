<template>
  <v-card class="elevation-12">
    <v-toolbar color="primary" dark flat>
      <v-toolbar-title>Login</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
      <v-form
        ref="form"
        v-model="valid"
        lazy-validation
        @keyup.native.enter="submit"
      >
        <v-text-field
          label="Login"
          name="username"
          prepend-icon="mdi-account"
          type="text"
          v-model="username"
          :counter="15"
          :rules="loginRules"
        />

        <v-text-field
          id="password"
          label="Password"
          name="password"
          prepend-icon="mdi-lock"
          type="password"
          v-model="password"
          :rules="passRules"
        />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="primary" :loading="loading" @click="submit">Login</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data () {
    return {
      loading: false,
      valid: true,
      username: null,
      password: null,
      redirect: undefined,
      loginRules: [
        v => !!v || 'Введите логин',
        v => (v && v.length > 2) || 'Введите более 3 символов'
      ],
      passRules: [v => !!v || 'Введите пароль']
    }
  },
  methods: {
    submit () {
      if (this.$refs.form.validate()) {
        this.loading = true
        const payload = {
          username: this.username.toLowerCase(),
          password: this.password
        }
        this.$store
          .dispatch('login', payload)
          .then(() => {
            this.$router.push({
              path: this.redirect || '/'
            })
          })
          .catch(error => {
            this.$log.error('login: ', error)
          })
          .finally(() => (this.loading = false))
      }
    }
  }
}
</script>

<style lang="css" scoped></style>
