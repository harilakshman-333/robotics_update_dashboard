import React, { useState } from 'react';
import { useFeedStore } from '../store/feedStore';

const sources = [
  { key: 'all', label: 'All' },
  { key: 'x', label: 'X' },
  { key: 'gmail', label: 'Gmail' },
  { key: 'web', label: 'Web' },
];
const categories = [
  'all',
  'Research',
  'Product Launch',
  'Funding',
  'Policy',
  'Events',
  'General',
];
const sentiments = [
  { key: 'all', label: 'All' },
  { key: 'positive', label: 'Positive' },
  { key: 'neutral', label: 'Neutral' },
  { key: 'negative', label: 'Negative' },
];

export const SourceFilter: React.FC = () => {
  const { selectedSource, setSource, selectedCategory, setCategory, selectedSentiment, setSentiment, searchQuery, setSearchQuery } = useFeedStore();
  const [search, setSearch] = useState(searchQuery);
  React.useEffect(() => {
    const handler = setTimeout(() => setSearchQuery(search), 300);
    return () => clearTimeout(handler);
  }, [search, setSearchQuery]);
  return (
    <div className="bg-zinc-900 rounded-lg p-4 mb-4 flex flex-col gap-3">
      <div className="flex gap-2">
        {sources.map((s) => (
          <button
            key={s.key}
            className={`px-3 py-1 rounded ${selectedSource === s.key ? 'bg-blue-600 text-white' : 'bg-zinc-800 text-zinc-200'}`}
            onClick={() => setSource(s.key)}
          >
            {s.label}
          </button>
        ))}
      </div>
      <div>
        <select
          className="w-full bg-zinc-800 text-zinc-200 rounded px-2 py-1"
          value={selectedCategory}
          onChange={(e) => setCategory(e.target.value)}
        >
          {categories.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>
      <div className="flex gap-2">
        {sentiments.map((s) => (
          <button
            key={s.key}
            className={`px-3 py-1 rounded ${selectedSentiment === s.key ? 'bg-green-600 text-white' : 'bg-zinc-800 text-zinc-200'}`}
            onClick={() => setSentiment(s.key)}
          >
            {s.label}
          </button>
        ))}
      </div>
      <input
        className="w-full bg-zinc-800 text-zinc-200 rounded px-2 py-1"
        placeholder="Search..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
    </div>
  );
};
