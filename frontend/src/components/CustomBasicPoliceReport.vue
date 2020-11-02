<template>
  <el-card class="box-card" shadow="always">
    <div style="position: relative">
      <div class="topcorner">
        <div align="center">
          <span
            style="font-size: 0.8em; font-weight: bold; margin-bottom: 5px"
            >{{ policeReport.location || 'Berlin' }}</span
          >

          <Wappen :district="policeReport.location" />
        </div>
      </div>
    </div>
    <div
      style="
        display: flex;
        justify-content: space-between;
        flex-direction: column;
      "
    >
      <div
        style="
          display: flex;
          justify-content: space-between;
          flex-direction: column;
        "
      >
        <div slot="header">
          <h3>{{ policeReport.title }}</h3>
          <p>{{ formatDate(policeReport.date) }}</p>
        </div>
        <el-row>
          <el-col>
            <p>{{ policeReport.snippet }}...</p>
          </el-col>
        </el-row>
      </div>
      <hr />
      <div>
        <el-row type="flex" :gutter="10">
          <el-col :span="12">
            <a :href="policeReport.url" target="_blank">
              <el-button type="primary" style="width: 100%" plain
                >Zum Original</el-button
              >
            </a>
          </el-col>
          <el-col :span="12">
            <el-button
              type="info"
              style="width: 100%"
              plain
              @click="showDetailsHandler(policeReport)"
              >Mehr Details</el-button
            >
          </el-col>
        </el-row>
      </div>
    </div>
  </el-card>
</template>
<script>
import Wappen from './Wappen.vue'

export default {
  name: 'CustomBasicPoliceReport',
  components: {
    Wappen
  },
  props: {
    policeReport: { type: Object, default: null },
    showDetailsHandler: { type: Function, default: null }
  },
  methods: {
    formatDate(timestamp) {
      const date = new Date(timestamp)
      return date.toLocaleDateString('de-DE', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
  }
}
</script>
<style scoped>
.box-card {
  height: 100%;
}
.box-card div h3 {
  font-family: 'Ubuntu', sans-serif;
}
.topcorner {
  position: absolute;
  top: 0px;
  right: 0px;
}
span {
  display: block;
  width: 100px;
  -webkit-hyphens: auto;
  -moz-hyphens: auto;
  -ms-hyphens: auto;
  hyphens: auto;
}
span:first-letter {
  text-transform: capitalize;
}
@media screen and (-webkit-min-device-pixel-ratio: 0) {
  span {
    word-wrap: break-word;
  }
  h3 {
    word-wrap: break-word;
  }
}
h3 {
  display: block;
  width: 200px;
  -webkit-hyphens: auto;
  -moz-hyphens: auto;
  -ms-hyphens: auto;
  hyphens: auto;
}
</style>
