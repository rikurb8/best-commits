import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
  integrations: [
    starlight({
      title: 'Best Commits',
      description: 'AI-powered Git workflow automation tools',
      social: {
        github: 'https://github.com/yourusername/best-commits',
      },
      sidebar: [
        {
          label: 'Getting Started',
          items: [
            { label: 'Introduction', slug: 'index' },
            { label: 'Installation', slug: 'installation' },
            { label: 'Configuration', slug: 'configuration' },
            { label: 'Troubleshooting', slug: 'troubleshooting' },
          ],
        },
        {
          label: 'Tools',
          items: [
            { label: 'Overview', slug: 'tools/index' },
            { label: 'Commit Tool', slug: 'tools/commit' },
            { label: 'Review Tool', slug: 'tools/review' },
            { label: 'Commit Prompt', slug: 'tools/commit-prompt' },
            { label: 'Review Prompt', slug: 'tools/review-prompt' },
            { label: 'Scoring System', slug: 'tools/scoring' },
          ],
        },
        {
          label: 'Evaluations',
          autogenerate: { directory: 'evals' },
        },
        {
          label: 'Development',
          items: [
            { label: 'Architecture', slug: 'development/architecture' },
            { label: 'Contributing', slug: 'development/contributing' },
            { label: 'Claude Code Guide', slug: 'development/claude' },
          ],
        },
        {
          label: 'Reference',
          items: [
            { label: 'API Providers', slug: 'reference/api-providers' },
            { label: 'Environment Variables', slug: 'reference/environment' },
            { label: 'FAQ', slug: 'reference/faq' },
          ],
        },
      ],
      customCss: ['./src/styles/custom.css'],
    }),
  ],
});
