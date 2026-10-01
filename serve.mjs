import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {basePath} from './site-config.mjs';
const root=fileURLToPath(new URL('./dist/',import.meta.url));
const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.png':'image/png','.svg':'image/svg+xml','.avif':'image/avif','.woff2':'font/woff2','.xml':'application/xml','.txt':'text/plain'};
http.createServer((req,res)=>{
 let pathname;try{pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);}catch{res.writeHead(400);return res.end('Invalid URL');}
 if(basePath&&pathname==='/'){res.writeHead(302,{Location:basePath+'/'});return res.end();}
 if(basePath&&!pathname.startsWith(basePath+'/')){res.writeHead(404);return res.end('Not found');}
 let file=path.resolve(root,'.'+pathname.slice(basePath.length));
 if(!file.startsWith(root)&&file!==path.resolve(root)){res.writeHead(404);return res.end('Not found');}
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404,{'Content-Type':types['.html']});return res.end(fs.readFileSync(path.join(root,'404.html')));}
 res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');fs.createReadStream(file).pipe(res);
}).listen(5173,'127.0.0.1',()=>console.log(`Preview: http://127.0.0.1:5173${basePath}/`));
