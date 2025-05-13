// src/components/ProtectedRoute.jsx
import React from 'react'
import { Navigate } from 'react-router-dom'

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')

  const isAuthenticated = Boolean(token && role)

  return isAuthenticated ? children : <Navigate to="/login" replace />
}

export default ProtectedRoute
