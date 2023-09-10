<template>
    <Bar :chart-data="chartData" :chart-options="chartOptions" />
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
            label: 'Положительных',
            backgroundColor: '#00cf00',
            data: [1, 21, 42, 21, 43, 1,8, 12, 42],
           
          },
          {label: 'Нейтральных',
            backgroundColor: '#D0D0D0',
            data: [40, 20, 12, 21, 54, 12,5, 54, 123]},
            {label: 'Негативных',
            backgroundColor: 'red',
            data: [100, 24, 65, 23, 87, 23,55, 88, 1]}
        ]
      }  ,
      chartOptions: {
        stacked: true
      }
    }
  }
}
</script>