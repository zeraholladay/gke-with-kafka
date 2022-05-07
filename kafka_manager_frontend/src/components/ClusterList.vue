<template>
  <div id="cluster-lists">
    <strong>Clusters</strong>
    <div class="accordion" >
      <div class="accordion-item" v-for="cluster in clusters" :key="cluster.pk">
        <h2 class="accordion-header" id="headingOne">
          <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
          {{ cluster.description.cluster_id }}
          </button>
        </h2>
        <div class="container">
          <div class="row">
            <div class="col">
              <strong>Bootstrap Servers:</strong> {{cluster.bootstrap_servers}}
            </div>
            <div class="col">
            </div>
            <div class="col">
              <div class="float-right">
                <router-link :to="{ name: 'topics-on-cluster', params: { id: cluster.pk }}">Topics</router-link>
              </div>
            </div>
          </div>
          <hr>
          <div class="row">
            <div class="col">
              Brokers
            </div>
          </div>
          <div v-for="broker in cluster.description.brokers" :key="broker.node_id" class="row">
            <div class="col">
              {{broker.host}}:{{broker.port}}
            </div>
            <div class="col">
              Node ID: {{broker.node_id}}
            </div>
            <div class="col">
              <div v-if="broker.rack">Rack: {{broker.rack}}</div>
              <div v-else>Rack: N/A</div>
            </div>
          </div>
        </div>

        <!-- <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
          <div class="accordion-body">
            <div class="mb-3 row">
              <label for="bootstrap_servers_id" class="col-sm-2 col-form-label">Bootstrap Servers</label>
              <div class="col-sm-10">
                <input type="text" readonly class="form-control-plaintext" id="bootstrap_servers_id" :value="cluster.bootstrap_servers">
              </div>
              <strong>Brokers</strong>

            </div>
          </div>
        </div> -->

      </div>
    </div>
  </div>
</template>

<script>
import DataService from "../services/DataService";
export default {
  name: "cluster-list",
  data() {
    return {
      clusters: []
    };
  },
  methods: {
    getClusters() {
      DataService.getClusters()
        .then(response => {
          console.log(response.data);
          this.clusters = response.data.results;
        })
        .catch(e => {
          console.log(e);
        });
    },
    refreshList() {
      this.getClusters();
    }
  },
  mounted() {
    this.getClusters();
  }
};
</script>
