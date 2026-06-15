/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "surface-container-highest": "#e5e2dd",
        "tertiary": "#382c1f",
        "surface-tint": "#466551",
        "on-tertiary-container": "#c2af9c",
        "on-error-container": "#93000a",
        "secondary-fixed": "#dae7c9",
        "on-primary-container": "#99baa2",
        "on-surface": "#1c1c19",
        "on-tertiary": "#ffffff",
        "error-container": "#ffdad6",
        "inverse-primary": "#adcfb6",
        "surface-container-low": "#f6f3ee",
        "on-primary-fixed": "#022111",
        "surface-container-lowest": "#ffffff",
        "on-primary-fixed-variant": "#2f4d3a",
        "on-tertiary-fixed": "#241a0e",
        "on-tertiary-fixed-variant": "#524436",
        "surface-bright": "#fcf9f4",
        "primary-container": "#2d4b38",
        "inverse-surface": "#31302d",
        "on-secondary-fixed": "#141e0c",
        "on-secondary-container": "#5c6851",
        "surface-variant": "#e5e2dd",
        "tertiary-fixed-dim": "#d7c3b0",
        "surface-dim": "#dcdad5",
        "surface-container": "#f0ede8",
        "secondary-fixed-dim": "#becbae",
        "secondary": "#56624b",
        "on-surface-variant": "#424843",
        "inverse-on-surface": "#f3f0eb",
        "error": "#ba1a1a",
        "tertiary-container": "#504234",
        "on-primary": "#ffffff",
        "outline-variant": "#c2c8c1",
        "on-error": "#ffffff",
        "on-secondary": "#ffffff",
        "outline": "#727972",
        "surface-container-high": "#ebe8e3",
        "primary": "var(--primary-color, #163423)",
        "primary-container": "var(--primary-container, #2d4b38)",
        "app-bg": "var(--bg-color, #0a0a0a)",
        "app-surface": "var(--surface-color, #111111)",
        "app-text": "var(--text-color, #fcf9f4)"
      },
      borderRadius: {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
      fontFamily: {
        "headline": ["Playfair Display", "serif"],
        "body": ["Be Vietnam Pro", "sans-serif"],
        "label": ["Be Vietnam Pro", "sans-serif"]
      }
    },
  },
  plugins: [],
}
