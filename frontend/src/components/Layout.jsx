import { NavLink } from 'react-router-dom'

const NAV_ITEMS = [
  { to: '/', label: 'Overview', icon: BarIcon },
  { to: '/learners', label: 'Learners', icon: UsersIcon },
  { to: '/courses', label: 'Courses', icon: BookIcon },
  { to: '/skills', label: 'Skills', icon: GridIcon },
  { to: '/engagement', label: 'Engagement', icon: PulseIcon },
  { to: '/settings', label: 'Settings', icon: GearIcon },
]

export default function Layout({ children }) {
  return (
    <div className="flex min-h-screen">
      <aside className="w-60 bg-sidebar flex flex-col flex-shrink-0 sticky top-0 h-screen">
        <div className="px-5 py-6 border-b border-slate-700/50">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-accent-500 flex items-center justify-center">
              <span className="text-white text-sm font-bold">xA</span>
            </div>
            <div>
              <h1 className="text-white font-semibold text-sm tracking-tight">xAPI Analytics</h1>
              <p className="text-slate-400 text-[11px]">Learning Dashboard</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto scrollbar-thin">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive
                    ? 'bg-accent-600/20 text-accent-400 font-medium'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-sidebar-hover'
                }`
              }
            >
              <Icon />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="px-4 py-3 border-t border-slate-700/50">
          <p className="text-slate-500 text-[10px] uppercase tracking-wider">Demo Mode</p>
        </div>
      </aside>

      <main className="flex-1 overflow-x-hidden">
        <div className="max-w-[1400px] mx-auto px-6 py-6">
          {children}
        </div>
      </main>
    </div>
  )
}

function BarIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
      <path d="M3 12h4v8H3zM10 8h4v12h-4zM17 4h4v16h-4z" />
    </svg>
  )
}

function UsersIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
      <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M9 11a4 4 0 100-8 4 4 0 000 8zM23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" />
    </svg>
  )
}

function BookIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
      <path d="M4 19.5A2.5 2.5 0 016.5 17H20M4 19.5V4.5A2.5 2.5 0 016.5 2H20v20H6.5A2.5 2.5 0 014 19.5z" />
    </svg>
  )
}

function GridIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
      <path d="M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z" />
    </svg>
  )
}

function PulseIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
    </svg>
  )
}

function GearIcon() {
  return (
    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2}>
      <path d="M12 15a3 3 0 100-6 3 3 0 000 6z" />
      <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z" />
    </svg>
  )
}
