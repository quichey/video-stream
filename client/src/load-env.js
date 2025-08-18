const fs = require('fs');
const dotenv = require('dotenv');

['.env.base', '.env.production', '.env.cloud'].forEach(file => {
  if (fs.existsSync(file)) {
    dotenv.config({ path: file });
  }
});

console.log("Environment variables loaded!");
console.log(process.env); // process.env now has all values
