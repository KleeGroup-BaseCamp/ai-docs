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
        @click="sendBundle()"
      />
    </div>
  </q-page>
</template>

<script>
import Algo_selection from "../components/Forms/Select_algorithms";
import Clustering_selection from "../components/Forms/Select_Clustering";
import axios from "axios";
export default {
  components: {
    Algo_selection,
    Clustering_selection
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
      const url = "http://127.0.0.1:8000/train_test/algos/"
      var parameters =this.$refs.AlgoForm.data_algo
      console.log(parameters)
      let response = await axios.post(url, parameters)
      .catch(error => {
        this.error = true;
        this.notifyError(error);
      })
      .then(response => {
        this.blank_fields()
        this.refresh_list()
        console.log(response)
        if (!this.error){
          this.creteSucceed(response);
          console.log("posted",response)
        }
      });
    },

    async refresh_list(){
      const url = "http://127.0.0.1:8000/donnees/dataset_models/"
      let response = await axios.get(url)
      const names = response.data.map((dict) => dict.name)
      this.$refs.AlgoForm.data_algo.dataset_options=names
      this.$refs.AlgoForm.data_algo.Algos_options=["Random Forest", "XGBoost", ].sort()
    },

    async blank_fields(){
      this.$refs.AlgoForm.data_algo={"algo_name":"","dataset":"",
                                    "algo_type":""}
    },
    notifyError(error) {
      
      console.log("error",error.response.data)
      },

    creteSucceed(response) {
      // window.location.href = '/explore'.concat("/", this.$refs.metaForm.meta.name);
    }
  }
}
</script>
