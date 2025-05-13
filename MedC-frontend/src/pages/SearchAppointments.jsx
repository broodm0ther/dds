// src/pages/SearchAppointments.jsx
import React, { useState } from 'react'

function SearchAppointments() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const token = localStorage.getItem('token')

  const handleSearch = async () => {
    if (!query) return

    try {
      const res = await fetch(`http://localhost:8000/appointments/search?q=${encodeURIComponent(query)}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      const data = await res.json()
      setResults(data)
    } catch (err) {
      console.error('Ошибка при поиске приёмов:', err)
    }
  }

  return (
    <div className="max-w-5xl mx-auto mt-10 p-6 bg-white rounded-2xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-center text-blue-800">Поиск приёмов</h2>

      <div className="flex flex-col sm:flex-row gap-2 mb-6">
        <input
          className="w-full border p-2 rounded"
          placeholder="Введите фамилию пациента или врача"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          onClick={handleSearch}
        >
          Искать
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm border">
          <thead className="bg-gray-100 text-left">
            <tr>
              <th className="p-2 border">Пациент</th>
              <th className="p-2 border">Врач</th>
              <th className="p-2 border">Услуга</th>
              <th className="p-2 border">Дата</th>
              <th className="p-2 border">Время</th>
              <th className="p-2 border">Статус</th>
            </tr>
          </thead>
          <tbody>
            {results.map((a) => (
              <tr key={a.id} className="hover:bg-gray-50">
                <td className="p-2 border">{a.patient?.last_name} {a.patient?.first_name}</td>
                <td className="p-2 border">{a.doctor?.last_name}</td>
                <td className="p-2 border">{a.service}</td>
                <td className="p-2 border">{a.appointment_day}</td>
                <td className="p-2 border">{a.appointment_time}</td>
                <td className="p-2 border">{a.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default SearchAppointments
