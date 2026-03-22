import React, { useState } from 'react';
import { FeedItem } from '../types/feed';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);

const sourceColors: Record<string, string> = {
  x: 'bg-black text-white',
  gmail: 'bg-teal-600 text-white',
  web: 'bg-blue-600 text-white',
};
const sentimentColors: Record<string, string> = {
  positive: 'bg-green-500',
  neutral: 'bg-gray-400',
  negative: 'bg-red-500',
};

export const FeedCard: React.FC<{ item: FeedItem }> = ({ item }) => {
  const [expanded, setExpanded] = useState(false);
  return (
    <div className="bg-zinc-900 rounded-lg shadow p-4 flex flex-col gap-2">
      <div className="flex items-center gap-2">
        <a href={item.url} target="_blank" rel="noopener noreferrer" className="font-bold text-lg hover:underline flex-1">{item.title}</a>
        <span className={`px-2 py-1 rounded text-xs font-semibold ${sourceColors[item.source] || 'bg-gray-700 text-white'}`}>{item.source}</span>
      </div>
      <div className="flex items-center gap-2">
        {item.category && <span className="px-2 py-0.5 bg-zinc-800 rounded text-xs border border-zinc-700">{item.category}</span>}
        {item.sentiment && <span className={`w-3 h-3 rounded-full inline-block ml-2 ${sentimentColors[item.sentiment] || 'bg-gray-500'}`}></span>}
        <span className="ml-auto text-xs text-zinc-400">{dayjs(item.created_at).fromNow()}</span>
      </div>
      <div>
        <button className="text-blue-400 text-xs underline" onClick={() => setExpanded((e) => !e)}>
          {expanded ? 'Hide AI Summary' : 'Show AI Summary'}
        </button>
        {expanded && (
          <div className="mt-2 text-sm text-zinc-200 whitespace-pre-line">{item.summary || 'No summary.'}</div>
        )}
      </div>
      {item.entities_json && (
        <div className="flex flex-wrap gap-1 mt-1">
          {item.entities_json.companies?.map((c) => (
            <span key={c} className="bg-purple-700 text-xs px-2 py-0.5 rounded">{c}</span>
          ))}
          {item.entities_json.technologies?.map((t) => (
            <span key={t} className="bg-cyan-700 text-xs px-2 py-0.5 rounded">{t}</span>
          ))}
        </div>
      )}
      <div className="flex items-center gap-2 mt-2">
        <div className="flex-1 bg-zinc-800 rounded h-2 overflow-hidden">
          <div className="bg-green-600 h-2" style={{ width: `${(item.relevance_score || 0) * 10}%` }}></div>
        </div>
        <span className="text-xs text-zinc-400">{item.relevance_score || 0}/10</span>
      </div>
    </div>
  );
};
