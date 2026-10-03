import { createHash } from 'node:crypto';
import { readdirSync, readFileSync, realpathSync, writeFileSync } from 'node:fs';
import { dirname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

type Update = { path: string; original: string; updated: string };

function* htmlFiles(directory: string): Generator<string> {
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    const path = resolve(directory, entry.name);
    if (entry.isDirectory()) yield* htmlFiles(path);
    else if (entry.isFile() && /\.html$/i.test(entry.name)) yield path;
  }
}

export function collectVersionUpdates(root: string): Update[] {
  const base = realpathSync(root);
  const hashes = new Map<string, string>();
  const updates: Update[] = [];
  for (const path of htmlFiles(resolve(base, 'fesicsExternal'))) {
    const original = readFileSync(path, 'utf8');
    const updated = original.replace(/<(?:script|link)\b[^>]*>/gi, (tag) =>
      tag.replace(/\b(src|href)\s*=\s*(["'])(.*?)\2/gi, (attribute, name: string, quote: string, href: string) => {
        if (/^(?:[a-z][a-z\d+.-]*:|\/\/)/i.test(href)) return attribute;
        const hashIndex = href.indexOf('#');
        const fragment = hashIndex < 0 ? '' : href.slice(hashIndex);
        const address = hashIndex < 0 ? href : href.slice(0, hashIndex);
        const queryIndex = address.indexOf('?');
        const pathname = queryIndex < 0 ? address : address.slice(0, queryIndex);
        if (!/\.(js|css)$/i.test(pathname)) return attribute;
        const asset = realpathSync(
          pathname.startsWith('/')
            ? resolve(base, '.' + decodeURIComponent(pathname))
            : resolve(dirname(path), decodeURIComponent(pathname)),
        );
        if (!asset.startsWith(base + sep)) throw new Error(`Asset outside repository: ${href}`);
        let hash = hashes.get(asset);
        if (!hash) {
          hash = createHash('sha256').update(readFileSync(asset)).digest('hex').slice(0, 12);
          hashes.set(asset, hash);
        }
        const encodedAmpersand = address.includes('&amp;');
        const query = new URLSearchParams(queryIndex < 0 ? '' : address.slice(queryIndex + 1).replaceAll('&amp;', '&'));
        query.set('v', hash);
        const search = encodedAmpersand ? query.toString().replaceAll('&', '&amp;') : query.toString();
        const versioned = `${pathname}?${search}${fragment}`;
        return versioned === href ? attribute : `${name}=${quote}${versioned}${quote}`;
      }),
    );
    if (original !== updated) updates.push({ path, original, updated });
  }
  return updates;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const root = resolve(process.argv[2] || '.');
  try {
    const updates = collectVersionUpdates(root);
    if (process.argv.includes('--patch')) {
      const limitIndex = process.argv.indexOf('--patch-limit');
      const limit = limitIndex < 0 ? updates.length : Number(process.argv[limitIndex + 1]);
      if (updates.length) {
        const chunks = ['*** Begin Patch'];
        for (const update of updates.slice(0, limit)) {
          chunks.push(`*** Update File: ${update.path}`);
          const before = update.original.split('\n');
          const after = update.updated.split('\n');
          for (let line = 0; line < before.length; line++) {
            if (before[line] !== after[line]) chunks.push('@@', `-${before[line]}`, `+${after[line]}`);
          }
        }
        chunks.push('*** End Patch');
        process.stdout.write(chunks.join('\n') + '\n');
      }
    } else if (process.argv.includes('--check')) {
      process.stdout.write(`${updates.length} HTML files need JS/CSS version updates\n`);
      process.exitCode = updates.length ? 1 : 0;
    } else {
      // All references are validated before any page is changed.
      for (const update of updates) writeFileSync(update.path, update.updated);
      process.stdout.write(`Updated JS/CSS versions in ${updates.length} HTML files\n`);
    }
  } catch (error) {
    process.stderr.write((error instanceof Error ? error.message : String(error)) + '\n');
    process.exitCode = 1;
  }
}
