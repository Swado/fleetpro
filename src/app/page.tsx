import { redirect } from 'next/navigation'
import Image from 'next/image'
import Link from 'next/link'
import { getServerSession } from 'next-auth'
import { authOptions } from './api/auth/[...nextauth]/route'

export default async function HomePage() {
  const session = await getServerSession(authOptions)

  if (session) {
    redirect('/dashboard')
  }

  return (
    <div className="min-h-screen relative">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <Image
          src="/static/images/truck-background.webp"
          alt="Truck Fleet Background"
          fill
          className="object-cover"
          priority
        />
        <div className="absolute inset-0 bg-black/50" />
      </div>

      {/* Content */}
      <div className="relative z-10 container mx-auto px-4">
        <nav className="flex justify-between items-center py-8">
          <div className="flex gap-4">
            <button className="nav-btn">About</button>
            <button className="nav-btn">Features</button>
          </div>
          <Link
            href="/login"
            className="login-btn px-6 py-2 bg-white/10 backdrop-blur-sm rounded-lg 
                     text-white hover:bg-white/20 transition duration-200"
          >
            Login
          </Link>
        </nav>

        <div className="mt-32 text-center">
          <h1 className="text-6xl font-bold text-white mb-4">
            Xpress360
          </h1>
          <p className="text-xl text-white/90 mb-8">
            Advanced Fleet Management Solutions
          </p>
        </div>
      </div>
    </div>
  )
}