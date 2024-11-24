'use client'

import React, { useState } from 'react';
import { Tabs, TabsList, TabsTrigger, TabsContent } from './ui/tabs';

const LandingPage: React.FC = () => {
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [textInput, setTextInput] = useState('');

  const handleCsvSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!csvFile) return;

    const formData = new FormData();
    formData.append('file', csvFile);

    try {
      const response = await fetch('/api/submit', {
        method: 'POST',
        body: formData,
      });
      // Handle response
    } catch (error) {
      console.error('Error uploading CSV:', error);
    }
  };

  const handleTextSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textInput }),
      });
      // Handle response
    } catch (error) {
      console.error('Error submitting text:', error);
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
              className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
            >
              Upload CSV
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
              className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
            >
              Submit Text
            </button>
          </form>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default LandingPage; 