<template>
  <body class="">
    <Header></Header>
    <div class="bg-idealblack min-h-[700px]">
      <div class="flex gap-3 pt-14 justify-center">
        <FormsFile></FormsFile>
      </div>
      <div class="px-24 py-12">
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
      question_list: [{id: 1, text: 'Какой у вас размер члена?'}, {id: 2, text: 'Какой у вас размер груди?'}, {id: 3, text: 'Какой рост у Артема?'}]
    }
  },
  mounted(){
  axios.get("http://26.200.185.61:8082/tableslist/").then(response => (this.question_list = response.data.result,
  console.log(response.data.result)));

  
}
};


</script>

<style></style>
