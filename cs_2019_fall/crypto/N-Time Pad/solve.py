a = '''
0f226124093d402b1a38190f1f1f26634e11453149020b487d150d4a167f1d05517f00467f525944505c0210414846085e5d194307060b5a0c42105145150e031510055456515055015d441f1e
342d222c1e201c7f172a1f4e1d122e3a0717482749190d487014174253300b44547f065b3a1e430d585741124a5d1f1259524b52064508511c13115c004115030c55464651455a01404c0d1f12
346c2d281523552d552b030f015b7f3b06000d390c1e164c3704444516360303152c0c5b2b1d172d5b12150a514b1215545051590b14165149130414150d070b0f44034d4c1f5652014f40560f
232861301230587f147f190f011330224e1648371b08110d3b041d075b3e01175a7f1b50395645165056411657185312115219580c004e400c5e00141500024b4f10325d5d511301445e42575d
242535671436103c1d3e190f0c033a3d4e0a4b741d05000d200d054e1d2b081c417f00467f565907474b11165d5c120348135a580f070a5a0c5d02140c15461508440e154c575a014250534d18
353c2e291f2d5e38553d021a4f182d6f0d0d4c26080e1148224102551c324d105d3a49453e571711465b0f0518555d05445f5845420407500c470c5b0b4f462b0710125d5d1f5444581f484c5d
323e342b0264423e1b3b040343573e3b4e0948351a19454c234108481d384d05467f1d5d3a134708545b0f165d40464d115d5c41071743460046165101410f0c41470e5a545a1f4e531f48515d
362d333357645131117f000b1f037f2c01085d380c19004129411742102d0810197f1d5d3a5d17105d5741105d4b470d455a575042060a440d5617400019124216590a59185d5a01485251500e
3525232b1e644430553b0e0d1d0e2f3b4e0a5f740b1f004c3b4f446e077f0505467f08592c5c170650570f42484a5d17545d19430a041714045d1c140608160a04424642514b57015557441f0d
342331220930497f1a394b1e0a05392a0d110d270c0e17483318444a062c1944402c0c1534564e17154508165018570757565a430b1306581c13115c004115030c5546475d4e4a48535a4c5a13
323f612608647f0b257f000b1604716f2a0c4a3d1d0c090d260416541a30031715300f15305d5249415b0c0718485305115050470a001147455b044200410407045e46404b5a5b01434601511c
32252e2908645630077f081c0603362c0f090d30001d09423d00104e107f0c0a517f045c335a4305474b410157555f145f5a5a56160c0c5a491307411141120a04101647575d53444c4c01501b
663f24240e36557f1e3a124e0b1e2c3b1c0c4f211d040a4370090551167f0005513a494137565a445c5f1110595b460852525517040a1114085c1640450016120d5905544c56504f52116e7442
'''
a = a.split()
b = [b'',b'',b'',b'',b'',b'',b'',b'',b'',b'',b'',b'',b'']
for j in range(13):
	for i in range(len(a[0])):
		if(i % 2 == 0):
			b[j] += chr(int(a[j][i:i+2],16)).encode('utf-8')

opt = b'FLAG{D0_u_know_One-Time-Pad\'s_md5_i5_37d52ab882a1397bec4e3e4eafba0f58??!!?!?}'
for i in range(13):
	for j in range(len(opt)):
		print(chr(int(opt[j]) ^ int(b[i][j])),end='')
	print('')




