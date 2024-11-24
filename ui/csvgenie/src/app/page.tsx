'use client'

import React from 'react';
import LandingPage from '@/components/LandingPage';
import Creations from '@/components/Creations';
import { useState } from 'react';
import { PlusIcon, EyeIcon } from '@heroicons/react/24/solid';

const Page: React.FC = () => {
  const [selectedOption, setSelectedOption] = useState<'create' | 'view'>('create');

  return (
    <main className="min-h-screen flex">
      <aside className="w-1/4 bg-gray-500 shadow p-4">
        {/* Logo and Subheadline */}
        <div className="flex items-center mb-6">
          <img src="/logo_cropped.png" alt="csvgenie" className="h-16 w-16 mr-2" />
          <div>
            <h1 className="text-white text-2xl font-bold">csvgenie</h1>
            <p className="text-white text-sm">A Purple Shores product</p>
          </div>
        </div>

        {/* Create Button */}
        <button
          className={`w-full text-left p-2 flex items-center text-white rounded ${
            selectedOption === 'create' ? 'bg-gray-700' : 'hover:bg-gray-600'
          }`}
          onClick={() => setSelectedOption('create')}
        >
          <PlusIcon className="h-5 w-5 mr-2" aria-hidden="true" />
          Create
        </button>

        {/* View Button */}
        <button
          className={`w-full text-left p-2 flex items-center text-white rounded mt-2 ${
            selectedOption === 'view' ? 'bg-gray-700' : 'hover:bg-gray-600'
          }`}
          onClick={() => setSelectedOption('view')}
        >
          <EyeIcon className="h-5 w-5 mr-2" aria-hidden="true" />
          View
        </button>
      </aside>

      {/* Main Content */}
      <div className="flex-1 p-4">
        {selectedOption === 'create' && <LandingPage />}
        {selectedOption === 'view' && <Creations />}
      </div>
    </main>
  );
};

export default Page;
