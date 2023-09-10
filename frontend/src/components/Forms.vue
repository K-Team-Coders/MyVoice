<template>
  <div
    class="bg-gray-50 2xl:max-w-4xl xl:max-w-3xl lg:max-w-2xl md:max-w-2xl sm:max-w-xl max-w-[320px] p-4 w-full px-4 py-3 rounded-lg">
    <form class="">
      <div class="flex items-center border-b border-orangeGod py-2">
        <input @input="text_processing()" v-model="text"
          class="appearance-none bg-transparent border-none w-full text-gray-700 font-semibold mr-3 py-1 px-2 leading-tight focus:outline-none"
          type="text" placeholder="Напишите ваш ответ" aria-label="Full name" />

        <div>
          <small v-if="textisProcessing" class="mr-10">Обработка запроса...</small>
          <small v-if="isTyping" class="2xl:mr-10">Пользователь печатает...</small>
        </div>
        <button @click="submitText()"
          class="flex-shrink-0 bg-orange-600 hover:bg-orange-700 border-orange-600 hover:border-orange-700 text-sm border-4 text-white font-semibold py-1 px-2 rounded"
          type="button">
          Отправить
        </button>
      </div>
      <div class="flex pt-2">
        <p class="text-sm rounded-lg bg-gray-100 text-center border-2 border-blueGod px-4 hover:bg-blue-600 cursor-pointer hover:text-whitesmoke"
          @click="t9_text_change(tone.t9)">
          {{ tone.t9 }}
        </p>
      </div>
      <div class="flex flex-col pt-1">
        <p class="text-gray-500">Вероятность того что ваш ответ будет:</p>
        <p class="">
          <span class="text-green-500 mr-2"> ■</span>Положительным -
          {{ tone.positive }}
        </p>
        <p class="">
          <span class="text-gray-400 mr-2"> ■</span>Нейтральным -
          {{ tone.neutral }}
        </p>
        <p class="">
          <span class="text-red-500 mr-2"> ■</span>Отрицательным -
          {{ tone.negative }}
        </p>
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
      textisProcessing: false,
      isError: false,
    };
  },
  methods: {
    t9_text_change(t9) {
      this.text = t9;
    },
    startTyping() {
      this.isTyping = true;
      this.debounceStopTyping();
    },

    textChange() { },

    debounceStopTyping: debounce(function () {
      this.isTyping = false;
    }, 500),
    text_processing() {
      this.isError = false;
      this.isTyping = true;
      this.debounceStopTyping();
      setTimeout(() => {
        if (this.isTyping == false) {
          (this.textisProcessing = true),
            axios
              .post(`http://${process.env.VUE_APP_USER_IP_WITH_PORT}/answer/`, {
                usertext: this.text,
              })
              .then((response) => {
                this.tone = response.data;
                this.textisProcessing = false;
              })
              .catch(function () {
                console.log("Ошибка в обработке");
                this.textisProcessing = false;
                this.isError = true;
              });
          this.textisProcessing = false;
        } else {
          console.log("Ошибка ");
          this.textisProcessing = false;
          this.isError = true;
        }
      }, 600);
    },
    submitText() {
      console.log( {"sentence": this.text})
      axios
        .post(`http://${process.env.VUE_APP_USER_IP_WITH_PORT}/processsentence?sentence=${this.text}&id_=${this.$route.params.id}`, { 
        })
        .then(() => this.$router.go(`/answer/${this.$route.params.id}`))
      .catch(function () {
        console.log("Ошибка в отправке предложения");
      });
    }}}
</script>
