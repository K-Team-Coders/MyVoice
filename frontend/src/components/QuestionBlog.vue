<template>
  <div class="grid gap-2.5 px-2 2xl:grid-cols-4 xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2">
    <div
      class="bg-gray-50 h-[250px] py-2 font-bold text-idealblack text-start hover:border-blueGod cursor-pointer shadow-inner hover:text-whitesmoke  hover:bg-orangeGod transition ease-in-out delay-50 relative"
      v-for="item in question_list"
      :key="item.table_id"
    >
      <div class="flex flex-col mb-auto">
        <p class="ml-3 text-xl">
          {{ item.table_id }}
        </p>
        <p
          class="absolute bottom-[22px] right-[20px] top-auto left-[10px] sm:text-lg text-xs"
        >
          {{ item.table_head_question }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    question_list: Array,
  },
  data() {
    return {
      colors: ["#4487BE", "#FF7E00", "#222"],
    };
  },
  methods: {
    setRandomColor() {
      
    }
  },
};
</script>

<style></style>
