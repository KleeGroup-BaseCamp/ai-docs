<template>
  <q-card class="create-card">
    <q-card-section>
      <div class="text-subtitle1 text-primary">Sélectionner un modèle</div>
    </q-card-section>
    <q-separator color="accent" inset />
    <q-card-section class="column">
      <div class="row justify-center">
        <div class="column col-9 q-pa-sm">
          <q-select
          filled 
          label="Name" 
          :options="data_algo.name_algos"
          v-model="data_algo.name"
          @update:model-value="inputChange(val)" />
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: "data_algo",
  data() {
    return {
      data_algo: {
        name: "",
        name_options: ["", ].sort()
      },
    };
  },
  async mounted() {
    refresh_list
  },
  methods: {
    inputChange(val){
        if (this.data_algo.algo_name<1){
            this.data_algo.upload=true
        }else{
            this.data_algo.upload=false
        }
    },
    uploadfile(file) {
      return {
        url: 'http://127.0.0.1:8000/train_test/predict/',
        method: 'POST',
      }
    },
    async onfinish() {
      const url= 'http://127.0.0.1:8000/train_test/predict/'
      var parameters={'uuid':this.data_algo.uuid,
                      'algo_name':this.data_algo.algo_name
                      }
      let response = await  axios.post(url, parameters)
      .catch(error => {
        this.error = true;
        })
      .then(response => {
        if (!this.error){
          console.log("posted",response)
        }
    })
    },
    onUploaded(info) {
      console.log(this.data_algo.uuid)
      let uuid = info.files[0].xhr.response
      // this.data_algo.uuid=uuid
      this.data_algo.download=false
    },
    async get_predict() {
      const url = "http://127.0.0.1:8000/train_test/predict/"
      var parameters =this.data_algo
      console.log(parameters.uuid)
      let response =axios.get(url, {
            params: {
                uuid: parameters.uuid.toString()
            }
        })
        .then(response => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'results.csv'); //or any other extension
          document.body.appendChild(link);
          link.click();
          this.$refs.uploader.reset()
          this.data_algo.download=true
          })
        }
    
  
  }
};
</script>
