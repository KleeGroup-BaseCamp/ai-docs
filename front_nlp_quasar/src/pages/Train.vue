<template>
  <q-page padding class="row">
    <div class="row col-12">
      <h1 class="col text-h6 text-primary items-center">
        Entrainement
      </h1>
    </div>
    <div class="column col-6 q-gutter-md q-pa-sm">
      <Algo_selection ref="AlgoForm" />
      <q-btn
        class="self-center"
        color="accent"
        icon="model_training"
        label="Send"
        style="height: 40px;"
        @click="post_algo_train()"
      />
    </div>
    <div class="column col-6 q-gutter-md q-pa-sm">
      <Clustering_selection ref="ClusterForm" />
      <q-btn
        class="self-center"
        color="accent"
        icon="model_training"
        label="Send"
        style="height: 40px;"
        @click="post_clustering_train()"
      />
    </div>
    <div class="column col-6 q-gutter-md q-pa-sm">
  
      <Remove_data ref="RemoveForm" />
      <q-btn
        class="self-center"
        color="accent"
        icon="send"
        label="Send"
        style="height: 40px;"
        @click="delete_algo()"
      />
    </div>
  </q-page>
</template>

<script>
import Algo_selection from "../components/Forms/Select_algorithms";
import Clustering_selection from "../components/Forms/Select_Clustering";
import Remove_data from "../components/Forms/Remove_data";
import axios from "axios";
import { QSpinnerFacebook } from 'quasar'
export default {
  components: {
    Algo_selection,
    Clustering_selection,
    Remove_data,
  },
  async mounted() {
      this.refresh_list()
  },
  data() {
    return {
      forkData: {},
      domains: {
        String: "str",
        Float: "float",
        Integer: "int",
        Boolean: "bool"
      }
    };
  },
  methods: {
    
    async post_algo_train() {
      this.$q.loading.show({
        spinner:QSpinnerFacebook,
        delay: 400 // ms
      })  
      const url = "/train_test/algos/"
      var parameters =this.$refs.AlgoForm.data_algo
      let response = await axios.post(url, parameters)
      .catch(error => {
        this.error = true;
        this.notifyError(error);
      })
      .then(response => {
        this.blank_fields()
        console.log(response)
        if (!this.error){
          console.log("posted",response)
        }
      });
      
    this.$q.loading.hide()
    },

    async post_clustering_train() {
      this.$q.loading.show({
        spinner:QSpinnerFacebook,
        delay: 400 // ms
      })  
      const url = "/train_test/algos/"
      var parameters =this.$refs.ClusterForm.data_algo
      let response = await axios.post(url, parameters)
      .catch(error => {
        this.error = true;
        this.notifyError(error);
      })
      .then(response => {
        this.blank_fields()
        if (!this.error){
          console.log("posted",response)
        }
      });
      
    this.$q.loading.hide()
    },
    async delete_algo() {
      this.$q.loading.show({
        spinner:QSpinnerFacebook,
        delay: 400 // ms
      })  
      const url = "/train_test/algos/"
      var parameters =this.$refs.RemoveForm.data_remove
      console.log(parameters)
      let response = await axios.delete(url, { data: { name: parameters.name.toString() } })
      .catch(error => {
        this.error = true;
        this.notifyError(error);
      })
      .then(response => {
        this.blank_fields()
        this.refresh_list()
        if (!this.error){
          console.log("posted",response)
        }
      });
      
    this.$q.loading.hide()
    },

    async refresh_list(){
      const url_data = "/donnees/dataset_models/"
      let response_data = await axios.get(url_data)
      const names_data = response_data.data.map((dict) => dict.name)
      this.$refs.AlgoForm.data_algo.dataset_options=names_data
      this.$refs.ClusterForm.dataset_options=names_data
      this.$refs.AlgoForm.data_algo.Algos_options=["Random Forest", "XGBoost", ].sort()
      const url = "/train_test/algos/"
      let response_algos = await axios.get(url)
      console.log(response_algos)
      const names_algo = response_algos.data.map((dict) => dict.algo_name)
      this.$refs.RemoveForm.data_remove.name_options=names_algo
    },

    async blank_fields(){
      this.$refs.AlgoForm.data_algo.algo_name=""
      this.$refs.AlgoForm.data_algo.dataset=""
      this.$refs.AlgoForm.data_algo.algo_type=""
      this.$refs.ClusterForm.data_algo.algo_name=""
      this.$refs.ClusterForm.data_algo.dataset=""
      this.$refs.ClusterForm.data_algo.cluster=""
      this.$refs.RemoveForm.data_remove.name=""
    },
    notifyError(error) {
      console.log("error",error.response.data)
      },


  }
}
</script>
