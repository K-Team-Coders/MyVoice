<template>
  <body class="">
    <Header></Header>
    <div class="bg-whiteBlue">
      <div class="font-semibold text-[25.5px] text-center pt-10">
        <p>Какие идеи для завтрашнего похода в горы?</p>
      </div>
      <div class="flex pt-12 pb-10 px-8 gap-2 justify-center">
        <Forms></Forms>
      </div>
    </div>
    <Footer></Footer>
  </body>
</template>

<script>
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";
import Forms from "@/components/Forms.vue";
import UAVCard from "../components/UAVCard.vue";
import Map from "../components/Map.vue";
import { mapActions, mapGetters } from "vuex";
export default {
  components: { Header, Footer, Map, UAVCard, Forms },
  data() {
    return {
      choosed_uav: "",
      choosed_range: 0,
      current_icon: "",
      selected: "Все страны",
    };
  },
  computed: {
    ...mapGetters(["allCountries", "allUAVS"]),
    filteredList() {
      let count = this.selected;
      return this.allUAVS.filter(function (elem) {
        if (count === "Все страны") return true;
        else return elem.country.indexOf(count) > -1;
      });
    },
  },
  methods: {
    ...mapActions([
      "GET_ALLCOUNTRIES",
      "CHANGE_UAV",
      "CHANGE_RANGE",
      "CHANGE_ICON",
      "GET_ALLUAVS",
    ]),
    click_drone(uav, range, max_speed) {
      this.choosed_uav = uav;
      this.choosed_range = range;
      this.CHANGE_UAV(uav);
      this.CHANGE_RANGE(range);
      if (0 <= max_speed && max_speed < 92.6) {
        this.current_icon =
          "https://cdn-icons-png.flaticon.com/512/974/974510.png";
      } else if (92.6 <= max_speed && max_speed < 463) {
        this.current_icon =
          "https://cdn-icons-png.flaticon.com/512/2792/2792018.png";
      } else {
        this.current_icon =
          "https://cdn-icons-png.flaticon.com/512/2223/2223188.png";
      }
      this.CHANGE_ICON(this.current_icon);
    },
  },
  async created() {
    this.GET_ALLUAVS();
  },
};
</script>

<style>
.ymap-container {
  width: 100%;
  height: 100vh;
}
</style>
