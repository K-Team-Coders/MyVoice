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
      <div class="p-20">

        <TagCloud></TagCloud>
      </div>
    </div>
    <Footer></Footer>
  </body>
</template>

<script>
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";
import Forms from "@/components/Forms.vue";
import TagCloud from "@/components/TagCloud.vue"
export default {
  components: { Header, Footer, TagCloud, Forms }
}
</script>

<style></style>