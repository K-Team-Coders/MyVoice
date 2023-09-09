<template>
    <Bar :chart-data="chartData" />
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'BarChart',
  components: { Bar },
  data() {
    return {
      chartData: {
        labels:  [
      "Антифашистский",
      "Казать",
      "Каркас",
      "Клуша",
      "Критика",
      "Отсвечивать",
      "Пробрить",
      "Тем",
    ],
        datasets: [
          {
            label: 'Распределение по кластерам',
            backgroundColor: '#FF7E00',
            data: [40, 20, 12, 21, 54, 12,5, 54, 123]
          }
        ]
      }   
    }
  }
}
</script>