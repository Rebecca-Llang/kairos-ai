/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    screens: {
      xs: '475px',
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1536px',
    },
    extend: {
      colors: {
        // Core cosmic theme
        'deep-space': '#0a0e27',
        'dark-matter': '#1a1f3a',
        stardust: '#2d3450',
        starlight: '#f9fafb',
        moonbeam: '#d1d5db',
        
        // Message system (accessibility-focused)
        'user-message': '#1e1b4b', // indigo-900
        'ai-message': '#115e59', // teal-800
        'ai-accent': '#99f6e4', // teal-200
        'message-text': '#ffffff',
        'message-meta': '#e5e7eb',
        
        // Interactive elements
        nebula: '#6366f1', // Used for hover states and links
        'aurora-teal': '#14b8a6', // Accent color for variety
      },
      backgroundImage: {
        constellation:
          'radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.15) 0%, transparent 50%), radial-gradient(circle at 80% 80%, rgba(20, 184, 166, 0.1) 0%, transparent 50%)',
        'glow-orb':
          'radial-gradient(circle, rgba(99, 102, 241, 0.4) 0%, transparent 70%)',
      },
      boxShadow: {
        glow: '0 0 20px rgba(99, 102, 241, 0.3)',
        'glow-lg': '0 0 40px rgba(99, 102, 241, 0.4)',
        'glow-teal': '0 0 20px rgba(20, 184, 166, 0.3)',
        'inner-glow': 'inset 0 0 20px rgba(99, 102, 241, 0.1)',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        float: 'float 6s ease-in-out infinite',
        twinkle: 'twinkle 3s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        twinkle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.3' },
        },
      },
      spacing: {
        18: '4.5rem',
        88: '22rem',
        128: '32rem',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
  darkMode: ['class', 'class'],
};
