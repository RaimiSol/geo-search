<template>
  <div id="mapid"></div>
</template>
<script>
import L from 'leaflet'

export default {
  name: 'CustomMap',
  props: {
    geojsons: {
      type: Array,
      default: null
    }
  },
  data() {
    return {
      map: null,
      geoLayer: null
    }
  },
  watch: {
    geojsons(newVal) {
      this.geoLayer.clearLayers()
      newVal.forEach((geojson) => {
        this.addLayer(geojson)
      })
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      this.map = L.map('mapid').setView([52.5, 13.4], 10)

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map)
      this.geoLayer = L.geoJSON().addTo(this.map)
      if (this.geojsons) {
        this.geojsons.forEach((geojson) => {
          this.addLayer(geojson)
        })
      }
    },
    addLayer(geojson) {
      const newLocation = L.geoJSON(geojson).bindTooltip(
        (layer) => layer.feature.properties.description,
        { permanent: true }
      )
      this.geoLayer.addLayer(newLocation)
    }
  }
}
</script>
<style scoped>
#mapid {
  height: 600px;
  width: 750px;
}
</style>
