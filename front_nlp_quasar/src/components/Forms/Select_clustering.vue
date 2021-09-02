<template>
  <q-card class="create-card">
    <q-card-section>
      <div class="text-subtitle1 text-primary">Clustering</div>
    </q-card-section>
    <q-separator color="accent" inset />
    <q-card-section class="column">
      <div class="row justify-center">
        <div class="column col-9 q-pa-sm">
          <q-input 
          filled 
          label="Nom du modèle" 
          v-model="data_algo.algo_name" />
        </div>
        <div class="column col-9 q-pa-sm">
          <q-select
            filled
            label="Nom du dataset"
            :options="dataset_options"
            v-model="data_algo.dataset"
          />
        </div>
        <div class="column col-12 q-pa-sm">
          <q-select
            filled
            label="nombre de clusters"
            :options="clusters_options"
            v-model="data_algo.cluster"
          />
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "Clustering_selection",
  data() {
    return {
      data_algo: {
        algo_name: "",
        algo_type:"k-means",
        dataset:"",
        cluster:"",
      },
      dataset_options: ["", ].sort(),
      clusters_options: ["auto",2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    };
  }
};
</script>
