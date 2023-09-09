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
    
    <Footer></Footer>
  </body>
</template>

<script>
import Header2 from "@/components/Header2.vue";
import Forms from "@/components/Forms.vue";
import TagCloud from "@/components/TagCloud.vue";
import Footer from "@/components/Footer.vue";

export default {
  components: {
    Header2,
    Forms,
    TagCloud,
    Footer,
  },
}
</script>

<style></style>
