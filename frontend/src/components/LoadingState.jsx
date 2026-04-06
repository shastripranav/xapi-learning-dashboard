export default function LoadingState({ rows = 4 }) {
  return (
    <div className="animate-pulse space-y-4">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="h-16 bg-slate-100 rounded-lg" />
      ))}
    </div>
  )
}

export function CardSkeleton() {
  return (
    <div className="animate-pulse bg-white rounded-xl border border-dash-border p-5">
      <div className="h-3 bg-slate-100 rounded w-24 mb-3" />
      <div className="h-7 bg-slate-100 rounded w-16 mb-2" />
      <div className="h-2.5 bg-slate-50 rounded w-20" />
    </div>
  )
}
