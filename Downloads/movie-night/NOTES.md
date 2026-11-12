# Notes: Lab 1

1. **Where are `<html>` and `<body>`?** it's in the `app/layout.tsx`which is the root layout.

2. **Which file renders `/`?** `the app/page.tsx`.

3. **Folder for images and static files?** `public/`. Files there are served from the root URL, so `public/next.svg` is referenced as `/next.svg`.

4. **What does `tsconfig.json` do?** It is the TypeScript configuration: compiler options and path aliases such as `@/*`. It tells TypeScript how to check the project.

5. **What does `@/*` mean?** It is an alias for the project root, so that you avoid long relative paths. Example: `import { getMovies } from "@/lib/movies";` points to `lib/movies.ts`.

6. **What does `layout.tsx` import from `next/font/google`?** The Geist and Geist_Mono fonts, at build time Next.js downloads the font files and serves them with the app itself, so the browser makes no request to Google.

7. **`layout.tsx` vs `page.tsx`?** A layout wraps pages and stays the same when you navigate. A page is the content of one specific URL.

8. **Where does a navbar for every page go?** In `app/layout.tsx` it's inside `<body>` and above `{children}`.

9. **What is `globals.css` for?** a global styles for the whole app including the Tailwind import and it is imported in `app/layout.tsx`.

10. **What is `AGENTS.md`?** A file of instructions for AI coding assistants and the app does not need it to run.