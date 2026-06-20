import { createClient } from '@supabase/supabase-js';

// Service-role client — bypasses RLS.
// ONLY import this file from src/app/api/ route handlers, never from client components.
export function getServiceClient() {
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!,
  );
}
