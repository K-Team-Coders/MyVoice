<template>
  <body class="">
    <Header></Header>
    <div class="bg-idealblack min-h-[700px]">
      <div class="flex gap-3 pt-14 px-10 justify-center">
        <FormsFile></FormsFile>
      </div>
      <div class="sm:px-24 px-8 py-12">
        <QuestionBlog :question_list="question_list"></QuestionBlog>
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
import axios from 'axios';
export default {
  components: { Header, Footer, FormsFile, QuestionBlog },
  data(){
    return{
      question_list: []
    }
  },
  mounted(){
  axios.get(`http://${process.env.VUE_APP_USER_IP_WITH_PORT}/tableslist/`).then(response => (this.question_list = response.data.result,
  console.log(response.data.result)));

  
}
};


</script>

<style></style>
