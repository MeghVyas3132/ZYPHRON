'use client';

import { motion } from 'framer-motion';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string;
  change: string;
  icon: React.ReactNode;
  positive: boolean;
}

export default function StatCard({
  title,
  value,
  change,
  icon,
  positive,
}: StatCardProps) {
  return (
    <motion.div
      className="glass p-6 rounded-xl cursor-pointer hover-lift"
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="p-2 bg-neutral-800 rounded-lg text-white">{icon}</div>
        <div
          className={`flex items-center gap-1 text-sm font-semibold ${
            positive ? 'text-green-400' : 'text-red-400'
          }`}
        >
          <span>{change}</span>
          {positive ? (
            <ArrowUpRight className="w-4 h-4" />
          ) : (
            <ArrowDownRight className="w-4 h-4" />
          )}
        </div>
      </div>

      <h3 className="text-neutral-400 text-sm font-medium mb-1">{title}</h3>
      <p className="text-2xl font-bold">{value}</p>

      {/* Animated bottom border */}
      <motion.div
        className="h-1 bg-gradient-to-r from-white to-transparent rounded-full mt-4"
        initial={{ width: 0 }}
        animate={{ width: '100%' }}
        transition={{ delay: 0.2, duration: 0.6 }}
      />
    </motion.div>
  );
}
