<template>
  <div class="backbody">
    <p>Положительных: </p>
    <p>Нейтральных: </p>
    <p>Отрицательных: </p>
    <BarChart/>
    <Doughnut></Doughnut>
    <span ref="tagcloud--item" class="Sphere cursor-pointer"></span>

    <div v-if="isOpened">
      <p class="bg-whitesmoke text-3xl">Кластер: {{ texts }}</p>
      <WordCloud />
    </div>


  </div>
</template>

<script>



import TagCloud from "TagCloud";
import WordCloud from "@/components/WordCloud.vue"
import BarChart from "@/components/charts/BarChart.vue"
import Doughnut from "@/components/charts/Doughnut.vue"

export default {
  components: { TagCloud, WordCloud, BarChart, Doughnut },
  data() {
    return {
      texts: 'nothing',
      isOpened: false
    }
  },
  methods: {
    onClick(e) {
      this.isOpened = true
      if (e.target.className === 'tagcloud--item') {
        this.texts = e.target.innerText
        console.log(this.texts)

      }

    }
  },
  mounted() {
    const Texts = ['Антифашистский', 'Казать', 'Каркас', 'Клуша', 'Критика', 'Отсвечивать', 'Пробрить', 'Тем'];

    let tagCloud = TagCloud(".Sphere", Texts, {
      // Sphere radius in px
      radius: 230,

      // animation speed
      // slow, normal, fast
      maxSpeed: "fast",
      initSpeed: "fast",

      // Rolling direction [0 (top) , 90 (left), 135 (right-bottom)]
      direction: 135,

      // interaction with mouse or not [Default true (decelerate to rolling init speed, and keep rolling with mouse).]
      keep: true,
    });

    // Giving color to each text in sphere
    let color = "#544adde1";
    document.querySelector(".Sphere").style.color = color;
    // let rootEl = this.$el.querySelector(".tagcloud");
    let element = this.$refs['tagcloud--item']
    element.addEventListener('click', this.onClick);
  }
}
</script>

<style>
/*     Importing Google fonts    */
@import url("https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap");

.backbody {
  background-color: #bba0a049;
}

/* Applying CSS to sphere */
.tagcloud {
  display: inline-block;
  font-weight: bold;
  letter-spacing: 1px;
  font-family: "Roboto", italic;
  font-size: 20px;
}

/* Change color of each text in sphere on hover   */
.tagcloud--item:hover {
  color: rgb(255, 255, 255);
}
</style>
