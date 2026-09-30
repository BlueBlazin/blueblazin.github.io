// Build-only renderer. Student pages load the finished SVG, never Mermaid/Chromium.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';
import { renderMermaid } from '@mermaid-js/mermaid-cli';
const root=path.dirname(fileURLToPath(import.meta.url));
const config=JSON.parse(fs.readFileSync(path.join(root,'mermaid-config.json'),'utf8'));
const jobs=JSON.parse(fs.readFileSync(0,'utf8'));
const launch={headless:true};
if(process.env.COURSE_CHROME_EXECUTABLE) launch.executablePath=process.env.COURSE_CHROME_EXECUTABLE;
if(process.env.COURSE_CHROME_ARGS) launch.args=JSON.parse(process.env.COURSE_CHROME_ARGS);
const browser=await puppeteer.launch(launch);
try {
  for(const job of jobs){
    const result=await renderMermaid(browser,job.source,job.format || 'svg',{
      mermaidConfig:{...config,deterministicIDSeed:job.id},
      svgId:job.id,backgroundColor:'#ffffff',fontEmbed:false,
      viewport:{width:1000,height:900,deviceScaleFactor:1}
    });
    fs.writeFileSync(job.output,result.data);
  }
} finally {await browser.close();}
