'use client';

import { motion } from 'framer-motion';
import { Rocket, Plus } from 'lucide-react';
import { useState, useEffect } from 'react';
import NewDeploymentModal from '@/components/deployments/NewDeploymentModal';

interface Deployment {
  id: string;
  name: string;
  status: 'success' | 'failed' | 'pending' | 'running';
  version: string;
  createdAt: string;
  updatedAt: string;
}

export default function DeploymentsPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [deployments, setDeployments] = useState<Deployment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch deployments on mount
  useEffect(() => {
    fetchDeployments();
  }, []);

  const fetchDeployments = async () => {
    try {
      setIsLoading(true);
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
      const response = await fetch(`${apiUrl}/deployments`);
      
      if (response.ok) {
        const data = await response.json();
        setDeployments(data.deployments || []);
      }
    } catch (err) {
      console.error('Failed to fetch deployments:', err);
      setError('Failed to load deployments');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewDeployment = async (data: any) => {
    // Refresh deployments after creating a new one
    await fetchDeployments();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'text-green-400 bg-green-500/10';
      case 'failed':
        return 'text-red-400 bg-red-500/10';
      case 'pending':
        return 'text-yellow-400 bg-yellow-500/10';
      case 'running':
        return 'text-blue-400 bg-blue-500/10';
      default:
        return 'text-neutral-400 bg-neutral-500/10';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return '✓';
      case 'failed':
        return '✕';
      case 'pending':
      case 'running':
        return '⟳';
      default:
        return '○';
    }
  };

  return (
    <>
      <motion.div
        className="space-y-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2 flex items-center gap-2">
              <Rocket className="w-8 h-8" />
              Deployments
            </h1>
            <p className="text-neutral-400">Manage your application deployments</p>
          </div>

          <motion.button
            onClick={() => setIsModalOpen(true)}
            className="flex items-center gap-2 px-6 py-2 bg-white text-black rounded-lg font-semibold hover:bg-neutral-200 transition-colors"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Plus className="w-5 h-5" />
            New Deployment
          </motion.button>
        </div>

        {/* Error Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="p-4 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400"
          >
            {error}
          </motion.div>
        )}

        {/* Loading State */}
        {isLoading && (
          <motion.div
            className="glass p-12 rounded-xl text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="inline-block">
              <div className="w-8 h-8 border-4 border-neutral-700 border-t-white rounded-full animate-spin mb-4" />
              <p className="text-neutral-400">Loading deployments...</p>
            </div>
          </motion.div>
        )}

        {/* Empty State */}
        {!isLoading && deployments.length === 0 && !error && (
          <motion.div
            className="glass p-12 rounded-xl text-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Rocket className="w-12 h-12 text-neutral-700 mx-auto mb-4 opacity-50" />
            <p className="text-neutral-400 text-lg">
              No deployments yet. Start by creating your first deployment!
            </p>
          </motion.div>
        )}

        {/* Deployments List */}
        {!isLoading && deployments.length > 0 && (
          <motion.div
            className="space-y-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ staggerChildren: 0.1 }}
          >
            {deployments.map((deployment, index) => (
              <motion.div
                key={deployment.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="glass p-6 rounded-xl hover:bg-neutral-900/80 transition-all group cursor-pointer"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4 flex-1">
                    <div className={`p-3 rounded-lg ${getStatusColor(deployment.status)}`}>
                      {getStatusIcon(deployment.status)}
                    </div>
                    <div>
                      <h3 className="font-semibold text-white mb-1">{deployment.name}</h3>
                      <p className="text-sm text-neutral-500">
                        {new Date(deployment.createdAt).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-mono text-neutral-300">{deployment.version}</p>
                    <p className={`text-xs font-semibold capitalize ${getStatusColor(deployment.status)}`}>
                      {deployment.status}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}
      </motion.div>

      {/* New Deployment Modal */}
      <NewDeploymentModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleNewDeployment}
      />
    </>
  );
}
