'use client'

import { useEffect, useState } from 'react'

export function ClientOnlyComponent() {
  const [width, setWidth] = useState<number>(0)

  useEffect(() => {
    setWidth(window.innerWidth)
  }, [])

  return <div className="p-5 bg-purple-350 text-purple-900 rounded-md">
    <h2 className="text-xl font-bold">Client Only Component</h2>
    <p className="mt-2">This component is styled with the deep purple theme.</p>
    <button className="mt-3 bg-purple-500 text-white px-3 py-1 rounded hover:bg-purple-600">
      Client Action
    </button>
  </div>
} 