import { useState, useEffect } from 'react'
import api from '../api/client'

export default function Settings() {
  const [status, setStatus] = useState(null)
  const [form, setForm] = useState({ endpoint: '', username: '', password: '' })
  const [connecting, setConnecting] = useState(false)
  const [message, setMessage] = useState(null)

  useEffect(() => {
    api.get('/data-source/status').then(setStatus).catch(() => {})
  }, [])

  async function handleConnect(e) {
    e.preventDefault()
    setConnecting(true)
    setMessage(null)
    try {
      const res = await api.post('/connect-lrs', form)
      setMessage({ type: 'success', text: `Connected! Loaded ${res.loaded} statements.` })
      setStatus(await api.get('/data-source/status'))
    } catch (err) {
      setMessage({ type: 'error', text: err.message })
    } finally {
      setConnecting(false)
    }
  }

  async function handleLoadDemo() {
    setConnecting(true)
    setMessage(null)
    try {
      const res = await api.post('/load-demo')
      setMessage({ type: 'success', text: `Demo loaded! ${res.loaded} statements.` })
      setStatus(await api.get('/data-source/status'))
    } catch (err) {
      setMessage({ type: 'error', text: err.message })
    } finally {
      setConnecting(false)
    }
  }

  async function handleUpload(e) {
    const file = e.target.files?.[0]
    if (!file) return
    setConnecting(true)
    setMessage(null)
    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await api.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setMessage({ type: 'success', text: `Uploaded! ${res.loaded} statements parsed.` })
      setStatus(await api.get('/data-source/status'))
    } catch (err) {
      setMessage({ type: 'error', text: err.message })
    } finally {
      setConnecting(false)
    }
  }

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h2 className="text-xl font-bold text-slate-800">Settings</h2>
        <p className="text-sm text-slate-500 mt-0.5">Data source configuration</p>
      </div>

      {/* current status */}
      {status && (
        <div className="bg-white rounded-xl border border-dash-border p-5">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Current Data Source</h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-[11px] text-slate-400 uppercase">Mode</p>
              <p className="font-medium capitalize">{status.mode}</p>
            </div>
            <div>
              <p className="text-[11px] text-slate-400 uppercase">Statements</p>
              <p className="font-medium">{status.statement_count?.toLocaleString()}</p>
            </div>
            {status.last_sync && (
              <div>
                <p className="text-[11px] text-slate-400 uppercase">Last Sync</p>
                <p className="text-xs">{new Date(status.last_sync).toLocaleString()}</p>
              </div>
            )}
            {status.lrs_endpoint && (
              <div>
                <p className="text-[11px] text-slate-400 uppercase">LRS Endpoint</p>
                <p className="text-xs truncate">{status.lrs_endpoint}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {message && (
        <div className={`p-3 rounded-lg text-sm ${
          message.type === 'success' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
            : 'bg-rose-50 text-rose-700 border border-rose-200'
        }`}>
          {message.text}
        </div>
      )}

      {/* LRS connection form */}
      <div className="bg-white rounded-xl border border-dash-border p-5">
        <h3 className="text-sm font-semibold text-slate-700 mb-4">Connect to LRS</h3>
        <form onSubmit={handleConnect} className="space-y-3">
          <div>
            <label className="block text-xs font-medium text-slate-600 mb-1">LRS Endpoint</label>
            <input
              type="url"
              placeholder="https://lrs.example.com/xapi/"
              value={form.endpoint}
              onChange={(e) => setForm({ ...form, endpoint: e.target.value })}
              className="w-full px-3 py-2 text-sm border border-dash-border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500/30"
              required
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Username / Key</label>
              <input
                type="text"
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-dash-border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500/30"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Password / Secret</label>
              <input
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-dash-border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500/30"
                required
              />
            </div>
          </div>
          <button
            type="submit"
            disabled={connecting}
            className="px-4 py-2 bg-teal-600 text-white text-sm rounded-lg hover:bg-teal-700 disabled:opacity-50 transition-colors"
          >
            {connecting ? 'Connecting…' : 'Connect & Sync'}
          </button>
        </form>
      </div>

      {/* alternative data sources */}
      <div className="bg-white rounded-xl border border-dash-border p-5">
        <h3 className="text-sm font-semibold text-slate-700 mb-4">Alternative Data Sources</h3>
        <div className="flex gap-3">
          <button
            onClick={handleLoadDemo}
            disabled={connecting}
            className="px-4 py-2 bg-slate-800 text-white text-sm rounded-lg hover:bg-slate-900 disabled:opacity-50 transition-colors"
          >
            Load Demo Data
          </button>
          <label className="px-4 py-2 border border-dash-border text-sm rounded-lg cursor-pointer hover:bg-slate-50 transition-colors">
            Upload JSON
            <input type="file" accept=".json" onChange={handleUpload} className="hidden" />
          </label>
        </div>
        <p className="text-xs text-slate-400 mt-2">
          Demo mode loads 10,000 sample xAPI statements with realistic learner patterns.
        </p>
      </div>
    </div>
  )
}
