import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Zyphron - Deploy Anywhere',
  description: 'One-click deployment platform for any repository',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
