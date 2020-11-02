<template>
  <figure>
    <vue-word-cloud
      style="min-width: 100px; min-height: 500px; margin-bottom 100px"
      :spacing="0.2"
      :words="this.words"
      :color="
        ([, weight]) =>
          weight > upper
            ? 'LightBlue'
            : weight > under
            ? '#92BCE5'
            : 'RoyalBlue'
      "
      font-family="Righteous"
    >
      <template slot-scope="{ text, weight }">
        <div
          :title="
            'Das Wort \'' +
            text +
            '\' kommt ' +
            weight +
            ' mal in der Suchergebnismenge vor.'
          "
          style="cursor: pointer"
        >
          {{ text }}
        </div>
      </template>
    </vue-word-cloud>
    <figcaption class="caption" align="center">
      WordCloud aus den {{ limit }} häufigsten Wörtern in der Suchergebnismenge
    </figcaption>
  </figure>
</template>
<script>
import axios from 'axios'

export default {
  name: 'WordCloud',
  props: ['location'],
  data() {
    return {
      flaskApi: '',
      words: [],
      upper: null,
      under: null,
      limit: 50
    }
  },
  watch: {
    async location(newVal) {
      this.words = await this.fetchWords(newVal)
      this.upper = this.getUpper()
      this.under = this.getUnder()
    }
  },
  async mounted() {
    this.words = await this.fetchWords(this.location)
    this.upper = this.getUpper()
    this.under = this.getUnder()
  },
  methods: {
    splitArrayInThree(array) {
      const len = array.length
      if (len < 3) {
        return [[3], [2], [1]]
      }

      const splitted = []
      const chunkSize = Math.floor(len / 3)

      splitted.push(array.splice(0, chunkSize))
      splitted.push(array.splice(0, chunkSize))
      splitted.push(array)
      return splitted
    },
    getUpper() {
      const weights = this.words
        .map((pair) => pair[1])
        .filter((weight, index, array) => array.indexOf(weight) === index)
      const parts = this.splitArrayInThree(weights)
      return parts[1][parts[1].length - 1]
    },
    getUnder() {
      const weights = this.words
        .map((pair) => pair[1])
        .filter((weight, index, array) => array.indexOf(weight) === index)
      const parts = this.splitArrayInThree(weights)
      return parts[2][parts[2].length - 1]
    },
    async fetchWords(query) {
      return axios
        .get(`${this.flaskApi}/api/v1/tf?location=${query}&limit=${this.limit}`)
        .then((response) => response.data.tf)
    }
  }
}
</script>
<style scoped>
.caption {
  color: #777;
  letter-spacing: 2px;
  font-family: 'Righteous', cursive;
}
</style>
