import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export default function ScoreHistogram({ data }) {
  if (!data || data.length === 0) return null

  return (
    <div className="bg-white rounded-xl border border-dash-border p-5">
      <h3 className="text-sm font-semibold text-slate-700 mb-4">Score Distribution</h3>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data} margin={{ top: 5, right: 10, bottom: 0, left: -10 }}>
          <XAxis dataKey="range" tick={{ fontSize: 10 }} />
          <YAxis tick={{ fontSize: 11 }} />
          <Tooltip
            contentStyle={{ borderRadius: 8, border: '1px solid #e2e8f0', fontSize: 13 }}
            formatter={(v) => [v, 'Learners']}
          />
          <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} barSize={24} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
