'use client'

import { useSession } from 'next-auth/react'
import { redirect } from 'next/navigation'
import DashboardLayout from '@/components/layout/DashboardLayout'
import ElevenLabsWidget from '@/components/ElevenLabsWidget'
import { useEffect, useState } from 'react'
import Button from '@/components/ui/Button'
import { TruckIcon, ChatBubbleLeftIcon } from '@heroicons/react/24/outline'

interface Truck {
  id: number
  plate_number: string
  driver_name: string
  status: string
  current_latitude: number
  current_longitude: number
  destination_city?: string
  destination_state?: string
}

export default function DashboardPage() {
  const { data: session, status } = useSession({
    required: true,
    onUnauthenticated() {
      redirect('/login')
    },
  })
  const [showAIChat, setShowAIChat] = useState(false)
  const [trucks, setTrucks] = useState<Truck[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchTrucks = async () => {
      try {
        const response = await fetch('/api/trucks')
        const data = await response.json()
        setTrucks(data)
      } catch (error) {
        console.error('Failed to fetch trucks:', error)
      } finally {
        setIsLoading(false)
      }
    }

    if (session) {
      fetchTrucks()
    }
  }, [session])

  if (status === 'loading' || isLoading) {
    return (
      <DashboardLayout title="Loading...">
        <div className="flex justify-center items-center min-h-[50vh]">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      </DashboardLayout>
    )
  }

  const handleAIChatClick = () => {
    setShowAIChat(true)
  }

  return (
    <DashboardLayout title="Dashboard">
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {trucks.map((truck) => (
          <div key={truck.id} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <TruckIcon className="h-8 w-8 text-primary-DEFAULT" />
                <div className="ml-3">
                  <h3 className="font-semibold">{truck.plate_number}</h3>
                  <p className="text-sm text-gray-600">{truck.driver_name}</p>
                </div>
              </div>
              <span
                className={`px-2 py-1 rounded text-sm ${
                  truck.status === 'active'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}
              >
                {truck.status}
              </span>
            </div>
            <div className="space-y-2">
              {truck.destination_city && (
                <p className="text-sm">
                  Destination: {truck.destination_city}, {truck.destination_state}
                </p>
              )}
            </div>
            <div className="mt-4 flex space-x-2">
              <Button
                variant="primary"
                size="sm"
                onClick={() => window.location.href = `/trucks/${truck.id}`}
                className="flex items-center"
              >
                <TruckIcon className="h-4 w-4 mr-2" />
                View Details
              </Button>
              <Button
                variant="info"
                size="sm"
                onClick={() => handleAIChatClick()}
                className="flex items-center"
              >
                <ChatBubbleLeftIcon className="h-4 w-4 mr-2" />
                AI Chat
              </Button>
            </div>
          </div>
        ))}
      </div>
      {showAIChat && <ElevenLabsWidget />}
    </DashboardLayout>
  )
}