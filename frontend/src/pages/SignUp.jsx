import { Link } from 'react-router-dom'

export default function SignUp() {
  return (
    <div className="w-full max-w-md">
      <h1 className="text-2xl font-semibold mb-6">
        Зарегистрироваться как пациент
      </h1>

      <input className="input" placeholder="Email" />
      <input className="input" placeholder="Пароль" />
      <input className="input" placeholder="Повторите пароль" />

      <button className="btn-primary">
        Sign up
      </button>

      <p className="text-sm mt-6">
        Already have an account?{' '}
        <Link to="/login" className="text-blue-600">
          Log in
        </Link>
      </p>
    </div>
  )
}
