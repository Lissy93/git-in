import { defineConfig } from 'astro/config'
import mdx from '@astrojs/mdx'
import tailwind from '@astrojs/tailwind'
import compress from 'astro-compress'
import dotenv from 'dotenv';
import sitemap from '@astrojs/sitemap';

dotenv.config();

const site = process.env.SITE_URL || undefined;
const base = process.env.BASE_PATH || '/';

export default defineConfig({
  site,
  base,
  compressHTML: true,
  integrations: [mdx(), tailwind(), compress(), sitemap()],
})
