from pathlib import Path
import hashlib,json,subprocess,re
B=Path('/workspace/cloud-setup/redesign/firmware-candidate');O=Path('/workspace/cloud-setup/redesign/core-review');T=Path('/workspace/cloud-setup/toolchains/xpack-arm-none-eabi-gcc-13.3.1-1.1/bin');od=str(T/'arm-none-eabi-objdump');nm=str(T/'arm-none-eabi-nm');reade=str(T/'arm-none-eabi-readelf');fail=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sourcepaths(r):return {str(p.relative_to(r)):p for p in r.rglob('*') if p.is_file() and not any(x.startswith('build') or x=='.git' for x in p.relative_to(r).parts) and (p.name=='Makefile' or p.suffix in ['.cpp','.c','.h','.hpp','.s','.lds'])}
scope=json.loads((B/'scope.json').read_text());manifest=json.loads((B/'build-artifacts.json').read_text());sourcehash={}
for group,folder in [('libDaisy','libDaisy'),('bootloader','bootloader-source')]:
 for k,v in scope['sources'][group]['changed_files'].items():
  actual=sha(B/folder/k);sourcehash[folder+'/'+k]=actual
  if actual!=v['candidate_sha256']:fail.append('Source hash '+folder+'/'+k)
 for patch in ['libDaisy-teresina.patch' if group=='libDaisy' else 'bootloader-teresina.patch']:
  if sha(B/patch)!=scope['sources'][group]['patch_sha256']:fail.append('Patch hash '+patch)
artifacts={k:{**v,'hash_matches':sha(B/k)==v['sha256'],'bytes_match':(B/k).stat().st_size==v['bytes']} for k,v in manifest.items()}
for k,v in artifacts.items():
 if not v['hash_matches'] or not v['bytes_match']:fail.append('Artifact '+k)
x=sourcepaths(B/'upstream-libDaisy');y=sourcepaths(B/'libDaisy');sdkdelta=sorted(k for k in x.keys()|y.keys() if not(k in x and k in y) or x[k].read_bytes()!=y[k].read_bytes());assert sdkdelta==sorted(scope['changed_lib_files'])
x=sourcepaths(Path('/workspace/cloud-setup/redesign/sources/DaisyBootloader'));y=sourcepaths(B/'bootloader-source');bootdelta=sorted(k for k in x.keys()|y.keys() if not(k in x and k in y) or x[k].read_bytes()!=y[k].read_bytes());assert bootdelta==sorted(scope['sources']['bootloader']['changed_files'])
def code(p):return '\n'.join(subprocess.check_output([od,'-dr',str(p)],text=True).splitlines()[2:])
def syms(p):return {tuple(l.split()[-2:]) for l in subprocess.check_output([nm,'-g','--defined-only',str(p)],text=True).splitlines() if len(l.split())>=3}
off={}
for f in ['sdram.o','daisy_patch_sm.o','system.o']:
 off[f]=code(next((B/'upstream-libDaisy/build').rglob(f)))==code(next((B/'libDaisy/build-default').rglob(f)))
 if not off[f]:fail.append('Default-off '+f)
a=syms(B/'upstream-libDaisy/build/libdaisy.a');z=syms(B/'libDaisy/build/libdaisy.a');assert a==z
linked=[]
def fn(t,name):
 marker='<'+name+'>:';i=t.find(marker);assert i>=0,name;return t[i:t.find('\n\n',i)]
