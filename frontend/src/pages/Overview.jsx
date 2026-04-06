import { Link } from 'react-router-dom'
import useApi from '../hooks/useApi'
import KPICard from '../components/KPICard'
import CompletionFunnel from '../components/CompletionFunnel'
import ActivityTimeline from '../components/ActivityTimeline'
import { CardSkeleton } from '../components/LoadingState'

export default function Overview() {
  const { data: kpi, loading: kpiLoading } = useApi('/overview')
  const { data: funnel } = useApi('/overview/funnel')
  const { data: timeline } = useApi('/overview/timeline?days=90')
  const { data: topCourses } = useApi('/overview/top-courses?limit=5')

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-800">Overview</h2>
        <p className="text-sm text-slate-500 mt-0.5">Organization-wide learning analytics</p>
      </div>

      {/* KPI cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpiLoading ? (
          <>
            <CardSkeleton /><CardSkeleton /><CardSkeleton /><CardSkeleton />
          </>
        ) : (
          <>
            <KPICard title="Total Learners" value={kpi?.total_learners} color="teal" />
            <KPICard title="Active (30d)" value={kpi?.active_30d} trend={kpi?.active_trend} color="blue" />
            <KPICard title="Avg Completion" value={kpi?.avg_completion_rate} format="percent" color="violet" />
            <KPICard title="Avg Score" value={kpi?.avg_score} format="score" trend={kpi?.score_trend ? Number((kpi.score_trend * 100).toFixed(1)) : undefined} color="amber" />
          </>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <CompletionFunnel data={funnel} />
        <ActivityTimeline data={timeline} />
      </div>

      {/* Top courses */}
      {topCourses && topCourses.length > 0 && (
        <div className="bg-white rounded-xl border border-dash-border p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Top Courses by Enrollment</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-dash-border text-left">
                  <th className="pb-2 font-medium text-slate-500 text-xs">Course</th>
                  <th className="pb-2 font-medium text-slate-500 text-xs text-right">Enrolled</th>
                  <th className="pb-2 font-medium text-slate-500 text-xs text-right">Completed</th>
                  <th className="pb-2 font-medium text-slate-500 text-xs text-right">Completion %</th>
                  <th className="pb-2 font-medium text-slate-500 text-xs text-right">Avg Score</th>
                </tr>
              </thead>
              <tbody>
                {topCourses.map((c) => (
                  <tr key={c.course_id} className="border-b border-slate-50 hover:bg-slate-50/50">
                    <td className="py-2.5">
                      <Link to={`/courses/${encodeURIComponent(c.course_id)}`} className="text-teal-600 hover:underline font-medium">
                        {c.course_name}
                      </Link>
                    </td>
                    <td className="py-2.5 text-right font-mono text-xs">{c.enrolled}</td>
                    <td className="py-2.5 text-right font-mono text-xs">{c.completed}</td>
                    <td className="py-2.5 text-right">
                      <span className="font-mono text-xs">{(c.completion_rate * 100).toFixed(0)}%</span>
                    </td>
                    <td className="py-2.5 text-right font-mono text-xs">{(c.avg_score * 100).toFixed(0)}</td>
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
