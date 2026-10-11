const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const host = process.env.HOST || '127.0.0.1';
const port = Number(process.env.PORT || 3000);
const contentTypes = {
  '.css': 'text/css; charset=utf-8',
  '.html': 'text/html; charset=utf-8',
  '.ico': 'image/x-icon',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
};

function getPublicSupabaseKey() {
  const key = process.env.SUPABASE_ANON_KEY || '';
  if (key.startsWith('sb_publishable_')) return key;

  const payload = key.split('.')[1];
  if (payload) {
    try {
      if (JSON.parse(Buffer.from(payload, 'base64url').toString('utf8')).role === 'anon') {
        return key;
      }
    } catch {
      // Invalid or non-JWT values are not safe to send to a browser.
    }
  }

  return '';
}

const server = http.createServer((request, response) => {
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    response.writeHead(405, { Allow: 'GET, HEAD' }).end();
    return;
  }

  let pathname;
  try {
    pathname = decodeURIComponent(new URL(request.url, `http://${host}`).pathname);
  } catch {
    response.writeHead(400).end('Invalid URL');
    return;
  }

  if (pathname === '/supabase-config.js') {
    const publicConfig = {
      url: process.env.SUPABASE_URL || '',
      anonKey: getPublicSupabaseKey(),
    };
    const script = `window.YAP_WALL_SUPABASE_CONFIG = ${JSON.stringify(publicConfig).replace(/</g, '\\u003c')};\n`;
    response.writeHead(200, {
      'Cache-Control': 'no-store',
      'Content-Type': 'text/javascript; charset=utf-8',
    });
    response.end(request.method === 'HEAD' ? undefined : script);
    return;
  }

  const segments = pathname.split('/').filter(Boolean);
  if (segments.some((segment) => segment.startsWith('.'))) {
    response.writeHead(404).end('Not found');
    return;
  }

  const requestedPath = pathname === '/' ? 'index.html' : segments.join(path.sep);
  const filePath = path.resolve(root, requestedPath);
  if (filePath !== root && !filePath.startsWith(`${root}${path.sep}`)) {
    response.writeHead(403).end('Forbidden');
    return;
  }

  fs.stat(filePath, (error, fileStats) => {
    if (error || !fileStats.isFile()) {
      response.writeHead(404).end('Not found');
      return;
    }

    response.writeHead(200, {
      'Cache-Control': 'no-cache',
      'Content-Length': fileStats.size,
      'Content-Type': contentTypes[path.extname(filePath)] || 'application/octet-stream',
    });
    if (request.method === 'HEAD') {
      response.end();
      return;
    }
    fs.createReadStream(filePath).pipe(response);
  });
});

server.listen(port, host, () => {
  console.log(`Podcast site listening at http://${host}:${port}`);
});