// src/pages/AddDiagnosis.jsx
import React, { useState } from 'react'

function AddDiagnosis() {
  const [appointmentId, setAppointmentId] = useState('')
  const [diagnosis, setDiagnosis] = useState('')
  const [recommendations, setRecommendations] = useState('')
  const token = localStorage.getItem('token')

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      const res = await fetch(`http://localhost:8000/appointments/${appointmentId}/diagnosis`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ diagnosis, recommendations }),
      })

      if (res.ok) {
        alert('Диагноз и рекомендации сохранены')
        setAppointmentId('')
        setDiagnosis('')
        setRecommendations('')
      } else {
        const err = await res.json()
        alert(err.detail || 'Ошибка сохранения')
      }
    } catch (err) {
      console.error(err)
      alert('Ошибка сервера')
    }
  }

  return (
    <div className="max-w-xl mx-auto mt-10 bg-white p-6 sm:p-8 rounded-2xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-center text-blue-800">
        Добавление диагноза и рекомендаций
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="appointmentId"
          value={appointmentId}
          onChange={(e) => setAppointmentId(e.target.value)}
          placeholder="ID приёма"
          className="w-full border p-2 rounded"
        />
        <textarea
          name="diagnosis"
          value={diagnosis}
          onChange={(e) => setDiagnosis(e.target.value)}
          placeholder="Диагноз"
          className="w-full border p-2 rounded min-h-[100px]"
        />
        <textarea
          name="recommendations"
          value={recommendations}
          onChange={(e) => setRecommendations(e.target.value)}
          placeholder="Рекомендации"
          className="w-full border p-2 rounded min-h-[100px]"
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Сохранить
        </button>
      </form>
    </div>
  )
}

export default AddDiagnosis
