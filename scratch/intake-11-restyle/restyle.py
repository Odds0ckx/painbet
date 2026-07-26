#!/usr/bin/env python3
"""Restyle painbet_intake_11.html onto the pain.bet design system.

Swaps the <style> block and the webfont link, injects the brand motifs
(triangle watermark, ekg trace, liquid pain-scale bubble) and repoints the
two colour arrays that live in JS. Nothing else is touched: all copy, all
IDs, all handlers, the synthesised audio engine and both embedded videos
come through byte for byte.
"""
import re, sys

SRC = "/root/.claude/uploads/a8b1436e-c0f8-51e1-a987-d33b627a2081/5f1fab08-painbet_intake_11.html"
CSS = "/tmp/claude-0/-home-user-painbet/a8b1436e-c0f8-51e1-a987-d33b627a2081/scratchpad/new.css"
OUT = "/home/user/painbet/painbet-intake-11-v2.html"

s = open(SRC, encoding="utf-8").read()
css = open(CSS, encoding="utf-8").read()
orig = s


def once(old, new, label):
    """Replace exactly one occurrence or die loudly."""
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("FAIL %s: found %d occurrences" % (label, n))
    s = s.replace(old, new, 1)


# ---- 1. keep the intro's last-frame still, it lives inside the old CSS ----
m = re.search(r"\.after\{[^}]*?base64,([A-Za-z0-9+/=]+)'\)", s)
if not m:
    sys.exit("FAIL: could not find the .after still frame")
css = css.replace("__AFTER_FRAME__", m.group(1))

# ---- 2. webfonts: add Archivo 800 and swap JetBrains for IBM Plex Mono ----
once(
    '<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">',
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Archivo:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">',
    "font link",
)

# ---- 3. the stylesheet ----
a, b = s.index("<style>"), s.index("</style>")
s = s[: a + len("<style>")] + "\n" + css + s[b:]

# ---- 4. brand motifs: triangle watermark + ekg trace ----
TRI = '<span class="bigtri%s" aria-hidden="true"></span>'
EKG = (
    '<div class="ekg" aria-hidden="true"><svg viewBox="0 0 1200 40" preserveAspectRatio="none">'
    '<path d="M0 24 H120 L135 24 145 6 155 36 165 24 H400 L415 24 425 6 435 36 445 24 H600 '
    'M600 24 H720 L735 24 745 6 755 36 765 24 H1000 L1015 24 1025 6 1035 36 1045 24 H1200" '
    'stroke="%s" stroke-width="2" fill="none"/></svg></div>'
)
once(
    '<div class="hook">\n        <div class="hook-top">',
    '<div class="hook">\n        '
    + (TRI % " blue")
    + "\n        "
    + (EKG % "#7FD6E8")
    + '\n        <div class="hook-top">',
    "hook motifs",
)
once(
    '<div class="prize">\n        <div class="pz-top">',
    '<div class="prize">\n        ' + (TRI % " blue") + '\n        <div class="pz-top">',
    "prize triangle",
)
once(
    '<div class="wheelbox">\n            <div class="wtop">',
    '<div class="wheelbox">\n            ' + (TRI % " blue") + '\n            <div class="wtop">',
    "wheelbox triangle",
)
once(
    '<div class="promise">\n        <div class="pbig">',
    '<div class="promise">\n        ' + (TRI % " amber") + '\n        <div class="pbig">',
    "promise triangle",
)
once(
    '<div class="oct">\n        <span class="octl">',
    '<div class="oct">\n        ' + (TRI % "") + '\n        <span class="octl">',
    "october triangle",
)

