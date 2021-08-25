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
          v-model="data_algos.model" />
        </div>
        <div class="column col-9 q-pa-sm">
          <q-input 
          filled 
          label="Nom du fichier" 
          v-model="data_algos.file_name" />
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
      data_algos: {
        model: "",
        file_name:"",
      },
    };
  }
};
</script>
