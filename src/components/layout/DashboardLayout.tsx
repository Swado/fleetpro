import { useState } from 'react'
import { useRouter } from 'next/router'
import { signOut, useSession } from 'next-auth/react'
import {
  ChartBarIcon,
  TruckIcon,
  UserGroupIcon,
  ChatBubbleLeftRightIcon,
  ArrowLeftOnRectangleIcon,
} from '@heroicons/react/24/outline'
import Button from '../ui/Button'

interface NavItem {
  name: string
  href: string
  icon: typeof ChartBarIcon
}

const navigation: NavItem[] = [
  { name: 'Dashboard', href: '/dashboard', icon: ChartBarIcon },
  { name: 'Fleet', href: '/fleet', icon: TruckIcon },
  { name: 'Drivers', href: '/drivers', icon: UserGroupIcon },
  { name: 'Messages', href: '/messages', icon: ChatBubbleLeftRightIcon },
]

export default function DashboardLayout({
  children,
  title,
}: {
  children: React.ReactNode
  title: string
}) {
  const router = useRouter()
  const { data: session } = useSession()
  const [unreadMessages] = useState(0)

  return (
    <div className="min-h-screen bg-background">
      <nav className="bg-primary shadow-md">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 justify-between">
            <div className="flex">
              <div className="flex flex-shrink-0 items-center">
                <TruckIcon className="h-8 w-8 text-white" />
                <span className="ml-2 text-xl font-bold text-white">Xpress360</span>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                {navigation.map((item) => (
                  <a
                    key={item.name}
                    href={item.href}
                    className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${
                      router.pathname === item.href
                        ? 'text-white border-b-2 border-accent'
                        : 'text-gray-300 hover:text-white'
                    }`}
                  >
                    <item.icon className="mr-2 h-5 w-5" />
                    {item.name}
                    {item.name === 'Messages' && unreadMessages > 0 && (
                      <span className="ml-2 rounded-full bg-red-500 px-2 py-1 text-xs text-white">
                        {unreadMessages}
                      </span>
                    )}
                  </a>
                ))}
              </div>
            </div>
            <div className="flex items-center">
              {session?.user?.email && (
                <span className="mr-4 text-white">{session.user.email}</span>
              )}
              <Button
                variant="secondary"
                size="sm"
                onClick={() => signOut()}
                className="flex items-center"
              >
                <ArrowLeftOnRectangleIcon className="mr-2 h-5 w-5" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h1 className="text-2xl font-semibold text-text">{title}</h1>
        </div>
        {children}
      </main>
    </div>
  )
}