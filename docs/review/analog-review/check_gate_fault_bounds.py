import math, json, pathlib
p=pathlib.Path(__file__).parent
q=json.load(open(p/'C20526-product.json')) if (p/'C20526-product.json').exists() else None
print('B-E clamp: exact JSCJ1N4148WS/C2128; VFmax0.715V at1mA and25C;6V exactJSCJtransistorVEBO')
print('Negative input-17V with99kohm minimum series: clamp current absolute bound17/99000='+str(17/99000*1e6)+' uA')
for temp in [70,85,105,125]:
 frac=min(1.,(155-temp)/85)
 for watts,label in [(0.0625,'existing0402'),(.125,'option0805')]:
  allowed=watts*frac;limit=math.sqrt(allowed/101)*1000
  print(f'{label} at{temp}C: rated resistor power={allowed*1000:.6f}mW; I_RMS limit at101ohm={limit:.6f}mA')
for milli in [0.5,23.,30.,50.]:print(f'Current{milli}mA at101ohm: P={(milli/1000)**2*101*1000:.6f}mW')
print('MCP6004 ±23mA short current is typical only;±30mA is absolute-pin rating,NOT a specified current limiter maximum')
