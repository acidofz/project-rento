'use client';

import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
  useCallback,
} from 'react';
import { getSupabase } from '@/lib/supabase';

const ACCESS_KEY = 'uy_click_access_token';
const REFRESH_KEY = 'uy_click_refresh_token';

interface AuthSession {
  accessToken: string;
  refreshToken: string;
  userId: string;
  userName: string;
  userEmail: string;
  isLoggedIn: boolean;
  isBlocked: boolean;
}

interface AuthContextValue extends AuthSession {
  loading: boolean;
  login: (email: string, password: string) => Promise<string | null>;
  register: (email: string, password: string) => Promise<string | null>;
  logout: () => Promise<void>;
  reload: () => Promise<void>;
}

const DEFAULT: AuthSession = {
  accessToken: '',
  refreshToken: '',
  userId: '',
  userName: 'Гость',
  userEmail: '',
  isLoggedIn: false,
  isBlocked: false,
};

const AuthContext = createContext<AuthContextValue>({
  ...DEFAULT,
  loading: true,
  login: async () => null,
  register: async () => null,
  logout: async () => {},
  reload: async () => {},
});

function humanizeAuthError(exc: unknown, action: string): string {
  const text = String(exc).toLowerCase();
  if (text.includes('email rate limit exceeded')) {
    return 'Слишком много попыток регистрации за короткое время. Подождите 1-5 минут или войдите в уже созданный аккаунт.';
  }
  if (text.includes('invalid login credentials')) return 'Неверный email или пароль.';
  if (text.includes('email not confirmed')) return 'Подтвердите email в письме от Supabase и повторите вход.';
  return `Не удалось выполнить ${action}. Проверьте данные и попробуйте снова.`;
}

async function upsertProfile(userId: string, email: string, accessToken: string) {
  const { getAuthedClient } = await import('@/lib/supabase');
  const sb = getAuthedClient(accessToken);
  const username = (email.split('@')[0] ?? '').trim() || 'user';
  try {
    await sb.from('profiles').upsert({ id: userId, email, username }, { onConflict: 'id' });
  } catch { /* ignore */ }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<AuthSession>(DEFAULT);
  const [loading, setLoading] = useState(true);

  const applySession = useCallback(async (access: string, refresh: string, userId: string, email: string) => {
    localStorage.setItem(ACCESS_KEY, access);
    localStorage.setItem(REFRESH_KEY, refresh);
    const { getAuthedClient } = await import('@/lib/supabase');
    const sb = getAuthedClient(access);
    let userName = email.split('@')[0] || 'Пользователь';
    let isBlocked = false;
    try {
      const { data } = await sb.from('profiles').select('username,is_blocked').eq('id', userId).limit(1).single();
      if (data) {
        userName = (data.username as string)?.trim() || userName;
        isBlocked = Boolean(data.is_blocked);
      }
    } catch { /* ignore */ }
    setSession({ accessToken: access, refreshToken: refresh, userId, userName, userEmail: email, isLoggedIn: true, isBlocked });
  }, []);

  const clearAuth = useCallback(() => {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
    setSession(DEFAULT);
  }, []);

  const validateAndLoad = useCallback(async (access: string, refresh: string) => {
    const sb = getSupabase();
    try {
      const { data: { user }, error } = await sb.auth.getUser(access);
      if (!error && user?.id) {
        await applySession(access, refresh, user.id, user.email ?? '');
        return;
      }
      if (refresh) {
        const { data } = await sb.auth.refreshSession({ refresh_token: refresh });
        if (data.session && data.user) {
          await applySession(data.session.access_token, data.session.refresh_token ?? '', data.user.id, data.user.email ?? '');
          return;
        }
      }
      clearAuth();
    } catch { /* network error — preserve existing auth state */ }
  }, [applySession, clearAuth]);

  useEffect(() => {
    const access = localStorage.getItem(ACCESS_KEY) ?? '';
    const refresh = localStorage.getItem(REFRESH_KEY) ?? '';
    if (access) {
      validateAndLoad(access, refresh).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [validateAndLoad]);

  const login = useCallback(async (email: string, password: string): Promise<string | null> => {
    if (!email || !password) return 'Введите email и пароль.';
    if (password.length < 6) return 'Пароль должен содержать не менее 6 символов.';
    const sb = getSupabase();
    try {
      const { data, error } = await sb.auth.signInWithPassword({ email, password });
      if (error || !data.session || !data.user) return humanizeAuthError(error, 'входа');
      await upsertProfile(data.user.id, data.user.email ?? '', data.session.access_token);
      await applySession(data.session.access_token, data.session.refresh_token ?? '', data.user.id, data.user.email ?? '');
      return null;
    } catch (e) {
      return humanizeAuthError(e, 'входа');
    }
  }, [applySession]);

  const register = useCallback(async (email: string, password: string): Promise<string | null> => {
    if (!email || !password) return 'Заполните email и пароль.';
    if (password.length < 6) return 'Пароль должен содержать не менее 6 символов.';
    const sb = getSupabase();
    try {
      const { data, error } = await sb.auth.signUp({ email, password });
      if (error || !data.user) return humanizeAuthError(error, 'регистрации');
      if (data.session) {
        await upsertProfile(data.user.id, data.user.email ?? '', data.session.access_token);
        await applySession(data.session.access_token, data.session.refresh_token ?? '', data.user.id, data.user.email ?? '');
        return null;
      }
      return 'Регистрация выполнена. Подтверди email и затем войди.';
    } catch (e) {
      return humanizeAuthError(e, 'регистрации');
    }
  }, [applySession]);

  const logout = useCallback(async () => {
    const access = session.accessToken;
    clearAuth();
    if (access) {
      try {
        const { getAuthedClient } = await import('@/lib/supabase');
        await getAuthedClient(access).auth.signOut();
      } catch { /* ignore */ }
    }
  }, [session.accessToken, clearAuth]);

  const reload = useCallback(async () => {
    const access = localStorage.getItem(ACCESS_KEY) ?? '';
    const refresh = localStorage.getItem(REFRESH_KEY) ?? '';
    if (access) await validateAndLoad(access, refresh);
  }, [validateAndLoad]);

  return (
    <AuthContext.Provider value={{ ...session, loading, login, register, logout, reload }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
