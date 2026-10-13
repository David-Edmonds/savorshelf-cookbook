"""Build resource-backed APK and AAB with the retained signer. Never creates a key."""
from pathlib import Path
import argparse, subprocess, tempfile, zipfile, hashlib, json, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
CERT='f6eac7b4b42570c9c29a73504a73a0f228e09d4a645651c7d9ff2370581b5eb3'
p=argparse.ArgumentParser(description=__doc__)
for name in ['jdk','tools','platform','bundletool','signing-backup']:p.add_argument('--'+name,type=Path,required=True)
mode=p.add_mutually_exclusive_group()
mode.add_argument('--public-samples',action='store_true',default=True,help='Default: exclude private/imported corpus and stage three original sample drafts.')
mode.add_argument('--private-review',dest='public_samples',action='store_false',help='Local private review only; never upload this corpus.')
a=p.parse_args(); ns='{http://schemas.android.com/apk/res/android}'
web=ROOT/'web'
if a.public_samples:
 import importlib.util
 spec=importlib.util.spec_from_file_location('public_web',ROOT/'scripts/prepare-public-web.py');public=importlib.util.module_from_spec(spec);spec.loader.exec_module(public)
 web=public.prepare(ROOT/'build/public-web')
m=ET.parse(ROOT/'android/AndroidManifest.xml').getroot();version=m.get(ns+'versionName');code=int(m.get(ns+'versionCode'))
assert m.get('package')=='com.recipekeeper.ourtable' and code>26
assert int(m.find('uses-sdk').get(ns+'targetSdkVersion'))>=36
out=ROOT/'build/out';out.mkdir(parents=True,exist_ok=True)
java=a.jdk/'bin/java.exe';aapt=a.tools/'aapt2.exe'
def run(cmd):
 result=subprocess.run([str(x) for x in cmd],capture_output=True,text=True)
 if result.returncode:raise RuntimeError(result.stdout+'\n'+result.stderr)
 return result.stdout
