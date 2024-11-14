import React from 'react';
import { Loader2 } from 'lucide-react';

export const LoadingSpinner = () => (
    <div className="flex items-center justify-center p-4">
        <Loader2 className="animate-spin h-8 w-8 text-blue-500" />
    </div>
);