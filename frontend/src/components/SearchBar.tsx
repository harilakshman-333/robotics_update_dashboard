import React, { useState } from 'react';
import { useFeedStore } from '../store/feedStore';

export const SearchBar: React.FC = () => {
  const { searchQuery, setSearchQuery } = useFeedStore();
  const [search, setSearch] = useState(searchQuery);
  React.useEffect(() => {
    const handler = setTimeout(() => setSearchQuery(search), 300);
    return () => clearTimeout(handler);
  }, [search, setSearchQuery]);
  return (
    <input
      className="w-full bg-zinc-800 text-zinc-200 rounded px-2 py-1 mb-4"
      placeholder="Search..."
      value={search}
      onChange={(e) => setSearch(e.target.value)}
    />
  );
};
