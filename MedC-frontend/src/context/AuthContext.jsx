import React, { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [role, setRole] = useState(localStorage.getItem('role'))

  const login = (newToken, newRole) => {
    localStorage.setItem('token', newToken)
    localStorage.setItem('role', newRole)
    setToken(newToken)
    setRole(newRole)
  }

  const logout = () => {
    localStorage.clear()
    setToken(null)
    setRole(null)
  }

  useEffect(() => {
    const savedToken = localStorage.getItem('token')
    const savedRole = localStorage.getItem('role')
    if (savedToken && savedRole) {
      setToken(savedToken)
      setRole(savedRole)
    }
  }, [])

  return (
    <AuthContext.Provider value={{ token, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
