<template>
  <el-card class="box-card">
    <div slot="header">
      <span>
        <strong>Frag Openthesaurus</strong>
      </span>
    </div>
    <el-row type="flex" justify="space-between">
      <el-col :span="16">
        <CustomSearchInput v-model="searchString" />
      </el-col>
      <el-col :span="6" style="margin-right: 20px">
        <el-button
          type="primary"
          icon="el-icon-search"
          @click="requestThesaurus"
          >Abschicken</el-button
        >
      </el-col>
    </el-row>
    <pre v-if="isRequested">
      {{ JSON.stringify(synsets, null, 2) }}
    </pre>
  </el-card>
</template>
<script>
import axios from 'axios'
import CustomSearchInput from './CustomSearchInput.vue'

export default {
  name: 'ThesaurusSearch',
  components: {
    CustomSearchInput
  },
  data() {
    return {
      isRequested: false,
      searchString: '',
      thesaurusResponse: null
    }
  },
  computed: {
    synsets() {
      try {
        let result = []
        this.thesaurusResponse.data.synsets.forEach((synset) => {
          synset.terms.forEach((term) => {
            if (term.level !== 'umgangssprachlich') {
              result = result.concat(term.term)
              console.log(term.term)
            }
          })
        })
        return result
      } catch (e) {
        return 'No result'
      }
    }
  },
  methods: {
    requestThesaurus() {
      axios
        .get(
          `https://www.openthesaurus.de/synonyme/search?q=${this.searchString}&format=application/json`
        )
        .then((response) => {
          this.thesaurusResponse = response
          this.isRequested = true
          return true
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