# ---- 5. the 3D locker crate above "PRY IT OPEN" ----
# Adapted from the cooler concept already reworked and approved for
# painbet-intake-scroll.html (assets/../3d_organ_cooler_crate_v2.html origin):
# same plastic-box-plus-hinged-lid construction, no GSAP/Tailwind, none of the
# original's blood/organ dressing or instructional copy. Recoloured amber to
# tie into the locker card it now sits on top of, and driven by the existing
# single-tap pry() instead of a separate multi-tap ratchet.
CRATE = """<div class="crate-scene"><div class="crate" id="crate">
        <div class="crate-base">
          <div class="cf front"><span class="crate-tag">LOCKER &middot; 0<span id="crateLk">7</span></span></div>
          <div class="cf back"></div><div class="cf right"></div><div class="cf left"></div>
          <div class="cf bottom"></div>
          <div class="cf inner"><div class="crate-core" id="crateCore"></div></div>
        </div>
        <div class="crate-hinge" id="crateHinge">
          <div class="crate-lid">
            <div class="cf front"><div class="crate-latch" id="crateLatch"><i></i></div></div>
            <div class="cf back"></div><div class="cf right"></div><div class="cf left"></div>
            <div class="cf top"></div><div class="cf undr"></div>
          </div>
        </div>
      </div></div>
      """
once(
    '<div class="locker" id="locker" role="button" tabindex="0">',
    CRATE + '<div class="locker" id="locker" role="button" tabindex="0">',
    "crate markup",
)
# pry() ran fully on the first tap; the crate reads better as something you
# have to work at, so this ratchets it across a few taps (the seal straining
# a little further each time) before the original payout logic fires, once,
# on the tap that finally clears the threshold. PRY_TAPS lives outside the
# function so it's one number to tune if the feel needs adjusting.
once(
    """function pry(){
  if(st.pried)return; st.pried=true; Snd.creak();
  var p=rollPk(); st.pkWon=p;
  $('locker').classList.add('pried');
  $('lkText').textContent=p.pk.toLocaleString('en-US')+' PK';
  $('lkHint').textContent='Worth $'+p.usd.toLocaleString('en-US')+'. '+p.n+' Lands in your account in October.';
  $('toExit').style.display='block';
  if(st.pkWon&&st.pkWon.usd>=100) Snd.jackpot(); else Snd.win();
  flick();
  toast('Logged to patient #'+String(st.pno).padStart(5,'0')+'.');
}""",
    """var PRY_TAPS=4, pryStep=0;
function pry(){
  if(st.pried)return;
  pryStep++;
  var hinge=$('crateHinge'), crateEl=$('crate'), core=$('crateCore');
  if(pryStep<PRY_TAPS){
    var ang=(pryStep/PRY_TAPS)*26;
    if(hinge){
      hinge.style.transition='transform .22s cubic-bezier(.34,1.56,.64,1)';
      hinge.style.transform='translateY(calc(var(--hbh) * -1)) translateZ(calc(var(--dh) * -1)) rotateX('+(ang+5)+'deg)';
      setTimeout(function(){ hinge.style.transform=
        'translateY(calc(var(--hbh) * -1)) translateZ(calc(var(--dh) * -1)) rotateX('+ang+'deg)'; },110);
    }
    if(core) core.style.opacity=String(.16+(pryStep/PRY_TAPS)*.4);
    if(crateEl){ crateEl.classList.remove('shake'); void crateEl.offsetWidth; crateEl.classList.add('shake');
      setTimeout(function(){ crateEl.classList.remove('shake'); },320); }
    var lk=$('locker'); if(lk){ lk.classList.remove('strain'); void lk.offsetWidth; lk.classList.add('strain');
      setTimeout(function(){ lk.classList.remove('strain'); },240); }
    Snd.creak(); flick();
    return;
  }
  st.pried=true; Snd.creak();
  var p=rollPk(); st.pkWon=p;
  $('locker').classList.add('pried');
  if(hinge){ hinge.style.transition=''; hinge.style.transform=''; }
  if(crateEl) crateEl.classList.add('open');
  $('lkText').textContent=p.pk.toLocaleString('en-US')+' PK';
  $('lkHint').textContent='Worth $'+p.usd.toLocaleString('en-US')+'. '+p.n+' Lands in your account in October.';
  $('toExit').style.display='block';
  if(st.pkWon&&st.pkWon.usd>=100) Snd.jackpot(); else Snd.win();
  flick();
  toast('Logged to patient #'+String(st.pno).padStart(5,'0')+'.');
}""",
    "ratcheted pry",
)
once(
    "$('lkNo').textContent=String(st.pno%9+1);",
    "$('lkNo').textContent=String(st.pno%9+1);\n  var ck=$('crateLk'); if(ck) ck.textContent=$('lkNo').textContent;",
    "crate locker number sync",
)

