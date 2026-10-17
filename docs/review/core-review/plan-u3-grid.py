from pathlib import Path
from decimal import Decimal as D,ROUND_HALF_UP
import json,sys,hashlib,collections
sys.path.insert(0,'/workspace/cloud-setup/tools/kicad-happy/skills/kicad/scripts')
from sexp_parser import parse_file,find_all,find_first
B=Path('/workspace/cloud-setup/redesign/organized-candidate');OUT=Path('/workspace/cloud-setup/redesign/core-review');grid=D('1.27')
def decstr(x):return str(x.quantize(D('0.01')))
root=parse_file(str(B/'memory-flash.kicad_sch'));s=next(s for s in find_all(root,'symbol') if any(p[1:3]==['Reference','U3'] for p in find_all(s,'property')));at=find_first(s,'at');ax,ay=D(at[1]),D(at[2]);assert at[3]=='0';assert ax%grid==0 and ay%grid==0
lib=next(v for v in find_all(find_first(root,'lib_symbols'),'symbol') if v[1]=='TeresinaRack:AS4C16M32MSA');pin_nodes=[p for u in find_all(lib,'symbol') for p in find_all(u,'pin')];assert len(pin_nodes)==90
external_root=parse_file(str(B/'TeresinaRack.kicad_sym'));external_symbol=next(v for v in find_all(external_root,'symbol') if v[1]=='AS4C16M32MSA');external_pins=[p for u in find_all(external_symbol,'symbol') for p in find_all(u,'pin')];assert pin_nodes==external_pins
wires=find_all(root,'wire');labels=find_all(root,'global_label');ncs=find_all(root,'no_connect');moves=[]
for p in pin_nodes:
 n=find_first(p,'number')[1];name=find_first(p,'name')[1];pa=find_first(p,'at');px,py=D(pa[1]),D(pa[2]);newy=(py/grid).quantize(D(1),rounding=ROUND_HALF_UP)*grid;oldworld=(ax+px,ay-py);newworld=(ax+px,ay-newy);deltaY=newworld[1]-oldworld[1];connected=[]
 for w in wires:
  points=[(D(pt[1]),D(pt[2])) for pt in find_first(w,'pts')[1:]]
  if oldworld in points:
   other=points[1] if points[0]==oldworld else points[0];assert oldworld[1]==other[1]
   ls=[l for l in labels if (D(find_first(l,'at')[1]),D(find_first(l,'at')[2]))==other];assert len(ls)==1,(n,other,ls)
   connected.append({'wire_uuid':find_first(w,'uuid')[1],'old_points_mm':[[decstr(x),decstr(y)] for x,y in points],'new_points_mm':[[decstr(x),decstr(y+deltaY)] for x,y in points],'label_uuid':find_first(ls[0],'uuid')[1],'label_name':ls[0][1],'old_label_at_mm':[decstr(x) for x in other],'new_label_at_mm':[decstr(other[0]),decstr(other[1]+deltaY)],'translate_all_label_property_at_by_mm':['0.00',decstr(deltaY)]})
 nc=[c for c in ncs if (D(find_first(c,'at')[1]),D(find_first(c,'at')[2]))==oldworld]
 if p[1]=='no_connect':assert len(nc)==1 and not connected
 else:assert len(connected)==1 and not nc
 moves.append({'number':n,'name':name,'electrical_type':p[1],'shape':p[2],'direction_degrees':pa[3],'length_mm':find_first(p,'length')[1],'old_local_mm':[decstr(px),decstr(py)],'new_local_mm':[decstr(px),decstr(newy)],'old_connection_world_mm':[decstr(x) for x in oldworld],'new_connection_world_mm':[decstr(x) for x in newworld],'world_delta_mm':['0.00',decstr(deltaY)],'stub_moves':connected,'no_connect_uuid':find_first(nc[0],'uuid')[1] if nc else None})
assert len(set(m['number'] for m in moves))==90
assert len(set(tuple(m['new_local_mm']) for m in moves))==90
assert all(D(v)%grid==0 for m in moves for v in m['new_local_mm']+m['new_connection_world_mm'])
assert sum(bool(m['stub_moves']) for m in moves)==85 and sum(bool(m['no_connect_uuid']) for m in moves)==5
minimum={}
for direction in ['0','180']:
 ys=sorted(D(m['new_local_mm'][1]) for m in moves if m['direction_degrees']==direction);minimum[direction]=decstr(min(b-a for a,b in zip(ys,ys[1:])));assert D(minimum[direction])>=D('2.54')
