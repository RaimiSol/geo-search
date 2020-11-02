<template>
  <div>
    <div v-if="noResult">
      <el-row type="flex" justify="center">
        <el-alert
          :key="noResult"
          title="Keine Ergebnisse"
          type="info"
          description="Die Suche hat zu keinem Ergebnis geführt,
          versuchen Sie es mit einer anderen Anfrage erneut."
          show-icon
          @close="onAlertClose"
        ></el-alert>
      </el-row>
    </div>
    <el-row type="flex" justify="center">
      <el-col :span="10">
        <el-form
          label-position="right"
          label-width="100px"
          :model="searchObject"
        >
          <el-row>
            <el-autocomplete
              v-model="searchObject.searchString"
              placeholder="Sucheingabe"
              style="width: 100%"
              :fetch-suggestions="fetchAutocomplete"
              :trigger-on-focus="false"
            ></el-autocomplete>
          </el-row>

          <el-form-item label="Zeitspanne">
            <el-col>
              <CustomDatePicker
                v-model="searchObject.searchDateRange"
                style="width: 100%"
              />
            </el-col>
          </el-form-item>
          <el-form-item label="Ort">
            <el-col>
              <CustomSelect
                v-model="searchObject.searchLocations"
                style="width: 100%"
              />
            </el-col>
          </el-form-item>

          <el-row>
            <el-button type="primary" style="width: 100%" @click="onSubmit"
              >Suchen</el-button
            >
          </el-row>
        </el-form>
      </el-col>
    </el-row>
    <div v-if="showResult">
      <el-row type="flex" justify="center">
        <el-col :span="8">
          <el-pagination
            layout="prev, pager, next"
            :current-page.sync="currentPage"
            :total="currentSearch.count"
            :page-size="pageSize"
            @current-change="onPageChanged"
          ></el-pagination>
        </el-col>
      </el-row>
      <el-row
        v-for="(row, index) in policeReports"
        :key="index"
        :gutter="20"
        type="flex"
        justify="center"
        class="card-container"
      >
        <el-col v-for="(policeReport, index) in row" :key="index" :span="8">
          <CustomBasicPoliceReport
            :police-report="policeReport"
            :show-details-handler="onShowDetails"
          />
        </el-col>
      </el-row>
    </div>
    <div v-if="showDetails">
      <div
        style="
          display: flex;
          justify-content: center;
          padding: 10px 30px 0px 30px;
        "
      >
        <el-button
          type="primary"
          style="width: 400px; margin-bottom: 40px"
          plain
          @click="onBackToResults"
          >Zurück zu den Ergebnissen</el-button
        >
      </div>
      <el-row type="flex" justify="center" style="padding: 10px 30px 0px 30px">
        <el-col :span="14">
          <el-card class="box-card" style="word-wrap: break-word">
            <div slot="header" class="clearfix">
              <div style="position: relative">
                <div class="topcorner">
                  <div align="center">
                    <span
                      class="wappen"
                      style="
                        font-size: 0.8em;
                        font-weight: bold;
                        margin-bottom: 5px;
                      "
                      >{{
                        currentDetailedPoliceReport.location || 'Berlin'
                      }}</span
                    >

                    <Wappen :district="currentDetailedPoliceReport.location" />
                  </div>
                </div>
              </div>
              <h2>{{ currentDetailedPoliceReport.title }}</h2>
              <el-tag type="info" style="margin-bottom: 10px">
                Zuletzt aktualisiert am
                {{ formatDate(currentDetailedPoliceReport.createdAt) }}
              </el-tag>
            </div>
            <div class="text item">
              <strong>{{ currentDetailedPoliceReport.header }}</strong>
            </div>
            <p style="word-break: break-word">
              {{ currentDetailedPoliceReport.content }}
            </p>
            <a :href="currentDetailedPoliceReport.url" target="_blank">
              <el-button type="primary" style="width: 100%" plain
                >Zum Original</el-button
              >
            </a>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import CustomDatePicker from './CustomDatePicker.vue'
import CustomSelect from './CustomSelect.vue'
import CustomBasicPoliceReport from './CustomBasicPoliceReport.vue'
import Wappen from './Wappen.vue'

