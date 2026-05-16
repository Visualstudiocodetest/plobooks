export const theme = {
  colors: {
    // Primary brand color extracted from recyclerie.ch (approximate orange)
    primary: '#FF7F00',
    // Secondary accent color (deep teal)
    secondary: '#004080',
    background: '#FAFAFA',
    surface: '#FFFFFF',
    textPrimary: '#333333',
    textSecondary: '#555555',
    border: '#E0E0E0',
    // Additional palette for gradients and effects
    gradientStart: '#FF7F00',
    gradientEnd: '#FFB84D',
    success: '#4CAF50',
    warning: '#FFC107',
    error: '#F44336',
  },
  spacing: (factor: number) => `${factor * 8}px`, // 8px grid
  borderRadius: '8px',
  fontFamily: `'Inter', 'Helvetica Neue', Arial, sans-serif`,
};
