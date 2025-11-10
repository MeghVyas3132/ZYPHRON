import type { Metadata } from 'next';
import './globals.css';
import { Suspense } from 'react';
import Sidebar from '@/components/layout/Sidebar';
import Header from '@/components/layout/Header';

export const metadata: Metadata = {
  title: 'Zyphron - Deployment Platform',
  description: 'Production-ready deployment platform for any repository',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="bg-black text-white">
        <div className="flex h-screen bg-black text-white overflow-hidden">
          {/* Sidebar */}
          <Suspense fallback={<div className="w-64 bg-neutral-900 skeleton" />}>
            <Sidebar />
          </Suspense>

          {/* Main Content */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Header */}
            <Suspense fallback={<div className="h-16 bg-neutral-900 skeleton" />}>
              <Header />
            </Suspense>

            {/* Page Content */}
            <main
              className="flex-1 overflow-auto"
              style={{
                animation: 'fadeIn 0.3s ease-in-out'
              }}
            >
              <div className="p-6 space-y-6">
                <Suspense
                  fallback={
                    <div className="space-y-4">
                      <div className="h-8 bg-neutral-800 rounded skeleton w-48" />
                      <div className="grid grid-cols-4 gap-4">
                        {[...Array(4)].map((_, i) => (
                          <div key={i} className="h-32 bg-neutral-800 rounded skeleton" />
                        ))}
                      </div>
                    </div>
                  }
                >
                  {children}
                </Suspense>
              </div>
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
