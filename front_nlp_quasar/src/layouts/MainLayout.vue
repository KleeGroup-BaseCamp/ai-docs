<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="header">
      <q-toolbar class="row inline items-center ">
        <q-toolbar-title class="col title ">
          Classification de textes
        </q-toolbar-title>


        <q-btn flat color="white button" to="/donnees">
          <q-icon
            name="data_exploration"
            class="text"
          />
          <q-tooltip>
            Gerer les données
          </q-tooltip>
        </q-btn>
        <q-btn flat color="white button" to="/Train">
          <q-icon
            name="model_training"
            class="text"
          />
          <q-tooltip>
            Entraîner des modeles
          </q-tooltip>
        </q-btn>
        <q-btn flat color="white button" to="/score">
          <q-icon
            name="science"
            class="text"
          />
          <q-tooltip>
            Évaluer
          </q-tooltip>
        </q-btn>     
        <q-btn flat color="white button" to="/Predict">
          <q-icon
            name="online_prediction"
            class="text"
          />
          <q-tooltip>
            Prédire
          </q-tooltip>
        </q-btn>        
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>
