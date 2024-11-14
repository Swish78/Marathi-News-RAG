import React, { useState, useEffect } from 'react';
import { AlertCircle } from 'lucide-react';
import { API_ENDPOINTS } from './schemas';
import { LoadingSpinner } from './LoadingSpinner';
import { ErrorMessage } from './ErrorMessage';
import { VideoInput } from './VideoInput';
import { SummaryDisplay } from './SummaryDisplay';

const VideoSummarizer = () => {
    const [url, setUrl] = useState('');
    const [summary, setSummary] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [stats, setStats] = useState(null);
    const [copied, setCopied] = useState(false);
    const [backendStatus, setBackendStatus] = useState('checking');

    useEffect(() => {
        checkBackendHealth();
    }, []);

    const checkBackendHealth = async () => {
        try {
            const response = await fetch(API_ENDPOINTS.HEALTH);
            if (response.ok) {
                setBackendStatus('healthy');
            } else {
                setBackendStatus('error');
            }
        } catch (err) {
            setBackendStatus('error');
            console.error('Backend health check failed:', err);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSummary('');
        setStats(null);

        try {
            const response = await fetch(API_ENDPOINTS.SUMMARIZE, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url,
                    max_length: 300
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to generate summary');
            }

            setSummary(data.summary);
            setStats({
                originalLength: data.original_length,
                summaryLength: data.summary_length
            });
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = async () => {
        try {
            await navigator.clipboard.writeText(summary);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            setError('Failed to copy to clipboard');
        }
    };

    if (backendStatus === 'error') {
        return (
            <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
                <div className="max-w-3xl mx-auto text-center">
                    <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        Backend Connection Error
                    </h2>
                    <p className="text-gray-600">
                        Unable to connect to the backend service. Please ensure the backend server is running at {API_ENDPOINTS.SUMMARIZE}
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto">
                {/* Header */}
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">
                        Video Summarizer
                    </h1>
                    <p className="text-gray-600">
                        Enter a video URL to generate a concise summary
                    </p>
                </div>

                {/* Main Card */}
                <div className="bg-white rounded-lg shadow-lg overflow-hidden">
                    {/* Input Form */}
                    <div className="p-6">
                        <VideoInput
                            url={url}
                            setUrl={setUrl}
                            loading={loading}
                            onSubmit={handleSubmit}
                        />
                    </div>

                    {/* Error Message */}
                    {error && <ErrorMessage message={error} />}

                    {/* Loading Spinner */}
                    {loading && <LoadingSpinner />}

                    {/* Summary Results */}
                    {summary && (
                        <SummaryDisplay
                            summary={summary}
                            stats={stats}
                            onCopy={copyToClipboard}
                            copied={copied}
                        />
                    )}
                </div>

                {/* Footer */}
                <div className="mt-8 text-center text-sm text-gray-500">
                    <p>
                        Supports YouTube videos and other video formats
                    </p>
                </div>
            </div>
        </div>
    );
};

export default VideoSummarizer;