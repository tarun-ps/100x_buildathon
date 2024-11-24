'use client'

import React, { useState } from 'react';
import { Tabs, TabsList, TabsTrigger, TabsContent } from './ui/tabs';
import { backendUrl } from '@/lib/utils';

const LandingPage: React.FC = () => {
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [textInput, setTextInput] = useState('');

  // State for CSV Submit Button
  const [isCsvSubmitting, setIsCsvSubmitting] = useState(false);
  const [csvSubmitButtonText, setCsvSubmitButtonText] = useState('Upload CSV');

  // State for Text Submit Button
  const [isTextSubmitting, setIsTextSubmitting] = useState(false);
  const [textSubmitButtonText, setTextSubmitButtonText] = useState('Submit Text');

  const handleCsvSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!csvFile) return;

    const formData = new FormData();
    formData.append('csv_file', csvFile);

    try {
      // Disable submit button and show a processing message
      setIsCsvSubmitting(true);
      setCsvSubmitButtonText('Processing...');
      
      const response = await fetch(`${backendUrl}/task`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        alert(`Task ID: ${data.id}\nDomain: ${data.domain}`);
      } else {
        alert('Failed to upload CSV.');
      }
    } catch (error) {
      console.error('Error uploading CSV:', error);
      alert('An error occurred while uploading the CSV.');
    } finally {
      // Re-enable submit button and reset button text
      setIsCsvSubmitting(false);
      setCsvSubmitButtonText('Upload CSV');
    }
  };

  const handleTextSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      // Disable submit button and show a processing message
      setIsTextSubmitting(true);
      setTextSubmitButtonText('Processing...');
      
      const response = await fetch(`${backendUrl}/texttask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textInput }),
      });

      if (response.ok) {
        const data = await response.json();
        alert(`Task ID: ${data.id}\nDomain: ${data.domain}`);
      } else {
        alert('Failed to submit text.');
      }
    } catch (error) {
      console.error('Error submitting text:', error);
      alert('An error occurred while submitting the text.');
    } finally {
      // Re-enable submit button and reset button text
      setIsTextSubmitting(false);
      setTextSubmitButtonText('Submit Text');
    }
  };

  return (
    <div className="container mx-auto p-4 bg-gray-50 text-gray-900">
      <Tabs defaultValue="csv" className="w-full">
        <TabsList className="flex space-x-1 bg-gray-500 p-1 rounded-md">
          <TabsTrigger value="csv" className="flex-1 text-center text-white">
            CSV
          </TabsTrigger>
          <TabsTrigger value="text" className="flex-1 text-center text-white">
            Text
          </TabsTrigger>
        </TabsList>
        <TabsContent value="csv" className="mt-4 bg-gray-100 p-4 rounded">
          <form onSubmit={handleCsvSubmit} className="flex flex-col space-y-4">
            <input
              type="file"
              accept=".csv"
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  setCsvFile(e.target.files[0]);
                }
              }}
              required
              className="border border-gray-300 p-2 rounded"
            />
            <button
              type="submit"
              disabled={isCsvSubmitting}
              className={`bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 ${
                isCsvSubmitting ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {csvSubmitButtonText}
            </button>
          </form>
        </TabsContent>
        <TabsContent value="text" className="mt-4 bg-gray-100 p-4 rounded">
          <form onSubmit={handleTextSubmit} className="flex flex-col space-y-4">
            <textarea
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              rows={5}
              className="border border-gray-300 p-2 rounded bg-gray-50 text-gray-900"
              placeholder="Enter your text here..."
              required
            />
            <button
              type="submit"
              disabled={isTextSubmitting}
              className={`bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 ${
                isTextSubmitting ? 'opacity-50 cursor-not-allowed' : ''
              }`}
            >
              {textSubmitButtonText}
            </button>
          </form>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default LandingPage; 