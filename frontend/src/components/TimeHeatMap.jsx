/**
 * Day-of-week × Hour activity heat map.
 * Custom grid — Recharts doesn't have native heat maps.
 */

const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

function intensityClass(count, maxCount) {
  if (count === 0) return 'bg-slate-50'
  const pct = count / maxCount
  if (pct < 0.15) return 'bg-teal-100'
  if (pct < 0.35) return 'bg-teal-200'
  if (pct < 0.55) return 'bg-teal-400'
  if (pct < 0.75) return 'bg-teal-500'
  return 'bg-teal-700'
}

export default function TimeHeatMap({ data }) {
  if (!data || data.length === 0) return null

  const maxCount = Math.max(...data.map((d) => d.count), 1)

  const grid = {}
  for (const { day, hour, count } of data) {
    if (!grid[day]) grid[day] = {}
    grid[day][hour] = count
  }

  return (
    <div className="bg-white rounded-xl border border-dash-border p-5 overflow-x-auto">
      <h3 className="text-sm font-semibold text-slate-700 mb-4">Activity by Time of Day</h3>

      <div className="min-w-[600px]">
        {/* hour labels */}
        <div className="flex gap-px mb-px">
          <div className="w-10 flex-shrink-0" />
          {Array.from({ length: 24 }, (_, h) => (
            <div key={h} className="flex-1 text-[9px] text-slate-400 text-center">
              {h}
            </div>
          ))}
        </div>

        {DAYS.map((day) => (
          <div key={day} className="flex gap-px mb-px">
            <div className="w-10 flex-shrink-0 text-[11px] text-slate-500 font-medium leading-6">
              {day}
            </div>
            {Array.from({ length: 24 }, (_, h) => {
              const count = grid[day]?.[h] || 0
              return (
                <div
                  key={h}
                  className={`flex-1 h-6 rounded-sm ${intensityClass(count, maxCount)} transition-colors`}
                  title={`${day} ${h}:00 — ${count} activities`}
                />
              )
            })}
          </div>
        ))}
      </div>

      <div className="flex items-center gap-3 mt-3 text-[10px] text-slate-500">
        <span>Activity:</span>
        <div className="flex items-center gap-1"><div className="w-4 h-3 bg-slate-50 rounded-sm border border-slate-200" /> None</div>
        <div className="flex items-center gap-1"><div className="w-4 h-3 bg-teal-200 rounded-sm" /> Low</div>
        <div className="flex items-center gap-1"><div className="w-4 h-3 bg-teal-400 rounded-sm" /> Med</div>
        <div className="flex items-center gap-1"><div className="w-4 h-3 bg-teal-700 rounded-sm" /> High</div>
      </div>
    </div>
  )
}
