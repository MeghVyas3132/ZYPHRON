'use client';

import { motion } from 'framer-motion';
import { Bell, Settings, Search, User } from 'lucide-react';

export default function Header() {
  return (
    <motion.header
      className="h-16 bg-neutral-950 border-b border-neutral-800 flex items-center justify-between px-6 sticky top-0 z-40"
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      {/* Search */}
      <div className="flex-1 max-w-md">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-neutral-500 w-4 h-4" />
          <input
            type="text"
            placeholder="Search deployments..."
            className="w-full pl-10 pr-4 py-2 bg-neutral-900 border border-neutral-800 rounded-lg text-sm text-white placeholder-neutral-500 focus:outline-none focus:border-neutral-700 transition-colors"
          />
        </div>
      </div>

      {/* Right section */}
      <div className="flex items-center gap-4 ml-6">
        {/* Notifications */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="relative p-2 hover:bg-neutral-900 rounded-lg transition-colors"
        >
          <Bell className="w-5 h-5 text-neutral-400" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
        </motion.button>

        {/* Settings */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="p-2 hover:bg-neutral-900 rounded-lg transition-colors"
        >
          <Settings className="w-5 h-5 text-neutral-400" />
        </motion.button>

        {/* User Profile */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="flex items-center gap-2 pl-4 pr-3 py-1 hover:bg-neutral-900 rounded-lg transition-colors"
        >
          <div className="w-8 h-8 bg-neutral-800 rounded-full flex items-center justify-center">
            <User className="w-4 h-4 text-neutral-400" />
          </div>
        </motion.button>
      </div>
    </motion.header>
  );
}
