'use client';

import { createAuthClient } from 'better-auth/react';
import { AuthClientProvider } from 'better-auth/react';
import { useEffect, useState } from 'react';

// Initialize auth client
const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3004',
  fetch: globalThis.fetch,
});

export function Providers({ children }: { children: React.ReactNode }) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Render children without auth provider during SSR/hydration
  // This avoids the hydration mismatch error
  if (!isMounted) {
    return <>{children}</>;
  }

  return (
    <AuthClientProvider client={authClient}>
      {children}
    </AuthClientProvider>
  );
}