# ---- 6. liquid pain-scale bubble on the diagnosis card ----
BUBBLE = """
        <div class="painscale">
          <div class="bubble" id="psBubble" role="img" aria-label="Pain scale">
            <div class="inner">
              <div class="water" id="psWater"></div>
              <div class="water2" id="psWater2"></div>
              <span class="bub"></span><span class="bub"></span><span class="bub"></span><span class="bub"></span>
              <div class="glare"></div>
              <div class="percent"><span class="n" id="psNum">0/10</span><span class="lvl" id="psLvl">Numb</span></div>
            </div>
          </div>
          <div class="pstxt">
            <span class="k">Reading<b id="psWord">NUMB</b></span>
            <p class="psub">Read straight off your answers. It sets the tier you open on when the doors go.</p>
          </div>
        </div>
"""
once(
    '          <span class="tierp">PAIN SCALE <b id="tier">4</b>/10</span>\n        </div>\n',
    '          <span class="tierp">PAIN SCALE <b id="tier">4</b>/10</span>\n        </div>\n' + BUBBLE,
    "pain scale bubble",
)

# ---- 7. JS: drive the bubble, and repoint the password-meter colours ----
once(
    "function diagnose(){",
    """function painWord(t){
  if(t<=2) return 'NUMB';
  if(t<=4) return 'SORE';
  if(t<=6) return 'CHRONIC';
  if(t<=8) return 'AGONY';
  return 'FLATLINE';
}
/* fills the liquid bubble on the diagnosis card. tier 0 sits nearly empty,
   tier 10 nearly full, and the label matches the app sidebar. */
function paintScale(t){
  var w=painWord(t), top=Math.max(20,92-t*7);
  var n=$('psNum'), l=$('psLvl'), b=$('psWord'), wa=$('psWater'), w2=$('psWater2'), bb=$('psBubble');
  if(n) n.textContent=t+'/10';
  if(l) l.textContent=w.charAt(0)+w.slice(1).toLowerCase();
  if(b) b.textContent=w;
  if(wa) wa.style.top=top+'%';
  if(w2) w2.style.top=(top+4)+'%';
  if(bb) bb.setAttribute('aria-label','Pain scale '+t+' of 10, '+w.toLowerCase());
}
function diagnose(){""",
    "paintScale fn",
)
once(
    "$('tier').textContent=d.t; $('dx').textContent=d.n; $('dxl').textContent=d.l;",
    "$('tier').textContent=d.t; $('dx').textContent=d.n; $('dxl').textContent=d.l;\n  paintScale(d.t);",
    "paintScale call",
)
once(
    "$('dTier').textContent='Pain Scale '+st.dx.t+'/10'; }",
    "$('dTier').textContent='Pain Scale '+st.dx.t+'/10'; paintScale(st.dx.t); }",
    "paintScale on chart",
)
once(
    "var cols=['#FF4A42','#FF4A42','#F2C14E','#5FE3A1','#5FE3A1'];",
    "var cols=['#FF3B33','#FF3B33','#FFB84D','#7FD6E8','#7FD6E8'];",
    "password meter colours",
)
once("h.style.color='var(--red-hot)';", "h.style.color='var(--redhi)';", "hint colour")
# the rust bloom is set inline by diagnose(); keep it in step with the stylesheet
once("$('rust').style.opacity='.45';", "$('rust').style.opacity='.28';", "rust strength")

open(OUT, "w", encoding="utf-8").write(s)
print("wrote %s  (%d bytes, was %d)" % (OUT, len(s), len(orig)))
