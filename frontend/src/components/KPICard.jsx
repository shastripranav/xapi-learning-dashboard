const COLORS = {
  teal: 'from-teal-500 to-emerald-600',
  blue: 'from-blue-500 to-indigo-600',
  amber: 'from-amber-500 to-orange-600',
  rose: 'from-rose-500 to-pink-600',
  violet: 'from-violet-500 to-purple-600',
}

export default function KPICard({ title, value, trend, color = 'teal', format }) {
  const gradient = COLORS[color] || COLORS.teal
  const displayValue = format === 'percent' ? `${(value * 100).toFixed(1)}%`
    : format === 'score' ? `${(value * 100).toFixed(0)}`
    : typeof value === 'number' ? value.toLocaleString()
    : value

  return (
    <div className="bg-white rounded-xl border border-dash-border p-5 relative overflow-hidden">
      <div className={`absolute top-0 left-0 w-1 h-full bg-gradient-to-b ${gradient}`} />
      <p className="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">{title}</p>
      <p className="text-2xl font-bold text-slate-800">{displayValue}</p>
      {trend !== undefined && trend !== null && (
        <div className="flex items-center gap-1 mt-1.5">
          <span className={trend >= 0 ? 'text-emerald-600' : 'text-rose-500'}>
            {trend >= 0 ? '↑' : '↓'}
          </span>
          <span className={`text-xs font-medium ${trend >= 0 ? 'text-emerald-600' : 'text-rose-500'}`}>
            {Math.abs(trend)} vs prev period
          </span>
        </div>
      )}
    </div>
  )
}
