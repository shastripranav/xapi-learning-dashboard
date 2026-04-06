import { useState } from 'react'
import { Link } from 'react-router-dom'
import useApi from '../hooks/useApi'
import useDebounce from '../hooks/useDebounce'
import LoadingState from '../components/LoadingState'

const STATUS_STYLES = {
  active: 'bg-emerald-100 text-emerald-700',
  'at-risk': 'bg-rose-100 text-rose-600',
  inactive: 'bg-slate-100 text-slate-500',
}

export default function Learners() {
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [sortBy, setSortBy] = useState('name')
  const [sortDir, setSortDir] = useState('asc')
  const debouncedSearch = useDebounce(search)

  const { data, loading } = useApi(
    `/learners?search=${debouncedSearch}&page=${page}&limit=20`,
    { deps: [debouncedSearch, page] }
  )

  const learners = data?.learners || []
  const total = data?.total || 0

  const sorted = [...learners].sort((a, b) => {
    const aVal = a[sortBy]
    const bVal = b[sortBy]
    const dir = sortDir === 'asc' ? 1 : -1
    if (typeof aVal === 'string') return aVal.localeCompare(bVal) * dir
    return (aVal - bVal) * dir
  })

  function handleSort(field) {
    if (sortBy === field) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc')
    } else {
      setSortBy(field)
      setSortDir('asc')
    }
  }

  const SortHeader = ({ field, children, align }) => (
    <th
      className={`pb-2 font-medium text-slate-500 text-xs cursor-pointer hover:text-slate-700 select-none ${align === 'right' ? 'text-right' : 'text-left'}`}
      onClick={() => handleSort(field)}
    >
      {children}
      {sortBy === field && <span className="ml-1">{sortDir === 'asc' ? '↑' : '↓'}</span>}
    </th>
  )

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-800">Learners</h2>
          <p className="text-sm text-slate-500 mt-0.5">{total} learners total</p>
        </div>
        <input
          type="text"
          placeholder="Search by name or email…"
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(1) }}
          className="w-72 px-3 py-2 text-sm border border-dash-border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500/30 focus:border-teal-500"
        />
      </div>

      {loading ? (
        <LoadingState rows={8} />
      ) : (
        <div className="bg-white rounded-xl border border-dash-border p-5">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-dash-border">
                  <SortHeader field="name">Name</SortHeader>
                  <SortHeader field="courses_completed" align="right">Courses Done</SortHeader>
                  <SortHeader field="avg_score" align="right">Avg Score</SortHeader>
                  <SortHeader field="engagement_score" align="right">Engagement</SortHeader>
                  <SortHeader field="last_active">Last Active</SortHeader>
                  <SortHeader field="status">Status</SortHeader>
                </tr>
              </thead>
              <tbody>
                {sorted.map((l) => (
                  <tr key={l.email} className="border-b border-slate-50 hover:bg-slate-50/50">
                    <td className="py-2.5">
                      <Link to={`/learners/${encodeURIComponent(l.email)}`} className="text-teal-600 hover:underline font-medium">
                        {l.name}
                      </Link>
                      <p className="text-[11px] text-slate-400">{l.email}</p>
                    </td>
                    <td className="py-2.5 text-right font-mono text-xs">{l.courses_completed}</td>
                    <td className="py-2.5 text-right font-mono text-xs">{(l.avg_score * 100).toFixed(0)}</td>
                    <td className="py-2.5 text-right font-mono text-xs">{l.engagement_score.toFixed(0)}</td>
                    <td className="py-2.5 text-xs text-slate-500">{new Date(l.last_active).toLocaleDateString()}</td>
                    <td className="py-2.5">
                      <span className={`text-[11px] px-2 py-0.5 rounded-full font-medium ${STATUS_STYLES[l.status] || STATUS_STYLES.active}`}>
                        {l.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {total > 20 && (
            <div className="flex items-center justify-between mt-4 pt-3 border-t border-dash-border">
              <button
                onClick={() => setPage(Math.max(1, page - 1))}
                disabled={page === 1}
                className="text-sm text-teal-600 disabled:text-slate-300"
              >
                ← Previous
              </button>
              <span className="text-xs text-slate-500">Page {page} of {Math.ceil(total / 20)}</span>
              <button
                onClick={() => setPage(page + 1)}
                disabled={page * 20 >= total}
                className="text-sm text-teal-600 disabled:text-slate-300"
              >
                Next →
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
