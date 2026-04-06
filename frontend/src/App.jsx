import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import Overview from './pages/Overview'
import Learners from './pages/Learners'
import LearnerDetail from './pages/LearnerDetail'
import Courses from './pages/Courses'
import CourseDetail from './pages/CourseDetail'
import SkillMap from './pages/SkillMap'
import Engagement from './pages/Engagement'
import Settings from './pages/Settings'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Overview />} />
        <Route path="/learners" element={<Learners />} />
        <Route path="/learners/:email" element={<LearnerDetail />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/courses/:courseId" element={<CourseDetail />} />
        <Route path="/skills" element={<SkillMap />} />
        <Route path="/engagement" element={<Engagement />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Layout>
  )
}
