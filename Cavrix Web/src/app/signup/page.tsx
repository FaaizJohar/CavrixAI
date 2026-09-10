import { signup } from '../auth/actions'

export default function SignupPage({ searchParams }: { searchParams: { error?: string } }) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-950 p-4">
      <div className="w-full max-w-md bg-gray-900 border border-gray-800 rounded-xl p-8 shadow-2xl">
        <h1 className="text-2xl font-mono text-teal-400 font-bold mb-6 text-center tracking-widest">
          CAVRIX REGISTRATION
        </h1>
        
        {searchParams?.error && (
          <div className="bg-red-900/50 border border-red-500 text-red-200 p-3 rounded-lg text-sm mb-6">
            {searchParams.error}
          </div>
        )}
        
        <form className="flex flex-col gap-4">
          <div>
            <label className="block text-gray-400 text-sm font-mono mb-2" htmlFor="email">EMAIL</label>
            <input
              id="email"
              name="email"
              type="email"
              required
              className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white focus:outline-none focus:border-teal-500 transition-colors"
            />
          </div>
          <div>
            <label className="block text-gray-400 text-sm font-mono mb-2" htmlFor="password">PASSWORD</label>
            <input
              id="password"
              name="password"
              type="password"
              required
              className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white focus:outline-none focus:border-teal-500 transition-colors"
            />
          </div>
          <button
            formAction={signup}
            className="mt-4 w-full bg-teal-600 hover:bg-teal-500 text-white font-bold py-3 rounded-lg transition-colors tracking-wide"
          >
            CREATE ACCOUNT
          </button>
        </form>
        
        <div className="mt-6 text-center text-sm text-gray-500">
          Already registered? <a href="/login" className="text-teal-400 hover:underline">Secure Login</a>
        </div>
      </div>
    </div>
  )
}
