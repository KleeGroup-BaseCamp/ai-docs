<template>
  <q-page padding class="row">
    <div class="row col-12">
      <h1 class="col text-h6 text-primary items-center">
        Entrainement
      </h1>
    </div>
    <div class="column col-7 q-gutter-md q-pa-sm">
      <Algo_selection ref="metaForm" />
      <q-btn
        class="self-center"
        color="accent"
        icon="online_prediction"
        label="Send"
        style="height: 40px;"
        @click="sendBundle()"
      />
    </div>
    <div class="column col-5 q-gutter-md q-pa-sm">
      <Clustering_selection ref="metaForm" />
      <q-btn
        class="self-center"
        color="accent"
        icon="online_prediction"
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
      console.log(this.$route.params.bundle)
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
    async sendBundle() {
      var parameters = this.$refs.parametersForm.parameters;
      parameters.hyperparameters = this.$refs.hyperparametersForm.parameters.hyperparameters;
      const bundle = {
        meta: this.$refs.metaForm.meta,
        algorithm: this.$refs.algorithmForm.algorithm,
        dataset: {
          db_config: this.$refs.databaseForm.database,
          data_config: this.$refs.datatableForm.datatable,
          domains: this.domains
        },
        parameters: parameters
      };
      let response = await axios.post("/api/deploy-train/", bundle)
      .catch(error => {
        this.error = true;
        this.notifyError(error);
      })
      .then(response => {
        if (!this.error){
          this.creteSucceed(response);
        }
      });
    },
    notifyError(error) {
      this.$q.notify({
        message: "An error occured during the creation of "
          .concat("", this.$refs.metaForm.meta.name)
          .concat(" v", this.$refs.metaForm.meta.version)
          .concat(":\n", error.response.data.error),
        color: "negative"
      });
    },
    creteSucceed(response) {

      window.location.href = '/explore'.concat("/", this.$refs.metaForm.meta.name);
    }
  }
}
</script>
