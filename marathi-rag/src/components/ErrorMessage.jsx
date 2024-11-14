import React from 'react';
import { AlertCircle } from 'lucide-react';

export const ErrorMessage = ({ message }) => (
    <div className="mx-6 mb-6 p-4 bg-red-50 rounded-md flex items-start">
        <AlertCircle className="h-5 w-5 text-red-400 mt-0.5 mr-2" />
        <p className="text-sm text-red-700">{message}</p>
    </div>
);