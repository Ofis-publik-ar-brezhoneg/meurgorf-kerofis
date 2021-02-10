module.exports = {
    outputDir: './static/dist/',
    publicPath: 'http://localhost:3000/staticfiles/dist/',
    lintOnSave: false,

    pages: {
      app: {
        entry: 'front/assets/main.js',
      },
    },

    pluginOptions: {
      i18n: {
        locale: 'br',
        fallbackLocale: 'br',
        localeDir: 'locales',
        enableInSFC: false,
      },
    },

    configureWebpack: config => {
      if (process.env.NODE_ENV === 'production') {
        // config.optimization.delete('splitChunks')
        config.output.filename = 'bundle.js'
      } else {
        config.output.filename = 'bundle.js'
      }
    },

    chainWebpack: config => {

        config.optimization
            .splitChunks(false)

        config.resolve.alias
            .set('__STATIC__', 'static')

        config.devServer
            .public('http://0.0.0.0:3000')
            .host('0.0.0.0')
            .port(3000)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["\*"]})
    }
};
