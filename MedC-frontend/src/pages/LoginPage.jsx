// src/pages/LoginPage.jsx
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const handleLogin = async () => {
    try {
      const res = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username, password }),
      })
      const data = await res.json()
      if (res.ok) {
        localStorage.setItem('token', data.access_token)
        localStorage.setItem('role', data.role)
        navigate('/dashboard')
      } else {
        alert(data.detail || 'Ошибка входа')
      }
    } catch (err) {
      console.error(err)
      alert('Ошибка сервера')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="bg-white p-6 sm:p-8 rounded-lg shadow max-w-md w-full">
        <h2 className="text-2xl font-bold text-center mb-6">Вход в систему</h2>
        <input
          className="w-full border p-2 rounded mb-4"
          placeholder="Логин"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          className="w-full border p-2 rounded mb-4"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded"
        >
          Войти
        </button>
      </div>
    </div>
  )
}

export default LoginPage
