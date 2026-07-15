import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath, URL } from 'node:url';

const projectFile = (path: string) => fileURLToPath(new URL(path, import.meta.url));

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      input: { popup: projectFile('./index.html'), background: projectFile('./src/background.ts'), contentScript: projectFile('./src/contentScript.ts') },
      output: { entryFileNames: (chunk) => chunk.name === 'popup' ? 'assets/[name]-[hash].js' : '[name].js', chunkFileNames: 'assets/[name]-[hash].js', assetFileNames: 'assets/[name]-[hash][extname]' }
    }
  }
});
