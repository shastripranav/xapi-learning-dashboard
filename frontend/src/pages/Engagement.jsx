import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import useApi from '../hooks/useApi'
import AtRiskTable from '../components/AtRiskTable'
import TimeHeatMap from '../components/TimeHeatMap'
import LoadingState from '../components/LoadingState'

export default function Engagement() {
  const { data: scores, loading } = useApi('/engagement/scores')
  const { data: atRisk } = useApi('/engagement/at-risk')
  const { data: timeOfDay } = useApi('/engagement/time-of-day')
  const { data: peakHours } = useApi('/engagement/peak-hours')
  const [sortBy, setSortBy] = useState('total_score')
  const [sortDir, setSortDir] = useState('desc')

  if (loading) return <LoadingState rows={6} />

  const sorted = [...(scores || [])].sort((a, b) => {
    return (a[sortBy] - b[sortBy]) * (sortDir === 'asc' ? 1 : -1)
  })

  function toggleSort(field) {
    if (sortBy === field) setSortDir(sortDir === 'asc' ? 'desc' : 'asc')
    else { setSortBy(field); setSortDir('desc') }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-800">Engagement Analytics</h2>
        <p className="text-sm text-slate-500 mt-0.5">Engagement scoring and at-risk detection</p>
      </div>

      <AtRiskTable data={atRisk} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <TimeHeatMap data={timeOfDay} />

        {peakHours && peakHours.length > 0 && (
          <div className="bg-white rounded-xl border border-dash-border p-5">
            <h3 className="text-sm font-semibold text-slate-700 mb-4">Peak Activity Hours</h3>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={peakHours} margin={{ top: 5, right: 10, bottom: 0, left: -10 }}>
                <XAxis dataKey="hour" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip contentStyle={{ borderRadius: 8, fontSize: 12 }} />
                <Bar dataKey="count" fill="#14b8a6" radius={[3, 3, 0, 0]} barSize={16} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* engagement scores table */}
      {scores && scores.length > 0 && (
        <div className="bg-white rounded-xl border border-dash-border p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Engagement Scores</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-dash-border text-left">
                  <th className="pb-2 font-medium text-slate-500 text-xs">Name</th>
                  {['frequency_score', 'recency_score', 'duration_score', 'total_score'].map((f) => (
                    <th
                      key={f}
                      className="pb-2 font-medium text-slate-500 text-xs text-right cursor-pointer hover:text-slate-700 select-none"
                      onClick={() => toggleSort(f)}
                    >
                      {f.replace('_score', '').replace('total', 'Total')}
                      {sortBy === f && <span className="ml-1">{sortDir === 'asc' ? '↑' : '↓'}</span>}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {sorted.slice(0, 30).map((s) => (
                  <tr key={s.email} className="border-b border-slate-50 hover:bg-slate-50/50">
                    <td className="py-2">{s.name}</td>
                    <td className="py-2 text-right font-mono text-xs">{s.frequency_score.toFixed(1)}</td>
                    <td className="py-2 text-right font-mono text-xs">{s.recency_score.toFixed(1)}</td>
                    <td className="py-2 text-right font-mono text-xs">{s.duration_score.toFixed(1)}</td>
                    <td className="py-2 text-right">
                      <span className={`font-mono text-xs font-medium ${
                        s.total_score >= 60 ? 'text-emerald-600' : s.total_score >= 30 ? 'text-amber-600' : 'text-rose-600'
                      }`}>
                        {s.total_score.toFixed(1)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
