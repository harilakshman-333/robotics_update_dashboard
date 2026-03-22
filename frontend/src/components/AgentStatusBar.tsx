import React from 'react';
import { useStatus } from '../hooks/useStatus';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);

export const AgentStatusBar: React.FC = () => {
  const { counts, unenriched, lastScraped, lastUpdate, connected } = useStatus();
  const sources = [
    { key: 'x', label: 'X' },
    { key: 'gmail', label: 'Gmail' },
    { key: 'web', label: 'Web' },
  ];
  return (
    <div className="w-full bg-zinc-800 text-xs text-zinc-200 px-4 py-1 flex items-center gap-4 border-b border-zinc-700">
      {sources.map((s) => (
        <span key={s.key} className="mr-2">
          {s.label}: {counts[s.key] ?? 0} items
        </span>
      ))}
      <span className="ml-2">{unenriched} items pending enrichment</span>
      <span className="ml-2">Last updated {lastUpdate ? dayjs(lastUpdate).fromNow() : '—'}</span>
      <span className={`ml-auto font-bold ${connected ? 'text-green-400' : 'text-red-400'}`}>{connected ? 'Live' : 'Offline'}</span>
    </div>
  );
};
