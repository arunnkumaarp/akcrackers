/**
 * The AK Crackers design tokens, the same as the website's "Diwali night": a night-violet sky with gold
 * on it, and cream panels with dark plum text. `ink` is the dark text on panels; things on the sky use `gold`.
 */
export const color = {
  bg: '#1c0a2e',
  bgDeep: '#12061f',
  gold: '#ffc93c',
  skyMuted: '#e9cfa3',
  red: '#e8432e',
  ink: '#2a1230',
  inkSoft: '#cdbfe0',
  paper: '#fff8ec',
  paperInk: '#2a1230',
  paperMuted: '#6e5a68',
  paperStep: '#f5e9d4',
  danger: '#b3261e',
};

export const font = {
  regular: 'Baloo2_400Regular',
  medium: 'Baloo2_600SemiBold',
  bold: 'Baloo2_800ExtraBold',
};

export const radius = { panel: 18, input: 10, pill: 999 };

export const space = { gutter: 16, margin: 16 };

/** Taps smaller than this are hard to hit; every button and link is at least this tall. */
export const TOUCH = 48;
