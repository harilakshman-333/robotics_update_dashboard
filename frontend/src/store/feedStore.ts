import create from 'zustand';

interface FeedStore {
  selectedSource: string;
  selectedCategory: string;
  selectedSentiment: string;
  searchQuery: string;
  setSource: (source: string) => void;
  setCategory: (category: string) => void;
  setSentiment: (sentiment: string) => void;
  setSearchQuery: (query: string) => void;
}

export const useFeedStore = create<FeedStore>((set) => ({
  selectedSource: 'all',
  selectedCategory: 'all',
  selectedSentiment: 'all',
  searchQuery: '',
  setSource: (source) => set({ selectedSource: source }),
  setCategory: (category) => set({ selectedCategory: category }),
  setSentiment: (sentiment) => set({ selectedSentiment: sentiment }),
  setSearchQuery: (query) => set({ searchQuery: query }),
}));
