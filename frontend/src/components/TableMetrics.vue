<template>
  <div class="flex justify-center w-full py-10">
    <div class="relative overflow-x-auto shadow-md sm:rounded-lg max-w-6xl">
      <table class="w-full text-sm text-left text-gray-500">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50">
          <tr>
            <th
              
              scope="col"
              class="px-6 py-3 whitespace-nowrap"
            >
            Silhoute
            </th>
            <th
              
              scope="col"
              class="px-6 py-3 whitespace-nowrap"
            >
            Inertial
            </th>
          </tr>
        </thead>
        <tbody>
          <tr class="bg-whitesmoke border-b hover:bg-gray-200">
            <th
             
              scope="row"
              class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap"
            >
              {{ metrics.silhoute_all }}
            </th>
            <th
             
             scope="row"
             class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap"
           >
           {{ metrics.inertial_all }}
           </th>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>

export default{
  props:{
    metrics: Object
  },
  mounted(){
    console.log(this.metrics)
  }
}
</script>

<style>

</style>