import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export default function ActivityTimeline({ data }) {
  if (!data || data.length === 0) return null

  return (
    <div className="bg-white rounded-xl border border-dash-border p-5">
      <h3 className="text-sm font-semibold text-slate-700 mb-4">Activity Timeline</h3>
      <ResponsiveContainer width="100%" height={240}>
        <AreaChart data={data} margin={{ top: 5, right: 10, bottom: 0, left: -10 }}>
          <defs>
            <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#14b8a6" stopOpacity={0.3} />
              <stop offset="100%" stopColor="#14b8a6" stopOpacity={0.02} />
            </linearGradient>
          </defs>
          <XAxis
            dataKey="date"
            tick={{ fontSize: 10 }}
            tickFormatter={(d) => d.slice(5)}
            interval="preserveStartEnd"
          />
          <YAxis tick={{ fontSize: 11 }} />
          <Tooltip
            contentStyle={{ borderRadius: 8, border: '1px solid #e2e8f0', fontSize: 13 }}
            labelFormatter={(l) => `Date: ${l}`}
          />
          <Area
            type="monotone"
            dataKey="count"
            stroke="#14b8a6"
            strokeWidth={2}
            fill="url(#areaGrad)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}
