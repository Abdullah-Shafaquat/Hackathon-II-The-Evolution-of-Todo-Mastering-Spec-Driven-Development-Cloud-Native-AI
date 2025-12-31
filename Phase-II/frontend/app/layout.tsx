import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Phase II - Todo App',
  description: 'Full-stack todo application with authentication',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
