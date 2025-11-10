'use client';

import { useEffect, useState, Suspense } from 'react';
import { motion } from 'framer-motion';
import { Database, RefreshCw, Play, Pause } from 'lucide-react';

export default function DatabasePage() {
  const [tables, setTables] = useState<any[]>([]);
  const [selectedTable, setSelectedTable] = useState<string | null>(null);
  const [tableData, setTableData] = useState<any[]>([]);
  const [isLiveMode, setIsLiveMode] = useState(true);
  const [loading, setLoading] = useState(false);

  // This would connect to your backend API in production
  const fetchTables = async () => {
    setLoading(true);
    try {
      // Replace with actual API call
      // const response = await fetch('/api/v1/database/tables');
      // const data = await response.json();
      // setTables(data);

      // Mock data for now
      setTables([
        { name: 'deployments', rows: 24 },
        { name: 'users', rows: 12 },
        { name: 'subdomains', rows: 18 },
        { name: 'monitoring_logs', rows: 2456 },
      ]);
    } catch (error) {
      console.error('Failed to fetch tables:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTables();

    // Set up real-time updates if live mode is on
    if (isLiveMode) {
      const interval = setInterval(fetchTables, 5000); // Refresh every 5 seconds
      return () => clearInterval(interval);
    }
  }, [isLiveMode]);

  return (
    <motion.div
      className="space-y-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2 flex items-center gap-2">
            <Database className="w-8 h-8" />
            Database Viewer
          </h1>
          <p className="text-neutral-400">Real-time database inspection</p>
        </div>

        <div className="flex items-center gap-3">
          <motion.button
            onClick={() => setIsLiveMode(!isLiveMode)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
              isLiveMode
                ? 'bg-green-500/20 text-green-400'
                : 'bg-neutral-800 text-neutral-400'
            }`}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {isLiveMode ? (
              <>
                <Play className="w-4 h-4" />
                Live
              </>
            ) : (
              <>
                <Pause className="w-4 h-4" />
                Paused
              </>
            )}
          </motion.button>

          <motion.button
            onClick={fetchTables}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-white text-black rounded-lg hover:bg-neutral-200 transition-colors disabled:opacity-50"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </motion.button>
        </div>
      </div>

      {/* Tables Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        {tables.map((table, index) => (
          <motion.div
            key={table.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            onClick={() => setSelectedTable(table.name)}
            className={`glass p-4 rounded-lg cursor-pointer transition-all ${
              selectedTable === table.name ? 'ring-2 ring-white' : ''
            }`}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <h3 className="font-semibold mb-2">{table.name}</h3>
            <p className="text-neutral-400 text-sm">{table.rows} rows</p>
          </motion.div>
        ))}
      </div>

      {/* Table Data Viewer */}
      {selectedTable && (
        <motion.div
          className="glass p-6 rounded-lg"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h2 className="text-xl font-bold mb-4">{selectedTable}</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-neutral-700">
                  <th className="px-4 py-2 text-left text-neutral-400">ID</th>
                  <th className="px-4 py-2 text-left text-neutral-400">Data</th>
                  <th className="px-4 py-2 text-left text-neutral-400">Created</th>
                </tr>
              </thead>
              <tbody>
                {[...Array(5)].map((_, i) => (
                  <tr key={i} className="border-b border-neutral-800 hover:bg-neutral-900">
                    <td className="px-4 py-2">{i + 1}</td>
                    <td className="px-4 py-2 text-neutral-400">Sample data...</td>
                    <td className="px-4 py-2 text-neutral-400">2 hours ago</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      )}

      {/* Info Box */}
      <motion.div
        className="glass p-6 rounded-lg border border-neutral-700"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <h3 className="font-semibold mb-2">💡 How to Use</h3>
        <ul className="space-y-2 text-sm text-neutral-400">
          <li>• Click on a table to view its data</li>
          <li>• Toggle Live mode to enable real-time updates</li>
          <li>• Click Refresh to manually update the data</li>
          <li>• Data refreshes automatically every 5 seconds in Live mode</li>
        </ul>
      </motion.div>
    </motion.div>
  );
}
