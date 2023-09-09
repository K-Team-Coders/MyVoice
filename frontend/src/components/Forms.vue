<template>
  <div class="bg-gray-50 max-w-2xl w-full px-4 py-3 rounded-lg">
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
