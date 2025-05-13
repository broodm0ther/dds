// src/pages/Archive.jsx
import React, { useEffect, useState } from 'react'

function Archive() {
  const [history, setHistory] = useState([])
  const token = localStorage.getItem('token')

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      const res = await fetch('http://localhost:8000/archive', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      const data = await res.json()
      setHistory(data)
    } catch (err) {
      console.error('Ошибка загрузки архива:', err)
    }
  }

  return (
    <div className="max-w-6xl mx-auto mt-10 p-4 bg-white rounded-2xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-center text-blue-800">Архив приёмов</h2>
      <div className="overflow-x-auto">
        <table className="w-full text-sm border">
          <thead className="bg-gray-100 text-left">
            <tr>
              <th className="p-2 border">ID Приёма</th>
              <th className="p-2 border">Старый статус</th>
              <th className="p-2 border">Новый статус</th>
              <th className="p-2 border">Причина</th>
              <th className="p-2 border">Время</th>
            </tr>
          </thead>
          <tbody>
            {history.map((entry) => (
              <tr key={entry.id} className="hover:bg-gray-50">
                <td className="p-2 border">{entry.appointment_id}</td>
                <td className="p-2 border">{entry.old_status}</td>
                <td className="p-2 border">{entry.new_status}</td>
                <td className="p-2 border">{entry.reason || '—'}</td>
                <td className="p-2 border">{new Date(entry.timestamp).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Archive
