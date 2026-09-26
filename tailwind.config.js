/** Config Tailwind pour la compilation statique (voir README.md).
 *  Doit rester alignée avec le tailwind.config inline historique. */
module.exports = {
  content: ['./index.html', './en/index.html'],
  theme: {
    extend: {
      colors: {
        // Ladder Style — obsidian dark theme, accent emerald (Tailwind's default
        // emerald/cyan scales cover the rest of the palette, no override needed).
        bg: '#0B0D12',
        surface: '#12151C',
        surface2: '#10131A',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'sans-serif'],
        display: ['Fraunces', 'ui-serif', 'serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
    },
  },
};
