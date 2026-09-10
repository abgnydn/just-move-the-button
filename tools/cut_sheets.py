#!/usr/bin/env python3
"""Cut the three Gemini sheets into transparent PNG assets for a hero.
Usage: python3 tools/cut_sheets.py <hero> <turnaround.jpg> <expressions.jpg> <poses.jpg>
Writes assets/<hero>/{stand-front,stand-quarter,face-*,pose-*}.png
Expects: turnaround = 2 figures on white; expressions = 3x2 grid with black borders (calm, thinking, worried / shocked, exhausted, relieved);
         poses = 4 figures on white, left→right: typing, phone, alarm, slumped.
"""
import sys, pathlib
HERO, T, E, PO = sys.argv[1:5]
OUT = pathlib.Path(__file__).resolve().parent.parent / 'assets' / HERO; OUT.mkdir(parents=True, exist_ok=True)
import numpy as np
from PIL import Image
from scipy import ndimage

def load(p): return np.array(Image.open(p).convert('RGB'))
def nonwhite(a, t=235): return (a<t).any(axis=2)

def segments(proj, minlen, gap=12):
    # find runs of True in 1D projection, merging small gaps
    idx=np.where(proj)[0]
    if len(idx)==0: return []
    segs=[]; s=idx[0]; p=idx[0]
    for i in idx[1:]:
        if i-p>gap: segs.append((s,p)); s=i
        p=i
    segs.append((s,p))
    return [(a,b) for a,b in segs if b-a>=minlen]

def bg_to_alpha(rgb, t=232):
    # transparent = near-white pixels connected to the image border
    a=np.array(rgb); white=(a>t).all(axis=2)
    lab,n=ndimage.label(white)
    border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))
    border.discard(0)
    mask=np.isin(lab,list(border))
    # soften edge: 1px erosion of the mask so halftone fringe stays
    alpha=np.where(mask,0,255).astype(np.uint8)
    out=np.dstack([a,alpha])
    return Image.fromarray(out,'RGBA')

def crop_content(img_rgb, pad=8):
    m=nonwhite(img_rgb); ys=np.where(m.any(axis=1))[0]; xs=np.where(m.any(axis=0))[0]
    y0,y1=max(ys[0]-pad,0),min(ys[-1]+pad,img_rgb.shape[0]); x0,x1=max(xs[0]-pad,0),min(xs[-1]+pad,img_rgb.shape[1])
    return img_rgb[y0:y1,x0:x1]

def save(rgb, path, maxh):
    im=bg_to_alpha(rgb)
    if im.height>maxh: im=im.resize((int(im.width*maxh/im.height),maxh),Image.LANCZOS)
    im.save(path,optimize=True); print(path, im.size)


def largest_component(png):
    a=np.array(Image.open(png)); solid=a[:,:,3]>0
    lab,n=ndimage.label(ndimage.binary_dilation(solid,iterations=6))
    if n>1:
        keep=np.argmax(ndimage.sum(solid,lab,range(1,n+1)))+1; a[lab!=keep]=0
        ys,xs=np.where(a[:,:,3]>0); a=a[ys.min():ys.max()+1, xs.min():xs.max()+1]
        Image.fromarray(a,'RGBA').save(png,optimize=True)

# turnaround
a=load(T); m=nonwhite(a); cols=segments(m.any(axis=0),200,gap=40)
for i,(x0,x1) in enumerate(cols[:2]): save(crop_content(a[:,x0:x1]), OUT/f'stand-{["front","quarter"][i]}.png', 900)
# expressions: real panel borders are lines that are dark across >85% of the image
b=load(E); dark=(b<60).all(axis=2)
v=segments(dark.mean(axis=0)>0.85,1,gap=3); hl=segments(dark.mean(axis=1)>0.85,1,gap=3)
xb=[(v[i][1]+3, v[i+1][0]-3) for i in range(0,len(v)-1,2)]; yb=[(hl[i][1]+3, hl[i+1][0]-3) for i in range(0,len(hl)-1,2)]
names=['calm','thinking','worried','shocked','exhausted','relieved']; k=0
for (y0,y1) in yb:
    for (x0,x1) in xb:
        if k<6: save(b[y0:y1,x0:x1], OUT/f'face-{names[k]}.png', 560); k+=1
# poses: split on white gaps; if only 3 columns found, split the widest at its emptiest column
c=load(PO); m=nonwhite(c); cols=segments(m.any(axis=0),150,gap=25)
if len(cols)==3:
    w=max(range(3),key=lambda i:cols[i][1]-cols[i][0]); x0,x1=cols[w]; col=m.sum(axis=0)
    lo,hi=x0+(x1-x0)//3, x0+2*(x1-x0)//3; s=min(range(lo,hi),key=lambda x:col[x])
    cols=cols[:w]+[(x0,s),(s,x1)]+cols[w+1:]
pn=['typing','phone','alarm','slumped']
for i,(x0,x1) in enumerate(cols[:4]):
    out=OUT/f'pose-{pn[i]}.png'; save(crop_content(c[:,x0:x1]), out, 900); largest_component(out)
print('done', OUT)
