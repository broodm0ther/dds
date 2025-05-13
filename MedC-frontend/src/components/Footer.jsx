// src/components/Footer.jsx
import React from 'react'
import { Link } from 'react-router-dom'

const Footer = ({ token, role, onLogout }) => (
  <footer className="bg-gray-200 text-center py-4 border-t border-gray-300 text-sm mt-auto">
    {token ? (
      <>
        <p className="mb-2">Вы вошли как: <strong>{role}</strong></p>
        <button onClick={onLogout} className="text-red-600 underline">Выйти</button>
      </>
    ) : (
      <>
        <Link to="/login" className="mr-4 underline">Войти</Link>
        <Link to="/register" className="underline">Регистрация</Link>
      </>
    )}
    <p className="mt-2 text-gray-500">© {new Date().getFullYear()} MedC</p>
  </footer>
)

export default Footer
