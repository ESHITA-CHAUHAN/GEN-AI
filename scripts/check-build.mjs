import { access, readFile } from "node:fs/promises";

const requiredFiles = [
  "public/index.html",
  "public/assets/styles.css",
  "public/assets/app.js",
  "netlify/functions/rewrite.mjs",
  "netlify/functions/status.mjs",
  "netlify/functions/ai-config.mjs",
];

for (const file of requiredFiles) {
  await access(new URL("../" + file, import.meta.url));
}

const html = await readFile(new URL("../public/index.html", import.meta.url), "utf8");
if (!html.includes("/assets/app.js") || !html.includes("/assets/styles.css")) {
  throw new Error("The page is missing its stylesheet or application script.");
}

console.log("Build files are present.");
