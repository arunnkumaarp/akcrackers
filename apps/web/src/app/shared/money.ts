const whole = new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 });
const paise = new Intl.NumberFormat('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

/** "₹1,299" or "₹19.80": whole rupees drop their paise, otherwise both digits show. */
export function money(value: string | number | null | undefined): string {
  if (value === null || value === undefined || value === '') return '';
  const n = Number(value);
  return `₹${(Number.isInteger(n) ? whole : paise).format(n)}`;
}
