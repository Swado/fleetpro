'use client'

import { useSession } from 'next-auth/react'
import { redirect } from 'next/navigation'
import DashboardLayout from '@/components/layout/DashboardLayout'
import ElevenLabsWidget from '@/components/ElevenLabsWidget'
import { useEffect, useState } from 'react'

export default function DashboardPage() {
  const { data: session, status } = useSession()
  const [showAIChat, setShowAIChat] = useState(false)

  useEffect(() => {
    // Load ElevenLabs script only when needed
    if (showAIChat) {
      const script = document.createElement('script')
      script.src = "https://elevenlabs.io/convai-widget/index.js"
      script.async = true
      document.body.appendChild(script)

      return () => {
        document.body.removeChild(script)
      }
    }
  }, [showAIChat])

  if (status === 'loading') {
    return <div>Loading...</div>
  }

  if (!session) {
    redirect('/login')
  }

  const handleAIChatClick = () => {
    setShowAIChat(true)
  }

  return (
    <DashboardLayout title="Dashboard">
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Dashboard cards and stats will go here */}
      </div>
      <button
        onClick={handleAIChatClick}
        className="fixed bottom-5 right-5 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-full shadow-lg transition-colors"
      >
        <span className="flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 100-12 6 6 0 000 12zm1-5a1 1 0 11-2 0 1 1 0 012 0zm-1-4a1 1 0 00-1 1v2a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          AI Assistant
        </span>
      </button>
      {showAIChat && <ElevenLabsWidget />}
    </DashboardLayout>
  )
}