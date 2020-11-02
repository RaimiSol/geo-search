module.exports = {
  assetsDir: 'static' // For simple configuration of static files in Flask (the "static_folder='client/dist/static'" part in app.py)
  /*
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:8080', // 141.45.146.242
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      },
      '^/flaskApi': {
        target: 'http://localhost:5000',
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/flaskApi': ''
        }
      }
    }
  }
  */
}
