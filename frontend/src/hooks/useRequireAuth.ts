'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

export function useRequireAuth() {
  const auth = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!auth.loading && !auth.isLoggedIn) {
      router.push('/login');
    }
  }, [auth.loading, auth.isLoggedIn, router]);

  return auth;
}
