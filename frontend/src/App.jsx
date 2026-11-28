import { Routes, Route, Navigate } from 'react-router-dom'
import Register from './pages/Register'

function LoginPlaceholder() {
  return (
    <div className='min-h-screen bg-slate-950 text-white flex items-center justify-center'>
      <p>
        Login page is coming next.
      </p>
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/register" replace />} />
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<LoginPlaceholder />} />
      <Route path="*" element={<Navigate to="/register" replace />} />
    </Routes>
  )
}

export default App