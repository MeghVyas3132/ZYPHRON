export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-white mb-4">
            Welcome to <span className="text-blue-500">Zyphron</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8">
            Deploy any repository with a single click
          </p>
          <div className="space-x-4">
            <a
              href="/auth/login"
              className="inline-block px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Login
            </a>
            <a
              href="/auth/signup"
              className="inline-block px-8 py-3 bg-slate-700 text-white rounded-lg hover:bg-slate-600"
            >
              Sign Up
            </a>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20">
          <div className="bg-slate-700 p-6 rounded-lg">
            <h3 className="text-xl font-bold text-white mb-2">One-Click Deploy</h3>
            <p className="text-gray-300">
              Deploy any repository type - frontend, backend, or full-stack - with minimal configuration
            </p>
          </div>
          <div className="bg-slate-700 p-6 rounded-lg">
            <h3 className="text-xl font-bold text-white mb-2">Auto-Detection</h3>
            <p className="text-gray-300">
              Automatically detects languages, frameworks, and dependencies
            </p>
          </div>
          <div className="bg-slate-700 p-6 rounded-lg">
            <h3 className="text-xl font-bold text-white mb-2">SRE Features</h3>
            <p className="text-gray-300">
              Monitoring, health checks, and automatic rollbacks included
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
