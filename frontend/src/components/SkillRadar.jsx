import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis,
  PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip,
} from 'recharts'

export default function SkillRadar({ skills, cohortAvg }) {
  if (!skills || skills.length === 0) return null

  const chartData = skills.map((s) => ({
    skill: s.skill,
    score: Math.round(s.score * 100),
    cohort: cohortAvg?.[s.skill] ? Math.round(cohortAvg[s.skill] * 100) : 0,
  }))

  return (
    <div className="bg-white rounded-xl border border-dash-border p-5">
      <h3 className="text-sm font-semibold text-slate-700 mb-2">Skill Profile</h3>
      <ResponsiveContainer width="100%" height={320}>
        <RadarChart data={chartData} outerRadius="70%">
          <PolarGrid stroke="#e2e8f0" />
          <PolarAngleAxis dataKey="skill" tick={{ fontSize: 11 }} />
          <PolarRadiusAxis domain={[0, 100]} tick={{ fontSize: 10 }} />
          <Radar
            name="Learner"
            dataKey="score"
            stroke="#14b8a6"
            fill="#14b8a6"
            fillOpacity={0.25}
            strokeWidth={2}
          />
          {cohortAvg && (
            <Radar
              name="Cohort Avg"
              dataKey="cohort"
              stroke="#8b5cf6"
              fill="#8b5cf6"
              fillOpacity={0.1}
              strokeWidth={1.5}
              strokeDasharray="4 3"
            />
          )}
          <Legend iconSize={10} wrapperStyle={{ fontSize: 12 }} />
          <Tooltip contentStyle={{ borderRadius: 8, fontSize: 12 }} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}
