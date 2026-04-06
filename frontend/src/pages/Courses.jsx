import { useState } from 'react'
import { Link } from 'react-router-dom'
import useApi from '../hooks/useApi'
import LoadingState from '../components/LoadingState'

const DOMAIN_COLORS = {
  Technical: 'bg-sky-100 text-sky-700',
  Compliance: 'bg-amber-100 text-amber-700',
  Leadership: 'bg-violet-100 text-violet-600',
  Product: 'bg-emerald-100 text-emerald-700',
}

export default function Courses() {
  const { data: courses, loading } = useApi('/courses')
  const [sortBy, setSortBy] = useState('enrollment_count')
  const [sortDir, setSortDir] = useState('desc')

  const sorted = [...(courses || [])].sort((a, b) => {
    const dir = sortDir === 'asc' ? 1 : -1
    return (a[sortBy] - b[sortBy]) * dir
  })

  function handleSort(field) {
    if (sortBy === field) setSortDir(sortDir === 'asc' ? 'desc' : 'asc')
    else { setSortBy(field); setSortDir('desc') }
  }

  const SortTh = ({ field, children }) => (
    <th
      className="pb-2 font-medium text-slate-500 text-xs cursor-pointer hover:text-slate-700 text-right select-none"
      onClick={() => handleSort(field)}
    >
      {children}
      {sortBy === field && <span className="ml-1">{sortDir === 'asc' ? '↑' : '↓'}</span>}
    </th>
  )

  return (
    <div className="space-y-5">
      <div>
        <h2 className="text-xl font-bold text-slate-800">Courses</h2>
        <p className="text-sm text-slate-500 mt-0.5">{courses?.length || 0} courses</p>
      </div>

      {loading ? (
        <LoadingState rows={6} />
      ) : (
        <div className="bg-white rounded-xl border border-dash-border p-5">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-dash-border text-left">
                  <th className="pb-2 font-medium text-slate-500 text-xs">Course</th>
                  <th className="pb-2 font-medium text-slate-500 text-xs">Domain</th>
                  <SortTh field="enrollment_count">Enrolled</SortTh>
                  <SortTh field="completion_rate">Completion</SortTh>
                  <SortTh field="avg_score">Avg Score</SortTh>
                  <SortTh field="avg_duration_minutes">Avg Time (min)</SortTh>
                </tr>
              </thead>
              <tbody>
                {sorted.map((c) => (
                  <tr key={c.course_id} className="border-b border-slate-50 hover:bg-slate-50/50">
                    <td className="py-2.5">
                      <Link to={`/courses/${encodeURIComponent(c.course_id)}`} className="text-teal-600 hover:underline font-medium">
                        {c.course_name}
                      </Link>
                      <p className="text-[10px] text-slate-400 capitalize">{c.difficulty}</p>
                    </td>
                    <td className="py-2.5">
                      <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${DOMAIN_COLORS[c.domain] || 'bg-slate-100 text-slate-500'}`}>
                        {c.domain}
                      </span>
                    </td>
                    <td className="py-2.5 text-right font-mono text-xs">{c.enrollment_count}</td>
                    <td className="py-2.5 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                          <div className="h-full bg-teal-500 rounded-full" style={{ width: `${(c.completion_rate * 100)}%` }} />
                        </div>
                        <span className="font-mono text-xs w-10 text-right">{(c.completion_rate * 100).toFixed(0)}%</span>
                      </div>
                    </td>
                    <td className="py-2.5 text-right font-mono text-xs">{(c.avg_score * 100).toFixed(0)}</td>
                    <td className="py-2.5 text-right font-mono text-xs">{c.avg_duration_minutes.toFixed(0)}</td>
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
