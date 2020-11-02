<template>
  <a :title="wappen.title" :href="wappen.file">
    <img width="32" :alt="wappen.alt" :src="wappen.image" />
  </a>
</template>
<script>
export default {
  name: 'Wappen',
  props: ['district'],
  data() {
    return {
      wappen: {
        title: '',
        alt: '',
        file: '',
        image: ''
      },
      berlin: {
        title:
          'Ottfried Neubecker [Public domain]" href="https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_Berlin.svg',
        alt: 'Wappen von Berlin',
        file:
          'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Coat_of_arms_of_Berlin.svg/256px-Coat_of_arms_of_Berlin.svg.png',
        image:
          'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Coat_of_arms_of_Berlin.svg/256px-Coat_of_arms_of_Berlin.svg.png'
      },
      districts: {
        reinickendorf: {
          title:
            'Wappenentwurf: unbekannt diese Datei: Jwnabd [Public domain], via Wikimedia Commons',
          alt: 'Wappen von Reinickendorf',
          file:
            'https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_borough_Reinickendorf.svg',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Coat_of_arms_of_borough_Reinickendorf.svg/256px-Coat_of_arms_of_borough_Reinickendorf.svg.png'
        },
        charlottenburgWilmersdorf: {
          title: 'Unbekannt [Public domain], via Wikimedia Commons',
          alt: 'Wappen von Charlottenburg-Wilmersdorf',
          file:
            'https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_Charlottenburg-Wilmersdorf.svg',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Coat_of_arms_of_Charlottenburg-Wilmersdorf.svg/256px-Coat_of_arms_of_Charlottenburg-Wilmersdorf.svg.png'
        },
        mitte: {
          title:
            'Wappenentwurf: unbekannt diese Datei: Jwnabd [Public domain], via Wikimedia Commons',
          alt: 'Wappen von Mitte',
          file:
            'https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_borough_Mitte.svg',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Coat_of_arms_of_borough_Mitte.svg/256px-Coat_of_arms_of_borough_Mitte.svg.png'
        },
        treptowKoepenick: {
          title:
            'Wappenentwurf: Frank Diemar diese Datei: Jwnabd [Public domain], via Wikimedia Commons',
          alt: 'Wappen von Treptow-Koepenick',
          file:
            'https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_borough_Treptow-Koepenick.svg',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Coat_of_arms_of_borough_Treptow-Koepenick.svg/256px-Coat_of_arms_of_borough_Treptow-Koepenick.svg.png'
        },
        tempelhofSchoeneberg: {
          title:
            'Wappenentwurf: unbekannt diese Datei: Jwnabd [Public domain], via Wikimedia Commons',
          alt: 'Wappen von Tempelhof-Schöneberg',
          file:
            'https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_borough_Tempelhof-Schoeneberg.svg',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Coat_of_arms_of_borough_Tempelhof-Schoeneberg.svg/256px-Coat_of_arms_of_borough_Tempelhof-Schoeneberg.svg.png'
        },
        lichtenberg: {
          title:
            'Wappenentwurf: Frank Diemar diese Datei: Jwnabd [Public domain], via Wikimedia Commons',
          alt: 'Wappen von Lichtenberg',
          file:
            'https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_borough_Lichtenberg.svg',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Coat_of_arms_of_borough_Lichtenberg.svg/256px-Coat_of_arms_of_borough_Lichtenberg.svg.png'
        },
        spandau: {
          title:
            'Wappenentwurf: unbekannt diese Datei: Jwnabd [Public domain], via Wikimedia Commons',
          alt: 'Wappen von Spandau',
          file:
            'https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_borough_Spandau.svg',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Coat_of_arms_of_borough_Spandau.svg/256px-Coat_of_arms_of_borough_Spandau.svg.png'
        },
        steglitzZehlendorf: {
          title:
            'Wappenentwurf: Frank Diemar diese Datei: Jwnabd [Public domain], via Wikimedia Commons',
          alt: 'Wappen von Steglitz-Zehlendorf',
          file:
            'https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_borough_Steglitz-Zehlendorf.svg',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Coat_of_arms_of_borough_Steglitz-Zehlendorf.svg/256px-Coat_of_arms_of_borough_Steglitz-Zehlendorf.svg.png'
        },
        friedrichshainKreuzberg: {
          title:
            'Wappenentwurf: unbekannt diese Datei: Jwnabd [Public domain], via Wikimedia Commons',
          alt: 'Wappen von Friedrichshain-Kreuzberg',
          file:
            'https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_borough_Friedrichshain-Kreuzberg.svg',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Coat_of_arms_of_borough_Friedrichshain-Kreuzberg.svg/256px-Coat_of_arms_of_borough_Friedrichshain-Kreuzberg.svg.png'
        },
        neukoelln: {
          title:
            'Wappenentwurf: unbekannt diese Datei: Jwnabd [Public domain], via Wikimedia Commons',
          alt: 'Wappen von Neukölln',
          file:
            'https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_borough_Neukoelln.svg',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Coat_of_arms_of_borough_Neukoelln.svg/256px-Coat_of_arms_of_borough_Neukoelln.svg.png'
        },
        pankow: {
          title:
            'Wappenentwurf: Jörg Mantzsch diese Datei: Jwnabd [Public domain], via Wikimedia Commons',
          alt: 'Wappen von Pankow',
          file:
            'https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_borough_Pankow.svg',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Coat_of_arms_of_borough_Pankow.svg/256px-Coat_of_arms_of_borough_Pankow.svg.png'
        },
        marzahnHellersdorf: {
          title:
            'Wappenentwurf: Lutz Döring diese Datei: Jwnabd [Public domain], via Wikimedia Commons',
          alt: 'Wappen von Marzahn-Hellersdorf',
          file:
            'https://commons.wikimedia.org/wiki/File:Coat_of_arms_of_borough_Marzahn-Hellersdorf.svg',
          image:
            'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Coat_of_arms_of_borough_Marzahn-Hellersdorf.svg/256px-Coat_of_arms_of_borough_Marzahn-Hellersdorf.svg.png'
        }
      }
    }
  },
  watch: {
    district(newVal) {
      this.updateWappen(newVal)
    }
  },
  mounted() {
    this.updateWappen(this.district)
  },
  methods: {
    updateWappen(currentDistrict) {
      switch (currentDistrict) {
        case 'Reinickendorf':
          this.wappen = this.districts.reinickendorf
          break
        case 'Neukölln':
          this.wappen = this.districts.neukoelln
          break
        case 'Charlottenburg-Wilmersdorf':
          this.wappen = this.districts.charlottenburgWilmersdorf
          break
        case 'Mitte':
          this.wappen = this.districts.mitte
          break
        case 'Friedrichshain-Kreuzberg':
          this.wappen = this.districts.friedrichshainKreuzberg
          break
        case 'Treptow-Köpenick':
          this.wappen = this.districts.treptowKoepenick
          break
        case 'Marzahn-Hellersdorf':
          this.wappen = this.districts.marzahnHellersdorf
          break
        case 'Spandau':
          this.wappen = this.districts.spandau
          break
        case 'Tempelhof-Schöneberg':
          this.wappen = this.districts.tempelhofSchoeneberg
          break
        case 'Steglitz-Zehlendorf':
          this.wappen = this.districts.steglitzZehlendorf
          break
        case 'Lichtenberg':
          this.wappen = this.districts.lichtenberg
          break
        case 'Pankow':
          this.wappen = this.districts.pankow
          break
        default:
          this.wappen = this.berlin
      }
    }
  }
}
</script>
