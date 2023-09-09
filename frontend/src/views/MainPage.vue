<template>
  <body class="">
    <Header></Header>
    <div class="bg-whiteBlue min-h-[600px]">
      <div class="flex gap-2 pt-24 justify-center">
        <FormsFile></FormsFile>
      </div>
      <div class="px-24 py-12">
        <QuestionBlog></QuestionBlog>
      </div>
    </div>
    <Footer></Footer>
  </body>
</template>

<script>
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";
import FormsFile from "@/components/FormsFile.vue";
import QuestionBlog from "@/components/QuestionBlog.vue";
export default {
  components: { Header, Footer, FormsFile, QuestionBlog },
};
</script>

<style></style>
