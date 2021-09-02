
<template>
  <q-page padding class="row">
    <div class="row col-12">
      <h1 class="col text-h6 text-primary items-center">
        Gestion de la base de données
      </h1>
    </div>
    <div class="column col-7 q-gutter-md q-pa-sm">
      <Add_data ref="AddForm" />
      <q-btn
        class="self-center"
        color="accent"
        icon="send"
        label="Send"
        style="height: 40px;"
        @click="post_dataset()"
      />
      <Remove_data ref="RemoveForm" />
      <q-btn
        class="self-center"
        color="accent"
        icon="send"
        label="Send"
        style="height: 40px;"
        @click="delete_dataset()"
      />
    </div>
  </q-page>
</template>

// <script>
import Add_data from "../components/Forms/Add_data";
import Remove_data from "../components/Forms/Remove_data";
import axios from "axios";
import { QSpinnerFacebook } from 'quasar'
export default {
  components: {
    Add_data,
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
    async post_dataset() {
      this.$q.loading.show({
        spinner:QSpinnerFacebook,
        delay: 400 // ms
      })  
      const url = "http://127.0.0.1:8000/donnees/dataset_models/"
      var parameters =this.$refs.AddForm.data_add
      console.log(parameters)
      let response = await axios.post(url, parameters)
      .catch(error => {
        this.error = true;
        this.notifyError(error);
      })
      .then(response => {
        this.refresh_list()
        this.blank_fields()
        console.log(response)
        if (!this.error){ 
          console.log("posted",response)
        }
      });
    this.$q.loading.hide()
    },
    async delete_dataset() {
      this.$q.loading.show({
        spinner:QSpinnerFacebook,
        delay: 400 // ms
      })  
      const url = "http://127.0.0.1:8000/donnees/dataset_models/"
      var parameters =this.$refs.RemoveForm.data_remove
      let response = await axios.delete(url, { data: { name: parameters.name.toString() } })
      .catch(error => {
        this.error = true;
        this.notifyError(error);
      })
      .then(response => {
        this.refresh_list()
        this.blank_fields()
        if (!this.error){
          console.log("suppressed",response)
        }
      });
    this.$q.loading.hide()
    },
    async blank_fields(){
          this.$refs.RemoveForm.data_remove={"name":""}
          this.$refs.AddForm.data_add={"dataset_path":"",
                                        "name":""}
    },
    async refresh_list(){
      const url = "http://127.0.0.1:8000/donnees/dataset_models/"
      let response = await axios.get(url)
      const names = response.data.map((dict) => dict.name)
      this.$refs.RemoveForm.data_remove.name_options=names
    },
  }
}
</script>
