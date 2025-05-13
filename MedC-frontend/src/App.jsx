// src/App.jsx
import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import Dashboard from './pages/Dashboard'
import RegisterPatient from './pages/RegisterPatient'
import RegisterAppointment from './pages/RegisterAppointment'
import RegisterDoctor from './pages/RegisterDoctor'
import Medications from './pages/Medications'
import Pharmacy from './pages/Pharmacy'
import Archive from './pages/Archive'
import SearchAppointments from './pages/SearchAppointments'
import ProtectedRoute from './components/ProtectedRoute'
import ManageAppointments from './pages/ManageAppointments'
import PatientDocuments from './pages/PatientDocuments'
import MedicationDetails from './pages/MedicationDetails'
import AddDiagnosis from './pages/AddDiagnosis'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* 🔐 Защищённые страницы */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Layout><Dashboard /></Layout>
          </ProtectedRoute>
        } />

        <Route path="/register-appointment" element={
          <ProtectedRoute>
            <Layout><RegisterAppointment /></Layout>
          </ProtectedRoute>
        } />

        {/* 🟢 Остальные публичные или пока незащищённые */}
        <Route path="/register-patient" element={<Layout><RegisterPatient /></Layout>} />
        <Route path="/register-doctor" element={<Layout><RegisterDoctor /></Layout>} />
        <Route path="/medications" element={<Layout><Medications /></Layout>} />
        <Route path="/pharmacy" element={<Layout><Pharmacy /></Layout>} />
        <Route path="/archive" element={<Layout><Archive /></Layout>} />
        <Route path="/search-appointments" element={<Layout><SearchAppointments /></Layout>} />
        <Route path="/manage-appointments" element={<Layout><ManageAppointments /></Layout>} />
        <Route path="/patient-documents" element={<Layout><PatientDocuments /></Layout>} />
        <Route path="/medication-details" element={<Layout><MedicationDetails /></Layout>} />
        <Route path="/add-diagnosis" element={<Layout><AddDiagnosis /></Layout>} />

        {/* 🔁 Редирект на логин по умолчанию */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  )
}

export default App
