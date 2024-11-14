import React from 'react';
import { CheckCircle2, Copy } from 'lucide-react';
import { SummaryStats } from './SummaryStats';

export const SummaryDisplay = ({ summary, stats, onCopy, copied }) => (
    <div className="border-t border-gray-200 px-6 py-4">
        <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-gray-900">Summary</h3>
            <button
                onClick={onCopy}
                className="flex items-center space-x-1 text-sm text-gray-500 hover:text-gray-700"
            >
                {copied ? (
                    <CheckCircle2 className="h-4 w-4 text-green-500" />
                ) : (
                    <Copy className="h-4 w-4" />
                )}
                <span>{copied ? 'Copied!' : 'Copy'}</span>
            </button>
        </div>

        {stats && (
            <SummaryStats
                originalLength={stats.originalLength}
                summaryLength={stats.summaryLength}
            />
        )}

        <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-gray-800 whitespace-pre-wrap">{summary}</p>
        </div>
    </div>
);