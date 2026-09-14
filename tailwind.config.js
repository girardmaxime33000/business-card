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
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'ui-sans-serif', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
    },
  },
};
