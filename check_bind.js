const {execSync} = require('child_process');
const skillDir = 'D:\\QClaw\\resources\\openclaw\\config\\skills\\email-skill\\scripts\\windows';

const cmd = `cmd /c "cd /d ${skillDir} && email_gateway.cmd bind-check --email 18339435211@139.com"`;
try {
  const r = execSync(cmd, {encoding:'utf8', timeout:20000});
  console.log('Result:', r);
} catch(e) {
  console.log('Exit code:', e.status);
  console.log('Stdout:', e.stdout ? e.stdout.substring(0,500) : 'none');
  console.log('Stderr:', e.stderr ? e.stderr.substring(0,500) : 'none');
}
