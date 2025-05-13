// src/pages/RegisterPatient.jsx
import React, { useState } from 'react'

function RegisterPatient() {
  const [form, setForm] = useState({
    last_name: '',
    first_name: '',
    patronymic: '',
    gender: '',
    date_of_birth: '',
    address: '',
    phone: '',
    insurance_policy: '',
    email: '',
  })

  const token = localStorage.getItem('token')

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch('http://localhost:8000/register/patient', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(form),
      })

      if (res.ok) {
        alert('Пациент успешно зарегистрирован')
        setForm({
          last_name: '',
          first_name: '',
          patronymic: '',
          gender: '',
          date_of_birth: '',
          address: '',
          phone: '',
          insurance_policy: '',
          email: '',
        })
      } else {
        const err = await res.json()
        alert(err.detail || 'Ошибка регистрации пациента')
      }
    } catch (error) {
      alert('Ошибка подключения к серверу')
      console.error(error)
    }
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 bg-white p-6 sm:p-8 rounded-2xl shadow">
      <h2 className="text-2xl sm:text-3xl font-bold mb-6 text-center text-blue-800">Регистрация пациента</h2>
      <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <input name="last_name" value={form.last_name} onChange={handleChange} placeholder="Фамилия" className="input" />
        <input name="first_name" value={form.first_name} onChange={handleChange} placeholder="Имя" className="input" />
        <input name="patronymic" value={form.patronymic} onChange={handleChange} placeholder="Отчество" className="input" />
        <input name="gender" value={form.gender} onChange={handleChange} placeholder="Пол (м/ж)" className="input" />
        <input name="date_of_birth" value={form.date_of_birth} onChange={handleChange} placeholder="Дата рождения (ДД.ММ.ГГГГ)" className="input" />
        <input name="address" value={form.address} onChange={handleChange} placeholder="Адрес" className="input col-span-1 sm:col-span-2" />
        <input name="phone" value={form.phone} onChange={handleChange} placeholder="Телефон" className="input" />
        <input name="insurance_policy" value={form.insurance_policy} onChange={handleChange} placeholder="Полис ОМС" className="input" />
        <input name="email" value={form.email} onChange={handleChange} placeholder="Email" className="input col-span-1 sm:col-span-2" />
        <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white py-2 rounded col-span-1 sm:col-span-2">
          Зарегистрировать пациента
        </button>
      </form>
    </div>
  )
}

export default RegisterPatient
