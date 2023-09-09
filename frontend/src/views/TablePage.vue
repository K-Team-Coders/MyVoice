<template>
  <body>
    <Header2></Header2>
    <div class="bg-idealblack">
      <p class="text-whitesmoke text-3xl text-center font-semibold pt-8">
        Пойдем в горы?
      </p>
      <div class="py-10">
        <div class="flex justify-center">
          <Forms></Forms>
        </div>
        <div class="flex justify-center pt-8">
          <TagCloud></TagCloud>
        </div>
      </div>
    </div>
    <div v-if="created">
      <transition-group
        enter-active-class="transition ease-out duration-100 "
        enter-from-class="transition opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-100"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="tranfrom opacity-0 scale-95"
      >
        <Alert></Alert>
      </transition-group>
    </div>
    <Footer></Footer>
  </body>
</template>

<script>
import Header2 from "@/components/Header2.vue";
import Forms from "@/components/Forms.vue";
import TagCloud from "@/components/TagCloud.vue";
import Footer from "@/components/Footer.vue";
import Alert from "@/components/Alert.vue";
import { mapActions, mapGetters } from "vuex";
export default {
  components: {
    Header2,
    Forms,
    TagCloud,
    Footer,
    Alert,
  },
  computed: {
    ...mapGetters(["allDrones"]),
  },
  data() {
    return {
      headers: [
        { text: "Тип паука", value: "spider", sortable: true },
        { text: "Источник", value: "url", sortable: true },
        { text: "Данные", value: "data", sortable: true },
      ],
    };
  },
  methods: {
    ...mapActions(["GET_ALLDRONES"]),
  },
  async created() {
    this.GET_ALLDRONES();
  },
};
</script>

<style></style>