for k in manifest:
 if not k.endswith('.elf'):continue
 p=B/k;s=subprocess.check_output([od,'-dC',str(p)],text=True);d=fn(s,'SdramHandle::DeviceInit()');init=fn(s,'daisy::System::Init(daisy::System::Config const&)');clk=fn(s,'daisy::System::ConfigureClocks()');h=subprocess.check_output([reade,'-h',str(p)],text=True)
 checks={'count369_at_refresh_write':'#369' in d and 'HAL_SDRAM_ProgramRefreshRate' in d,'geometry_gate_compares_0x1e9':'#489' in d,'RGE2_actual_register_gate':'#128' in d,'M3_encoded_register_gate':'#12288' in d,'PLL2_N37_encoded_gate':'#36' in d,'RevV_before_HAL_Init':'#8195' in init and init.index('HAL_GetREVID')<init.index('HAL_Init'),'fresh_COUNT_and_SDCLK_before_HAL_Init':'#16382' in init and '#3072' in init and init.index('#3072')<init.index('HAL_Init'),'PLL1_both_integer_N_values':'#299' in clk and '#249' in clk,'four_checked_startup_commands':d.count('<HAL_SDRAM_SendCommand>')==4}
 for name,ok in checks.items():
  if not ok:fail.append(k+' '+name)
 linked.append({'elf':k,'sha256':sha(p),'entry':next(l.strip() for l in h.splitlines() if 'Entry point' in l),'checks':checks})
validation={}
for v in ['0','1','','0 1','invalid']:
 r=subprocess.run(['make','--question','TERESINA_SDRAM_PROFILE='+v],cwd=B/'libDaisy',capture_output=True,text=True);validation[v]=r.returncode
assert validation=={'0':1,'1':0,'':2,'0 1':2,'invalid':2}
text=subprocess.check_output([str(B/'profile-test')],text=True).strip();assert '17 invalid' in text and '7936' in text
bootbin=next(k for k in artifacts if k.endswith('.bin'));used=artifacts[bootbin]['bytes'];assert used<=131072
res={'status':'PASS for bounded source/linked prototype review; hardware tests unrun, production unqualified','passed':not fail,'scope_sha256':sha(B/'scope.json'),'artifact_manifest_sha256':sha(B/'build-artifacts.json'),'source_hashes':sourcehash,'patch_hashes':{n:sha(B/n) for n in ['libDaisy-teresina.patch','bootloader-teresina.patch']},'source_deltas':{'SDK':sdkdelta,'bootloader':bootdelta},'artifacts':artifacts,'linked_reviews':linked,'SDK_default_off_machine_code_and_relocations':off,'SDK_added_or_removed_global_symbols':[],'SDK_existing_public_headers_unchanged':True,'bootloader_API_delta':'Additive ProcessControls method; AudioProcess and other existing APIs preserved','make_question_profile_exit_codes':validation,'host_profile_test':text,'bootloader_flash_bytes':used,'bootloader_flash_limit_bytes':131072,'bootloader_flash_headroom_bytes':131072-used,'bootloader_flash_headroom_percent':(131072-used)*100/131072,'runtime_clock_modes_hz':{'Boost':478400000,'Default':398400000,'PLL2_R':200000000,'SDCLK':100000000},'refresh_count':369,'hardware_tests_run':False,'production_qualified':False,'failures':fail,'explicit_limits':['Oscillator frequency/load/startup/drive and1000ppm bound require hardware qualification','SDRAM command timing/max-load refresh/temperature/supply tests unrun','TimerHandle nominal microsecond conversion bias0.08368% Boost/0.10050% Default; no exact timing equivalence','Upstream USB/SD internal initialization statuses are not comprehensively propagated','Only selected SDK/archive/profile supported; stock or arbitrary third-party binaries unsupported','Concurrent conflicting profile builds in one directory unsupported','No live clock/FMC reinitialization, SDRAM execution/early-access or retention-across-reset support']}
(O/'firmware-final-review.json').write_text(json.dumps(res,indent=2));print(json.dumps({'passed':not fail,'source_hashes_checked':len(sourcehash),'artifact_hashes_checked':len(artifacts),'linked_ELFs_checked':len(linked),'default_off':off,'host':text,'bootloader_flash_bytes':used,'headroom_bytes':131072-used,'failures':fail},indent=2));assert not fail
