/** Config Tailwind pour la compilation statique (voir README.md).
 *  Doit rester alignée avec le tailwind.config inline historique. */
module.exports = {
  content: ['./index.html', './en/index.html'],
  theme: {
    extend: {
      colors: {
        bg: '#FBFBFB',
        surface: '#FFFFFF',
        surface2: '#F1F1F1',
        // Accent de marque — remplace le lime-400 par défaut de Tailwind (#a3e635).
        // lime-600/700 (texte lisible sur fond clair) restent les teintes par défaut.
        lime: { 400: '#ddff57' },
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'ui-sans-serif', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
    },
  },
};
