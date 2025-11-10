'use client';

import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Mon', value: 12 },
  { name: 'Tue', value: 15 },
  { name: 'Wed', value: 22 },
  { name: 'Thu', value: 18 },
  { name: 'Fri', value: 28 },
  { name: 'Sat', value: 24 },
  { name: 'Sun', value: 20 },
];

export default function DeploymentChart() {
  return (
    <motion.div
      className="glass p-6 rounded-xl"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.3 }}
    >
      <h2 className="text-lg font-semibold mb-6">Deployments (7 Days)</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis stroke="#666" />
          <YAxis stroke="#666" />
          <Tooltip
            contentStyle={{
              background: '#1a1a1a',
              border: '1px solid #333',
              borderRadius: '8px',
            }}
            labelStyle={{ color: '#fff' }}
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#fff"
            strokeWidth={2}
            dot={{ fill: '#fff', r: 4 }}
            activeDot={{ r: 6 }}
            animationDuration={1000}
          />
        </LineChart>
      </ResponsiveContainer>
    </motion.div>
  );
}
