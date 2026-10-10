import fs from 'node:fs'; import path from 'node:path';
fs.copyFileSync('public/sw.js','sw.js');
fs.rmSync('dist',{recursive:true,force:true}); fs.mkdirSync('dist',{recursive:true});
for(const name of ['index.html','src','public','data']) fs.cpSync(name,path.join('dist',name),{recursive:true});
fs.copyFileSync('public/sw.js','dist/sw.js');
console.log('Built static PWA to dist/');
