function getPublicSupabaseKey() {
  const key = process.env.SUPABASE_ANON_KEY || '';
  if (!key) return '';

  if (key.startsWith('sb_publishable_')) return key;

  const payload = key.split('.')[1];
  if (!payload) return '';

  try {
    const decoded = JSON.parse(Buffer.from(payload, 'base64url').toString('utf8'));
    return decoded.role === 'anon' ? key : '';
  } catch {
    return '';
  }
}

module.exports = (req, res) => {
  const url = process.env.SUPABASE_URL || '';
  const anonKey = getPublicSupabaseKey();

  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Content-Type', 'text/javascript; charset=utf-8');

  const script = `window.YAP_WALL_SUPABASE_CONFIG = ${JSON.stringify({
    url,
    anonKey,
  }).replace(/</g, '\\u003c')};\n`;

  res.status(200).send(script);
};
