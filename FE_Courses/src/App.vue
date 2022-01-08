<template>
  <div>
    <router-view name="nav-bar" />
    <div class="container">
      <router-view :key="$route.fullPath" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>

<style>
/* @import url("./styles/main.css"); */
</style>
