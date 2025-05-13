// src/pages/Pharmacy.jsx
import React, { useEffect, useState } from 'react'

function Pharmacy() {
  const [drugs, setDrugs] = useState([])
  const token = localStorage.getItem('token')

  useEffect(() => {
    fetchPharmacy()
  }, [])

  const fetchPharmacy = async () => {
    try {
      const res = await fetch('http://localhost:8000/pharmacy', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      const data = await res.json()
      setDrugs(data)
    } catch (err) {
      console.error('Ошибка загрузки данных аптеки:', err)
    }
  }

  return (
    <div className="max-w-6xl mx-auto mt-10 p-4 bg-white rounded-2xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-center text-blue-800">Аптечный склад</h2>

      <div className="overflow-x-auto">
        <table className="w-full text-sm border">
          <thead className="bg-gray-100 text-left">
            <tr>
              <th className="p-2 border">Название</th>
              <th className="p-2 border">Дозировка</th>
              <th className="p-2 border">Инструкция</th>
              <th className="p-2 border">Остаток</th>
              <th className="p-2 border">Срок годности</th>
            </tr>
          </thead>
          <tbody>
            {drugs.map((drug) => (
              <tr key={drug.id} className="hover:bg-gray-50">
                <td className="p-2 border">{drug.name}</td>
                <td className="p-2 border">{drug.dosage}</td>
                <td className="p-2 border">{drug.instruction || '—'}</td>
                <td className="p-2 border">{drug.quantity}</td>
                <td className="p-2 border">{drug.expiration_date || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Pharmacy