export default {
  name: 'BasicSearch',
  components: {
    CustomDatePicker,
    CustomSelect,
    CustomBasicPoliceReport,
    Wappen
  },
  data() {
    return {
      basicApi: 'http://127.0.0.1:8080',
      searchObject: {
        searchString: '',
        searchDateRange: ['', ''],
        searchLocations: ['']
      },
      noResult: false,
      currentSearch: {
        count: 0,
        searchId: ''
      },
      policeReports: [],
      pageCount: null,
      currentPage: null,
      pageSize: 12,
      lastPageSize: null,
      lastRowsCount: null,
      rowsCount: 4,
      colsCount: 3,
      showDetails: false,
      showResult: false,
      currentDetailedPoliceReport: null
    }
  },
  computed: {
    currentRowsCount() {
      if (this.pageCount === this.currentPage) {
        return this.lastRowsCount
      }
      return this.rowsCount
    }
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
    },
    async onShowDetails(policeReport) {
      this.currentDetailedPoliceReport = policeReport
      await axios
        .get(
          `${this.basicApi}/policeReports/${this.currentDetailedPoliceReport.id}`
        )
        .then((response) => {
          this.showResult = false
          this.showDetails = true
          const rawPoliceReport = response.data
          this.currentDetailedPoliceReport = Object.assign(
            this.currentDetailedPoliceReport,
            rawPoliceReport
          )
        })
    },
    onAlertClose() {
      this.noResult = false
    },
    onBackToResults() {
      this.showDetails = false
      this.showResult = true
    },
    async onSubmit() {
      this.showResult = false
      this.showDetails = false
      await this.requestPoliceReports()
      if (this.noResult === false) {
        this.currentPage = 1
        await this.onPageChanged(this.currentPage)
      }
    },
    chunkPoliceReports(policeReports, chunkSize) {
      const chunkedPoliceReports = []

      while (policeReports.length) {
        chunkedPoliceReports.push(policeReports.splice(0, chunkSize))
      }
      return chunkedPoliceReports
    },
    async onPageChanged(newCurrentPage) {
      await axios
        .get(
          `${this.basicApi}/policeReports?searchId=${
            this.currentSearch.searchId
          }&page=${newCurrentPage - 1}&pageSize=${
            newCurrentPage === this.pageCount
              ? this.lastPageSize
              : this.pageSize
          }`
        )
        .then((response) => {
          this.showResult = true
          this.showDetails = false
          this.lastRowsCount = this.lastPageSize % this.colsCount
          const rawPoliceReports = response.data
          this.policeReports = this.chunkPoliceReports(
            rawPoliceReports,
            this.colsCount
          )
        })
    },
    async requestPoliceReports() {
      await axios
        .post(
          `${this.basicApi}/policeReports`,
          this.searchObject, // the data to post
          {
            headers: {
              'Content-type': 'application/json'
            }
          }
        )
        .then((response) => {
          this.currentSearch = response.data
          if (this.currentSearch.count === 0) {
            this.noResult = true
            this.showResult = false
            this.showDetails = false
          } else {
            this.noResult = false
            this.showResult = true
            this.showDetails = false
          }
          this.lastPageSize = this.currentSearch.count % this.pageSize
          if (this.lastPageSize === 0) {
            this.lastPageSize = this.pageSize
            this.pageCount = this.currentSearch.count / this.pageSize
          } else {
            this.pageCount = Math.ceil(this.currentSearch.count / this.pageSize)
          }
        })
        .catch((e) => {
          this.noResult = true
          this.showResult = false
          this.showDetails = false
          return e
        })
    },
    async fetchAutocomplete(query, cb) {
      if (query !== '') {
        await axios
          .get(`${this.basicApi}/autocomplete?sb=${query}&size=10`)
          .then((response) => {
            const rawRecommendations = response.data
            cb(
              rawRecommendations.map((item) => ({
                value: item,
                label: item
              }))
            )
          })
      } else {
        cb([])
      }
    }
  }
}
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
h1 {
  letter-spacing: 3px;
}
.el-row {
  margin-bottom: 20px;
}
.el-col {
  border-radius: 4px;
}
.topcorner {
  position: absolute;
  top: 0px;
  right: 0px;
}
.clearfix {
  min-height: 60px;
}
.wappen {
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
  h2 {
    word-wrap: break-word;
  }
}
h2 {
  display: block;
  width: 500px;
  -webkit-hyphens: auto;
  -moz-hyphens: auto;
  -ms-hyphens: auto;
  hyphens: auto;
}
</style>
