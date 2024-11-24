'use client'

import React from 'react'
import { useRouter } from 'next/navigation'
import { PlusIcon, EyeIcon } from '@heroicons/react/24/solid'

interface NavigationButtonProps {
  label: 'create' | 'view'
  selectedOption: 'create' | 'view'
  setSelectedOption: (option: 'create' | 'view') => void
}

export const NavigationButton: React.FC<NavigationButtonProps> = ({
  label,
  selectedOption,
  setSelectedOption,
}) => {
  const router = useRouter()

  const handleClick = () => {
    setSelectedOption(label)
    // Example navigation (optional)
    // router.push(`/desired-path/${label}`)
  }

  return (
    <button
      className={`w-full text-left p-2 flex items-center text-white rounded ${
        selectedOption === label ? 'bg-gray-700' : 'hover:bg-gray-600'
      }`}
      onClick={handleClick}
    >
      {label === 'create' ? (
        <PlusIcon className="h-5 w-5 mr-2" aria-hidden="true" />
      ) : (
        <EyeIcon className="h-5 w-5 mr-2" aria-hidden="true" />
      )}
      {label.charAt(0).toUpperCase() + label.slice(1)}
    </button>
  )
} 