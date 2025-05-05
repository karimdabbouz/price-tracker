import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import fs from 'fs';


const slugify = (str) => {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)+/g, '');
};

const products = JSON.parse(fs.readFileSync('src/lib/data/products.json', 'utf-8'));

const productEntries = products.map(
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
      entries: ['*', ...productEntries],
      crawl: true,
    }
  },
  preprocess: vitePreprocess()
};

export default config;
