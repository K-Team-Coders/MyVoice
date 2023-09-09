<template>
  <div class="grid gap-2.5 px-2 grid-cols-4">
    <div
      class="bg-gray-50 h-32 py-2 font-bold text-idealblack text-start hover:border-blueGod cursor-pointer shadow-inner hover:bg-orange-600 hover:text-whitesmoke transition ease-in-out delay-50"
      v-for="item in 20"
    >
      <div class="flex flex-col mb-auto">
        <p class="ml-3 text-xl">
          {{ item }}
        </p>
        <p class="ml-3 text-2xl">Lorem ipsum dolor</p>
      </div>
    </div>
  </div>
</template>
