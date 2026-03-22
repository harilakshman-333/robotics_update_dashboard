import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { TrendingData } from '../types/feed';

export const TrendPanel: React.FC = () => {
  const { data, isLoading } = useQuery<TrendingData>({
    queryKey: ['trending'],
    queryFn: async () => {
      const res = await fetch('http://localhost:8000/feeds/trending');
      if (!res.ok) throw new Error('Failed to fetch trending');
      return res.json();
    },
    refetchInterval: 60000,
  });
  return (
    <div className="bg-zinc-900 rounded-lg p-4 mb-4">
      <h3 className="font-bold mb-2 text-zinc-200">Top Companies</h3>
      <ul className="mb-4">
        {isLoading ? <li>Loading...</li> : data?.companies.map(([name, count]) => (
          <li key={name} className="flex items-center gap-2 text-sm">
            <span className="flex-1">{name}</span>
            <span className="bg-purple-700 px-2 rounded text-xs">{count}</span>
            <div className="bg-purple-700 h-2 rounded" style={{ width: `${Math.min(count * 10, 100)}%`, minWidth: 10 }}></div>
          </li>
        ))}
      </ul>
      <h3 className="font-bold mb-2 text-zinc-200">Top Technologies</h3>
      <ul>
        {isLoading ? <li>Loading...</li> : data?.technologies.map(([name, count]) => (
          <li key={name} className="flex items-center gap-2 text-sm">
            <span className="flex-1">{name}</span>
            <span className="bg-cyan-700 px-2 rounded text-xs">{count}</span>
            <div className="bg-cyan-700 h-2 rounded" style={{ width: `${Math.min(count * 10, 100)}%`, minWidth: 10 }}></div>
          </li>
        ))}
      </ul>
    </div>
  );
};
