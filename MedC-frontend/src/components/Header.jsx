import React, { useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { useAuth } from '../context/authcontext'

const Header = () => {
  const { token, role, logout } = useAuth()
  const [mobileOpen, setMobileOpen] = useState(false)

  const navItems = [
    { to: '/dashboard', label: 'Главная' },
    { to: '/register-patient', label: 'Пациенты' },
    { to: '/register-appointment', label: 'Приёмы' },
    { to: '/medications', label: 'Медикаменты' },
  ]

  return (
    <header className="bg-blue-700 text-white px-4 py-3 shadow-md">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="text-2xl font-bold">MedC</div>

        {/* Desktop Navigation */}
        {token && (
          <nav className="hidden md:flex gap-6 text-sm">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `hover:underline hover:text-blue-200 transition ${
                    isActive ? 'font-bold underline' : ''
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        )}

        {/* Mobile burger button */}
        <div className="md:hidden">
          <button onClick={() => setMobileOpen(!mobileOpen)}>
            <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              {mobileOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile nav menu */}
      {mobileOpen && token && (
        <div className="md:hidden mt-2 flex flex-col gap-2 text-sm px-2">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={() => setMobileOpen(false)}
              className={({ isActive }) =>
                `block px-2 py-1 rounded hover:bg-blue-600 transition ${
                  isActive ? 'bg-blue-800 font-semibold' : ''
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>
      )}

      {/* Session Info (desktop only) */}
      <div className="hidden md:flex justify-end items-center mt-2 gap-4 text-sm">
        {token ? (
          <>
            <span>Роль: <strong>{role}</strong></span>
            <button
              onClick={logout}
              className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded text-white"
            >
              Выйти
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="underline">Войти</Link>
            <Link to="/register" className="underline">Регистрация</Link>
          </>
        )}
      </div>
    </header>
  )
}

export default Header
