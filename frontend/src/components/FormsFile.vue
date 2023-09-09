<template>
  <div
    class="bg-gray-50 max-w-2xl w-full px-4 py-4 border-[1.5px] border-orangeGod shadow-md"
  >
    <form action="">
      <div class="flex justify-start">
        <input
          v-on:change="handleFilesUpload()"
          
          class="w-full text-sm text-gray-700 border-[0.5px] py-1 px-2 border-orange-500 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
          aria-describedby="file_input_help"
          id="files"
          ref="files"
          type="file"
        />
        <p class="mt-2.5 ml-2 text-sm text-gray-500" id="file_input_help">
          .json
        </p>
      </div>
      <div class="flex justify-end pt-2">
        <button
          @click="submitFiles()"
          type="submit"
          class="text-white bg-orangeGod hover:bg-orange-600 focus:ring-4 focus:outline-none focus:ring-orange-600 font-semibold rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center mt-2"
        >
          Отправить файл
        </button>
      </div>
    </form>
  </div>
</template>
<script>
import axios from "axios";
import debounce from "lodash/debounce";
export default {
  data() {
    return {
      files: "",
      text: "",
      isTyping: false,
      colors:["#4487BE","#FF7E00","#222",]
    };
  },
  methods: {

    submitFiles() {
      console.log(this.files)
      let formData = new FormData();
      for (var i = 0; i < this.files.length; i++) {
        let file = this.files[i];
        formData.append('file', file);
      }
      // let FileArray = [];
      // for (var value of formData.values()) {
      //   FileArray.push(value);
      // }
      console.log(formData);
      axios
        .post(
          "http://26.200.185.61:8082/files/", formData,
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
        .catch(function () {
          console.log("FAILURE!!");
        });
    },
    handleFilesUpload() {
      this.files = this.$refs.files.files;
    },

  },
};
</script>
