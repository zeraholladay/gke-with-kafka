const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://kafka-manager-api:8888/',
        ws: true,
        changeOrigin: true
        // pathRewrite: {'^/api' : ''}
      }
    }
  }
});
