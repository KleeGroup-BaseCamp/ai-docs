<template>
  <q-page class="q-pa-sm">
      <h6 class="q-mt-none">Bienvenue Sur l'outil de classification KLEE AI</h6>
      <p>Ici,vous pouvez selectionner les fichiers sur lesquels lancer les analyses</p>
    <q-field helper="Path to data store">
      <!-- <q-input clearable v-model="settings.data_path" stack-label="Data storage" />
      <input type="file" id="dataPath" v-on:change="setDataPath" ref="fileInput" hidden /> -->
    </q-field>
    <q-btn color="secondary" v-on:click="selectPath">Set data path</q-btn>
  </q-page>
</template>

<script>
export default {
  name: 'PageIndex',
  data () {
    return {
    }
  },
  methods: {
    selectPath () {
      console.log('Selecting path for data store')

      this.$refs.folderInput.click()
    },

    setDataPath (file) {
      this.settings.data_path = file.target.files[0].path
    }
  }
}
</script>
