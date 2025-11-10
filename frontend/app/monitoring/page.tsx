'use client';

import { motion } from 'framer-motion';
import { Monitor } from 'lucide-react';

export default function MonitoringPage() {
  return (
    <motion.div
      className="space-y-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div>
        <h1 className="text-3xl font-bold mb-2 flex items-center gap-2">
          <Monitor className="w-8 h-8" />
          Monitoring
        </h1>
        <p className="text-neutral-400">Monitor your deployments in real-time</p>
      </div>

      <motion.div
        className="glass p-12 rounded-xl text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <p className="text-neutral-400 text-lg">
          Monitoring dashboard coming soon...
        </p>
      </motion.div>
    </motion.div>
  );
}
