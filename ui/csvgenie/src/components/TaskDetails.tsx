import React, { useEffect, useState } from 'react';

interface Question {
  question: string;
  video: string;
}

interface TaskDetail {
  id: string;
  domain: string;
  questions: Question[];
}

const TaskDetails: React.FC<{ id: string }> = ({ id }) => {

  const [taskDetails, setTaskDetails] = useState<TaskDetail | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [hasError, setHasError] = useState<boolean>(false);

  useEffect(() => {
    const fetchCreations = async () => {
      try {
        const response = await fetch(`https://backend.csvgenie.purpleshores.in/tasks/${id}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data: TaskDetail = await response.json();
        setTaskDetails(data);
      } catch (error) {
        console.error('Error fetching task details:', error);
        setHasError(true);
      } finally {
        setIsLoading(false);
      }
    };

    fetchCreations();
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (hasError) {
    return <div>Error loading creations.</div>;
  }

  return (
    <div className="flex">
      
      <div className="p-4 flex-1">
        <h1 className="text-2xl font-bold mb-4">{taskDetails?.domain}</h1>
        <ul>
          {taskDetails?.questions.map((q, index) => (
            <li key={index} className="mb-2">
              <p className="font-semibold">{q.question}</p>
              <video src={`https://backend.csvgenie.purpleshores.in/tasks/${q.video}`} controls className="mt-1 w-full" />
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default TaskDetails; 