<template>
  <div>
    <el-row type="flex" justify="center">
      <el-col :span="10">
        <el-select
          v-model="selectedLocation"
          filterable
          remote
          reserve-keyword
          placeholder="Polizeibericht nach enthaltener Ortsangabe suchen"
          :remote-method="fetchRecommendations"
          :loading="loading"
          style="width: 100%"
          @change="fetchPoliceReports"
        >
          <el-option
            v-for="item in recommendations"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </el-col>
    </el-row>
    <div v-if="showResult">
      <el-row type="flex" justify="center">
        <el-col :span="8">
          <el-pagination
            layout="prev, pager, next"
            :current-page.sync="currentPage"
            :total="totalCount"
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
          <CustomPoliceReport
            :police-report="policeReport"
            :show-details-handler="onShowDetails"
          />
        </el-col>
      </el-row>
      <el-row type="flex" justify="center">
        <el-col :span="16">
          <WordCloud :location="this.selectedLocation" />
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
          style="width: 400px"
          plain
          @click="onBackToResults"
          >Zurück zu den Ergebnissen</el-button
        >
      </div>
      <el-row style="padding: 30px 30px 0px 30px">
        <el-collapse v-model="isPredictionStrategySettingsOpen">
          <el-collapse-item name="1">
            <template slot="title">
              <img src="@/assets/settings.png" alt="Einstellungen" />
            </template>
            <el-col :span="7" style="padding: 0px 0px 30px 30px">
              <p>Wähle Bereichs-Vorhersage Strategie:</p>
            </el-col>
            <el-col :span="17" style="padding-top: 10px">
              <el-radio-group
                v-model="selectedPredictionStrategy"
                size="medium"
                @change="onChangePredictionStrategy"
              >
                <el-popover
                  placement="top-start"
                  width="300"
                  trigger="hover"
                  content="Visualisiere das berechnete Zentrum der erkannten Ortsangaben."
                >
                  <el-radio-button
                    slot="reference"
                    label="Zentrum"
                  ></el-radio-button>
                </el-popover>
                <el-popover
                  placement="top-start"
                  width="300"
                  trigger="hover"
                  content="Visualisiere den kleinsten gemeinsamen Bereich der erkannten Ortsangaben."
                >
                  <el-radio-button
                    slot="reference"
                    label="Kleinster gemeinsamer Bereich"
                  ></el-radio-button>
                </el-popover>
                <el-popover
                  placement="top-start"
                  width="250"
                  trigger="hover"
                  content="Visualisiere alle erkannten Ortsangaben."
                >
                  <el-radio-button
                    slot="reference"
                    label="Konkatenierung"
                  ></el-radio-button>
                </el-popover>
              </el-radio-group>
            </el-col>
          </el-collapse-item>
        </el-collapse>
      </el-row>
      <el-row type="flex" style="padding: 10px 30px 0px 30px">
        <el-col :span="14">
          <CustomMap :geojsons="currentGeojsons" />
        </el-col>
        <el-col :span="10" style="height: 600px; overflow: hidden">
          <el-card
            class="box-card"
            style="word-wrap: break-word; overflow-y: scroll"
          >
            <div slot="header" class="clearfix">
              <div style="position: relative">
                <div class="topcorner">
                  <div align="center">
                    <span
                      class="wappen-title"
                      style="
                        font-size: 0.8em;
                        font-weight: bold;
                        margin-bottom: 5px;
                      "
                      >{{
                        currentDetailedPoliceReport.district || 'Berlin'
                      }}</span
                    >

                    <Wappen :district="currentDetailedPoliceReport.district" />
                  </div>
                </div>
              </div>
              <h2>{{ currentDetailedPoliceReport.title }}</h2>
            </div>
            <div class="text item">
              <strong>{{ currentDetailedPoliceReport.header }}</strong>
            </div>
            <h3>Ortsangaben</h3>
            <h4 v-if="currentDetailedPoliceReport.district">
              {{ currentDetailedPoliceReport.district }}
            </h4>
            <ul>
              <li
                v-for="(location,
                index) in currentDetailedPoliceReport.locations"
                :key="index"
              >
                {{ location }}
              </li>
            </ul>
            <h3>Sätze die potenziell einen Ort enthalten</h3>
            <ul>
              <li
                v-for="(sentence,
                index) in currentDetailedPoliceReport.relevantSentences"
                :key="index"
              >
                {{ sentence }}
              </li>
            </ul>
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
import CustomMap from '@/components/CustomMap.vue'
import CustomPoliceReport from '@/components/CustomPoliceReport.vue'
import axios from 'axios'
import { featureCollection, center, point } from 'turf/turf'
import Wappen from './Wappen.vue'
import WordCloud from './WordCloud.vue'

