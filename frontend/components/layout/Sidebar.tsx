'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Package,
  Monitor,
  Settings,
  LogOut,
  ChevronRight,
  Rocket,
  Database,
} from 'lucide-react';

const menuItems = [
  {
    label: 'Dashboard',
    href: '/',
    icon: LayoutDashboard,
  },
  {
    label: 'Deployments',
    href: '/deployments',
    icon: Rocket,
  },
  {
    label: 'Monitoring',
    href: '/monitoring',
    icon: Monitor,
  },
  {
    label: 'Database',
    href: '/database',
    icon: Database,
  },
  {
    label: 'Subdomains',
    href: '/subdomains',
    icon: Package,
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  const containerVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: {
      opacity: 1,
      x: 0,
      transition: {
        duration: 0.3,
        staggerChildren: 0.05,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, x: -10 },
    visible: { opacity: 1, x: 0 },
  };

  return (
    <motion.aside
      className="w-64 bg-neutral-950 border-r border-neutral-800 flex flex-col h-screen"
      initial={{ x: -280 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Logo */}
      <motion.div
        className="p-6 border-b border-neutral-800"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center font-bold text-black">
            Z
          </div>
          <div>
            <h1 className="font-bold text-lg">Zyphron</h1>
            <p className="text-xs text-neutral-500">v1.0</p>
          </div>
        </div>
      </motion.div>

      {/* Navigation */}
      <motion.nav
        className="flex-1 px-3 py-6 space-y-2"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {menuItems.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;

          return (
            <motion.div key={item.href} variants={itemVariants}>
              <Link href={item.href}>
                <motion.button
                  className={`w-full flex items-center justify-between px-4 py-3 rounded-lg transition-all ${
                    isActive
                      ? 'bg-white text-black'
                      : 'text-neutral-400 hover:bg-neutral-900'
                  }`}
                  whileHover={{ x: 4 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <div className="flex items-center gap-3">
                    <Icon className="w-5 h-5" />
                    <span className="font-medium text-sm">{item.label}</span>
                  </div>
                  {isActive && (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                    >
                      <ChevronRight className="w-4 h-4" />
                    </motion.div>
                  )}
                </motion.button>
              </Link>
            </motion.div>
          );
        })}
      </motion.nav>

      {/* Footer */}
      <motion.div
        className="p-3 border-t border-neutral-800 space-y-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <motion.button
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-neutral-400 hover:bg-neutral-900 transition-colors"
          whileHover={{ x: 4 }}
          whileTap={{ scale: 0.98 }}
        >
          <Settings className="w-5 h-5" />
          <span className="text-sm font-medium">Settings</span>
        </motion.button>

        <motion.button
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-neutral-400 hover:bg-neutral-900 transition-colors"
          whileHover={{ x: 4 }}
          whileTap={{ scale: 0.98 }}
        >
          <LogOut className="w-5 h-5" />
          <span className="text-sm font-medium">Logout</span>
        </motion.button>
      </motion.div>
    </motion.aside>
  );
}
