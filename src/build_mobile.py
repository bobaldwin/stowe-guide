import base64, io, re, urllib.parse, os
import qrcode, qrcode.image.svg
from PIL import Image

def am(q): return 'https://maps.apple.com/?q=' + urllib.parse.quote(q)

AM = {
 'recpath':'Stowe Recreation Path, Stowe, VT','cadyhill':'Cady Hill Forest, Stowe, VT',
 'ranchcamp':'Ranch Camp, Stowe, VT','lvrt':'Lamoille Valley Rail Trail, Morrisville, VT',
 'ajs':"AJ's Ski & Sports, Stowe, VT",'pinnacleski':'Pinnacle Ski & Sports, Stowe, VT',
 'barnescamp':'Barnes Camp Visitor Center, Stowe, VT','tollroad':'Mount Mansfield Toll Road, Stowe, VT',
 'pinnacle':'Stowe Pinnacle Trailhead, Stowe, VT','sterling':'Sterling Pond Trailhead, VT',
 'bingham':'Bingham Falls Trailhead, Stowe, VT','mossglen':'Moss Glen Falls, Stowe, VT',
 'wiessner':'Wiessner Woods, Stowe, VT','topnotch':'Topnotch Resort, Stowe, VT',
 'memorial':'Memorial Park, Stowe, VT','vontrapplodge':'Trapp Family Lodge, Stowe, VT',
 'swimhole':'The Swimming Hole, Stowe, VT','phit':'PHIT Performance, Stowe, VT',
 'gondola':'Stowe Mountain Resort, Stowe, VT','waterburysp':'Waterbury Center State Park, Waterbury Center, VT',
 'umiak':'Umiak Outdoor Outfitters, Stowe, VT','arbortrek':'ArborTrek Canopy Adventures, Jeffersonville, VT',
 'discgolf':'Brewster Ridge Disc Golf Course, Jeffersonville, VT','flyrod':'The Fly Rod Shop, Stowe, VT',
 'alchemist':'The Alchemist, Stowe, VT','bierhall':'von Trapp Brewing Bierhall, Stowe, VT',
 'idletyme':'Idletyme Brewing Company, Stowe, VT','stowecider':'Stowe Cider, Stowe, VT',
 'smugdist':"Smugglers' Notch Distillery, Stowe, VT",'butlers':"Butler's Pantry, Stowe, VT",
 'bench':'The Bench, Stowe, VT','blackcap':'Black Cap Coffee & Beer, Stowe, VT',
 'pk':'PK Coffee, Stowe, VT','bluedonkey':'Blue Donkey, Stowe, VT',
 'docponds':'Doc Ponds, Stowe, VT','harrisons':"Harrison's Restaurant, Stowe, VT",
 'michaels':"Michael's on the Hill, Waterbury Center, VT",'edson':'Edson Hill, Stowe, VT',
 'laughingmoon':'Laughing Moon Chocolates, Stowe, VT','coldhollow':'Cold Hollow Cider Mill, Waterbury Center, VT',
 'goldbrook':'Gold Brook Covered Bridge, Stowe, VT',
}
AM_URLS = {k: am(v) for k,v in AM.items()}

QR_TARGETS = {
 'q_cadyhill':AM_URLS['cadyhill'],'q_recpath':AM_URLS['recpath'],'q_lvrt':AM_URLS['lvrt'],
 'q_stowetrails':'https://www.stowetrails.org','q_barnescamp':AM_URLS['barnescamp'],
 'q_pinnacle':AM_URLS['pinnacle'],'q_sterling':AM_URLS['sterling'],
 'q_gmc':'https://www.greenmountainclub.org',
 'q_weather':'https://forecast.weather.gov/MapClick.php?lat=44.4654&lon=-72.6874',
 'q_topnotch':AM_URLS['topnotch'],'q_memorial':AM_URLS['memorial'],'q_swimhole':AM_URLS['swimhole'],
 'q_umiak':AM_URLS['umiak'],'q_waterburysp':AM_URLS['waterburysp'],'q_arbortrek':AM_URLS['arbortrek'],
 'q_alchemist':AM_URLS['alchemist'],'q_bierhall':AM_URLS['bierhall'],
 'q_stowecider':AM_URLS['stowecider'],'q_smugdist':AM_URLS['smugdist'],'q_gondola':AM_URLS['gondola'],
}
def qr_svg(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage,
                      border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    buf = io.BytesIO(); img.save(buf)
    svg = buf.getvalue().decode()
    svg = re.sub(r'<\?xml[^>]*\?>', '', svg)
    svg = re.sub(r'\s(width|height)="[^"]*"', '', svg, count=2)
    return svg.strip()
QR_SVGS = {k: qr_svg(u) for k,u in QR_TARGETS.items()}

IMGS = ['longtrail','recpath','mansfield_se','bingham','mossglen','trapp','waterbury','church','bridge']
def img_datauri(name, width=880, q=68):
    im = Image.open(f'img/{name}.jpg').convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height*width/im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf,'JPEG',quality=q,progressive=True,optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'<img src="data:image/jpeg;base64,{b64}" alt="{name}" loading="lazy" width="{im.width}" height="{im.height}">'
IMG_TAGS = {n: img_datauri(n) for n in IMGS}

PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>'

body = open('mobile_a.html').read() + open('mobile_b.html').read() + open('mobile_c.html').read()
body = body.replace('{{PIN}}', PIN)
for k,u in AM_URLS.items(): body = body.replace('{{AM:%s}}'%k, u)
for k,svg in QR_SVGS.items(): body = body.replace('{{QR:%s}}'%k, svg)
for k,tag in IMG_TAGS.items(): body = body.replace('{{IMG:%s}}'%k, tag)

leftover = re.findall(r'\{\{[^}]+\}\}', body)
print('unresolved tokens:', leftover[:10] if leftover else 'none')

open('stowe-mobile.html','w').write(body)

title_tag = "<title>The Friends' Guide to Stowe · July 2026</title>"
body_no_title = body.replace(title_tag + '\n', '', 1)
standalone = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
 + title_tag + '\n</head>\n<body>\n' + body_no_title + '\n</body>\n</html>\n')
open('/Users/robertbaldwin/Documents/Claude/Stowe Guide (Mobile).html','w').write(standalone)
print('fragment KB:', os.path.getsize('stowe-mobile.html')//1024)
print('standalone KB:', os.path.getsize('/Users/robertbaldwin/Documents/Claude/Stowe Guide (Mobile).html')//1024)
