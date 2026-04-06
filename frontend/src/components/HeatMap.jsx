/**
 * Learners × Skills heat map — custom grid implementation.
 * Recharts doesn't have a native heat map, so we build with CSS grid.
 */

function scoreColor(val) {
  if (val <= 0) return 'bg-slate-100'
  if (val < 0.4) return 'bg-rose-300'
  if (val < 0.6) return 'bg-amber-300'
  if (val < 0.75) return 'bg-yellow-300'
  return 'bg-emerald-400'
}

export default function HeatMap({ data }) {
  if (!data || !data.skills || data.learners?.length === 0) return null

  const { skills, learners } = data
  const displayed = learners.slice(0, 30)

  return (
    <div className="bg-white rounded-xl border border-dash-border p-5 overflow-x-auto">
      <h3 className="text-sm font-semibold text-slate-700 mb-4">
        Skill Heat Map
        {learners.length > 30 && (
          <span className="ml-2 text-xs font-normal text-slate-400">
            (showing top 30 of {learners.length})
          </span>
        )}
      </h3>

      <div className="min-w-[700px]">
        {/* header row */}
        <div className="flex gap-px mb-px">
          <div className="w-36 flex-shrink-0" />
          {skills.map((skill) => (
            <div
              key={skill}
              className="flex-1 text-[10px] font-medium text-slate-500 text-center px-0.5 truncate"
              title={skill}
            >
              {skill}
            </div>
          ))}
        </div>

        {/* data rows */}
        {displayed.map((learner) => (
          <div key={learner.email} className="flex gap-px mb-px">
            <div className="w-36 flex-shrink-0 text-[11px] text-slate-600 truncate pr-2 leading-6" title={learner.name}>
              {learner.name}
            </div>
            {skills.map((skill) => {
              const val = learner.scores?.[skill] || 0
              return (
                <div
                  key={skill}
                  className={`flex-1 h-6 rounded-sm ${scoreColor(val)} flex items-center justify-center`}
                  title={`${learner.name}: ${skill} — ${(val * 100).toFixed(0)}%`}
                >
                  <span className="text-[9px] text-slate-700/70 font-mono">
                    {val > 0 ? (val * 100).toFixed(0) : ''}
                  </span>
                </div>
              )
            })}
          </div>
        ))}
      </div>

      <div className="flex items-center gap-4 mt-4 text-[10px] text-slate-500">
        <span>Score:</span>
        <div className="flex items-center gap-1"><div className="w-4 h-3 bg-rose-300 rounded-sm" /> &lt;40%</div>
        <div className="flex items-center gap-1"><div className="w-4 h-3 bg-amber-300 rounded-sm" /> 40-60%</div>
        <div className="flex items-center gap-1"><div className="w-4 h-3 bg-yellow-300 rounded-sm" /> 60-75%</div>
        <div className="flex items-center gap-1"><div className="w-4 h-3 bg-emerald-400 rounded-sm" /> &gt;75%</div>
      </div>
    </div>
  )
}
