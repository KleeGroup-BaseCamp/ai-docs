
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '/donnees/', component: () => import('pages/donnees.vue') },
      { path: '/train/', component: () => import('pages/Train.vue') },
      { path: '/predict/', component: () => import('pages/Predict.vue') },
      { path: '/score/', component: () => import('pages/score.vue') },
      { path: '', component: () => import('pages/Index.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue'),
    children: [
    ]
  }
]

export default routes
