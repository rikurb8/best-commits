# Best Commits Documentation

This directory contains the [Starlight](https://starlight.astro.build/) documentation site for Best Commits.

## Documentation Structure

The documentation uses a **hybrid approach**:

1. **Co-located docs** are synced from the parent repository (via `sync-docs.mjs`)
2. **Standalone docs** are written directly in `src/content/docs/`

### Co-located Documentation

These files are synced from the parent repository:

- `README.md` → `index.mdx` (Introduction)
- `tools/*/PROMPT.md` → `tools/*-prompt.md`
- `tools/*/SCORING_SYSTEM.md` → `tools/scoring.md`
- `evals/**/*.md` → `evals/*.md`
- `CLAUDE.md` → `development/claude.md`
- `PROMPT_IMPROVEMENTS.md` → `development/prompt-improvements.md`
- `specs/*.md` → `development/specs-*.md`

### Standalone Documentation

These files are written directly for the docs site:

- `installation.md` - Installation guide
- `troubleshooting.md` - Troubleshooting guide
- `configuration.md` - Configuration reference
- `tools/index.md` - Tools overview
- `tools/commit.md` - Commit tool documentation
- `tools/review.md` - Review tool documentation
- `reference/api-providers.md` - API providers guide
- `reference/environment.md` - Environment variables reference
- `reference/faq.md` - Frequently asked questions
- `development/architecture.md` - Architecture deep dive
- `development/contributing.md` - Contributing guide

## Development

### Prerequisites

- Node.js 18+
- npm or pnpm

### Local Development

```bash
# Install dependencies
npm install

# Sync co-located docs and start dev server
npm run dev

# Or sync docs separately
npm run sync
npm start
```

The dev server will be available at `http://localhost:4321`.

### Building

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Syncing Documentation

The `sync-docs.mjs` script copies co-located documentation from the parent directory and adds Starlight frontmatter:

```bash
# Manual sync
npm run sync
```

**Note**: The sync runs automatically before `dev` and `build` commands.

## Project Structure

```
docs/
├── src/
│   ├── content/
│   │   ├── docs/           # Documentation content
│   │   │   ├── index.mdx   # Synced from ../README.md
│   │   │   ├── installation.md
│   │   │   ├── configuration.md
│   │   │   ├── troubleshooting.md
│   │   │   ├── tools/      # Tool documentation
│   │   │   ├── reference/  # Reference documentation
│   │   │   ├── development/ # Development guides
│   │   │   └── evals/      # Evaluation documentation
│   │   └── config.ts       # Content collections config
│   └── styles/
│       └── custom.css      # Custom styles
├── public/                 # Static assets
├── astro.config.mjs        # Astro configuration
├── tsconfig.json           # TypeScript configuration
├── package.json            # Dependencies and scripts
├── sync-docs.mjs           # Documentation sync script
└── README.md               # This file
```

## Adding Documentation

### Adding a New Page

1. Create a new `.md` or `.mdx` file in `src/content/docs/`:

   ```bash
   touch src/content/docs/new-page.md
   ```

2. Add frontmatter:

   ```markdown
   ---
   title: Page Title
   description: Page description for SEO
   ---

   Your content here...
   ```

3. Update `astro.config.mjs` sidebar if needed:

   ```javascript
   sidebar: [
     {
       label: 'Section',
       items: [
         { label: 'New Page', slug: 'new-page' },
       ],
     },
   ],
   ```

### Syncing Co-located Documentation

To add a new co-located document to sync:

1. Edit `sync-docs.mjs`:

   ```javascript
   const docMappings = [
     // ... existing mappings ...
     { src: '../path/to/file.md', dest: 'destination/path.md', title: 'Page Title' },
   ];
   ```

2. Run sync:

   ```bash
   npm run sync
   ```

### Updating Existing Documentation

For **co-located docs**: Edit the source file in the parent repository.

For **standalone docs**: Edit directly in `src/content/docs/`.

## Styling

Custom styles are in `src/styles/custom.css`. The documentation uses Starlight's default theme with enhancements for:

- Code blocks
- Tables
- Callouts
- Badges
- Responsive design

## Configuration

### Starlight Configuration

Edit `astro.config.mjs` to configure:

- Site title and description
- Sidebar navigation
- Social links
- Custom CSS
- Plugins and integrations

### Content Collections

Content configuration is in `src/content.config.ts`. Currently uses the default Starlight docs schema.

## Deployment

The documentation can be deployed to any static hosting service:

### GitHub Pages

```bash
# Build
npm run build

# Deploy dist/ directory to gh-pages branch
```

### Netlify

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"
```

### Vercel

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist"
}
```

## Troubleshooting

### Dev server won't start

```bash
# Clear cache and reinstall
rm -rf node_modules .astro
npm install
npm run dev
```

### Synced docs not appearing

```bash
# Manually run sync
npm run sync

# Check sync script output for errors
```

### Build errors

```bash
# Check for TypeScript errors
npm run astro check

# Validate markdown/MDX files
# Look for unclosed tags, invalid frontmatter
```

## Contributing

See the [Contributing Guide](./src/content/docs/development/contributing.md) for information on how to contribute to the documentation.

## License

Same as the parent project (MIT).
