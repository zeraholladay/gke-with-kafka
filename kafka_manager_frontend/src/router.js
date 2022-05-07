import { createWebHistory, createRouter } from "vue-router";
const routes =  [
  {
    path: "/",
    name: "cluster-list",
    component: () => import("./components/ClusterList")
  },
  {
    path: "/topics-on-cluster/:id",
    name: "topics-on-cluster",
    component: () => import("./components/TopicsOnCluster")
  }
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;
