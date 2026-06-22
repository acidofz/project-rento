export interface Listing {
  id: number;
  title: string;
  district: string;
  rooms: number;
  price: number;
  owner_id: string;
  image_url: string | null;
  latitude: number | null;
  longitude: number | null;
  is_premium: boolean;
  phone: string;
  created_at?: string;
}

export interface ChatSummary {
  id: number;
  created_by: string;
  peer_user_id: string;
  peer_label: string;
  created_at: string;
}

export interface ChatMessage {
  id: number;
  chat_id: number;
  sender_id: string;
  sender_label: string;
  body: string;
  created_at: string;
}

export interface QuickContact {
  user_id: string;
  label: string;
}

export interface Profile {
  id: string;
  email: string;
  username: string;
  is_blocked: boolean;
  created_at?: string;
}
