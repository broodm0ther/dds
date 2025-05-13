// src/components/Layout.jsx
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Header from './Header'
import Sidebar from './Sidebar'
import Footer from './Footer'

function Layout({ children }) {
  const [menuOpen, setMenuOpen] = useState(false)
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')
  const navigate = useNavigate()

  const logout = () => {
    localStorage.clear()
    navigate('/login')
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-100 text-gray-800">
      <Header token={token} role={role} onLogout={logout} toggleMenu={() => setMenuOpen(!menuOpen)} />

      <div className="md:flex flex-1">
        <Sidebar token={token} menuOpen={menuOpen} setMenuOpen={setMenuOpen} />
        <main className="flex-1 p-4 overflow-y-auto">{children}</main>
      </div>

      <Footer token={token} role={role} onLogout={logout} />
    </div>
  )
}

export default Layout
