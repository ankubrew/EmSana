import { Outlet } from 'react-router-dom'
import illustration from '../assets/emsana-illustration.png'

export default function AuthLayout() {
  return (
    <div className="min-h-screen flex bg-gray-50">
      
      {/* Левая часть — форма */}
      <div className="w-full md:w-1/2 flex items-center justify-center p-10">
        <Outlet />
      </div>

      {/* Правая часть — иллюстрация */}
      <div className="hidden md:flex w-1/2 items-center justify-center bg-white">
        <img
          src={illustration}
          alt="EmSana"
          className="max-w-lg"
        />
      </div>

    </div>
  )
}
