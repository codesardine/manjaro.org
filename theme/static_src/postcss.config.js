module.exports = {
  plugins: {
    "postcss-import": {},
    "postcss-simple-vars": {},
    "postcss-nested": {},
    "autoprefixer": {},
    "postcss-preset-env": {},
    //"postcss-combine-media-query":{}, not working with breakpoints
    "cssnano": { preset: 'default' }
  },
}
