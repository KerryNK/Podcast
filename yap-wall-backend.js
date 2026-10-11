(() => {
  const config = window.YAP_WALL_SUPABASE_CONFIG || {};
  const baseUrl = (config.url || '').replace(/\/+$/, '');
  const anonKey = config.anonKey || '';

  const isConfigured = () => Boolean(baseUrl && anonKey);

  function buildSupabaseError(message) {
    return `Supabase connection failed: ${message} Check the Vercel environment variables for SUPABASE_URL and SUPABASE_ANON_KEY so they match the same Supabase project.`;
  }

  async function request(path, { method = 'GET', body, prefer = 'return=minimal' } = {}) {
    if (!isConfigured()) {
      throw new Error('Supabase is not configured. Set SUPABASE_URL and SUPABASE_ANON_KEY in your Vercel project environment variables, then redeploy.');
    }

    let response;
    try {
      response = await fetch(`${baseUrl}/rest/v1/${path}`, {
        method,
        headers: {
          apikey: anonKey,
          Authorization: `Bearer ${anonKey}`,
          'Content-Type': 'application/json',
          Prefer: prefer,
        },
        body: body === undefined ? undefined : JSON.stringify(body),
      });
    } catch (error) {
      throw new Error(buildSupabaseError(error instanceof Error ? error.message : 'request failed.'));
    }

    if (!response.ok) {
      const detail = await response.json().catch(() => null);
      throw new Error(detail?.message || `Supabase request failed (${response.status}).`);
    }

    if (response.status === 204) return null;
    return response.json().catch(() => null);
  }

  function mapYap(row) {
    return {
      id: row.id,
      author: row.author,
      topic: row.topic,
      category: row.topic,
      text: row.text,
      flames: row.flames,
      mics: row.mics,
      createdAt: row.created_at,
      replies: (row.replies || []).map((reply) => ({
        id: reply.id,
        author: reply.author,
        text: reply.text,
        createdAt: reply.created_at,
      })),
    };
  }

  async function loadYaps() {
    const rows = await request('yaps?select=id,author,topic,text,flames,mics,created_at,replies(id,author,text,created_at)&order=created_at.desc');
    return (rows || []).map(mapYap);
  }

  async function submitYap({ author, topic, text }) {
    const rows = await request('yaps?select=id,author,topic,text,flames,mics,created_at,replies(id,author,text,created_at)', {
      method: 'POST',
      body: { author, topic, text },
    });
    const row = Array.isArray(rows) ? rows[0] : rows;
    return row ? mapYap(row) : null;
  }

  async function submitReply({ yapId, author, text }) {
    const rows = await request('replies?select=id,author,text,created_at', {
      method: 'POST',
      body: { yap_id: yapId, author, text },
    });
    const row = Array.isArray(rows) ? rows[0] : rows;
    if (!row) return null;
    return {
      id: row.id,
      author: row.author,
      text: row.text,
      createdAt: row.created_at,
    };
  }

  function getVisitorId() {
    const key = 'kerry-yaps-wall-visitor-id';
    let visitorId = window.localStorage.getItem(key);
    if (!visitorId) {
      visitorId = globalThis.crypto?.randomUUID?.();
      if (!visitorId) throw new Error('This browser cannot create a secure reaction ID.');
      window.localStorage.setItem(key, visitorId);
    }
    return visitorId;
  }

  async function react({ yapId, type }) {
    const result = await request('rpc/react_to_yap', {
      method: 'POST',
      prefer: 'return=representation',
      body: { p_yap_id: yapId, p_reaction: type, p_visitor_id: getVisitorId() },
    });
    return Array.isArray(result) ? result[0] : result;
  }

  window.YapWallBackend = { isConfigured, loadYaps, submitYap, submitReply, react };
})();
