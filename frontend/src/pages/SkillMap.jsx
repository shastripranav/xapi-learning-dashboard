import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import useApi from '../hooks/useApi'
import HeatMap from '../components/HeatMap'
import LoadingState from '../components/LoadingState'

export default function SkillMap() {
  const { data: skills, loading } = useApi('/skills')
  const { data: heatmap } = useApi('/skills/heatmap')
  const { data: distribution } = useApi('/skills/distribution')

  if (loading) return <LoadingState rows={6} />

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-800">Skill Map</h2>
        <p className="text-sm text-slate-500 mt-0.5">Organization skill strengths and gaps</p>
      </div>

      <HeatMap data={heatmap} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* skill distribution — box plot approximation */}
        {distribution && distribution.length > 0 && (
          <div className="bg-white rounded-xl border border-dash-border p-5">
            <h3 className="text-sm font-semibold text-slate-700 mb-4">Skill Score Distributions</h3>
            <div className="space-y-3">
              {distribution.map((d) => (
                <div key={d.skill} className="flex items-center gap-3">
                  <span className="text-xs text-slate-600 w-28 truncate" title={d.skill}>{d.skill}</span>
                  <div className="flex-1 h-4 bg-slate-50 rounded relative">
                    <div
                      className="absolute h-full bg-teal-200 rounded"
                      style={{ left: `${d.q1 * 100}%`, width: `${(d.q3 - d.q1) * 100}%` }}
                    />
                    <div
                      className="absolute w-0.5 h-full bg-teal-600"
                      style={{ left: `${d.median * 100}%` }}
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 w-10 text-right font-mono">
                    {(d.median * 100).toFixed(0)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* lowest skills bar chart */}
        {skills && skills.length > 0 && (
          <div className="bg-white rounded-xl border border-dash-border p-5">
            <h3 className="text-sm font-semibold text-slate-700 mb-4">Skills by Average Score</h3>
            <ResponsiveContainer width="100%" height={Math.max(200, skills.length * 32)}>
              <BarChart data={skills} layout="vertical" margin={{ left: 10, right: 20 }}>
                <XAxis type="number" domain={[0, 1]} tick={{ fontSize: 11 }} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
                <YAxis dataKey="skill" type="category" tick={{ fontSize: 11 }} width={110} />
                <Tooltip
                  contentStyle={{ borderRadius: 8, fontSize: 12 }}
                  formatter={(v) => [`${(v * 100).toFixed(1)}%`, 'Avg Score']}
                />
                <Bar dataKey="avg_score" fill="#0d9488" radius={[0, 4, 4, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  )
}
