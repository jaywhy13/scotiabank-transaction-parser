<template>
  <div id="app">
    <img src="./assets/logo.png">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body {
    font-family: 'Josefin Sans';
    background-color: #dad5d5;
}

div#app-header {
    margin-top: 250px;
    background-color: white;
    padding: 40px;
    border-radius: 8px;
    text-transform: uppercase;
    text-align: center;
}

div#app {
    margin-top: 45px;
    background-color: white;
    padding: 40px;
}

/**
 * Bootstrap overrides
 */
.navbar {
    border-radius: 0px;
    height: 300px;
    background-color: #a00909;
    border-color: transparent;
}

</style>
