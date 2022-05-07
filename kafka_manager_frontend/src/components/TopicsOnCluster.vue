<template>
  <div>
    <ul id="topics-on-cluster">
      <li v-for="(item, key) in topics" :key="item.pk">
        {{ item.name }} -- {{ item.num_partitions }} -- {{ item.replication_factor }}  -- {{ key }} -- {{ item.cluster_id }}
      </li>
    </ul>
  </div>
</template>

<script>
import DataService from "../services/DataService";
export default {
  name: "topics-on-cluster",
  data() {
    return {
      topics: null
    };
  },
  methods: {
    getTopics(id) {
      DataService.getTopicsOnCluster(id)
        .then(response => {
          console.log(response.data);
          this.topics = response.data.results;
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
    this.getTopics(this.$route.params.id);
  }
};
</script>
