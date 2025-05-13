// src/pages/PatientDocuments.jsx
import React, { useEffect, useState } from 'react'

function PatientDocuments() {
  const [patientId, setPatientId] = useState('')
  const [documents, setDocuments] = useState([])
  const [file, setFile] = useState(null)
  const [category, setCategory] = useState('')
  const token = localStorage.getItem('token')

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file || !patientId) {
      alert('Заполните все поля и выберите файл')
      return
    }

    const formData = new FormData()
    formData.append('file', file)
    formData.append('patient_id', patientId)
    formData.append('category', category)

    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      })

      if (res.ok) {
        alert('Файл успешно загружен')
        setFile(null)
        setCategory('')
        fetchDocuments()
      } else {
        alert('Ошибка при загрузке файла')
      }
    } catch (err) {
      console.error('Ошибка сервера:', err)
    }
  }

  const fetchDocuments = async () => {
    if (!patientId) return
    try {
      const res = await fetch(`http://localhost:8000/patient/${patientId}/documents`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await res.json()
      setDocuments(data)
    } catch (err) {
      console.error('Ошибка загрузки документов:', err)
    }
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 bg-white p-6 sm:p-8 rounded-2xl shadow">
      <h2 className="text-2xl font-bold mb-6 text-center text-blue-800">Документы пациента</h2>

      <form onSubmit={handleUpload} className="space-y-4 mb-6">
        <input
          className="w-full border p-2 rounded"
          placeholder="ID пациента"
          value={patientId}
          onChange={(e) => setPatientId(e.target.value)}
        />
        <input
          className="w-full border p-2 rounded"
          placeholder="Категория документа (например, анализ)"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="w-full border rounded p-2"
        />
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Загрузить документ
        </button>
      </form>

      <h3 className="text-lg font-semibold mb-2 text-gray-800">Загруженные документы:</h3>
      {documents.length === 0 ? (
        <p className="text-sm text-gray-500">Документы не найдены.</p>
      ) : (
        <ul className="list-disc pl-6 text-sm space-y-1">
          {documents.map((doc) => (
            <li key={doc.id}>
              <span className="font-medium">{doc.upload_date?.split('T')[0]}</span> — {doc.original_name} [{doc.category}]
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default PatientDocuments
