<template>
  <div>
    <navigation123 />
    <router-view />
  </div>
</template>

<script>
import Navigation123 from "../NavigationBrand.vue";
export default {
  components: { Navigation123 },
  data() {
    return {};
  },
};
</script>