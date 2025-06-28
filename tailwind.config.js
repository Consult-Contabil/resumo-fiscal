/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        sky: colors.sky,
        teal: colors.teal,
        cyan: colors.cyan,
        rose: colors.rose,
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/line-clamp'),
  ],
}

