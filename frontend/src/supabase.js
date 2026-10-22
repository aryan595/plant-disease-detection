import { createClient } from "@supabase/supabase-js";

/**
 * Supabase Client Configuration
 *
 * Reads VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY from frontend/.env
 * If not set or placeholder, isSupabaseConfigured will be false and
 * the app gracefully falls back to instant local farmer storage.
 */
const supabaseUrl = (import.meta.env.VITE_SUPABASE_URL || "").trim();
const supabaseAnonKey = (import.meta.env.VITE_SUPABASE_ANON_KEY || "").trim();

export const isSupabaseConfigured = Boolean(
  supabaseUrl &&
    supabaseAnonKey &&
    supabaseUrl.startsWith("http") &&
    !supabaseUrl.includes("your-supabase-project")
);

export const supabase = isSupabaseConfigured
  ? createClient(supabaseUrl, supabaseAnonKey, {
      auth: {
        autoRefreshToken: true,
        persistSession: true,
        detectSessionInUrl: true,
      },
    })
  : null;

// =========================================
// Supabase Auth Helpers
// =========================================

/**
 * Sign in / Sign up with Google OAuth via Supabase
 */
export async function signInWithGoogleSupabase() {
  if (!supabase) {
    throw new Error("Supabase is not configured. Please add VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.");
  }

  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: "google",
    options: {
      redirectTo: window.location.origin,
      queryParams: {
        access_type: "offline",
        prompt: "consent",
      },
    },
  });

  if (error) throw error;
  return data;
}

/**
 * Sign in with email and password via Supabase
 */
export async function signInWithEmailSupabase(email, password) {
  if (!supabase) {
    throw new Error("Supabase is not configured.");
  }

  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) throw error;
  return data;
}

/**
 * Create a new farmer account with email and password via Supabase
 */
export async function signUpWithEmailSupabase(email, password, { fullName, primaryCrop, district }) {
  if (!supabase) {
    throw new Error("Supabase is not configured.");
  }

  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        full_name: fullName,
        primary_crop: primaryCrop || "Tomato",
        district: district || "Pune",
      },
    },
  });

  if (error) throw error;

  // If user object returned, also ensure profile record exists
  if (data?.user) {
    try {
      await supabase.from("profiles").upsert({
        id: data.user.id,
        email: data.user.email,
        full_name: fullName,
        primary_crop: primaryCrop,
        district: district,
        updated_at: new Date().toISOString(),
      });
    } catch (e) {
      console.warn("Could not upsert profile:", e);
    }
  }

  return data;
}

/**
 * Sign out of Supabase
 */
export async function signOutSupabase() {
  if (!supabase) return;
  const { error } = await supabase.auth.signOut();
  if (error) console.warn("Supabase sign out error:", error);
}

/**
 * Get current authenticated user session
 */
export async function getSupabaseUser() {
  if (!supabase) return null;
  const { data: { session } } = await supabase.auth.getSession();
  if (!session?.user) return null;

  const u = session.user;
  return {
    id: u.id,
    name: u.user_metadata?.full_name || u.user_metadata?.name || u.email?.split("@")[0] || "Farmer",
    email: u.email,
    picture: u.user_metadata?.avatar_url || u.user_metadata?.picture || null,
    provider: u.app_metadata?.provider || "supabase",
    district: u.user_metadata?.district || "Pune",
    primaryCrop: u.user_metadata?.primary_crop || "Tomato",
    verified: Boolean(u.email_confirmed_at || u.app_metadata?.provider === "google"),
    createdAt: u.created_at,
  };
}

/**
 * Save / upsert farmer profile into Supabase database table `profiles`
 */
export async function saveProfileToSupabase(user) {
  if (!supabase || !user || !user.id) return null;

  try {
    const { data, error } = await supabase.from("profiles").upsert(
      {
        id: String(user.id),
        email: user.email || "farmer@agrisense.ai",
        full_name: user.name || "Farmer",
        primary_crop: user.primaryCrop || "Tomato",
        district: user.district || "Pune",
        avatar_url: user.picture || null,
        role: user.role || "farmer",
        updated_at: new Date().toISOString(),
      },
      { onConflict: "id" }
    ).select();

    if (error) {
      console.warn("Supabase upsert profile warning:", error.message);
      return null;
    }
    return data;
  } catch (err) {
    console.warn("Failed to upsert profile to Supabase:", err);
    return null;
  }
}

/**
 * Save leaf disease scan to Supabase database table `scan_history`
 */
export async function saveScanToSupabase(userId, scan) {
  if (!supabase || !userId) return null;

  try {
    const { data, error } = await supabase.from("scan_history").insert([
      {
        user_id: String(userId),
        plant: scan.plant,
        disease: scan.disease,
        confidence: Number(scan.confidence) || 0.95,
        severity_percentage: scan.severity ? Number(scan.severity) : null,
        image_url: scan.preview || null,
        created_at: new Date().toISOString(),
      },
    ]).select();

    if (error) {
      console.warn("Supabase insert scan error:", error.message);
      return null;
    }
    return data;
  } catch (err) {
    console.warn("Failed to save scan to Supabase:", err);
    return null;
  }
}

/**
 * Fetch scan history from Supabase database table `scan_history`
 */
export async function fetchScanHistoryFromSupabase(userId) {
  if (!supabase || !userId) return [];

  try {
    const { data, error } = await supabase
      .from("scan_history")
      .select("*")
      .eq("user_id", userId)
      .order("created_at", { ascending: false })
      .limit(30);

    if (error) {
      console.warn("Supabase fetch scans error:", error.message);
      return [];
    }

    return (data || []).map((row) => ({
      id: row.id,
      plant: row.plant,
      disease: row.disease,
      confidence: row.confidence,
      severity: row.severity_percentage,
      preview: row.image_url,
      timestamp: new Date(row.created_at).toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }),
    }));
  } catch (err) {
    console.warn("Failed to fetch scans from Supabase:", err);
    return [];
  }
}
