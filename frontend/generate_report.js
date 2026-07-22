const fs = require('fs');
const path = require('path');

const srcDir = 'c:\\DACSS\\frontend\\src';
const rootDir = 'c:\\DACSS\\frontend';
const output = [];

output.push('# Project State Report\n');
output.push('### 1. File Tree of frontend/src\n```text');
function walk(dir) {
    if (!fs.existsSync(dir)) return;
    const items = fs.readdirSync(dir);
    for (const item of items) {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            output.push(`${fullPath}\\ (DIR)`);
            walk(fullPath);
        } else {
            output.push(`${fullPath} (${stat.size} bytes)`);
        }
    }
}
walk(srcDir);
output.push('```\n');

output.push('### 2. File Contents\n');

const requestedFiles = [
    path.join(srcDir, 'app', 'layout.tsx'),
    path.join(srcDir, 'app', 'page.tsx'),
    path.join(srcDir, 'app', 'globals.css'),
    path.join(rootDir, 'tailwind.config.js'),
    path.join(rootDir, 'tsconfig.json'),
    path.join(rootDir, 'next.config.js'),
    path.join(rootDir, 'next.config.mjs'),
    path.join(rootDir, 'next.config.ts'),
    path.join(srcDir, 'app', 'case-studies', '[id]', 'page.tsx'),
    path.join(srcDir, 'app', 'case-studies', '[id]', 'submit', 'page.tsx'),
    path.join(srcDir, 'app', 'case-studies', '[id]', 'result', '[submissionId]', 'page.tsx'),
    path.join(srcDir, 'app', 'profile', '[userId]', 'layout.tsx'),
    path.join(srcDir, 'app', 'profile', '[userId]', 'page.tsx')
];

if (fs.existsSync(path.join(srcDir, 'components'))) {
    const compFiles = fs.readdirSync(path.join(srcDir, 'components'));
    for (const f of compFiles) {
        if (f.endsWith('.tsx') || f.endsWith('.ts') || f.endsWith('.js')) {
            requestedFiles.push(path.join(srcDir, 'components', f));
        }
    }
}

for (const f of requestedFiles) {
    output.push(`#### FILE: ${f}`);
    if (!fs.existsSync(f)) {
        output.push(`(File does not exist)\n`);
        continue;
    }
    const stat = fs.statSync(f);
    if (stat.size === 0) {
        output.push('**EMPTY FILE**\n');
        continue;
    }
    const content = fs.readFileSync(f, 'utf8');
    const noComments = content.replace(/\/\/.*|\/\*[\s\S]*?\*\//g, '').trim();
    if (noComments === '') {
        output.push('**EMPTY FILE** (Only comments/whitespace found)\n```tsx\n' + content + '\n```\n');
    } else {
        output.push('```tsx\n' + content + '\n```\n');
    }
}

const outputPath = 'C:\\Users\\prani\\.gemini\\antigravity\\brain\\50de21de-3953-47b5-9caf-331b1c645ff2\\project_state_report.md';
const dir = path.dirname(outputPath);
if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
}
fs.writeFileSync(outputPath, output.join('\n'));
console.log('Report generated at ' + outputPath);
