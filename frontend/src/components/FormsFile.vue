<template>
  <div class="bg-gray-50 2xl:max-w-4xl xl:max-w-4xl lg:max-w-xl md:max-w-xl sm:max-w-md max-w-sm w-full px-4 py-4 border-[1.5px] border-orangeGod shadow-md">
    <LoadingPage v-if="is_Loading"/>
    <form v-else action="">
      <div class="flex justify-start">
        <input v-on:change="handleFilesUpload()"
          class="w-full text-sm text-gray-700 border-[0.5px] py-1 px-2 border-orange-500 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
          aria-describedby="file_input_help" id="files" ref="files" type="file" />
        <p class="mt-2.5 ml-2 text-sm text-gray-500" id="file_input_help">
          .json
        </p>
      </div>
      <div class="flex justify-end pt-2">
        <button @click="submitFiles()" type="submit"
          class="text-white bg-orange-600 hover:bg-orange-700 focus:ring-4 focus:outline-none focus:ring-orange-700 font-semibold rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center mt-2">
          Отправить файл
        </button>
      </div>
    </form>

  </div>
</template>
<script>
import axios from "axios";
import LoadingPage from "./LoadingPage.vue";

export default {
  components:{
    LoadingPage
  },
  data() {
    return {
      is_Error: false,
      IP: process.env.VUE_APP_USER_IP_WITH_PORT,
      files: "",
      text: "",
      isTyping: false,
      is_Loading: false,
      colors: ["#4487BE", "#FF7E00", "#222",]
    };
  },
  methods: {

    submitFiles() {
      console.log(this.files)
      this.is_Loading = true
      let formData = new FormData();
      for (var i = 0; i < this.files.length; i++) {
        let file = this.files[i];
        formData.append('file', file);
      }
      console.log(this.IP);
      axios
        .post(
          `http://${this.IP}/files/`, formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }
        )
        .then(function () {
          console.log("SUCCESS!!");
          location.reload();
        })
        .catch(function (response) {
          console.log("FAILURE!!");
          if (response.statusCode == 400) {
            alert('Такой файл уже был загружен! Загрузите другой.')
          }
        })
        .finally(function (){
          is_Loading = false
        });
       
      },
      handleFilesUpload() 
        {this.files = this.$refs.files.files;}
    }
  }

</script>
