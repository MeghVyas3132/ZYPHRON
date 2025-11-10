'use client';

import { motion } from 'framer-motion';
import { CheckCircle2, AlertCircle, Clock } from 'lucide-react';

const deployments = [
  {
    id: 1,
    name: 'api-gateway',
    status: 'success',
    time: '2 hours ago',
    version: 'v1.2.0',
  },
  {
    id: 2,
    name: 'frontend-app',
    status: 'success',
    time: '5 hours ago',
    version: 'v2.0.1',
  },
  {
    id: 3,
    name: 'worker-service',
    status: 'pending',
    time: 'In progress',
    version: 'v1.1.0',
  },
  {
    id: 4,
    name: 'auth-service',
    status: 'failed',
    time: '12 hours ago',
    version: 'v1.0.5',
  },
];

const statusConfig = {
  success: { icon: CheckCircle2, color: 'text-green-400', bg: 'bg-green-500/10' },
  pending: { icon: Clock, color: 'text-yellow-400', bg: 'bg-yellow-500/10' },
  failed: { icon: AlertCircle, color: 'text-red-400', bg: 'bg-red-500/10' },
};

export default function RecentDeployments() {
  return (
    <motion.div
      className="glass p-6 rounded-xl"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.4 }}
    >
      <h2 className="text-lg font-semibold mb-6">Recent Deployments</h2>

      <div className="space-y-3">
        {deployments.map((deployment, index) => {
          const status = statusConfig[deployment.status as keyof typeof statusConfig];
          const Icon = status.icon;

          return (
            <motion.div
              key={deployment.id}
              className="flex items-center justify-between p-4 bg-neutral-900 rounded-lg hover:bg-neutral-800 transition-colors"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * index, duration: 0.3 }}
              whileHover={{ x: 4 }}
            >
              <div className="flex items-center gap-4 flex-1">
                <div className={`p-2 rounded-lg ${status.bg}`}>
                  <Icon className={`w-5 h-5 ${status.color}`} />
                </div>
                <div>
                  <p className="font-medium">{deployment.name}</p>
                  <p className="text-sm text-neutral-500">{deployment.time}</p>
                </div>
              </div>

              <div className="text-right">
                <p className="text-sm font-semibold text-neutral-300">
                  {deployment.version}
                </p>
                <p className="text-xs text-neutral-500 capitalize">
                  {deployment.status}
                </p>
              </div>
            </motion.div>
          );
        })}
      </div>
    </motion.div>
  );
}
