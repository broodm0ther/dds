// src/pages/RegisterAppointment.jsx
import React, { useState, useEffect } from 'react'

function RegisterAppointment() {
  const [form, setForm] = useState({
    patient_id: '',
    doctor_id: '',
    service: '',
    appointment_day: '',
    appointment_time: '',
  })

  const [patients, setPatients] = useState([])
  const [doctors, setDoctors] = useState([])

  const token = localStorage.getItem('token')

  useEffect(() => {
    fetchAll('http://localhost:8000/api/patients', setPatients)
    fetchAll('http://localhost:8000/api/doctors', setDoctors)
  }, [])

  const fetchAll = async (url, setter) => {
    try {
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await res.json()
      setter(data)
    } catch (err) {
      console.error('Ошибка загрузки:', err)
    }
  }

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch('http://localhost:8000/register/appointment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(form),
      })

      if (res.ok) {
        alert('Приём успешно создан')
        setForm({
          patient_id: '',
          doctor_id: '',
          service: '',
          appointment_day: '',
          appointment_time: '',
        })
      } else {
        const err = await res.json()
        alert(err.detail || 'Ошибка при создании приёма')
      }
    } catch (err) {
      console.error(err)
      alert('Ошибка подключения к серверу')
    }
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 bg-white p-6 sm:p-8 rounded-2xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-center text-blue-800">Создание приёма</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1 text-sm text-gray-600">Пациент</label>
          <select
            name="patient_id"
            value={form.patient_id}
            onChange={handleChange}
            className="w-full border p-2 rounded"
          >
            <option value="">Выберите пациента</option>
            {patients.map((p) => (
              <option key={p.id} value={p.id}>
                {p.last_name} {p.first_name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block mb-1 text-sm text-gray-600">Врач</label>
          <select
            name="doctor_id"
            value={form.doctor_id}
            onChange={handleChange}
            className="w-full border p-2 rounded"
          >
            <option value="">Выберите врача</option>
            {doctors.map((d) => (
              <option key={d.id} value={d.id}>
                {d.last_name} {d.first_name}
              </option>
            ))}
          </select>
        </div>

        <input
          name="service"
          value={form.service}
          onChange={handleChange}
          placeholder="Услуга"
          className="w-full border p-2 rounded"
        />

        <input
          name="appointment_day"
          value={form.appointment_day}
          onChange={handleChange}
          placeholder="Дата приёма (ГГГГ-ММ-ДД)"
          className="w-full border p-2 rounded"
        />

        <input
          name="appointment_time"
          value={form.appointment_time}
          onChange={handleChange}
          placeholder="Время (например, 14:30)"
          className="w-full border p-2 rounded"
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Назначить приём
        </button>
      </form>
    </div>
  )
}

export default RegisterAppointment
