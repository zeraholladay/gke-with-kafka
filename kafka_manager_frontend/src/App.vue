<template>
  <div id="app">
    <nav class="navbar navbar-light bg-light">
      <a class="navbar-brand" href="#">Kafka Manager</a>
    </nav>
    <div class="container mt-3">
      <router-view />
    </div>
  </div>
</template>

<script>
  export default {
    name: "app"
  };
</script>
