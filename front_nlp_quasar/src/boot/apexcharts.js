import VueApexCharts from 'vue-apexcharts'

// leave the export, even if you don't use it
export default async ({ Vue }) => {

    Vue.component('apexchart', VueApexCharts)

}