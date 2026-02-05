'use client';

import { useEffect, useState } from 'react';

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

  // Since better-auth/react doesn't export an AuthProvider, just return children
  // Individual components will create their own auth client instances as needed
  return (
    <>
      {children}
    </>
  );
}