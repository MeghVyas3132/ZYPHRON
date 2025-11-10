'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { useState } from 'react';

interface NewDeploymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: DeploymentFormData) => void;
}

export interface DeploymentFormData {
  name: string;
  repository: string;
  branch: string;
  description: string;
}

export default function NewDeploymentModal({
  isOpen,
  onClose,
  onSubmit,
}: NewDeploymentModalProps) {
  const [formData, setFormData] = useState<DeploymentFormData>({
    name: '',
    repository: '',
    branch: 'main',
    description: '',
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Validate form
      if (!formData.name.trim()) {
        setError('Project name is required');
        setIsLoading(false);
        return;
      }
      if (!formData.repository.trim()) {
        setError('Repository URL is required');
        setIsLoading(false);
        return;
      }

      // Call the API to create deployment
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}/deployments`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to create deployment: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('Deployment created:', result);

      // Reset form and close modal
      setFormData({
        name: '',
        repository: '',
        branch: 'main',
        description: '',
      });
      onSubmit(formData);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create deployment');
      console.error('Error creating deployment:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ duration: 0.2 }}
            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-md bg-neutral-950 border border-neutral-800 rounded-xl shadow-2xl z-50 p-6"
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">Create New Deployment</h2>
              <button
                onClick={onClose}
                className="p-1 hover:bg-neutral-900 rounded-lg transition-colors"
                disabled={isLoading}
              >
                <X className="w-5 h-5 text-neutral-400" />
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Project Name */}
              <div>
                <label className="block text-sm font-medium text-neutral-300 mb-2">
                  Project Name <span className="text-red-400">*</span>
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="My Awesome App"
                  className="w-full px-4 py-2 bg-neutral-900 border border-neutral-800 rounded-lg text-white placeholder-neutral-600 focus:border-white focus:outline-none transition-colors disabled:opacity-50"
                  disabled={isLoading}
                />
              </div>

              {/* Repository URL */}
              <div>
                <label className="block text-sm font-medium text-neutral-300 mb-2">
                  Repository URL <span className="text-red-400">*</span>
                </label>
                <input
                  type="text"
                  name="repository"
                  value={formData.repository}
                  onChange={handleChange}
                  placeholder="https://github.com/username/repo"
                  className="w-full px-4 py-2 bg-neutral-900 border border-neutral-800 rounded-lg text-white placeholder-neutral-600 focus:border-white focus:outline-none transition-colors disabled:opacity-50"
                  disabled={isLoading}
                />
              </div>

              {/* Branch */}
              <div>
                <label className="block text-sm font-medium text-neutral-300 mb-2">
                  Branch
                </label>
                <select
                  name="branch"
                  value={formData.branch}
                  onChange={handleChange}
                  className="w-full px-4 py-2 bg-neutral-900 border border-neutral-800 rounded-lg text-white focus:border-white focus:outline-none transition-colors disabled:opacity-50"
                  disabled={isLoading}
                >
                  <option value="main">main</option>
                  <option value="develop">develop</option>
                  <option value="staging">staging</option>
                  <option value="production">production</option>
                </select>
              </div>

              {/* Description */}
              <div>
                <label className="block text-sm font-medium text-neutral-300 mb-2">
                  Description
                </label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Brief description of your deployment"
                  rows={3}
                  className="w-full px-4 py-2 bg-neutral-900 border border-neutral-800 rounded-lg text-white placeholder-neutral-600 focus:border-white focus:outline-none transition-colors resize-none disabled:opacity-50"
                  disabled={isLoading}
                />
              </div>

              {/* Error Message */}
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm"
                >
                  {error}
                </motion.div>
              )}

              {/* Buttons */}
              <div className="flex gap-3 pt-6">
                <button
                  type="button"
                  onClick={onClose}
                  className="flex-1 px-4 py-2 bg-neutral-900 border border-neutral-800 rounded-lg text-white hover:bg-neutral-800 transition-colors disabled:opacity-50"
                  disabled={isLoading}
                >
                  Cancel
                </button>
                <motion.button
                  type="submit"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="flex-1 px-4 py-2 bg-white text-black rounded-lg font-semibold hover:bg-neutral-200 transition-colors disabled:opacity-50"
                  disabled={isLoading}
                >
                  {isLoading ? 'Creating...' : 'Create Deployment'}
                </motion.button>
              </div>
            </form>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
