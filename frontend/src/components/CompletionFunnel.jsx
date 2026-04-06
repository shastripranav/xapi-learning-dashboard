import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const STAGE_COLORS = ['#0d9488', '#0891b2', '#6366f1', '#8b5cf6']

export default function CompletionFunnel({ data }) {
  if (!data) return null

  const stages = [
    { name: 'Registered', value: data.registered },
    { name: 'Started', value: data.started },
    { name: 'In Progress', value: data.in_progress },
    { name: 'Completed', value: data.completed },
  ]

  return (
    <div className="bg-white rounded-xl border border-dash-border p-5">
      <h3 className="text-sm font-semibold text-slate-700 mb-4">Completion Funnel</h3>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={stages} layout="vertical" margin={{ left: 10, right: 20 }}>
          <XAxis type="number" tick={{ fontSize: 12 }} />
          <YAxis dataKey="name" type="category" tick={{ fontSize: 12 }} width={85} />
          <Tooltip
            contentStyle={{ borderRadius: 8, border: '1px solid #e2e8f0' }}
            formatter={(val) => [val, 'Learners']}
          />
          <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={28}>
            {stages.map((_, idx) => (
              <Cell key={idx} fill={STAGE_COLORS[idx]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
