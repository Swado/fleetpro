'use client'

import { useEffect, useRef } from 'react'

interface ElevenLabsWidgetProps {
  agentId?: string
  className?: string
}

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'elevenlabs-convai': React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & {
          'agent-id'?: string
        },
        HTMLElement
      >
    }
  }
}

export default function ElevenLabsWidget({ agentId = "kIJtewstoJnssPcE7t9p", className }: ElevenLabsWidgetProps) {
  const widgetRef = useRef<HTMLElement>(null)

  useEffect(() => {
    // Prevent multiple script insertions
    if (!document.querySelector(`script[src="https://elevenlabs.io/convai-widget/index.js"]`)) {
      const script = document.createElement('script')
      script.src = "https://elevenlabs.io/convai-widget/index.js"
      script.async = true
      document.body.appendChild(script)
    }

    return () => {
      // Cleanup if necessary
    }
  }, [])

  return (
    <elevenlabs-convai
      ref={widgetRef}
      agent-id={agentId}
      className={className || "fixed bottom-5 right-5 z-50"}
    />
  )
}