with tempfile.TemporaryDirectory(prefix='leggacy-private-build-') as directory:
 t=Path(directory)
 with zipfile.ZipFile(a.signing_backup) as z:
  (t/'signing.jks').write_bytes(z.read('.local-signing/preview.jks'))
  (t/'password.txt').write_bytes(z.read('.local-signing/password.txt'))
 cert=subprocess.check_output([str(a.jdk/'bin/keytool.exe'),'-exportcert','-keystore',str(t/'signing.jks'),'-storepass:file',str(t/'password.txt'),'-alias','ourtable-preview'],stderr=subprocess.PIPE)
 assert hashlib.sha256(cert).hexdigest()==CERT,'Original signing identity required'
 for n in ['classes','dex','generated']:(t/n).mkdir()
 run([aapt,'compile','--dir',ROOT/'android/res','-o',t/'res.zip'])
 for proto in [False,True]:
  cmd=[aapt,'link','-o',t/('proto.apk' if proto else 'base.apk'),'-I',a.platform/'android.jar','--manifest',ROOT/'android/AndroidManifest.xml','-A',web,t/'res.zip']
  if proto:cmd.append('--proto-format')
  else:cmd+=['--java',t/'generated']
  run(cmd)
 sources=list((ROOT/'android/src').rglob('*.java'))+list((t/'generated').rglob('*.java'))
 (t/'sources.txt').write_text('\n'.join('"'+x.as_posix()+'"' for x in sources),'utf-8')
 run([a.jdk/'bin/javac.exe','--release','8','-encoding','UTF-8','-cp',a.platform/'android.jar','-d',t/'classes','@'+str(t/'sources.txt')])
 run([a.jdk/'bin/jar.exe','cf',t/'classes.jar','-C',t/'classes','.'])
 run([java,'-cp',a.tools/'lib/d8.jar','com.android.tools.r8.D8','--lib',a.platform/'android.jar','--min-api','26','--output',t/'dex',t/'classes.jar'])
 with zipfile.ZipFile(t/'base.apk','a',zipfile.ZIP_DEFLATED) as z:
  for dex in (t/'dex').glob('*.dex'):z.write(dex,dex.name)
 apk=out/f'Leggacy-{version}.apk';bundle=out/f'Leggacy-{version}.aab'
 run([a.tools/'zipalign.exe','-f','-p','4',t/'base.apk',t/'aligned.apk'])
 run([java,'-jar',a.tools/'lib/apksigner.jar','sign','--ks',t/'signing.jks','--ks-pass','file:'+str(t/'password.txt'),'--ks-key-alias','ourtable-preview','--out',apk,t/'aligned.apk'])
 assert CERT in run([java,'-jar',a.tools/'lib/apksigner.jar','verify','--verbose','--print-certs',apk])
 with zipfile.ZipFile(t/'proto.apk') as source,zipfile.ZipFile(t/'module.zip','w',zipfile.ZIP_DEFLATED) as module:
  for name in source.namelist():
   if name.endswith('/'):continue
   mapped='manifest/AndroidManifest.xml' if name=='AndroidManifest.xml' else name if name.startswith(('res/','assets/')) or name=='resources.pb' else 'root/'+name
   module.writestr(mapped,source.read(name))
  for dex in (t/'dex').glob('*.dex'):module.write(dex,'dex/'+dex.name)
 run([java,'-jar',a.bundletool,'build-bundle','--modules='+str(t/'module.zip'),'--output='+str(bundle),'--overwrite'])
 run([a.jdk/'bin/jarsigner.exe','-keystore',t/'signing.jks','-storepass:file',t/'password.txt',bundle,'ourtable-preview'])
 run([java,'-jar',a.bundletool,'validate','--bundle='+str(bundle)])
 assert 'jar verified' in run([a.jdk/'bin/jarsigner.exe','-verify',bundle]).lower()
 run([java,'-jar',a.bundletool,'build-apks','--bundle='+str(bundle),'--output='+str(t/'release.apks'),'--mode=universal','--ks='+str(t/'signing.jks'),'--ks-key-alias=ourtable-preview','--ks-pass=file:'+str(t/'password.txt'),'--key-pass=file:'+str(t/'password.txt'),'--overwrite'])
 with zipfile.ZipFile(t/'release.apks') as z:
  bundle_apk=out/f'Leggacy-{version}-from-bundle.apk';bundle_apk.write_bytes(z.read('universal.apk'))
 assert CERT in run([java,'-jar',a.tools/'lib/apksigner.jar','verify','--verbose','--print-certs',bundle_apk])
 info=run([aapt,'dump','badging',apk]);assert f"versionCode='{code}' versionName='{version}'" in info and "application-label:'Leggacy'" in info and "targetSdkVersion:'36'" in info
 assets=list(x for x in web.rglob('*') if x.is_file())
 for file in [apk,bundle]:
  with zipfile.ZipFile(file) as z:
   assert z.testzip() is None
   prefix='base/assets/' if file==bundle else 'assets/'
   for x in assets:assert z.read(prefix+x.relative_to(web).as_posix())==x.read_bytes()
 report={'version':version,'versionCode':code,'applicationId':m.get('package'),'targetSdk':36,'contentMode':'public-samples' if a.public_samples else 'private-review-only','certificateSha256':CERT,'assetsMatched':len(assets),'apkSha256':hashlib.sha256(apk.read_bytes()).hexdigest(),'aabSha256':hashlib.sha256(bundle.read_bytes()).hexdigest(),'bundleValidated':True,'bundleApkSignatureVerified':True,'finalLogoSupplied':False,'storeStatus':'prepared','physicalPhoneTested':False}
 (out/'verification.json').write_text(json.dumps(report,indent=2),'utf-8');print(json.dumps(report,indent=2))
