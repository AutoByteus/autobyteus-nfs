from pathlib import Path
import subprocess,hashlib,json
E=Path(__file__).resolve().parent
p=Path((E/'scratch-path.txt').read_text().strip())
a=p/'tools/go1.27.2.darwin-arm64.tar.gz'
assert hashlib.sha256(a.read_bytes()).hexdigest()=='76812b213b1b2302c978d28fa52fa92d541704b9e7d9d5db8002c50e4018c4c5'
# Archive passed official metadata SHA assertion in preserved initial attempt.
# System tar avoids relying on Python's newer extractall(filter=) interface.
subprocess.run(['tar','-xzf',str(a),'-C',str(p/'tools')],check=True)
g=p/'tools/go/bin/go'
(E/'toolchain.json').write_text(json.dumps({'go':str(g),'version':subprocess.check_output([str(g),'version'],text=True),'archive':str(a),'sha256':hashlib.sha256(a.read_bytes()).hexdigest(),'initialFailurePreserved':'prepare-console.log'},indent=2)+'\n')
print(g)
