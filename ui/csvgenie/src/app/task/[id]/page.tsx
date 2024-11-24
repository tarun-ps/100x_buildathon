'use client'

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { NavigationButton } from '@/components/NavigationButton';

interface Question {
  question: string;
  video: string;
}

interface CreationDetail {
  id: string;
  domain: string;
  questions: Question[];
}

const CreationDetailPage: React.FC = () => {
  const router = useRouter();
  const params = useParams();
  const id = params.id;

  const [creation, setCreation] = useState<CreationDetail | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [hasError, setHasError] = useState<boolean>(false);
  const [selectedOption, setSelectedOption] = useState<'create' | 'view' | 'details'>('details')

  useEffect(() => {
    if (!id) return;

    const fetchCreationDetail = async () => {
      try {
        const response = await fetch(`http://localhost:8000/tasks/${id}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data: CreationDetail = await response.json();
        setCreation(data);
      } catch (error) {
        console.error('Error fetching creation details:', error);
        setHasError(true);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCreationDetail();
  }, [id]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (hasError || !creation) {
    return <div>Error loading creation details.</div>;
  }


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
        {selectedOption !== 'details' && (
          <NavigationButton
            label="create"
          selectedOption={selectedOption}
          setSelectedOption={setSelectedOption}
        />
        )}

        {/* View Button */}
        {selectedOption !== 'details' && (
        <NavigationButton
          label="view"
          selectedOption={selectedOption}
          setSelectedOption={setSelectedOption}
          />
        )};
      </aside>
    <div className="flex">
      
      <div className="p-4 flex-1">
      <Link href="/" className="text-blue-500 hover:underline mt-4 block">
          Back 
        </Link>
        <h1 className="text-2xl font-bold mb-4">{creation.domain}</h1>
        <ul>
          {creation.questions.map((q, index) => (
            <li key={index} className="mb-2">
              <p className="font-semibold">{q.question}</p>
              <video src={`http://localhost:8000/tasks/${q.video}`} controls className="mt-1 w-full" />
            </li>
          ))}
        </ul>
        <Link href="/" className="text-blue-500 hover:underline mt-4 block">
          Back 
        </Link>
      </div>
    </div>
    </main>
  );
};

export default CreationDetailPage; 