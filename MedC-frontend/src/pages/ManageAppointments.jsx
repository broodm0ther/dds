// src/pages/ManageAppointments.jsx
import React, { useEffect, useState } from 'react'

function ManageAppointments() {
  const [appointments, setAppointments] = useState([])
  const token = localStorage.getItem('token')

  useEffect(() => {
    fetchAppointments()
  }, [])

  const fetchAppointments = async () => {
    try {
      const res = await fetch('http://localhost:8000/appointments', {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await res.json()
      setAppointments(data)
    } catch (err) {
      console.error('Ошибка при загрузке приёмов:', err)
    }
  }

  const updateStatus = async (id, newStatus) => {
    const reason = prompt('Укажите причину изменения статуса:')
    if (!reason) return

    try {
      const res = await fetch(`http://localhost:8000/appointments/${id}/status`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ new_status: newStatus, reason }),
      })

      if (res.ok) {
        fetchAppointments()
        alert('Статус обновлён')
      } else {
        alert('Ошибка обновления статуса')
      }
    } catch (err) {
      console.error(err)
      alert('Ошибка сервера')
    }
  }

  return (
    <div className="max-w-6xl mx-auto mt-10 p-4 bg-white rounded-2xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-center text-blue-800">Управление приёмами</h2>

      <div className="overflow-x-auto">
        <table className="w-full text-sm border">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-2 border">Пациент</th>
              <th className="p-2 border">Врач</th>
              <th className="p-2 border">Дата</th>
              <th className="p-2 border">Время</th>
              <th className="p-2 border">Статус</th>
              <th className="p-2 border">Действия</th>
            </tr>
          </thead>
          <tbody>
            {appointments.map((a) => (
              <tr key={a.id} className="hover:bg-gray-50">
                <td className="p-2 border">{a.patient?.last_name} {a.patient?.first_name}</td>
                <td className="p-2 border">{a.doctor?.last_name}</td>
                <td className="p-2 border">{a.appointment_day}</td>
                <td className="p-2 border">{a.appointment_time}</td>
                <td className="p-2 border">{a.status}</td>
                <td className="p-2 border space-x-2">
                  <button
                    onClick={() => updateStatus(a.id, 'Завершён')}
                    className="text-green-600 hover:underline"
                  >
                    Завершить
                  </button>
                  <button
                    onClick={() => updateStatus(a.id, 'Отменён')}
                    className="text-red-600 hover:underline"
                  >
                    Отменить
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default ManageAppointments
