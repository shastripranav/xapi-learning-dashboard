import { useParams, Link } from 'react-router-dom'
import useApi from '../hooks/useApi'
import SkillRadar from '../components/SkillRadar'
import LoadingState from '../components/LoadingState'

export default function LearnerDetail() {
  const { email } = useParams()
  const { data: profile, loading } = useApi(`/learners/${email}`)
  const { data: skillData } = useApi(`/learners/${email}/skills`)
  const { data: activity } = useApi(`/learners/${email}/activity?limit=20`)
  const { data: progress } = useApi(`/learners/${email}/progress`)

  if (loading) return <LoadingState rows={6} />

  if (!profile) {
    return <p className="text-slate-500 py-8 text-center">Learner not found</p>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 text-sm text-slate-500">
        <Link to="/learners" className="hover:text-teal-600">Learners</Link>
        <span>/</span>
        <span className="text-slate-800 font-medium">{profile.name}</span>
      </div>

      {/* profile header */}
      <div className="bg-white rounded-xl border border-dash-border p-5">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-800">{profile.name}</h2>
            <p className="text-sm text-slate-500">{profile.email}</p>
          </div>
          <div className="text-right">
            <p className="text-xs text-slate-400">Engagement Score</p>
            <p className="text-2xl font-bold text-teal-600">
              {profile.engagement?.total_score?.toFixed(0) || '—'}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-dash-border">
          <div>
            <p className="text-[11px] text-slate-400 uppercase">Statements</p>
            <p className="text-lg font-semibold">{profile.statement_count}</p>
          </div>
          <div>
            <p className="text-[11px] text-slate-400 uppercase">First Active</p>
            <p className="text-sm">{new Date(profile.first_activity).toLocaleDateString()}</p>
          </div>
          <div>
            <p className="text-[11px] text-slate-400 uppercase">Last Active</p>
            <p className="text-sm">{new Date(profile.last_activity).toLocaleDateString()}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* skill radar */}
        <SkillRadar
          skills={skillData?.learner_skills}
          cohortAvg={skillData?.cohort_avg}
        />

        {/* course progress */}
        <div className="bg-white rounded-xl border border-dash-border p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Course Progress</h3>
          {progress && progress.length > 0 ? (
            <div className="space-y-2.5">
              {progress.map((p) => (
                <div key={p.course_id} className="flex items-center justify-between py-1.5 border-b border-slate-50 last:border-0">
                  <div>
                    <Link to={`/courses/${encodeURIComponent(p.course_id)}`} className="text-sm text-teal-600 hover:underline">
                      {p.course_name}
                    </Link>
                  </div>
                  <div className="flex items-center gap-3">
                    {p.best_score !== null && (
                      <span className="text-xs font-mono text-slate-500">
                        {(p.best_score * 100).toFixed(0)}%
                      </span>
                    )}
                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${
                      p.completed
                        ? 'bg-emerald-100 text-emerald-700'
                        : 'bg-amber-100 text-amber-700'
                    }`}>
                      {p.completed ? 'Completed' : 'In Progress'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-slate-400">No course data available</p>
          )}
        </div>
      </div>

      {/* recent activity */}
      <div className="bg-white rounded-xl border border-dash-border p-5">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">Recent Activity</h3>
        {activity && activity.length > 0 ? (
          <div className="space-y-0">
            {activity.map((a, i) => (
              <div key={i} className="flex items-center gap-3 py-2 border-b border-slate-50 last:border-0">
                <VerbBadge verb={a.verb} />
                <span className="text-sm text-slate-700 flex-1">{a.activity_name}</span>
                {a.score !== null && a.score !== undefined && (
                  <span className="text-xs font-mono text-slate-500">{(a.score * 100).toFixed(0)}%</span>
                )}
                <span className="text-[11px] text-slate-400">
                  {new Date(a.timestamp).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-slate-400">No recent activity</p>
        )}
      </div>
    </div>
  )
}

const VERB_COLORS = {
  completed: 'bg-emerald-100 text-emerald-700',
  passed: 'bg-emerald-100 text-emerald-700',
  failed: 'bg-rose-100 text-rose-600',
  scored: 'bg-indigo-100 text-indigo-600',
  experienced: 'bg-sky-100 text-sky-600',
  registered: 'bg-violet-100 text-violet-600',
  initialized: 'bg-slate-100 text-slate-600',
  attempted: 'bg-amber-100 text-amber-700',
}

function VerbBadge({ verb }) {
  const cls = VERB_COLORS[verb] || 'bg-slate-100 text-slate-500'
  return (
    <span className={`text-[10px] px-2 py-0.5 rounded font-medium min-w-[72px] text-center ${cls}`}>
      {verb}
    </span>
  )
}
