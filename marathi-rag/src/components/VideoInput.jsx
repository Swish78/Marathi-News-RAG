import React from 'react';
import { Youtube, Loader2 } from 'lucide-react';

export const VideoInput = ({ url, setUrl, loading, onSubmit }) => (
    <form onSubmit={onSubmit} className="space-y-4">
        <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Youtube className="h-5 w-5 text-gray-400" />
            </div>
            <input
                type="url"
                placeholder="Enter video URL (YouTube or other video link)"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="block w-full pl-10 pr-12 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                required
            />
        </div>
        <button
            type="submit"
            disabled={loading}
            className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white 
        ${loading ? 'bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'}
        focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
        >
            {loading ? (
                <>
                    <Loader2 className="animate-spin -ml-1 mr-2 h-5 w-5" />
                    Processing Video
                </>
            ) : (
                'Generate Summary'
            )}
        </button>
    </form>
);