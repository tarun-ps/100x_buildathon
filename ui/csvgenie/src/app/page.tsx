'use client'

import React, { useState } from 'react'
import LandingPage from '@/components/LandingPage'
import Creations from '@/components/Creations'
import TaskDetails from '@/components/TaskDetails'
import { NavigationButton } from '@/components/NavigationButton'

const Page: React.FC = () => {
  const [selectedOption, setSelectedOption] = useState<'create' | 'view' | 'task'>('create')
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null)
  return (
    <main className="min-h-screen flex">
      <aside className="w-1/4 bg-gray-500 shadow p-4">
        {/* Logo and Subheadline */}
        <div className="flex items-center mb-6">
          <img src="/genie.png" alt="csvgenie" className="h-16 w-16 mr-2" />
          <div>
            <h1 className="text-white text-2xl font-bold">csvgenie</h1>
            <p className="text-white text-sm">A Purple Shores product</p>
          </div>
        </div>

        {/* Create Button */}
        <NavigationButton
          label="create"
          selectedOption={selectedOption}
          setSelectedOption={setSelectedOption}
        />

        {/* View Button */}
        <NavigationButton
          label="view"
          selectedOption={selectedOption}
          setSelectedOption={setSelectedOption}
        />
      </aside>

      {/* Main Content */}
      <div className="flex-1 p-4">
        {selectedOption === 'create' && <LandingPage />}
        {selectedOption === 'view' && <Creations setSelectedTaskId={setSelectedTaskId} setSelectedOption={setSelectedOption} />}
        {selectedOption === 'task' && selectedTaskId && <TaskDetails id={selectedTaskId} />}
      </div>
    </main>
  )
}

export default Page 