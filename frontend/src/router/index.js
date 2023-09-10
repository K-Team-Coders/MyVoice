import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "home",

    component: () =>
      import(/* webpackChunkName: "about" */ "../views/MainPage.vue"),
  },
  {
    path: "/answer",
    name: "answer",

    component: () =>
      import("../views/TablePage.vue"),
  },
  {
    path: "/answer/:id",
    name: "DetailTable",
    component: () =>
    import("../views/TablePage.vue"),
    props: true
  },
  {
    path: "/notfound",
    name: "NotFound",
    component: () =>
    import( "../components/PageNotFound.vue"),
    props: true
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
