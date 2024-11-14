import React from 'react';

export const SummaryStats = ({ originalLength, summaryLength }) => (
    <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="bg-blue-50 rounded-md p-3">
            <p className="text-sm text-blue-700 font-medium">Original Length</p>
            <p className="text-2xl text-blue-900">{originalLength} words</p>
        </div>
        <div className="bg-green-50 rounded-md p-3">
            <p className="text-sm text-green-700 font-medium">Summary Length</p>
            <p className="text-2xl text-green-900">{summaryLength} words</p>
        </div>
    </div>
);
