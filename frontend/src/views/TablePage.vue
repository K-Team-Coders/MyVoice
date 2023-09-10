<template>
  <body>
    <Header2></Header2>
    <LoadingPage v-if="isLoading" />
    <div v-else class="bg-idealblack">
      <p
        class="text-whitesmoke 2xl:text-3xl text-lg text-center font-semibold pt-8"
      >
        {{ result.headQuestion }}
      </p>
      <div class="py-10">
        <div class="flex flex-col gap-2 items-center justify-center">
          <Forms></Forms>
          <div class="">
            <button
              @click="DownloadFile()"
              type="submit"
              class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none h-12 focus:ring-blue-300 font-semibold rounded-lg text-sm w-full sm:w-auto px-5 py-1 text-center"
            >
              Экспорт результатов .json
            </button>
          </div>
        </div>
        <div>
          <TableMetrics :metrics="result.metrics" />
        </div>
        <div class="flex justify-center pt-3">
          <TagCloud :result="result"></TagCloud>
        </div>
      </div>
    </div>

    <Footer></Footer>
  </body>
</template>

<script>
import Header2 from "@/components/Header2.vue";
import Forms from "@/components/Forms.vue";
import TagCloud from "@/components/TagCloud.vue";
import Footer from "@/components/Footer.vue";
import axios from "axios";
import LoadingPage from "@/components/LoadingPage.vue";
import TableMetrics from "@/components/TableMetrics.vue";

export default {
  components: {
    Header2,
    Forms,
    TagCloud,
    Footer,
    LoadingPage,
    TableMetrics,
  },
  data() {
    return {
      result: 0,
      isLoading: false,
    };
  },
  methods: {
    DownloadFile() {
      axios
        .post(
          `http://${process.env.VUE_APP_USER_IP_WITH_PORT}/export/${this.$route.params.id}/`
        )
        .then((response) => {
          const link = document.createElement("a");
          link.href = window.URL.createObjectURL(new Blob([response.data]));
          link.setAttribute(
            "download",
            `labeled_${this.$route.params.id}.json`
          );
          document.body.appendChild(link);
          link.click();
        });
    },
  },
  created() {
    this.isLoading = true;

    axios
      .post(
        `http://${process.env.VUE_APP_USER_IP_WITH_PORT}/tabledetailview/${this.$route.params.id}/`
      )
      .then((res) => {
        this.result = res.data.result;
      })
      .finally(() => {
        this.isLoading = false;
      });
  },
};
</script>

<style></style>
