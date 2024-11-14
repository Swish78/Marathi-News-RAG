import React from 'react';
import VideoSummarizer from './components/VideoSummarizer';

function App() {
    return (
        <div className="min-h-screen bg-gray-50">
            <nav className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16 items-center">
                        <div className="flex-shrink-0">
                            <h1 className="text-xl font-bold text-gray-900">Video Summarizer</h1>
                        </div>
                    </div>
                </div>
            </nav>

            <main>
                <VideoSummarizer />
            </main>

            <footer className="bg-white mt-8">
                <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
                    <p className="text-center text-sm text-gray-500">
                        © {new Date().getFullYear()} Video Summarizer. All rights reserved.
                    </p>
                </div>
            </footer>
        </div>
    );
}

export default App;