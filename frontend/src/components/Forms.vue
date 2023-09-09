<template>
  <div class="bg-gray-50 max-w-2xl w-full px-4 py-3 rounded-lg">
    <form class="">
      <div class="flex items-center border-b border-orangeGod py-2">
        <input
          @input="text_processing()"
          v-model="text"
          class="appearance-none bg-transparent border-none w-full text-gray-700 font-semibold mr-3 py-1 px-2 leading-tight focus:outline-none"
          type="text"
          placeholder="Напишите ваш ответ"
          aria-label="Full name"
        />
        <div>
      <small v-if="isTyping">Чел печатает...</small>
    </div>
        <button
          @click="submitText()"
          class="flex-shrink-0 bg-orangeGod hover:bg-orange-600 border-orangeGod hover:border-orange-600 text-sm border-4 text-white font-semibold py-1 px-2 rounded"
          type="button"
        >
          Отправить
        </button>
      </div>
      <div class="flex flex-col pt-2">
        <p class="text-gray-500">Вероятность того что ваш ответ будет:</p>
        <p class=""><span class="text-green-500 mr-2"> ■</span>Положительным - {{ tone.positive }}</p>
        <p class=""><span class="text-gray-400 mr-2"> ■</span>Нейтральным - {{ tone.neutral }}</p>
        <p class=""><span class="text-red-500 mr-2"> ■</span>Отрицательным - {{ tone.negative }}</p>
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
      tone: {},
      files: "",
      text: "",
      isTyping: false,
      textisProessing: false
    };
  },
  methods: {
    startTyping() {
      this.isTyping = true;
      this.debounceStopTyping();
    },
    
 debounceStopTyping: debounce(function () {
      this.isTyping = false;
    }, 500),
    text_processing(){
      this.isTyping = true;
      this.debounceStopTyping()
      setTimeout(() => {if (this.isTyping == false){
        console.log(this.text)
        axios.post(`http://${process.env.VUE_APP_USER_IP_WITH_PORT}/answer/`, { usertext: this.text })
        .then((response) => {this.tone = response.data;
        })
        .catch(function () {
          console.log("Ошибка в обработке");
        });
      }
      else{
        console.log('Даун')
      }}, 600);
      console.log(this.isTyping)
      
      
    },
    submitText() {
      let text = this.text;
      axios
        .post(`http://${process.env.VUE_APP_USER_IP_WITH_PORT}/answer/`, { usertext: text })
        .then((response) => console.log(response.data))
        .catch(function () {
          console.log("Ошибка в отправке файла");
        });
    },
  },
};
</script>
