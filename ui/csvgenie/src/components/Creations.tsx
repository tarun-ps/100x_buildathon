import React, { useEffect, useState } from 'react';
import Link from 'next/link';

interface Creation {
  id: string;
  domain: string;
}

interface CreationsProps {
  setSelectedTaskId: (id: string) => void;
  setSelectedOption: (option: 'create' | 'view' | 'task') => void;
}

const Creations: React.FC<CreationsProps> = ({ setSelectedTaskId, setSelectedOption }) => {
  const [creations, setCreations] = useState<Creation[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [hasError, setHasError] = useState<boolean>(false);
  useEffect(() => {
    const fetchCreations = async () => {
      try {
        const response = await fetch('https://backend.csvgenie.purpleshores.in/tasks');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data: Creation[] = await response.json();
        setCreations(data);
      } catch (error) {
        console.error('Error fetching creations:', error);
        setHasError(true);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCreations();
  }, []);

  const handleClick = (id: string) => {
    setSelectedOption('task')
    setSelectedTaskId(id)
  }

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (hasError) {
    return <div>Error loading creations.</div>;
  }

  return (
    <div className="mt-4 bg-gray-100 text-gray-900">
      <ul>
        {creations.map((creation) => (
          <li key={creation.id} className="mb-2">
            <div className="flex items-center">
                <Link onClick={() => handleClick(creation.id)} href="#" className="text-blue-500 hover:underline">
                    {creation.domain}
                </Link>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Creations; 