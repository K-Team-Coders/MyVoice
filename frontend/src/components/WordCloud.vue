<template>
  <div class="flex justify-center pt-10">
    <vue-word-cloud
      style="height: 300px; width: 800px"
      :words="words"
      :animation-duration="1000"
      :animation-easing="ease"
      :animation-overlap="1/5"
      :spacing = 0.1
      :color="
        ([, weight]) =>
          weight > 10 ? '#00cf00' : weight > 5 ? 'red' : 'whitesmoke'
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
  data() {
    return {
      words: [
        ["Жора", 11],
        ["КУШАТЬ", 4],
        ["ПИЦЦА", 16],
        ["ХЛЕЕЕБ!", 6],
        ["СЫР!", 3],
        ["ХЛЕЕЕБ!", 8],
        ["ХЛЕЕЕБ!", 3],
        ["ХЛЕЕЕБ!", 3],
      ],
    };
  },
};
</script>

<style></style>
