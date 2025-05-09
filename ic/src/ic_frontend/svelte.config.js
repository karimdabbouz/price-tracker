import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

import fs from 'fs';
import path from 'path';

const slugify = (str) => {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)+/g, '');
};

let products = [];
try {
  const productsPath = path.resolve(process.cwd(), 'src/lib/data/products.json');
  products = JSON.parse(fs.readFileSync(productsPath, 'utf-8'));
} catch (e) {
  products = [];
}

const productPageURLs = products.map(
  (p) =>
    `/products/${p.id}-${slugify(p.manufacturer)}-${p.manufacturer_id}-${slugify(p.name)}`
);

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    // adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
    // If your environment is not supported or you settled on a specific environment, switch out the adapter.
    // See https://kit.svelte.dev/docs/adapters for more information about adapters.
    adapter: adapter({
      pages: 'dist',
      assets: 'dist',
      fallback: undefined,
      precompress: false,
      strict: true,
    }),
    prerender: {
      entries: ['*', ...productPageURLs],
      crawl: true,
    }
  },
  preprocess: vitePreprocess()
};

export default config;
