// src/pages/RegisterPage.jsx
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function RegisterPage() {
  const [form, setForm] = useState({
    username: '',
    password: '',
    role: 'doctor',
  })
  const navigate = useNavigate()

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch('http://localhost:8000/register_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      if (res.ok) {
        alert('Пользователь создан! Войдите.')
        navigate('/login')
      } else {
        const err = await res.json()
        alert(err.detail || 'Ошибка регистрации')
      }
    } catch (err) {
      console.error(err)
      alert('Ошибка сервера')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="bg-white p-6 sm:p-8 rounded-lg shadow max-w-md w-full">
        <h2 className="text-2xl font-bold text-center mb-6">Регистрация</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            name="username"
            value={form.username}
            onChange={handleChange}
            placeholder="Логин"
            className="w-full border p-2 rounded"
          />
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            placeholder="Пароль"
            className="w-full border p-2 rounded"
          />
          <select name="role" value={form.role} onChange={handleChange} className="w-full border p-2 rounded">
            <option value="admin">Администратор</option>
            <option value="doctor">Врач</option>
            <option value="registrar">Регистратор</option>
          </select>
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded"
          >
            Зарегистрироваться
          </button>
        </form>
      </div>
    </div>
  )
}

export default RegisterPage
