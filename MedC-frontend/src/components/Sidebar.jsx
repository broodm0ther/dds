// src/components/Sidebar.jsx
import React from 'react'
import { NavLink } from 'react-router-dom'

const Sidebar = ({ token, menuOpen, setMenuOpen }) => {
  const links = [
    { to: '/dashboard', label: 'Главная' },
    { to: '/register-patient', label: 'Пациенты' },
    { to: '/register-doctor', label: 'Врачи' },
    { to: '/register-appointment', label: 'Приёмы' },
    { to: '/medications', label: 'Назначения' },
    { to: '/pharmacy', label: 'Аптека' },
    { to: '/archive', label: 'Архив' },
    { to: '/documents', label: 'Документы' },
    { to: '/search-appointments', label: 'Поиск' },
    { to: '/manage-appointments', label: 'Управление' },
    { to: '/add-diagnosis', label: 'Диагноз' },
    { to: '/medication-details', label: 'Детали' },
  ]

  return (
    <aside className={`bg-white shadow-md md:w-64 ${menuOpen ? 'block' : 'hidden'} md:block`}>
      <nav className="p-4 space-y-1 text-sm">
        {token ? (
          links.map(link => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `block px-3 py-2 rounded hover:bg-blue-100 transition-all ${
                  isActive ? 'bg-blue-200 font-semibold' : ''
                }`
              }
              onClick={() => setMenuOpen(false)}
            >
              {link.label}
            </NavLink>
          ))
        ) : (
          <p className="text-gray-500">Войдите, чтобы увидеть меню</p>
        )}
      </nav>
    </aside>
  )
}

export default Sidebar
