import http from "../http-common";

class DataService {
  getClusters() {
    return http.get("/cluster",  { auth: { username: "admin", password: "admin" }});
  }
  getTopicsOnCluster(cluster_id) { 
    return http.get(`/topics-on-cluster/${cluster_id}`, { auth: { username: "admin", password: "admin" }})
  }
}

export default new DataService();
