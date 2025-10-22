# Copilot Instructions for AI Coding Agents

## Project Overview
- This is a Next.js web application bootstrapped with `create-next-app`.
- Main app code is in `src/app/` and `pages/`.
- Authentication is handled via NextAuth in `pages/api/auth/[...nextauth].ts`.
- Global styles are in `src/app/globals.css`.

## Architecture & Patterns
- Uses the Next.js App Router (`src/app/`) and legacy Pages Router (`pages/`).
- Entry point for the app is `src/app/page.tsx`.
- Layouts and global styles are managed in `src/app/layout.tsx` and `src/app/globals.css`.
- API routes are under `pages/api/`.
- Authentication logic is in `pages/api/auth/[...nextauth].ts`.
- Font optimization uses `next/font` and Geist font.

## Developer Workflows
- Start development server: `npm run dev` (or `yarn dev`, `pnpm dev`, `bun dev`).
- Hot-reloading is enabled for all changes in `src/app/` and `pages/`.
- Edit main page at `src/app/page.tsx`.
- Environment variables should be placed in `.env.local` (not committed).

## Conventions & Integration
- TypeScript is used throughout (`.ts`, `.tsx`).
- Project configuration: `tsconfig.json`, `next.config.ts`, `postcss.config.mjs`.
- Use modern React patterns (function components, hooks).
- Authentication is via NextAuth, see `pages/api/auth/[...nextauth].ts` for provider setup.
- Public assets are in `public/`.

## External Dependencies
- Next.js, React, NextAuth, Geist font, PostCSS.
- See `package.json` for all dependencies.

## Examples
- To add a new page: create a file in `src/app/` (App Router) or `pages/` (Pages Router).
- To add an API route: create a file in `pages/api/`.
- To update authentication: edit `pages/api/auth/[...nextauth].ts`.

## References
- [Next.js Documentation](https://nextjs.org/docs)
- [NextAuth Documentation](https://next-auth.js.org/)

---
If any section is unclear or missing, please provide feedback to improve these instructions.