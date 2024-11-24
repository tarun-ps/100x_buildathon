'use client'

import { useEffect, useState } from 'react'

export function ExampleComponent() {
  const [currentTime, setCurrentTime] = useState<string>('')

  useEffect(() => {
    setCurrentTime(new Date().toLocaleTimeString())
  }, [])

  return <div className="p-4 bg-purple-200 text-purple-800 rounded">
    <h2 className="text-xl font-semibold">Example Component</h2>
    <p className="mt-2">This is an example component with a deep purple theme.</p>
    <button className="mt-4 bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700">
      Action
    </button>
  </div>
} 