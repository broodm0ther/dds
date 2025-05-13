import React from 'react'

function Dashboard() {
  const username = localStorage.getItem('username') || 'Пользователь'

  return (
    <div className="max-w-3xl mx-auto mt-10 bg-white p-6 sm:p-8 rounded-2xl shadow">
      <h1 className="text-3xl font-bold text-blue-800 mb-6 text-center">
        Добро пожаловать, {username}!
      </h1>

      <div className="grid sm:grid-cols-2 gap-4">
        <div className="bg-blue-100 rounded-xl p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-blue-800 mb-1">Пациенты и приёмы</h2>
          <p className="text-sm text-gray-700">Управляйте пациентами, назначениями и медицинскими документами.</p>
        </div>

        <div className="bg-green-100 rounded-xl p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-green-800 mb-1">Медикаменты и назначения</h2>
          <p className="text-sm text-gray-700">Просматривайте назначения, диагнозы и аптечные остатки.</p>
        </div>

        <div className="bg-yellow-100 rounded-xl p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-yellow-800 mb-1">Администрирование</h2>
          <p className="text-sm text-gray-700">Управление ролями, тестированием и аудитом действий.</p>
        </div>

        <div className="bg-purple-100 rounded-xl p-4 shadow-sm">
          <h2 className="text-lg font-semibold text-purple-800 mb-1">Интеллектуальный помощник</h2>
          <p className="text-sm text-gray-700">Работайте с AI для интерпретации текстов, PDF и рекомендаций.</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
