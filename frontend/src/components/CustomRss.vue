<template>
  <div>
    <el-row type="flex" justify="center">
      <h2>Aktuelle Polizeimeldungen vom offiziellen RSS-Feed</h2>
    </el-row>
    <el-row v-for="(row, i) in feed" :key="i" type="flex" justify="center">
      <el-col v-for="(policeReport, j) in row" :key="j" :span="8">
        <el-card class="box-card">
          <div style="padding: 14px">
            <span>{{ policeReport.title }}</span>
            <div class="bottom clearfix">
              <time class="time">{{ formatDate(policeReport.pubDate) }}</time>
              <a :href="policeReport.link" target="_blank">
                <el-button type="text" class="button">Zum Original</el-button>
              </a>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import Parser from 'rss-parser'

export default {
  name: 'CustomRss',
  components: {},
  props: [],
  data() {
    return {
      feed: [],
      rowSize: 3
    }
  },
  mounted() {
    this.getFeed()
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
    async getFeed() {
      const parser = new Parser()
      const CORS_PROXY = 'https://cors-anywhere.herokuapp.com/'
      const feed = await parser.parseURL(
        `${CORS_PROXY}https://www.berlin.de/polizei/polizeimeldungen/index.php/rss`
      )
      this.feed = this.chunkFeed(feed.items, this.rowSize)
    },
    chunkFeed(feed, chunkSize) {
      const chunkedFeed = []

      while (feed.length) {
        chunkedFeed.push(feed.splice(0, chunkSize))
      }
      return chunkedFeed
    }
  }
}
</script>

<style scoped>
.box-card {
  min-height: 80px;
  margin: 20px;
}

.time {
  font-size: 13px;
  color: #999;
}

.bottom {
  margin-top: 30px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: right;
}

.image {
  width: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: '';
}

.clearfix:after {
  clear: both;
}
h2 {
  font-family: 'Ubuntu', sans-serif;
}
</style>
