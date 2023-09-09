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
  data() {
    return {
      words: [
        ["Проблема", 11],
        ["Бутылка", 4],
        ["Открывашка", 16],
        ["Отдых", 6],
        ["Каподастер", 3],
        ["Мышка", 8],
        ["Анклав", 3],
        ["Хлеб", 3],
        ["Энергетик", 23],
        ["Проблема", 7],
        ["Печаль", 25],
        ["Самоотстранение", 25],
      ],
    };
  },
};
</script>

<style></style>
