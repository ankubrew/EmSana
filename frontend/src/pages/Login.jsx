import { Link } from 'react-router-dom'

export default function Login() {
  return (
    <div className="w-full max-w-md">
      <h1 className="text-2xl font-semibold mb-6">
        Вход в EmSana
      </h1>

      <input
        type="email"
        placeholder="Email"
        className="input"
      />

      <input
        type="password"
        placeholder="Пароль"
        className="input"
      />

      <button className="btn-primary">
        Log in
      </button>

      <a href="#" className="block text-sm text-blue-600 mt-4">
        Forgot password?
      </a>

      <div className="flex gap-3 mt-6">
        <button className="btn-social">Google</button>
        <button className="btn-social">Facebook</button>
      </div>

      <p className="text-sm mt-6">
        Don’t have an account?{' '}
        <Link to="/signup" className="text-blue-600">
          Sign up
        </Link>
      </p>
    </div>
  )
}
