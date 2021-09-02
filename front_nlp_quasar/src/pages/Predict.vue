<template>
  <q-page padding class="row">
    <div class="row col-12">
      <h1 class="col text-h6 text-primary items-center">
        Prédiction
      </h1>
    </div>
    <div class="column col-7 q-gutter-md q-pa-sm">
      <Predict_selection ref="PredictionForm" /> 
    </div>
  </q-page>
</template>

<script>
import Predict_selection from "../components/Forms/Predict_form";
import axios from "axios";
import { QSpinnerFacebook } from 'quasar'
export default {
  components: {
    Predict_selection,
  },

  async mounted() {
      this.refresh_list()
  },
  data() {
    return {
    };
  },
  methods: {
    
    async refresh_list(){
      const url = "/train_test/algos/"
      let response = await axios.get(url)
      var names = response.data.map((dict) => dict.algo_name)
      names.push("")
      this.$refs.PredictionForm.data_algo.algos_options=names
    },

    blank_fields(){
      this.$refs.PredictionForm.data_algo.algo_name=""
    },
    
    async get_predict() {
      this.$q.loading.show({
        spinner:QSpinnerFacebook,
        delay: 400 // ms
      })  
      const url = "/train_test/predict/"
      var parameters =this.$refs.PredictionForm.data_algo
      console.log(parameters.uuid)
      let response =axios.get(url, {
            params: {
                uuid: parameters.uuid.toString()
            }
        })
        .then(response => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'results.csv'); //or any other extension
          document.body.appendChild(link);
          link.click();
          console.log(this.$refs.PredictionForm.uploader)
          })
          
      this.$q.loading.hide()
        }
        
  }
}
</script>
