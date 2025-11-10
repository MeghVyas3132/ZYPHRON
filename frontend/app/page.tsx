'use client';

import { motion } from 'framer-motion';
import {
  Zap,
  Clock,
  TrendingUp,
  Activity,
} from 'lucide-react';
import StatCard from '@/components/dashboard/StatCard';
import DeploymentChart from '@/components/dashboard/DeploymentChart';
import RecentDeployments from '@/components/dashboard/RecentDeployments';

export default function Dashboard() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.4 },
    },
  };

  return (
    <motion.div
      className="space-y-6"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Page Title */}
      <motion.div variants={itemVariants}>
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-neutral-400">Welcome back to Zyphron</p>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
        variants={containerVariants}
      >
        <motion.div variants={itemVariants}>
          <StatCard
            title="Total Deployments"
            value="24"
            change="+12%"
            icon={<Zap className="w-6 h-6" />}
            positive
          />
        </motion.div>
        <motion.div variants={itemVariants}>
          <StatCard
            title="Active Services"
            value="18"
            change="+5%"
            icon={<Activity className="w-6 h-6" />}
            positive
          />
        </motion.div>
        <motion.div variants={itemVariants}>
          <StatCard
            title="Success Rate"
            value="98.5%"
            change="-0.2%"
            icon={<TrendingUp className="w-6 h-6" />}
            positive={false}
          />
        </motion.div>
        <motion.div variants={itemVariants}>
          <StatCard
            title="Avg. Deploy Time"
            value="2.4m"
            change="-15%"
            icon={<Clock className="w-6 h-6" />}
            positive
          />
        </motion.div>
      </motion.div>

      {/* Charts and Recent Activity */}
      <motion.div className="grid grid-cols-1 lg:grid-cols-3 gap-6" variants={containerVariants}>
        {/* Deployment Chart */}
        <motion.div variants={itemVariants} className="lg:col-span-2">
          <DeploymentChart />
        </motion.div>

        {/* Quick Stats */}
        <motion.div variants={itemVariants}>
          <div className="glass p-6 rounded-xl">
            <h2 className="text-lg font-semibold mb-4">Quick Stats</h2>
            <div className="space-y-4">
              {[
                { label: 'Uptime', value: '99.9%', color: 'from-green-500' },
                { label: 'CPU Usage', value: '45%', color: 'from-blue-500' },
                { label: 'Memory', value: '62%', color: 'from-yellow-500' },
              ].map((stat) => (
                <div key={stat.label}>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm text-neutral-400">{stat.label}</span>
                    <span className="text-sm font-semibold">{stat.value}</span>
                  </div>
                  <div className="w-full h-2 bg-neutral-800 rounded-full overflow-hidden">
                    <motion.div
                      className={`h-full bg-gradient-to-r ${stat.color} to-transparent`}
                      initial={{ width: 0 }}
                      animate={{ width: stat.value }}
                      transition={{ delay: 0.5, duration: 0.8 }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </motion.div>

      {/* Recent Deployments */}
      <motion.div variants={itemVariants}>
        <RecentDeployments />
      </motion.div>
    </motion.div>
  );
}
