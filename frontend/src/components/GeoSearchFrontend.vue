<template>
  <div id="app">
    <link
      href="https://fonts.googleapis.com/css?family=Righteous"
      rel="stylesheet"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Ubuntu"
      rel="stylesheet"
    />
    <link
      href="https://fonts.googleapis.com/css?family=PT+Sans+Caption"
      rel="stylesheet"
    />
    <el-container>
      <el-header id="header" height="120px">
        <h1>Berliner Polizeimeldungen</h1>
      </el-header>
      <div class="right-margin">
        <el-tabs tab-position="left" style="padding: 20px">
          <el-tab-pane label="Ortssuche">
            <LocationSearch />
          </el-tab-pane>
          <el-tab-pane label="Aktuelle Polizeimeldungen">
            <CustomRss />
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-container>
  </div>
</template>

<script>
import LocationSearch from '@/components/panes/LocationSearch.vue'
import CustomRss from '@/components/panes/CustomRss.vue'

export default {
  name: 'GeoSearchFrontend',
  components: {
    LocationSearch,
    CustomRss
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
h1 {
  letter-spacing: 3px;
  font-family: 'Arial';
}
#header {
  color: #327cbb;
  text-align: center;
  font-size: 30px;
}
.el-row {
  margin-bottom: 20px;
}
.el-col {
  border-radius: 4px;
}
.right-margin {
  margin-right: 200px;
}
</style>
