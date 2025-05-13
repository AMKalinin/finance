<script>
  import { getUserInfo, logout } from '../keycloak/keycloak.js'

  export default{
    data() {
      return getUserInfo()
    },
    methods: {
      userLogOut(){
        return logout()
      }
    }
  }
</script>


<template>
  <div>
      <h1>Profile</h1>
      <h2>Email: {{email}}</h2>
      <button @click="userLogOut()">Log out</button>
  </div>
</template>



<style>


</style>
