<template>
  <el-card class="box-card" shadow="always">
    <div style="position: relative">
      <div class="topcorner">
        <div align="center">
          <span
            style="font-size: 0.8em; font-weight: bold; margin-bottom: 5px"
            >{{ policeReport.district || 'Berlin' }}</span
          >

          <Wappen :district="policeReport.district" />
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
      <div>
        <div slot="header" class="clearfix">
          <h3>{{ policeReport.title }}</h3>
          <p>{{ getDateFromHeader(policeReport.header) }}</p>
        </div>
        <el-row>
          <el-col>
            <el-collapse>
              <el-collapse-item title="Ortsangaben">
                <h4 v-if="policeReport.district">
                  {{ policeReport.district }}
                </h4>
                <ul>
                  <li
                    v-for="(data, index) in policeReport.locations"
                    :key="index"
                  >
                    {{ data }}
                  </li>
                </ul>
              </el-collapse-item>
            </el-collapse>
          </el-col>
        </el-row>
      </div>
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
  name: 'CustomPoliceReport',
  components: {
    Wappen
  },
  props: {
    policeReport: { type: Object, default: null },
    showDetailsHandler: { type: Function, default: null }
  },
  methods: {
    getDateFromHeader(header) {
      const germanFormat = header.match(
        /(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,4})/g
      )[0]
      const parts = germanFormat.match(/(\d+)/g)
      const date = new Date(parts[2], parts[1] - 1, parts[0])
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
