'use client';

import { Suspense } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import { motion } from 'framer-motion';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
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
        <motion.main
          className="flex-1 overflow-auto"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
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
        </motion.main>
      </div>
    </div>
  );
}
