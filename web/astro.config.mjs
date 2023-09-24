import { defineConfig } from 'astro/config'
import mdx from '@astrojs/mdx'
import tailwind from '@astrojs/tailwind'
import compress from 'astro-compress'

// https://astro.build/config
export default defineConfig({
  site: 'https://lissy93.github.io',
  base: '/git-into-open-source',
  compressHTML: true,
  integrations: [mdx(), tailwind(), compress()],
})
