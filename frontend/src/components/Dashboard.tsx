import React from 'react';
import { SourceFilter } from './SourceFilter';
import { TrendPanel } from './TrendPanel';
import { AgentStatusBar } from './AgentStatusBar';
import { FeedCard } from './FeedCard';
import { useFeeds } from '../hooks/useFeeds';

export const Dashboard: React.FC = () => {
  const { data: feeds, isLoading } = useFeeds();
  return (
    <div className="flex h-screen bg-zinc-950 text-zinc-100">
      {/* Sidebar */}
      <aside className="w-80 min-w-[220px] max-w-xs bg-zinc-900 border-r border-zinc-800 p-4 flex flex-col gap-4 hidden md:flex">
        <SourceFilter />
        <TrendPanel />
      </aside>
      {/* Main */}
      <main className="flex-1 flex flex-col h-full">
        <AgentStatusBar />
        <div className="p-4 flex-1 overflow-y-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {isLoading ? (
              <div>Loading...</div>
            ) : feeds && feeds.length > 0 ? (
              feeds.map((item) => <FeedCard key={item.id} item={item} />)
            ) : (
              <div>No feeds found.</div>
            )}
          </div>
        </div>
      </main>
      {/* Mobile sidebar */}
      <aside className="fixed bottom-0 left-0 right-0 bg-zinc-900 border-t border-zinc-800 p-2 flex gap-2 md:hidden z-10">
        <SourceFilter />
      </aside>
    </div>
  );
};
