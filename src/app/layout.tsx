import './globals.css'
import { Inter } from 'next/font/google'
import SessionProvider from '@/components/providers/SessionProvider'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <script src="https://elevenlabs.io/convai-widget/index.js" async></script>
      </head>
      <body className={inter.className}>
        <SessionProvider>
          {children}
        </SessionProvider>
      </body>
    </html>
  )
}