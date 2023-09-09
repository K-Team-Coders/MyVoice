<template>
  <vue-word-cloud
  style="
    height: 300px;
    width: 400px;
  "
  :words="words"
  :color="([, weight]) => weight > 10 ? 'DeepPink' : weight > 5 ? 'RoyalBlue' : 'Indigo'"
  font-family="Geologica"
/>
</template>

<script>
import VueWordCloud from 'vuewordcloud';

export default {
  components: {
    [VueWordCloud.name]: VueWordCloud,
  },
  data(){
    return{
        words: [['Жора', 3], ['КУШАТЬ', 4], ['ПИЦЦА', 3], ['ХЛЕЕЕБ!', 3],['СЫР!', 3], ['ХЛЕЕЕБ!', 3],['ХЛЕЕЕБ!', 3],['ХЛЕЕЕБ!', 3]]
    }
  }
};
</script>

<style>

</style>