import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="text-center max-w-2xl">
        <h1 className="text-5xl font-bold mb-4 text-gray-900">Phase II Todo App</h1>
        <p className="text-lg text-gray-600 mb-8">
          Full-stack web application with authentication and database persistence
        </p>

        <div className="flex gap-4 justify-center">
          <Link
            href="/signup"
            className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-md"
          >
            Get Started
          </Link>
          <Link
            href="/login"
            className="px-6 py-3 bg-white text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors shadow-md border border-gray-300"
          >
            Sign In
          </Link>
        </div>

        <div className="mt-12 grid grid-cols-3 gap-6 text-sm">
          <div className="p-4 bg-white rounded-lg shadow">
            <div className="font-semibold text-gray-900 mb-1">Secure Auth</div>
            <div className="text-gray-600">JWT-based authentication</div>
          </div>
          <div className="p-4 bg-white rounded-lg shadow">
            <div className="font-semibold text-gray-900 mb-1">Task Management</div>
            <div className="text-gray-600">Create, view, and organize tasks</div>
          </div>
          <div className="p-4 bg-white rounded-lg shadow">
            <div className="font-semibold text-gray-900 mb-1">Database Sync</div>
            <div className="text-gray-600">PostgreSQL persistence</div>
          </div>
        </div>
      </div>
    </main>
  )
}
