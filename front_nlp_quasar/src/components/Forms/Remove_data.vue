<template>
  <q-card class="create-card">
    <q-card-section>
      <div class="text-subtitle1 text-primary">Supprimer des données</div>
    </q-card-section>
    <q-separator color="accent" inset />
    <q-card-section class="column">
      <div class="row justify-center">
        <div class="column col-9 q-pa-sm">
          <q-select
          filled 
          label="Name" 
          :options="data_remove.name_options"
          v-model="data_remove.name" />
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "Remove_data",
  data() {
    return {
      data_remove: {
        name: "",
        name_options: ["", ].sort()
      },
    };
  }
};
</script>
