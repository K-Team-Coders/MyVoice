<template>
  <div class="">
    <span class="Sphere"></span>
  </div>
</template>

<script>
import TagCloud from "TagCloud";
export default {
  components: [TagCloud],
  mounted() {
    const Texts = ["Жора", "Еда", "По идее один кластер??", "Шавуха"];

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
    let rootEl = document.querySelector(".tagcloud");
    rootEl.addEventListener("click", function clickEventHandler(e) {
      if (e.target.className === "tagcloud--item") {
      }
    });
  },
};
</script>

<style>
/*     Importing Google fonts    */
@import url("https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap");

.backbody {
  background-color: #000;
}

/* Applying CSS to sphere */
.tagcloud {
  display: inline-block;
  left: 30%;
  font-weight: bold;
  letter-spacing: 1px;
  font-family: "Roboto", italic;
  font-size: 24px;
}

/* Change color of each text in sphere on hover   */
.tagcloud--item:hover {
  color: #1a128fe1;
}
</style>
