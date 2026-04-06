import { Link } from 'react-router-dom'

export default function AtRiskTable({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-dash-border p-5">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">At-Risk Learners</h3>
        <p className="text-sm text-slate-400">No at-risk learners detected.</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl border border-dash-border p-5">
      <h3 className="text-sm font-semibold text-slate-700 mb-3">
        At-Risk Learners
        <span className="ml-2 text-xs font-normal bg-rose-100 text-rose-600 px-2 py-0.5 rounded-full">
          {data.length}
        </span>
      </h3>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-dash-border text-left">
              <th className="pb-2 font-medium text-slate-500 text-xs">Name</th>
              <th className="pb-2 font-medium text-slate-500 text-xs">Days Inactive</th>
              <th className="pb-2 font-medium text-slate-500 text-xs">Score Trend</th>
              <th className="pb-2 font-medium text-slate-500 text-xs">Engagement</th>
              <th className="pb-2 font-medium text-slate-500 text-xs">Risk Reasons</th>
            </tr>
          </thead>
          <tbody>
            {data.map((r) => (
              <tr key={r.email} className="border-b border-slate-50 hover:bg-slate-50/50">
                <td className="py-2.5">
                  <Link to={`/learners/${encodeURIComponent(r.email)}`} className="text-teal-600 hover:underline font-medium">
                    {r.name}
                  </Link>
                </td>
                <td className="py-2.5 font-mono text-xs">{r.days_since_active}d</td>
                <td className="py-2.5">
                  <span className={`text-xs px-2 py-0.5 rounded-full ${
                    r.score_trend === 'declining'
                      ? 'bg-rose-100 text-rose-600'
                      : 'bg-slate-100 text-slate-500'
                  }`}>
                    {r.score_trend}
                  </span>
                </td>
                <td className="py-2.5 font-mono text-xs">{r.engagement_score.toFixed(0)}</td>
                <td className="py-2.5">
                  <div className="flex flex-wrap gap-1">
                    {r.risk_reasons.map((reason, i) => (
                      <span key={i} className="text-[10px] bg-amber-50 text-amber-700 px-1.5 py-0.5 rounded">
                        {reason}
                      </span>
                    ))}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
