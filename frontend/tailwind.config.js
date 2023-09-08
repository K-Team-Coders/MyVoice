/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./public/index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        corme: "Cormorant Garamond",
        rale: "Raleway",
        roboto: "Roboto",
        monster: "Montserrat",
      },
      colors: {
        "dark-blue": "#1a1e22",
        "dark-gray": "#0e0f10",
        whitesmoke: "#f5f5f5",
        idealblack: "#222",
        whiteBlue: "#EDF1F7",
        orangeGod: "#FF7E00",
        blueGod: "#4487BE",
      },
    },
  },
  plugins: [],
};
