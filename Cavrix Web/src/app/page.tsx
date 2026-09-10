import ChatInterface from '../components/ChatInterface';
import { logout } from './auth/actions';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-8 bg-gray-950">
      <div className="z-10 max-w-7xl w-full items-center justify-between font-mono text-sm lg:flex">
        <p className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-800 bg-gradient-to-b from-gray-900 pb-6 pt-8 backdrop-blur-2xl lg:static lg:w-auto lg:rounded-xl lg:border lg:bg-gray-800 lg:p-4">
          <code className="font-mono font-bold text-teal-400">CAVRIX WEB &nbsp; v2.0</code>
        </p>
        <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-gray-900 via-gray-900 lg:static lg:h-auto lg:w-auto lg:bg-none">
          <div className="flex gap-4 p-4 text-gray-400 items-center">
            <span className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500"></span> Vercel Ready
            </span>
            <form action={logout}>
              <button type="submit" className="text-xs bg-gray-800 hover:bg-gray-700 text-gray-300 py-1 px-3 rounded border border-gray-700 transition-colors">
                Logout
              </button>
            </form>
          </div>
        </div>
      </div>

      <div className="relative flex place-items-center w-full max-w-5xl h-[70vh] mt-10">
        <ChatInterface />
      </div>
    </main>
  );
}
