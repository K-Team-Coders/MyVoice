<template>
  <div class="flex justify-center pt-10">
    <vue-word-cloud
      style="height: 300px; width: 800px"
      :words="words"
      :animation-duration="1000"
      :animation-easing="ease"
      :animation-overlap="1/5"
      :spacing = 0.2
      :color="
        ([, weight]) =>
          weight > 20 ? '#00cf00' : weight > 10 ? 'red' : 'whitesmoke'
      "
      font-family="Geologica"
    />
  </div>
</template>

<script>
import VueWordCloud from "vuewordcloud";

export default {
  components: {
    [VueWordCloud.name]: VueWordCloud,
  },
  props: {
    words: Object,
    wordcolors: Object
  },
  mounted(){
    console.log(this.wordcolors)
  }
};
</script>

<style></style>
