
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Sommaire.vue') },
      { path: '/entrainement', component: () => import('pages/Entrainement.vue') },
      { path: '/prediction', component: () => import('pages/Prediction.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
