import { useParams, Link } from 'react-router-dom'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import useApi from '../hooks/useApi'
import ScoreHistogram from '../components/ScoreHistogram'
import LoadingState from '../components/LoadingState'

export default function CourseDetail() {
  const { courseId } = useParams()
  const { data: course, loading } = useApi(`/courses/${courseId}`)
  const { data: scores } = useApi(`/courses/${courseId}/scores`)
  const { data: dropoff } = useApi(`/courses/${courseId}/dropoff`)

  if (loading) return <LoadingState rows={6} />
  if (!course) return <p className="text-slate-500 py-8 text-center">Course not found</p>

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 text-sm text-slate-500">
        <Link to="/courses" className="hover:text-teal-600">Courses</Link>
        <span>/</span>
        <span className="text-slate-800 font-medium">{course.course_name}</span>
      </div>

      <div className="bg-white rounded-xl border border-dash-border p-5">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-800">{course.course_name}</h2>
            <p className="text-sm text-slate-500">{course.domain} · {course.difficulty}</p>
          </div>
          <div className="text-right">
            <p className="text-xs text-slate-400">Completion Rate</p>
            <p className="text-2xl font-bold text-teal-600">{(course.completion_rate * 100).toFixed(0)}%</p>
          </div>
        </div>
        <div className="grid grid-cols-4 gap-4 mt-4 pt-4 border-t border-dash-border">
          <div>
            <p className="text-[11px] text-slate-400 uppercase">Enrolled</p>
            <p className="text-lg font-semibold">{course.enrollment_count}</p>
          </div>
          <div>
            <p className="text-[11px] text-slate-400 uppercase">Completed</p>
            <p className="text-lg font-semibold">{course.completion_count}</p>
          </div>
          <div>
            <p className="text-[11px] text-slate-400 uppercase">Avg Score</p>
            <p className="text-lg font-semibold">{(course.avg_score * 100).toFixed(0)}</p>
          </div>
          <div>
            <p className="text-[11px] text-slate-400 uppercase">Learners</p>
            <p className="text-lg font-semibold">{course.unique_learners}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <ScoreHistogram data={scores} />

        {/* weekly completions */}
        {course.weekly_completions && course.weekly_completions.length > 0 && (
          <div className="bg-white rounded-xl border border-dash-border p-5">
            <h3 className="text-sm font-semibold text-slate-700 mb-4">Weekly Completions</h3>
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={course.weekly_completions} margin={{ top: 5, right: 10, bottom: 0, left: -10 }}>
                <XAxis dataKey="week" tick={{ fontSize: 11 }} label={{ value: 'Week', position: 'insideBottom', offset: -2, fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip contentStyle={{ borderRadius: 8, fontSize: 12 }} />
                <Line type="monotone" dataKey="completions" stroke="#0d9488" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* drop-off analysis */}
      {dropoff && dropoff.length > 0 && (
        <div className="bg-white rounded-xl border border-dash-border p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-4">Drop-off Analysis</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={dropoff} margin={{ top: 5, right: 10, bottom: 0, left: -10 }}>
              <XAxis dataKey="module" tick={{ fontSize: 10 }} />
              <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
              <Tooltip
                contentStyle={{ borderRadius: 8, fontSize: 12 }}
                formatter={(v) => [`${(v * 100).toFixed(1)}%`, '% of starters']}
              />
              <Bar dataKey="pct_of_starters" fill="#8b5cf6" radius={[4, 4, 0, 0]} barSize={24} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
