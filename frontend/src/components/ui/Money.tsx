export function Money({ amount }: { amount: number }) {
  const value = Number.isFinite(amount) ? amount : 0
  return <span style={{ fontWeight: 900 }}>{value.toFixed(2)} CHF</span>
}
