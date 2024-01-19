const defaultTheme = require('tailwindcss/defaultTheme');
// https://kitwind.io/products/kometa/components

module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
          fontFamily: {
            sans: ['Montserrat', defaultTheme.fontFamily.sans],
          },
          transitionProperty: {
            'max-height': 'max-height'
          },
          colors: {
            red: {
              '50': '#ffebee',
              '100': '#ffcdd2',
              '400': '#ef5350',
              '700': '#d32f2f',
              '800': '#c62828',
              '900': '#b71c1c',
            },
            purple: {
              500: '#9c27b0',
            },
            'deep-purple': {
              500: '#673ab7',
              700: '#512da8',
            },
            teal: {
              50: '#e0f2f1',
              200: '#80cbc4',
              300: '#4db6ac',
              400: '#26a69a',
              500: '#009688',
              600: '#00897b',
              700: '#00796b',
              800: '#00695c',
              900: '#004d40',
              'accent-400': '#1de9b6',
              'accent-700': '#00bfa5',
            },
            indigo: {
              600: '#3949ab',
              700: '#303f9f',
            },
            pink: {
              500: '#e91e63',
              600: '#d81b60',
              700: '#c2185b',
            },
            blue: {
              100: '#bbdefb',
              300: '#64b5f6',
              400: '#42a5f5',
              500: '#2196f3',
              700: '#1976d2',
              800: '#1565c0',
              900: '#0d47a1',
              101: 'rgb(41, 126, 255)',
            },
            'light-blue': {
              300: '#4fc3f7',
              800: '#0277bd',
            },
            cyan: {
              300: '#4dd0e1',
              400: '#26c6da',
              700: '#0097a7',
            },
            gray: {
              50: '#fafafa',
              100: '#f5f5f5',
              200: '#eeeeee',
              300: '#e0e0e0',
              400: '#bdbdbd',
              500: '#9e9e9e',
              600: '#757575',
              700: '#616161',
              800: '#424242',
              900: '#212121',
            },
            'blue-gray': {
              100: '#cfd8dc',
              200: '#b0bec5',
              500: '#607d8b',
              600: '#546e7a',
              700: '#455a64',
              800: '#37474f',
              900: '#263238',
            },
            green: {
              50: '#e8f5e9',
              400: '#66bb6a',
              500: '#4caf50',
              'accent-400': '#00e676',
            },
            amber: {
              600: '#ffb300',
            },
            yellow: {
              50: '#fffde7',
              700: '#fbc02d',
              'accent-700': '#ffd600',
            },
            orange: {
              300: '#ffb74d',
              400: '#ffa726',
              500: '#ff9800',
              900: '#e65100',
            },
          },
          spacing: {
            '7': '1.75rem',
            '9': '2.25rem',
            '28': '7rem',
            '80': '20rem',
            '96': '24rem',
          },
          height: {
            '1/2': '50%',
          },
          scale: {
            '30': '.3',
          },
          boxShadow: {
            outline: '0 0 0 3px rgba(101, 31, 255, 0.4)',
          },
        },
      },
      variants: {
        scale: ['responsive', 'hover', 'focus'],
        textColor: ['responsive', 'hover', 'focus'],
        opacity: ['responsive', 'hover', 'focus'],
        backgroundColor: ['responsive', 'hover', 'focus'],
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
