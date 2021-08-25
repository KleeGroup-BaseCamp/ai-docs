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
          v-model="data_algos.name" />
        </div>
        <div class="column col-9 q-pa-sm">
          <q-input 
          filled 
          label="Nom du dataset" 
          v-model="data_algos.dataset_name" />
        </div>
        <div class="column col-12 q-pa-sm">
          <q-select
            filled
            label="Algorithm"
            :options="Algos_options"
            v-model.number="data_algos.Algo"
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
      data_algos: {
        name: "",
        Path:"",
        Algo:"",
      },
      Algos_options: ["K-means"].sort()
    };
  }
};
</script>
