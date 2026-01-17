import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig(({ mode }) => ({
  base: mode === "development" ? "/" : "/personal-website/",
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, "index.html"),
        interests: resolve(__dirname, "interests/index.html"),
        wallstreetbets: resolve(__dirname, "wallstreetbets/index.html")
      }
    }
  }
}));
