<template>
  <div class="bg-gray-50 max-w-2xl w-full px-4 pt-12 pb-3 rounded-xl">
    <form class="">
      <div class="flex items-center border-b border-orangeGod py-2">
        <input
          @input="startTyping()"
          v-model="text"
          class="appearance-none bg-transparent border-none w-full text-gray-700 font-semibold mr-3 py-1 px-2 leading-tight focus:outline-none"
          type="text"
          placeholder="Напишите ваш ответ"
          aria-label="Full name"
        />
        <button
          @click="submitText()"
          class="flex-shrink-0 bg-orangeGod hover:bg-orange-600 border-orangeGod hover:border-orange-600 text-sm border-4 text-white font-semibold py-1 px-2 rounded"
          type="button"
        >
          Отправить
        </button>
      </div>
    </form>
  </div>
  <div class="bg-gray-50 max-w-2xl w-full px-4 pb-3 rounded-xl">
    <form action="">
      <div class="pt-6 flex">
        <input
          v-on:change="handleFilesUpload()"
          multiple="multiple"
          class="w-3/5 text-sm text-gray-700 border-[0.5px] py-1 px-1 border-orange-500 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
          aria-describedby="file_input_help"
          id="files"
          ref="files"
          type="file"
        />
        <p class="mt-2 ml-2 text-sm text-gray-500" id="file_input_help">
          .json
        </p>
      </div>
      <div class="flex justify-start">
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
    };
  },
  methods: {
    startTyping() {
      this.isTyping = true;
      this.debounceStopTyping();
    },
    debounceStopTyping: debounce(function () {
      this.isTyping = false;
    }, 100),

    submitFiles(){
        let formData = new FormData();
        for( var i = 0; i < this.files.length; i++ ){
          let file = this.files[i];
          formData.append('files[' + i + ']', file);
          
        }
        let FileArray = []
        for (var value of formData.values()) {
         FileArray.push(value)
}
  console.log({"files": formData})
        axios.post( 'http://26.200.185.61:8082/files/',
          {"files": formData},
          {
            headers: {
                'Content-Type': 'multipart/form-data/'
            }
          }
        ).then(function(){
          console.log('SUCCESS!!');
        })
        .catch(function () {
          console.log("FAILURE!!");
        });
    },
    handleFilesUpload() {
      this.files = this.$refs.files.files;
    },

    submitText() {
      let text = this.text;
      axios
        .post("http://26.200.185.61:8082/answer", { usertext: text })
        .then((response) => console.log(response.data))
        .catch(function () {
          console.log("Ошибка в отправке файла");
        });
    },
  },
};
</script>