# Reject endpoint collision with unrelated nodes in the current sheet.
old_wire_ids={t['wire_uuid'] for m in moves for t in m['stub_moves']};old_label_ids={t['label_uuid'] for m in moves for t in m['stub_moves']};old_nc_ids={m['no_connect_uuid'] for m in moves if m['no_connect_uuid']};unrelated=[]
for k in ['wire','global_label','label','no_connect','junction']:
 for n in find_all(root,k):
  uid=find_first(n,'uuid')[1];
  if uid in old_wire_ids|old_label_ids|old_nc_ids:continue
  points=find_first(n,'pts')[1:] if k=='wire' else [find_first(n,'at')]
  for pt in points:
   if pt:unrelated.append((D(pt[1]),D(pt[2]),uid))
newpoints={(D(m['new_connection_world_mm'][0]),D(m['new_connection_world_mm'][1])) for m in moves}
newpoints.update((D(t['new_label_at_mm'][0]),D(t['new_label_at_mm'][1])) for m in moves for t in m['stub_moves'])
assert not [(x,y,uid) for x,y,uid in unrelated if (x,y) in newpoints]
# All affected lines are horizontal; reject any intersection with unrelated wire segments.
for m in moves:
 for t in m['stub_moves']:
  (xa,ya),(xb,yb)=[(D(x),D(y)) for x,y in t['new_points_mm']];assert ya==yb;lo,hi=sorted([xa,xb])
  for w in wires:
   if find_first(w,'uuid')[1] in old_wire_ids:continue
   (xc,yc),(xd,yd)=[(D(pt[1]),D(pt[2])) for pt in find_first(w,'pts')[1:]]
   if yc==yd:
    assert not(ya==yc and max(lo,min(xc,xd))<=min(hi,max(xc,xd)))
   elif min(yc,yd)<=ya<=max(yc,yd):
    crossing_x=xc+(xd-xc)*(ya-yc)/(yd-yc);assert not(lo<=crossing_x<=hi)
result={'scope':'Read-only graphic/grid normalization proposal, not a memory qualification or part selection','grid_mm':'1.27','source_sheet':str(B/'memory-flash.kicad_sch'),'source_sha256':hashlib.sha256((B/'memory-flash.kicad_sch').read_bytes()).hexdigest(),'symbol_library_id_before':'TeresinaRack:AS4C16M32MSA','suggested_neutral_library_id':'TeresinaRack:SDRAM_16Mx32_FBGA90','physical_U3_value_MPN_SKU_footprint_unchanged':True,'instance_anchor_unchanged':at[1:],'pin_count':90,'individual_connected_stubs':85,'individual_no_connect_markers':5,'minimum_same_side_pin_spacing_mm':minimum,'collisions':[],'source_cache_external_pin_tables_match':True,'body_rectangle_optional_grid_change':{'old_start_mm':['-22.86','62.00'],'old_end_mm':['22.86','-62.00'],'new_start_mm':['-22.86','62.23'],'new_end_mm':['22.86','-62.23']},'moves':moves,'acceptance_constraints':['Preserve all90 unique pin numbers,names,electricaltypes,shapes,lengths,directions andvisibility','Keep supply balls individually represented; do not stack/coalesce same-net pins','Update external library and everycachedcopy identically; assert actualsourcehash beforeapplying','Move bothends of each85 horizontalstub anditsglobal label/properties byworlddelta; preserve UUIDs andlabelnames','Move allfiveNCmarkers to newpin endpoints, preserving theirUUIDs','Do not edit U3 candidateMPN,Value,LCSC,Datasheet orfootprint; RAM remainsunqualified','Use neutralgraphic symbolidentity andremove allunsupported drop-in compatibilitywording; distinguish pinmap fromelectricalqualification','Native netlist mustretain all90 U3 pin-netfunctions andallothercomponentconnections; compare completeproject','ERC86 U3-relatedoffgridrecords should disappear; no newERCerrors orwarnings; librarycache/externalmustmatch','Review renderedpage for readability andcheck no physicalPCB orfirmwarechanged']}
(OUT/'u3-grid-plan.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['moves','acceptance_constraints']},indent=2))