export default {
  name: 'LocationSearch',
  components: {
    CustomMap,
    CustomPoliceReport,
    Wappen,
    WordCloud
  },
  data() {
    return {
      flaskApi: '',
      isPredictionStrategySettingsOpen: null,
      selectedPredictionStrategy: 'Zentrum',
      selectedLocation: null,
      recommendations: [],
      loading: false,
      policeReports: [],
      currentLocation: null,
      currentPage: null,
      totalCount: null,
      showResult: false,
      showDetails: false,
      rowsCount: 4,
      colsCount: 3,
      pageSize: 12,
      currentDetailedPoliceReport: null,
      currentGeojsons: [],
      detailed: null
    }
  },
  methods: {
    resetDetailed() {
      this.currentGeojsons = null
      this.detailed = {
        center: {
          computed: false,
          geojson: null
        },
        concat: {
          computed: false,
          locations: [], // (geojson, location)
          geojsons: []
        },
        smallest: {
          computed: false,
          locations: [], // (neighbourhood, suburb, city_district, village, location)
          geojson: null
        }
      }
    },
    computeCenter(points) {
      if (points) {
        const customPolygon = featureCollection(points)
        return center(customPolygon)
      }
      return []
    },
    onBackToResults() {
      this.showDetails = false
      this.showResult = true
    },
    onChangePredictionStrategy() {
      switch (this.selectedPredictionStrategy) {
        case 'Zentrum':
          if (this.detailed.center.computed) {
            this.currentGeojsons = [this.detailed.center.geojson]
          } else {
            this.predictCenter(this.currentDetailedPoliceReport)
          }
          break
        case 'Konkatenierung':
          if (this.detailed.concat.computed) {
            this.currentGeojsons = this.detailed.concat.geojsons
          } else {
            this.predictConcat(this.currentDetailedPoliceReport)
          }
          break
        case 'Kleinster gemeinsamer Bereich':
          if (this.detailed.smallest.computed) {
            this.currentGeojsons = [this.detailed.smallest.geojson]
          } else {
            this.predictSmallest(this.currentDetailedPoliceReport)
          }
          break
        default:
      }
    },
    async predictSmallest(policeReport) {
      await Promise.all(
        policeReport.locations.map((locationName) =>
          axios
            .get(
              `https://nominatim.openstreetmap.org/search/${locationName},${
                policeReport.district
                  ? ` ${policeReport.district}, Berlin, `
                  : ' ' /* Augment request */
              }Deutschland?format=json&limit=1&addressdetails=1`
            )
            .then((response) => ({
              response: response.data[0],
              location: locationName
            }))
        )
      )
        .then((responses) =>
          responses
            .filter((responseObject) => {
              if (
                responseObject.response !== undefined &&
                responseObject.response.importance > 0.3
              ) {
                return true
              }
              return false
            })
            .map((responseObject) => {
              const { address } = responseObject.response
              return {
                neighbourhood: address.neighbourhood,
                suburb: address.suburb,
                city_district: address.city_district,
                village: address.village
              }
            })
        )
        .then((augmentedLocations) => {
          const neighbourhoods = Array.from(
            new Set(
              augmentedLocations
                .map((loc) => loc.neighbourhood)
                .filter((loc) => loc !== undefined)
            )
          )

          if (neighbourhoods.size === 1) {
            return neighbourhoods[0]
          }

          const suburbs = Array.from(
            new Set(
              augmentedLocations
                .map((loc) => loc.suburb)
                .filter((loc) => loc !== undefined)
            )
          )

          if (suburbs.size === 1) {
            return suburbs[0]
          }
          const cityDistricts = Array.from(
            new Set(
              augmentedLocations
                .map((loc) => loc.city_district)
                .filter((loc) => loc !== undefined)
            )
          )

          if (cityDistricts.size === 1) {
            return cityDistricts[0]
          }
          const villages = Array.from(
            new Set(
              augmentedLocations
                .map((loc) => loc.village)
                .filter((loc) => loc !== undefined)
            )
          )
          if (villages.size === 1) {
            return villages[0]
          }
          return policeReport.district
        })
        .then(async (address) => {
          await axios
            .get(
              `https://nominatim.openstreetmap.org/search/${address}, Berlin, Deutschland?format=json&limit=1&polygon_geojson=1`
            )
            .then((response) => {
              if (response.data[0]) {
                this.currentGeojsons = [
                  {
                    type: 'Feature',
                    geometry: response.data[0].geojson,
                    properties: {
                      description: address
                    }
                  }
                ]
                this.detailed.smallest = {
                  geojson: this.currentGeojsons[0],
                  computed: true
                }
              }
            })
        })
    },
    async predictConcat(policeReport) {
      await Promise.all(
        policeReport.locations.map((locationName) =>
          axios
            .get(
              `https://nominatim.openstreetmap.org/search/${locationName},${
                policeReport.district
                  ? ` ${policeReport.district}, Berlin, `
                  : ' ' /* Augment request */
              }Deutschland?format=json&limit=1&polygon_geojson=1`
            )
            .then((response) => ({
              response: response.data[0],
              location: locationName
            }))
        )
      )
        .then((responses) =>
          responses
            .filter((responseObject) => {
              if (
                responseObject.response !== undefined &&
                responseObject.response.importance > 0.3
              ) {
                return true
              }
              return false
            })
            .map((responseObject) => {
              const { geojson } = responseObject.response
              return {
                type: 'Feature',
                geometry: geojson,
                properties: {
                  description: responseObject.location
                }
              }
            })
        )
        .then((augmentedLocations) => {
          if (augmentedLocations.length > 0) {
            this.currentGeojsons = augmentedLocations
            this.detailed.concat = {
              geojsons: this.currentGeojsons,
              computed: true
            }
          } else {
            axios
              .get(
                `https://nominatim.openstreetmap.org/search/${policeReport.district}, Berlin, Deutschland?format=json&limit=1&polygon_geojson=1`
              )
              .then((response) => {
                if (response.data[0]) {
                  this.currentGeojsons = [
                    {
                      type: 'Feature',
                      geometry: response.data[0].geojson,
                      properties: {
                        description: policeReport.district
                      }
                    }
                  ]
                  this.detailed.concat = {
                    geojsons: this.currentGeojsons,
                    computed: true
                  }
                }
              })
          }
        })
    },
    async predictCenter(policeReport) {
      await Promise.all(
        policeReport.locations.map((locationName) =>
          axios
            .get(
              `https://nominatim.openstreetmap.org/search/${locationName},${
                policeReport.district
                  ? ` ${policeReport.district}, Berlin, `
                  : ' ' /* Augment request */
              }Deutschland?format=json&limit=1`
            )
            .then((response) => ({
              response: response.data[0],
              location: locationName
            }))
        )
      )
        .then((responses) =>
          responses
            .filter((responseObject) => {
              if (
                responseObject.response !== undefined &&
                responseObject.response.importance > 0.3
              ) {
                return true
              }
              return false
            })
            .map((responseObject) => {
              const { lat, lon } = responseObject.response
              return {
                lat,
                lon,
                location: responseObject.location
              }
            })
        )
        .then((augmentedLocations) => {
          const points = augmentedLocations.map((location) =>
            point([parseFloat(location.lat), parseFloat(location.lon)])
          )
          const currentCenter = this.computeCenter(points)
          if (augmentedLocations.length > 0) {
            const currentLat = currentCenter.geometry.coordinates[0]
            const currentLon = currentCenter.geometry.coordinates[1]
            axios
              .get(
                `https://nominatim.openstreetmap.org/reverse.php?format=json&lat=${currentLat}&lon=${currentLon}`
              )
              .then((response) => {
                if (response.data) {
                  const addr = response.data.address
                  if (addr.neighbourhood) {
                    return addr.neighbourhood
                  }
                  if (addr.suburb) {
                    return addr.suburb
                  }
                  if (addr.city_district) {
                    return addr.city_district
                  }
                  if (addr.village) {
                    return addr.village
                  }
                  return policeReport.district
                }
                return []
              })
              .then((address) => {
                if (address) {
                  return axios
                    .get(
                      `https://nominatim.openstreetmap.org/search/${address}, Berlin, Deutschland?format=json&limit=1&polygon_geojson=1`
                    )
                    .then((response) => {
                      if (response.data[0]) {
                        this.currentGeojsons = [
                          {
                            type: 'Feature',
                            geometry: response.data[0].geojson,
                            properties: {
                              description: address
                            }
                          }
                        ]
                        this.detailed.center = {
                          geojson: this.currentGeojsons[0],
                          computed: true
                        }
                      }
                    })
                }
                return []
              })
          } else {
            axios
              .get(
                `https://nominatim.openstreetmap.org/search/${policeReport.district}, Berlin, Deutschland?format=json&limit=1&polygon_geojson=1`
              )
              .then((response) => {
                if (response.data[0]) {
                  this.currentGeojsons = [
                    {
                      type: 'Feature',
                      geometry: response.data[0].geojson,
                      properties: {
                        description: policeReport.district
                      }
                    }
                  ]
                  this.detailed.center = {
                    geojson: this.currentGeojsons[0],
                    computed: true
                  }
                }
              })
          }
        })
    },
    async getPoliceReportDetails(policeReport) {
      await axios
        .get(
          `${this.flaskApi}/api/v1/relevantsentences?policereport=${policeReport.id}`
        )
        .then((response) => {
          this.showDetails = true
          this.showResult = false
          this.currentDetailedPoliceReport = {
            url: policeReport.url,
            title: policeReport.title,
            header: policeReport.header,
            locations: policeReport.locations,
            id: policeReport.id,
            district: policeReport.district,
            relevantSentences:
              response.data /* Adding relevantSentences from response */
          }
        })
    },
    async onShowDetails(policeReport) {
      this.resetDetailed()
      this.currentDetailedPoliceReport = policeReport
      switch (this.selectedPredictionStrategy) {
        case 'Zentrum':
          await this.predictCenter(policeReport)
          await this.getPoliceReportDetails(policeReport)
          break
        case 'Konkatenierung':
          await this.predictConcat(policeReport)
          await this.getPoliceReportDetails(policeReport)
          break
        case 'Kleinster gemeinsamer Bereich':
          await this.predictSmallest(policeReport)
          await this.getPoliceReportDetails(policeReport)
          break
        default:
      }
    },
    async onPageChanged(newCurrentPage) {
      await axios
        .get(
          `${this.flaskApi}/api/v1/policereports?location=${this.currentLocation}&page=${newCurrentPage}&getTotalCount=False`
        )
        .then((response) => {
          this.showResult = true
          this.showDetails = false
          const rawPoliceReports = response.data.policeReports
          this.policeReports = this.chunkPoliceReports(
            rawPoliceReports,
            this.colsCount
          )
        })
    },
    chunkPoliceReports(policeReports, chunkSize) {
      const chunkedPoliceReports = []

      while (policeReports.length) {
        chunkedPoliceReports.push(policeReports.splice(0, chunkSize))
      }
      return chunkedPoliceReports
    },
    async fetchRecommendations(query) {
      if (query !== '') {
        this.loading = true
        await axios
          .get(`${this.flaskApi}/api/v1/location?name=${query}&limit=10`)
          .then((response) => {
            const rawRecommendations = response.data
            this.recommendations = rawRecommendations.map((item) => ({
              value: item,
              label: item
            }))
          })
        this.loading = false
      } else {
        this.recommendations = []
      }
    },
    async fetchPoliceReports(location) {
      await axios
        .get(
          `${this.flaskApi}/api/v1/policereports?location=${location}&getTotalCount=True`
        )
        .then((response) => {
          this.showResult = true
          this.showDetails = false
          this.currentPage = 1
          this.totalCount = response.data.totalCount
          this.currentLocation = location
          const rawPoliceReports = response.data.policeReports
          this.policeReports = this.chunkPoliceReports(
            rawPoliceReports,
            this.colsCount
          )
        })
    }
  }
}
</script>

<style scoped>
.box-card {
  height: 100%;
}
.topcorner {
  position: absolute;
  top: 0px;
  right: 0px;
}
.clearfix {
  min-height: 60px;
}
.wappen-title {
  display: block;
  width: 100px;
  -webkit-hyphens: auto;
  -moz-hyphens: auto;
  -ms-hyphens: auto;
  hyphens: auto;
}
.wappen-title:first-letter {
  text-transform: capitalize;
}
@media screen and (-webkit-min-device-pixel-ratio: 0) {
  .wappen-title {
    word-wrap: break-word;
  }
  h2 {
    word-wrap: break-word;
  }
}
h2 {
  display: block;
  width: 300px;
  -webkit-hyphens: auto;
  -moz-hyphens: auto;
  -ms-hyphens: auto;
  hyphens: auto;
}
</style>
