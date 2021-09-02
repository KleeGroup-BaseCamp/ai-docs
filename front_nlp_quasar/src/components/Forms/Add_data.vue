<template>
  <q-card class="create-card">
    <q-card-section>
      <div class="text-subtitle1 text-primary">Ajouter des données</div>
    </q-card-section>
    <q-separator color="accent" inset />
    <q-card-section class="column">
      <div class="row justify-center">
        <div class="column col-9 q-pa-sm">
          <q-input
            filled
            class="col-10"
            label="Path"
            v-model="data_add.dataset_path"
          />
        </div>
        <div class="column col-9 q-pa-sm">
          <q-input 
          filled 
          label="Name" 
          v-model="data_add.name" />
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "Add_data",
  data() {
    return {
      data_add: {
        dataset_path:"",
        name: "",
      },
    };
  }
};
</script>
