// src/load-env.js
const fs = require("fs");
const path = require("path");
const dotenv = require("dotenv");

// List of env files to merge (order matters: later files override earlier)
const envFiles = [
  path.resolve(__dirname, "../.env.base"),
  path.resolve(__dirname, "../.env.production"),
  path.resolve(__dirname, "../.env.cloud"),
  path.resolve(__dirname, "../env/azure/.env"),
];

// Merge all env files into a single object
let mergedEnv = {};

envFiles.forEach((file) => {
  if (fs.existsSync(file)) {
    const parsed = dotenv.parse(fs.readFileSync(file));
    mergedEnv = { ...mergedEnv, ...parsed };
  }
});

// Ensure all keys have REACT_APP_ prefix for CRA
Object.keys(mergedEnv).forEach((key) => {
  if (!key.startsWith("REACT_APP_")) {
    const value = mergedEnv[key];
    delete mergedEnv[key];
    mergedEnv[`REACT_APP_${key}`] = value;
  }
});

// Write merged env to project root as .env.generated
const outputFile = path.resolve(__dirname, "../.env.production");
const outputContent = Object.entries(mergedEnv)
  .map(([k, v]) => `${k}=${v}`)
  .join("\n");

fs.writeFileSync(outputFile, outputContent);

console.log(`Merged environment variables written to ${outputFile}`);
