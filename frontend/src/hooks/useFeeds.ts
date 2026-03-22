import { useQuery } from '@tanstack/react-query';
import { useFeedStore } from '../store/feedStore';
import { FeedItem } from '../types/feed';

const fetchFeeds = async (params: Record<string, string>) => {
  const url = new URL('/feeds', window.location.origin.replace('3000', '8000'));
  Object.entries(params).forEach(([key, value]) => {
    if (value && value !== 'all') url.searchParams.append(key, value);
  });
  const res = await fetch(url.toString());
  if (!res.ok) throw new Error('Failed to fetch feeds');
  return res.json() as Promise<FeedItem[]>;
};

export const useFeeds = () => {
  const { selectedSource, selectedCategory, selectedSentiment, searchQuery } = useFeedStore();
  return useQuery({
    queryKey: ['feeds', selectedSource, selectedCategory, selectedSentiment, searchQuery],
    queryFn: () => fetchFeeds({
      source: selectedSource,
      category: selectedCategory,
      sentiment: selectedSentiment,
      search: searchQuery,
    }),
    refetchInterval: 60000,
  });
};
