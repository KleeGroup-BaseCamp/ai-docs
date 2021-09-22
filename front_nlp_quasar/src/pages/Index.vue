<template>
  <q-page class="flex flex-center">
    <img
      alt="Quasar logo"
      src="~assets/quasar-logo-vertical.svg"
      style="width: 200px; height: 200px">
    <div>
      <apexchart
        width="500"
        type="heatmap"
        :options="chartOptions"
        :series="series">
      </apexchart>
    </div>
  </q-page>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";

export default {
  name: 'PageIndex',
  components: { 
    apexchart: VueApexCharts,
  },
  name: "Overview",
  mounted() {
  },
  data: function() {
    return {
      chartOptions: {
        chart: {
          id: "vuechart-example",
        },
        xaxis: {
          categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998],
        },
      },
      series: [
        {
          name: "series-1",
          data: [30, 40, 35, 50, 49, 60, 70, 91],
        },
      ],
    };
  },
  methods: {

  }
};
</script>
