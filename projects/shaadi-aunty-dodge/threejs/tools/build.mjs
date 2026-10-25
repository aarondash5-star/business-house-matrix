import {build} from 'esbuild';import {cp,copyFile,mkdir,stat} from 'node:fs/promises';import {gzipSync} from 'node:zlib';import {readFile} from 'node:fs/promises';
await mkdir('dist',{recursive:true});
await build({entryPoints:['src/main.js'],bundle:true,minify:true,format:'esm',target:'es2022',outfile:'dist/main.js',logLevel:'warning',legalComments:'none'});
await copyFile('index.html','dist/index.html');await mkdir('dist/assets',{recursive:true});
await cp('assets','dist/assets',{recursive:true,force:true});
const s=await readFile('dist/main.js');const gz=gzipSync(s,{level:9});
console.log(JSON.stringify({js_bytes:s.byteLength,js_gzip_bytes:gz.byteLength,html_bytes:(await stat('dist/index.html')).size,webgl:'webgl2',renderer:'three@0.186.1'}));

