import { NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { prisma } from '@/lib/prisma'
import { authOptions } from '../auth/[...nextauth]/route'

export async function GET() {
  const session = await getServerSession(authOptions)

  if (!session) {
    return new NextResponse('Unauthorized', { status: 401 })
  }

  try {
    const user = await prisma.user.findUnique({
      where: {
        email: session.user?.email
      }
    })

    if (!user) {
      return new NextResponse('User not found', { status: 404 })
    }

    const trucks = await prisma.truck.findMany({
      where: {
        user_id: user.id
      },
      select: {
        id: true,
        plate_number: true,
        driver_name: true,
        status: true,
        current_latitude: true,
        current_longitude: true,
        destination_city: true,
        destination_state: true,
      }
    })

    return NextResponse.json(trucks)
  } catch (error) {
    console.error('Failed to fetch trucks:', error)
    return new NextResponse('Internal Server Error', { status: 500 })
  }
}