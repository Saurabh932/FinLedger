
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { Link } from 'react-router-dom'
import { Wallet, LoaderCircle } from 'lucide-react'

import { registerUser } from '../services/auth.service'

// 1. Define the frontend validation rules
const registerSchema = z.object({
  full_name: z
    .string()
    .trim()
    .min(2, 'Name must contain at least 2 characters')
    .max(100, 'Name cannot exceed 100 characters'),

  email: z
    .string()
    .trim()
    .email('Enter a valid email address'),

  password: z
    .string()
    .min(8, 'Password must contain at least 8 characters')
    .max(128, 'Password is too long'),
})

export default function Register() {
  const [serverError, setServerError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')

  // 2. Initialize form handling and validation
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      full_name: '',
      email: '',
      password: '',
    },
  })

  // 3. Execute after frontend validation succeeds
  const onSubmit = async (formData) => {
    setServerError('')
    setSuccessMessage('')

    try {
      await registerUser(formData)

      setSuccessMessage(
        'Your account has been created successfully!'
      )

      reset()
    } catch (error) {
      const message =
        error.response?.data?.detail ||
        'Unable to create your account. Please try again.'

      setServerError(message)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-md">

        {/* Brand */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-600">
            <Wallet size={28} />
          </div>

          <h1 className="text-3xl font-bold tracking-tight">
            FinLedger
          </h1>

          <p className="mt-2 text-sm text-slate-400">
            Create your financial management account
          </p>
        </div>

        {/* Registration form */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-7 shadow-xl">

          <h2 className="text-xl font-semibold">
            Create an account
          </h2>

          <p className="mt-1 mb-6 text-sm text-slate-400">
            Enter your details to get started.
          </p>

          {serverError && (
            <div
              role="alert"
              className="mb-5 rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300"
            >
              {serverError}
            </div>
          )}

          {successMessage && (
            <div
              role="status"
              className="mb-5 rounded-lg border border-green-500/30 bg-green-500/10 p-3 text-sm text-green-300"
            >
              {successMessage}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">

            {/* Full name */}
            <div>
              <label htmlFor="full_name" className="mb-2 block text-sm font-medium">
                Full name
              </label>

              <input
                id="full_name"
                type="text"
                autoComplete="name"
                placeholder="John Doe"
                {...register('full_name')}
                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none transition focus:border-blue-500"
              />

              {errors.full_name && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.full_name.message}
                </p>
              )}
            </div>

            {/* Email */}
            <div>
              <label htmlFor="email" className="mb-2 block text-sm font-medium">
                Email address
              </label>

              <input
                id="email"
                type="email"
                autoComplete="email"
                placeholder="john@example.com"
                {...register('email')}
                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none transition focus:border-blue-500"
              />

              {errors.email && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.email.message}
                </p>
              )}
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="mb-2 block text-sm font-medium">
                Password
              </label>

              <input
                id="password"
                type="password"
                autoComplete="new-password"
                placeholder="At least 8 characters"
                {...register('password')}
                className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none transition focus:border-blue-500"
              />

              {errors.password && (
                <p className="mt-1 text-xs text-red-400">
                  {errors.password.message}
                </p>
              )}
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-3 text-sm font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSubmitting && (
                <LoaderCircle size={18} className="animate-spin" />
              )}

              {isSubmitting ? 'Creating account...' : 'Create account'}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-slate-400">
            Already have an account?{' '}
            <Link
              to="/login"
              className="font-medium text-blue-400 hover:text-blue-300"
            >
              Sign in
            </Link>
          </p>
        </div>

        <p className="mt-6 text-center text-xs text-slate-500">
          FinLedger · Secure financial management
        </p>
      </div>
    </div>
  )
}
