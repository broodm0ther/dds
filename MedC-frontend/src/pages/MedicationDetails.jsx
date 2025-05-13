// src/pages/MedicationDetails.jsx
import React, { useState } from 'react'

function MedicationDetails() {
  const [appointmentId, setAppointmentId] = useState('')
  const [details, setDetails] = useState(null)
  const token = localStorage.getItem('token')

  const fetchDetails = async () => {
    if (!appointmentId) return

    try {
      const res = await fetch(`http://localhost:8000/appointments/${appointmentId}/details`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await res.json()
      setDetails(data)
    } catch (err) {
      console.error('Ошибка загрузки деталей приёма:', err)
    }
  }

  return (
    <div className="max-w-3xl mx-auto mt-10 p-6 bg-white rounded-2xl shadow">
      <h2 className="text-2xl font-bold text-blue-800 mb-4 text-center">Детали приёма и назначений</h2>

      <div className="flex gap-2 mb-6">
        <input
          className="w-full border p-2 rounded"
          placeholder="ID приёма"
          value={appointmentId}
          onChange={(e) => setAppointmentId(e.target.value)}
        />
        <button
          onClick={fetchDetails}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Показать
        </button>
      </div>

      {details && (
        <div className="space-y-3 text-sm text-gray-700">
          <div><strong>Пациент:</strong> {details.patient?.last_name} {details.patient?.first_name}</div>
          <div><strong>Врач:</strong> {details.doctor?.last_name} {details.doctor?.first_name}</div>
          <div><strong>Дата:</strong> {details.appointment_day}</div>
          <div><strong>Время:</strong> {details.appointment_time}</div>
          <div><strong>Услуга:</strong> {details.service}</div>
          <div><strong>Диагноз:</strong> {details.diagnosis || '—'}</div>
          <div><strong>Рекомендации:</strong> {details.recommendations || '—'}</div>
          <div className="pt-2"><strong>Назначения:</strong></div>
          <ul className="list-disc pl-5">
            {details.medications?.length > 0 ? (
              details.medications.map((m, i) => (
                <li key={i}>
                  {m.pharmacy_drug?.name} — {m.dosage}
                </li>
              ))
            ) : (
              <li>Нет назначений</li>
            )}
          </ul>
        </div>
      )}
    </div>
  )
}

export default MedicationDetails
