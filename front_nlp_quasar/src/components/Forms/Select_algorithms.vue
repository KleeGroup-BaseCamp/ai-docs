<template>
  <q-card class="create-card">
    <q-card-section>
      <div class="text-subtitle1 text-primary">Classification supervisé</div>
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
            :options="data_algo.dataset_options"
            v-model="data_algo.dataset"
          />
        </div>
        <div class="column col-12 q-pa-sm">
          <q-select
            filled
            label="Algorithm"
            :options="data_algo.Algos_options"
            v-model="data_algo.algo_type"
          />
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "Algo_selection",
  data() {
    return {
      data_algo: {
        algo_name: "",
        algo_type:"",
        dataset:"",
        Algos_options: ["Random Forest", "XGBoost", ].sort(),
        dataset_options: ["", ].sort()
      },
    };
  }
};
</script>
