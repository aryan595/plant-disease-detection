-- ============================================================
-- AgriSense AI: Supabase PostgreSQL Database Schema
-- Run this script in your Supabase Dashboard -> SQL Editor
-- ============================================================

-- 1. Create or Update Profiles Table (Stores farmer profile metadata)
CREATE TABLE IF NOT EXISTS public.profiles (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL,
  full_name TEXT,
  avatar_url TEXT,
  primary_crop TEXT DEFAULT 'Tomato',
  district TEXT DEFAULT 'Pune',
  role TEXT DEFAULT 'farmer',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- In case profiles was previously created with UUID / foreign key constraint:
DO $$
BEGIN
  ALTER TABLE public.profiles DROP CONSTRAINT IF EXISTS profiles_id_fkey;
  ALTER TABLE public.profiles ALTER COLUMN id TYPE TEXT;
EXCEPTION WHEN OTHERS THEN NULL;
END $$;

-- Enable Row Level Security (RLS) on profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Profiles Policies: Allow reading and writing farmer profiles
DROP POLICY IF EXISTS "Public profiles are viewable by owners" ON public.profiles;
DROP POLICY IF EXISTS "Users can insert their own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can update their own profile" ON public.profiles;
DROP POLICY IF EXISTS "Allow all profile access" ON public.profiles;
CREATE POLICY "Allow all profile access" ON public.profiles FOR ALL USING (true) WITH CHECK (true);

-- 2. Trigger to automatically sync profiles when an email or OAuth user is created in auth.users
CREATE OR REPLACE FUNCTION public.handle_new_user() 
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name, avatar_url, primary_crop, district)
  VALUES (
    new.id::text,
    new.email,
    COALESCE(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name', split_part(new.email, '@', 1)),
    COALESCE(new.raw_user_meta_data->>'avatar_url', new.raw_user_meta_data->>'picture', NULL),
    COALESCE(new.raw_user_meta_data->>'primary_crop', 'Tomato'),
    COALESCE(new.raw_user_meta_data->>'district', 'Pune')
  )
  ON CONFLICT (id) DO UPDATE SET
    avatar_url = EXCLUDED.avatar_url,
    full_name = EXCLUDED.full_name,
    updated_at = timezone('utc'::text, now());
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- 3. Create or Update Scan History Table (Stores leaf diagnosis results)
CREATE TABLE IF NOT EXISTS public.scan_history (
  id BIGSERIAL PRIMARY KEY,
  user_id TEXT NOT NULL,
  plant TEXT NOT NULL,
  disease TEXT NOT NULL,
  confidence FLOAT NOT NULL,
  severity_percentage FLOAT,
  image_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- In case scan_history was previously created with UUID / foreign key constraint:
DO $$
BEGIN
  ALTER TABLE public.scan_history DROP CONSTRAINT IF EXISTS scan_history_user_id_fkey;
  ALTER TABLE public.scan_history ALTER COLUMN user_id TYPE TEXT;
EXCEPTION WHEN OTHERS THEN NULL;
END $$;

-- Enable RLS on scan_history
ALTER TABLE public.scan_history ENABLE ROW LEVEL SECURITY;

-- Scan History Policies: Allow reading and writing scans so every diagnosis is visible in Supabase
DROP POLICY IF EXISTS "Users can view own scan history" ON public.scan_history;
DROP POLICY IF EXISTS "Users can insert own scans" ON public.scan_history;
DROP POLICY IF EXISTS "Users can delete own scans" ON public.scan_history;
DROP POLICY IF EXISTS "Allow all scan history access" ON public.scan_history;
CREATE POLICY "Allow all scan history access" ON public.scan_history FOR ALL USING (true) WITH CHECK (true);

-- Create index for fast lookups by user and date
CREATE INDEX IF NOT EXISTS idx_scan_history_user_date ON public.scan_history (user_id, created_at DESC);

