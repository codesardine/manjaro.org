module.exports = {
  plugins: [
    require("postcss-import"),
    require("postcss-simple-vars"),
    require("postcss-nested"),
    require("autoprefixer"),
    require("postcss-preset-env"),
    require("postcss-combine-media-query")
  ],
}
