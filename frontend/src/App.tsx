import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Dashboard } from './components/Dashboard';

const queryClient = new QueryClient();

const App: React.FC = () => (
  <div className="dark bg-zinc-950 min-h-screen">
    <QueryClientProvider client={queryClient}>
      <Dashboard />
    </QueryClientProvider>
  </div>
);

export default App;
