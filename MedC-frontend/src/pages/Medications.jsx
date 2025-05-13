// src/pages/Medications.jsx
import React, { useEffect, useState } from 'react'

function Medications() {
  const [medications, setMedications] = useState([])
  const token = localStorage.getItem('token')

  useEffect(() => {
    fetchMedications()
  }, [])

  const fetchMedications = async () => {
    try {
      const res = await fetch('http://localhost:8000/medications', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      const data = await res.json()
      setMedications(data)
    } catch (err) {
      console.error('Ошибка при загрузке лекарств:', err)
    }
  }

  return (
    <div className="max-w-5xl mx-auto mt-10 p-4 bg-white rounded-2xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-center text-blue-800">Назначенные препараты</h2>
      <div className="overflow-x-auto">
        <table className="w-full text-sm border">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-2 border">Пациент</th>
              <th className="p-2 border">Препарат</th>
              <th className="p-2 border">Дозировка</th>
              <th className="p-2 border">Приём</th>
            </tr>
          </thead>
          <tbody>
            {medications.map((m) => (
              <tr key={m.id} className="hover:bg-gray-50">
                <td className="p-2 border">{m.patient?.last_name} {m.patient?.first_name}</td>
                <td className="p-2 border">{m.pharmacy_drug?.name || '—'}</td>
                <td className="p-2 border">{m.dosage || '—'}</td>
                <td className="p-2 border">{m.appointment_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Medications
