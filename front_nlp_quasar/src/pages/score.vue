<template>
<div>
  <apexchart width="500" type="bar" :options="options" :series="series"></apexchart>
</div>
</template>
<script>

import VueApexCharts from 'vue-apexcharts'
import CardBase from 'components/Cards/CardBase'
import { QSpinnerFacebook } from 'quasar'
export default {
  name: 'PageIndex',
  components: {
    // CardBase,
    // ApexHeatmap: () => import('components/Charts/ApexHeatmap'),
  },  
  data: function() {
    return {
      options: {
        chart: {
          id: 'vuechart-example'
        },
        xaxis: {
          categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998]
        }
      },
      series: [{
        name: 'series-1',
        data: [30, 40, 45, 50, 49, 60, 70, 91]
      }]
    }
    // this.$q.loading.show({
    //   backgroundColor: 'purple-10',
    //   delay: 0
    // })
    // setTimeout(() => {
    //   this.$q.loading.hide()
    // }, 1300)
  }
}
</script>