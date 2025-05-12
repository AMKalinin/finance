<script >
  import { getUserInfo } from '../keycloak/keycloak.js'
  export default{
    data() {
      return getUserInfo()
    }
  }
</script>


<template>
  <div>
      <h1>Profile</h1>
      <h2>Email: {{email}}</h2>
  </div>
</template>



<style>


</style>
