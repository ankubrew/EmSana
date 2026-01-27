import { useState } from "react"
import { Link } from "react-router-dom"

export default function SignUp() {
  const [formData, setFormData] = useState({
    email: "",
    first_name: "",
    last_name: "",
    iin: "",
    role: "",
    password: "",
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  return (
    <div className="w-full max-w-md">
      <h1 className="text-2xl font-semibold mb-6">
        Зарегистрироваться
      </h1>

      {/* Email */}
      <input
        className="input"
        type="email"
        name="email"
        placeholder="Email"
        value={formData.email}
        onChange={handleChange}
      />

      {/* First Name */}
      <input
        className="input"
        type="text"
        name="first_name"
        placeholder="First name"
        value={formData.first_name}
        onChange={handleChange}
      />

      {/* Last Name */}
      <input
        className="input"
        type="text"
        name="last_name"
        placeholder="Last name"
        value={formData.last_name}
        onChange={handleChange}
      />

      {/* IIN */}
      <input
        className="input"
        type="text"
        name="iin"
        placeholder="IIN"
        value={formData.iin}
        onChange={handleChange}
        maxLength={12}
      />

      {/* Role */}
      <select
        className="input"
        name="role"
        value={formData.role}
        onChange={handleChange}
      >
        <option value="">Select role</option>
        <option value="patient">Patient</option>
        <option value="doctor">Doctor</option>
      </select>

      {/* Password */}
      <input
        className="input"
        type="password"
        name="password"
        placeholder="Password"
        value={formData.password}
        onChange={handleChange}
      />

      <button className="btn-primary mt-2">
        Sign up
      </button>

      <p className="text-sm mt-6">
        Already have an account?{" "}
        <Link to="/login" className="text-blue-600">
          Log in
        </Link>
      </p>
    </div>
  )
}
