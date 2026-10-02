"""Builds the Divi layout JSON for the automatic fire suppression page.

Output: autokatasvesi-divi.json (Divi portability format, context et_builder).
Divi 5 converts this format to native Divi 5 modules on import.
Images are embedded (base64) so Divi uploads them to the Media Library on import.
"""
import base64
import json
import pathlib
import re

HERE = pathlib.Path(__file__).parent
IMG_DIR = HERE / "images"
IMG_BASE = "https://underpro-security.gr/wp-content/uploads/upk-autokatasvesi/"
BV = "4.27.4"
BOOKING = "https://underpro-security.gr/%cf%81%ce%b1%ce%bd%cf%84%ce%b5%ce%b2%ce%bf%cf%8d"

USED_IMAGES = []


def img(name):
    if name not in USED_IMAGES:
        USED_IMAGES.append(name)
    return IMG_BASE + name


def one_line(html):
    html = re.sub(r"\s*\n\s*", "", html.strip())
    assert "[" not in html and "]" not in html, "square brackets break Divi shortcodes"
    return html


def attrs(**kw):
    out = []
    for k, v in kw.items():
        v = str(v)
        assert '"' not in v and "[" not in v and "]" not in v, (k, v)
        out.append(f'{k}="{v}"')
    return " ".join(out)


def text(html, cls=""):
    return f'[et_pb_text {attrs(_builder_version=BV, module_class=("upk-t " + cls).strip())}]{one_line(html)}[/et_pb_text]'


def code(html, cls=""):
    return f'[et_pb_code {attrs(_builder_version=BV, module_class=("upk-c " + cls).strip())}]{one_line(html)}[/et_pb_code]'


def image(name, alt, cls=""):
    return (f'[et_pb_image {attrs(src=img(name), alt=alt, title_text=alt, align="center", _builder_version=BV, module_class=("upk-img " + cls).strip())}]'
            "[/et_pb_image]")


def column(kind, *modules):
    return f'[et_pb_column {attrs(type=kind, _builder_version=BV)}]' + "".join(modules) + "[/et_pb_column]"


def row(structure, *columns, cls=""):
    a = attrs(column_structure=structure, use_custom_gutter="on", gutter_width="3", width="90%", max_width="1120px",
              custom_padding="0px||0px||true|false", custom_margin="0px|auto|40px|auto|false|false",
              _builder_version=BV, module_class=("upk-row " + cls).strip())
    return f"[et_pb_row {a}]" + "".join(columns) + "[/et_pb_row]"


def section(label, bg, cls, *rows):
    a = attrs(admin_label=label, background_color=bg, custom_padding="72px||32px||true|false",
              _builder_version=BV, module_class=f"upk {cls}")
    return f'[et_pb_section fb_built="1" {a}]' + "".join(rows) + "[/et_pb_section]"


# ---------------------------------------------------------------- CSS
CSS = """
<style>
.upk{--upk-ink:#121a24;--upk-soft:#4a5665;--upk-line:#dbe3ec;--upk-alt:#f3f6fa;--upk-blue:#3a8ded;--upk-blue-ink:#1f6fcf;--upk-sand:#cbb28c;--upk-fire:#d7262e;--upk-fire-soft:#fdecec;--upk-dark:#0f1823;font-family:Manrope,'Segoe UI',Helvetica,Arial,sans-serif;color:var(--upk-ink)}
.upk .upk-t,.upk .upk-t p,.upk .upk-t li{font-size:16px;line-height:1.65;color:var(--upk-ink)}
.upk h1,.upk h2,.upk h3,.upk h4{font-family:Barlow,'Arial Narrow',Arial,sans-serif;line-height:1.12;color:var(--upk-ink);padding-bottom:0;text-wrap:balance}
.upk h2{font-size:clamp(28px,4vw,40px);font-weight:700;margin:0 0 14px}
.upk h3{font-size:clamp(22px,2.6vw,28px);font-weight:700;margin:0 0 12px}
.upk h4{font-size:20px;font-weight:700;margin:10px 0 6px}
.upk .upk-t p{padding-bottom:12px}
.upk .upk-eyebrow{display:block;font-weight:600;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--upk-blue-ink);margin-bottom:10px}
.upk .upk-lead,.upk .upk-t p.upk-lead{font-size:18px;color:var(--upk-soft);max-width:65ch}
.upk .upk-badge{display:inline-block;font-weight:700;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--upk-fire);border:1.5px solid var(--upk-fire);padding:6px 10px;border-radius:999px;margin-bottom:14px}
.upk .upk-btns{display:flex;flex-wrap:wrap;gap:12px;margin:8px 0 18px}
.upk a.upk-btn{display:inline-flex;align-items:center;gap:8px;padding:14px 22px;border-radius:10px;font-weight:700;font-size:15px;line-height:1;text-decoration:none}
.upk a.upk-btn.primary{background:var(--upk-blue);color:#fff}
.upk a.upk-btn.ghost{border:1.5px solid rgba(255,255,255,.35);color:#f4f7fb}
.upk .upk-css-row,.upk .upk-css-row .et_pb_column,.upk .upk-styles{margin:0!important;padding:0!important;min-height:0}
.upk-hero,.upk-cta{background-image:radial-gradient(ellipse at 85% 110%,rgba(215,38,46,.35),transparent 55%)}
.upk-hero .upk-t,.upk-hero .upk-t p,.upk-cta .upk-t,.upk-cta .upk-t p{color:#b7c3d1}
.upk-hero h1{font-size:clamp(36px,6vw,64px);font-weight:800;color:#f4f7fb;margin:0 0 18px}
.upk-hero h1 em{font-style:normal;color:#ff6a6f}
.upk-cta h2{color:#f4f7fb}
.upk-hero .upk-eyebrow{color:var(--upk-sand)}
.upk-facts{display:flex;flex-wrap:wrap;gap:10px 22px;font-size:14px}
.upk-facts span:before{content:'';display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--upk-sand);margin-right:8px;vertical-align:middle}
.upk .upk-img img{border-radius:14px;background:#fff}
.upk .upk-img.framed img{border:1px solid var(--upk-line);padding:12px}
.upk .upk-sizes img{max-height:320px;width:auto}
.upk .upk-caption{font-size:13px;color:var(--upk-soft)}
.upk-timeline{background:#fff;border:1px solid var(--upk-line);border-radius:14px;padding:28px 24px 22px;overflow-x:auto;margin-bottom:28px}
.upk-tl-track{position:relative;min-width:620px;height:150px}
.upk-tl-bar{position:absolute;left:0;right:0;top:64px;height:14px;border-radius:7px;background:linear-gradient(90deg,#ffd27a 0%,#ff9f40 30%,#d7262e 62%,#7a0f14 100%)}
.upk-tl-zone{position:absolute;left:0;top:56px;width:6%;height:30px;border:2px dashed var(--upk-blue);border-radius:8px}
.upk-tl-mark{position:absolute;top:0;transform:translateX(-50%);display:grid;justify-items:center;gap:6px;width:150px;text-align:center}
.upk-tl-mark .t{font-family:Barlow,Arial,sans-serif;font-weight:800;font-size:20px;line-height:1;color:var(--upk-ink)}
.upk-tl-mark .pin{width:2px;height:30px;background:var(--upk-soft)}
.upk-tl-mark .d{font-size:13px;line-height:1.35;color:var(--upk-soft);margin-top:24px}
.upk-tl-mark.first{transform:none;justify-items:start;text-align:left}
.upk-tl-mark.first .t{color:var(--upk-blue-ink)}
.upk-tl-axis{display:flex;justify-content:space-between;min-width:620px;font-size:12px;color:var(--upk-soft);border-top:1px solid var(--upk-line);padding-top:8px;margin-top:4px}
.upk-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.upk-stat{background:#fff;border:1px solid var(--upk-line);border-radius:12px;padding:22px;display:grid;gap:8px;align-content:start}
.upk-stat .n{font-family:Barlow,Arial,sans-serif;font-weight:800;font-size:clamp(34px,4vw,46px);line-height:1;color:var(--upk-fire)}
.upk-stat .l{font-weight:600;color:var(--upk-ink);line-height:1.4}
.upk-stat .s{font-size:13px;color:var(--upk-soft);line-height:1.45}
.upk-gr .upk-stat .n{color:var(--upk-blue-ink)}
.upk-gr-head{border-top:1px solid var(--upk-line);padding-top:28px;margin-top:8px}
.upk .upk-callout{border-left:4px solid var(--upk-fire);background:var(--upk-fire-soft);padding:18px 20px;border-radius:0 10px 10px 0;font-size:17px;max-width:820px}
.upk ul.upk-ticks{list-style:none;padding:0;margin:0 0 8px}
.upk ul.upk-ticks li{padding:0 0 10px 28px;position:relative}
.upk ul.upk-ticks li:before{content:'';position:absolute;left:2px;top:7px;width:14px;height:8px;border-left:2.5px solid var(--upk-blue);border-bottom:2.5px solid var(--upk-blue);transform:rotate(-45deg)}
.upk .upk-card{background:#fff;border:1px solid var(--upk-line);border-radius:12px;padding:20px}
.upk .upk-card ul{padding-left:18px;margin:0 0 10px}
.upk .upk-card p,.upk .upk-card li{font-size:15px;color:var(--upk-soft)}
.upk-spec{display:flex;flex-wrap:wrap;gap:8px}
.upk-spec span{font-size:13px;font-weight:600;background:var(--upk-alt);border:1px solid var(--upk-line);padding:5px 9px;border-radius:6px;color:var(--upk-ink)}
.upk-temps{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 18px}
.upk-temps span{font-weight:700;font-size:14px;line-height:1;padding:8px 11px;border-radius:999px;color:#fff}
.upk-heads{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.upk-head-card{border:1px solid var(--upk-line);border-radius:10px;padding:14px;background:#fff}
.upk-head-card b{display:block;font-family:Barlow,Arial,sans-serif;font-size:18px;color:var(--upk-ink)}
.upk-head-card span{font-size:14px;color:var(--upk-soft)}
.upk-tablewrap{overflow-x:auto;border:1px solid var(--upk-line);border-radius:12px;background:#fff}
.upk-tablewrap table{border-collapse:collapse;width:100%;min-width:620px;font-size:15px;border:0;margin:0}
.upk-tablewrap th,.upk-tablewrap td{text-align:left;padding:14px 16px;border:0;border-bottom:1px solid var(--upk-line);vertical-align:top;color:var(--upk-ink)}
.upk-tablewrap thead th{font-family:Barlow,Arial,sans-serif;font-size:17px;background:var(--upk-alt)}
.upk-tablewrap tbody th{font-weight:600;color:var(--upk-soft);width:26%}
.upk-tablewrap tr:last-child th,.upk-tablewrap tr:last-child td{border-bottom:0}
.upk-props{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.upk-props div{background:#fff;border:1px solid var(--upk-line);border-radius:10px;padding:14px;font-weight:600;font-size:15px;color:var(--upk-ink)}
.upk-apps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.upk-app{border-top:3px solid var(--upk-sand);padding-top:12px;display:grid;gap:4px}
.upk-app b{font-family:Barlow,Arial,sans-serif;font-size:18px;color:var(--upk-ink)}
.upk-app span{font-size:14px;color:var(--upk-soft)}
.upk-contact{display:grid;gap:10px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:24px;color:#f4f7fb}
.upk-contact small{color:#b7c3d1;font-size:14px}
.upk-contact .big{font-family:Barlow,Arial,sans-serif;font-weight:800;font-size:28px;line-height:1.1}
.upk-sources ol{padding-left:20px;font-size:14px;color:var(--upk-soft)}
.upk-sources li{padding-bottom:8px}
@media (max-width:980px){.upk-stats,.upk-apps{grid-template-columns:1fr 1fr}.upk-heads{grid-template-columns:1fr}}
@media (max-width:520px){.upk-stats,.upk-props{grid-template-columns:1fr}}
@media (prefers-reduced-motion:no-preference){.upk-tl-bar{background-size:200% 100%;animation:upkburn 6s ease-in-out infinite alternate}@keyframes upkburn{from{background-position:0 0}to{background-position:30% 0}}}
</style>
"""

# ---------------------------------------------------------------- content
def stat(n, l, s):
    return f'<div class="upk-stat"><span class="n">{n}</span><span class="l">{l}</span><span class="s">{s}</span></div>'


hero = section(
    "Α. Εισαγωγή", "#0f1823", "upk-hero",
    row("4_4", column("4_4", code(CSS, "upk-styles")), cls="upk-css-row"),
    row("3_5,2_5",
        column("3_5", text("""
            <span class="upk-eyebrow">Αυτόματη κατάσβεση στην πηγή της φωτιάς</span>
            <h1>Η φωτιά δεν περιμένει. <em>Σβήστε τη στα πρώτα δευτερόλεπτα.</em></h1>
            <p>Συστήματα αυτόματης κατάσβεσης με αέριο FK-5-1-12 που μπαίνουν μέσα σε ηλεκτρολογικούς πίνακες, racks, μηχανοστάσια και κινητήρες. Ανιχνεύουν και σβήνουν τη φωτιά εκεί που ξεκινά, χωρίς ρεύμα, χωρίς άνθρωπο, χωρίς υπολείμματα.</p>
            <div class="upk-btns"><a class="upk-btn primary" href="%s">Κλείστε αυτοψία</a><a class="upk-btn ghost" href="tel:2106096050">Καλέστε 210 609 6050</a></div>
            <div class="upk-facts"><span>Χωρίς παροχή ρεύματος</span><span>Χωρίς συντήρηση έως 10 έτη (ΦΕΙΔΙΑΣ)</span><span>Πιστοποίηση VdS (AMFE)</span></div>
            """ % BOOKING)),
        column("2_5", image("feidias-hero.jpg", "Θερμοευαίσθητος σωλήνας κατάσβεσης ΦΕΙΔΙΑΣ με μανόμετρο"))),
)

timeline = """
<div class="upk-timeline" role="img" aria-label="Χρονολόγιο πυρκαγιάς: 0 λεπτά έναρξη, 2 λεπτά απειλητική για τη ζωή, 4 λεπτά και 50 δευτερόλεπτα flashover">
<div class="upk-tl-track"><div class="upk-tl-bar"></div><div class="upk-tl-zone"></div>
<div class="upk-tl-mark first" style="left:0"><span class="t">0′</span><span class="pin"></span><span class="d">Η φωτιά ξεκινά.<br><b>Εδώ σβήνει το αυτόματο σύστημα.</b></span></div>
<div class="upk-tl-mark" style="left:33.3%"><span class="t">2′</span><span class="pin"></span><span class="d">Η φωτιά γίνεται απειλητική για τη ζωή</span></div>
<div class="upk-tl-mark" style="left:80.6%"><span class="t">4′50″</span><span class="pin"></span><span class="d">Flashover: όλος ο χώρος αναφλέγεται. Στα 5′ έχει τυλιχτεί στις φλόγες.</span></div>
</div>
<div class="upk-tl-axis"><span>0 λεπτά</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6 λεπτά</span></div>
</div>
"""

intl_stats = '<div class="upk-stats">' + "".join([
    stat("4′50″", "Χρόνος μέχρι το flashover σε δωμάτιο με σύγχρονα έπιπλα", "Με παλαιότερα, φυσικά υλικά: πάνω από 30 λεπτά. UL FSRI (1)"),
    stat("2′", "Αρκούν για να γίνει μια φωτιά απειλητική για τη ζωή", "Σε 5 λεπτά ένα σπίτι μπορεί να έχει τυλιχτεί στις φλόγες. Ready.gov, Υπ. Εσωτ. Ασφάλειας ΗΠΑ (2)"),
    stat("−90%", "Λιγότεροι θάνατοι ανά πυρκαγιά όπου υπάρχει αυτόματη κατάσβεση", "Και 32% λιγότεροι τραυματισμοί. NFPA (3)"),
    stat("−69%", "Μικρότερες υλικές ζημιές σε καταστήματα και γραφεία", "66% σε χώρους συνάθροισης, 60% σε κατοικίες. NFPA (3)"),
    stat("1 στις 3", "Πυρκαγιές ξεκινά από ηλεκτρικό ρεύμα", "Υπερθέρμανση, κακές συνδέσεις, γήρανση υλικών. IFS 2002–2023 (4)"),
    stat("40%", "Των επιχειρήσεων δεν ξανανοίγουν μετά από καταστροφή", "Ακόμα 25% κλείνουν μέσα σε έναν χρόνο. FEMA (5)"),
]) + "</div>"

gr_stats = '<div class="upk-stats">' + "".join([
    stat("~49", "Αστικές πυρκαγιές την ημέρα, κατά μέσο όρο", "17.992 τον χρόνο, μέσος όρος 2010–2019. Αρχηγείο Π.Σ. (6)"),
    stat("~12", "Πυρκαγιές σε κτίρια κάθε μέρα", "4.298 τον χρόνο, μέσος όρος 2010–2019. Αρχηγείο Π.Σ. (6)"),
    stat("4.500–5.000", "Αστικές πυρκαγιές τον χρόνο από ηλεκτρικά αίτια", "Εκτίμηση του ΕΛΙΤΗΕ (2026), με βάση ευρωπαϊκά στοιχεία κινδύνου (7)"),
    stat("33.171", "Αστικές πυρκαγιές το 2020, με 68 νεκρούς", "Η χειρότερη χρονιά από το 2010. Αρχηγείο Π.Σ. (6)"),
    stat("25–30%", "Των πυρκαγιών σε κατοικίες στην Ευρώπη οφείλονται σε ηλεκτρικά αίτια", "FEEDS, όπως το παραθέτει το ΕΛΙΠΥΚΑ (8)"),
    stat("95,6%", "Των θυμάτων του 2020 πέθαναν σε κατοικίες ή χώρους διαμονής", "Αρχηγείο Π.Σ. (6)"),
]) + "</div>"

speed = section(
    "Β. Γιατί κάθε λεπτό μετράει", "#ffffff", "upk-speed",
    row("4_4", column("4_4",
        text("""
            <span class="upk-eyebrow">Τα πρώτα λεπτά κρίνουν τα πάντα</span>
            <h2>Ένας χώρος μπορεί να τυλιχτεί στις φλόγες σε λιγότερο από 5 λεπτά</h2>
            <p class="upk-lead">Με τα σημερινά συνθετικά υλικά, η φωτιά μεγαλώνει πολύ πιο γρήγορα απ' ό,τι πριν από μερικές δεκαετίες. Όσο πιο κοντά στο πρώτο δευτερόλεπτο γίνει η κατάσβεση, τόσο μικρότερη είναι η ζημιά. Μετά από ένα σημείο δεν μιλάμε πια για ζημιά, αλλά για καταστροφή.</p>
            """),
        code(timeline),
        code(intl_stats),
        text("""
            <div class="upk-gr-head"><span class="upk-eyebrow">Στην Ελλάδα</span><h3>Τι λένε τα στοιχεία του Πυροσβεστικού Σώματος</h3></div>
            """),
        code(gr_stats, "upk-gr"),
        text("""
            <p class="upk-callout"><b>Το συμπέρασμα είναι απλό:</b> η πυροσβεστική χρειάζεται λεπτά για να φτάσει, η φωτιά χρειάζεται λεπτά για να καταστρέψει. Ένα σύστημα που βρίσκεται ήδη μέσα στον πίνακα ή στο μηχανοστάσιο σβήνει τη φωτιά πριν καν τη δει κάποιος.</p>
            """),
    )),
)

feidias = section(
    "Γ. ΦΕΙΔΙΑΣ (σωλήνας)", "#f3f6fa", "upk-feidias",
    row("1_2,1_2",
        column("1_2", text("""
            <span class="upk-badge">Σωλήνας κατάσβεσης</span>
            <h2>ΦΕΙΔΙΑΣ FK-5-1-12: ο σωλήνας που βρίσκει τη φωτιά και τη σβήνει</h2>
            <p class="upk-lead">Ένας εύκαμπτος, θερμοευαίσθητος σωλήνας που κάνει τρεις δουλειές μαζί: είναι ο ανιχνευτής, η δεξαμενή του κατασβεστικού και το ακροφύσιο. Περνάει μέσα από τον χώρο που θέλετε να προστατέψετε και στερεώνεται απλώς με δεματικά.</p>
            <p>Όταν η θερμοκρασία ανέβει, ο σωλήνας λιώνει ακριβώς στο σημείο της φωτιάς. Από εκείνη την οπή βγαίνει το αέριο και σβήνει την εστία. Δεν χρειάζεται ρεύμα, ηλεκτρονικά ή άνθρωπο να το ενεργοποιήσει.</p>
            <ul class="upk-ticks">
            <li><b>Χωρίς συντήρηση</b> σε όλη τη διάρκεια ζωής του, έως και 10 χρόνια</li>
            <li><b>Μανόμετρο</b> για να βλέπετε την πίεση με μια ματιά</li>
            <li><b>Προαιρετικός πιεσοστάτης</b> που στέλνει σήμα στον πίνακα πυρανίχνευσης ή σε φαροσειρήνα</li>
            <li><b>Για φωτιές κατηγορίας A, B, C και ηλεκτρικές</b></li>
            <li><b>Αβλαβές</b> για τον εξοπλισμό και τους ανθρώπους στον χώρο</li>
            </ul>
            """)),
        column("1_2",
            image("feidias-diagram.jpg", "Μέρη του συστήματος ΦΕΙΔΙΑΣ: θερμοευαίσθητος σωλήνας, ανοξείδωτα ρακόρ, μανόμετρο, πιεσοστάτης", "framed"),
            text('<p class="upk-caption">Τα μέρη του συστήματος: θερμοευαίσθητος σωλήνας, ανοξείδωτα ρακόρ, μανόμετρο και προαιρετικός πιεσοστάτης.</p>'))),
    row("4_4", column("4_4",
        image("feidias-steps.jpg", "Τέσσερα βήματα λειτουργίας σε κινητήρα: εγκατάσταση, ανίχνευση, κατάσβεση, ολοκλήρωση", "framed"),
        text('<p class="upk-caption">Πώς λειτουργεί σε κινητήρα: εγκατάσταση, ανίχνευση, κατάσβεση, ολοκλήρωση.</p>'))),
    row("1_2,1_2",
        column("1_2",
            image("feidias-white.jpg", "ΦΕΙΔΙΑΣ T Series λευκός σωλήνας", "framed"),
            text("""
                <div class="upk-card"><h4>T Series · λευκός σωλήνας</h4>
                <p>Για εσωτερικούς, κλειστούς χώρους με ηλεκτρικό και ηλεκτρονικό εξοπλισμό.</p>
                <ul><li>Ηλεκτρολογικοί πίνακες, ερμάρια ασφαλειών, τροφοδοτικά</li><li>Racks και δικτυακός εξοπλισμός, οπτικοακουστικά</li><li>ATM, 3D εκτυπωτές</li></ul>
                <div class="upk-spec"><span>0,25 έως 4 m</span><span>έως 1,8 m³ σε πίνακα</span><span>NFPA 2001:2022</span></div></div>
                """)),
        column("1_2",
            image("feidias-black.jpg", "ΦΕΙΔΙΑΣ T Series R μαύρος σωλήνας", "framed"),
            text("""
                <div class="upk-card"><h4>T Series R · μαύρος σωλήνας</h4>
                <p>Ενισχυμένος για κινητήρες και σκληρά περιβάλλοντα, από −20 έως 90 °C.</p>
                <ul><li>Κινητήρες αυτοκινήτων, φορτηγών, λεωφορείων</li><li>Μηχανοστάσια σκαφών και εξωλέμβιες</li><li>Κλαρκ, εκσκαφείς, γερανοί, γεωργικά μηχανήματα</li></ul>
                <div class="upk-spec"><span>0,25 έως 7 m</span><span>έως 3,6 m³ σε πίνακα</span><span>NFPA 2001:2022</span></div></div>
                """))),
)

amfe = section(
    "Δ. AMFE (φιαλίδια)", "#ffffff", "upk-amfe",
    row("1_2,1_2",
        column("1_2",
            image("amfe-cabinet.jpg", "Δύο φιαλίδια AMFE τοποθετημένα σε ηλεκτρολογικό πίνακα", "framed"),
            text('<p class="upk-caption">Δύο φιαλίδια AMFE εγκατεστημένα σε ηλεκτρολογικό πίνακα.</p>')),
        column("1_2",
            text("""
                <span class="upk-badge">Φιαλίδια κατάσβεσης</span>
                <h2>AMFE: αυτόματος πυροσβεστήρας μινιατούρας</h2>
                <p class="upk-lead">Μικρά φιαλίδια με αέριο FK-5-1-12 και κεφαλή με θερμοευαίσθητη αμπούλα. Τοποθετούνται μέσα σε πίνακες, μηχανήματα και συσκευές και αδειάζουν αυτόματα μόλις η θερμοκρασία φτάσει το όριο ενεργοποίησης.</p>
                <p>Είναι πιστοποιημένα κατά VdS και προτείνονται από ασφαλιστικές εταιρείες. Τα χρησιμοποιούν ήδη εταιρείες όπως η TK Elevator, ο ταξιδιωτικός όμιλος FTI και το ζυθοποιείο Oettinger.</p>
                """),
            code("""
                <p style="font-weight:600;margin:0 0 4px">Θερμοκρασίες ενεργοποίησης</p>
                <div class="upk-temps"><span style="background:#e0a100">68 °C</span><span style="background:#d1342f">79 °C</span><span style="background:#2b7a3d">93 °C</span><span style="background:#2c62c6">141 °C</span><span style="background:#6d3fb3">182 °C</span></div>
                <div class="upk-heads"><div class="upk-head-card"><b>AMFE</b><span>Θερμική ενεργοποίηση</span></div><div class="upk-head-card"><b>S-AMFE</b><span>Θερμική, με σήμα ενεργοποίησης</span></div><div class="upk-head-card"><b>R-AMFE</b><span>Θερμική ή απομακρυσμένη, με σήμα</span></div></div>
                """))),
    row("1_2,1_2",
        column("1_2",
            image("amfe-sizes.jpg", "Τα 6 μεγέθη φιαλιδίων AMFE", "framed upk-sizes"),
            text("""
                <div class="upk-card"><h4>6 μεγέθη για κάθε όγκο</h4>
                <p>Το φιαλίδιο διαλέγεται με βάση τον όγκο του πίνακα ή του μηχανήματος.</p>
                <div class="upk-spec"><span>24 ml έως 603 ml</span><span>έως ~1,2 m³ ανά φιαλίδιο</span><span>0,25 έως 2,7 kg</span></div></div>
                """)),
        column("1_2",
            image("amfe-steps.jpg", "Εγκατάσταση σε πίνακα, η φωτιά ξεσπά, το AMFE τη σβήνει", "framed"),
            text("""
                <div class="upk-card"><h4>Σβήνει και ειδοποιεί</h4>
                <ul><li>Σβήνει γρήγορα, χωρίς να αφήνει υπολείμματα</li><li>Οι εκδόσεις S και R αναφέρουν το συμβάν σε πίνακα ή φαροσειρήνα</li><li>Έλεγχος μία φορά τον χρόνο από το μανόμετρο ή συνεχής ψηφιακή παρακολούθηση πίεσης (4–20 mA)</li><li>Με τη μονάδα ελέγχου Mini συνδυάζεται με ανιχνευτές καπνού και φαροσειρήνα</li></ul></div>
                """))),
)

compare = section(
    "Ε. Σύγκριση", "#f3f6fa", "upk-compare",
    row("4_4", column("4_4",
        text("""
            <h2>Σωλήνας ή φιαλίδιο;</h2>
            <p class="upk-lead">Συχνά συνδυάζονται. Μετά την αυτοψία σάς προτείνουμε τη λύση που ταιριάζει στον χώρο σας.</p>
            """),
        code("""
            <div class="upk-tablewrap"><table>
            <thead><tr><th scope="col"></th><th scope="col">ΦΕΙΔΙΑΣ (σωλήνας)</th><th scope="col">AMFE (φιαλίδιο)</th></tr></thead>
            <tbody>
            <tr><th scope="row">Πώς ανιχνεύει</th><td>Σε όλο το μήκος του σωλήνα</td><td>Στο σημείο της κεφαλής</td></tr>
            <tr><th scope="row">Ιδανικό για</th><td>Μακριούς ή ακανόνιστους χώρους, κινητήρες, οχήματα, σκάφη</td><td>Πίνακες, συσκευές, αυτόματους πωλητές, οθόνες</td></tr>
            <tr><th scope="row">Κάλυψη</th><td>Μήκη 0,25 έως 7 m</td><td>6 μεγέθη, έως ~1,2 m³ το καθένα</td></tr>
            <tr><th scope="row">Ειδοποίηση</th><td>Με προαιρετικό πιεσοστάτη</td><td>Με κεφαλή S-AMFE / R-AMFE ή αισθητήρα 4–20 mA</td></tr>
            <tr><th scope="row">Συντήρηση</th><td>Καμία, έως 10 χρόνια ζωής</td><td>Έλεγχος μανομέτρου μία φορά τον χρόνο</td></tr>
            <tr><th scope="row">Κατασβεστικό</th><td colspan="2">FK-5-1-12, καθαρό αέριο που δεν αφήνει υπολείμματα</td></tr>
            </tbody></table></div>
            """),
    )),
)

agent = section(
    "ΣΤ. Το αέριο FK-5-1-12", "#ffffff", "upk-agent",
    row("1_2,1_2",
        column("1_2", text("""
            <span class="upk-eyebrow">Clean agent</span>
            <h2>Σβήνει τη φωτιά χωρίς να καταστρέψει τον εξοπλισμό</h2>
            <p class="upk-lead">Το νερό και η σκόνη σβήνουν τη φωτιά αλλά συχνά καταστρέφουν ό,τι έσωσαν. Το FK-5-1-12 απορροφά τη θερμότητα και σπάει τη χημική αντίδραση της καύσης. Μετά την κατάσβεση ο πίνακας ή το μηχάνημα μένει καθαρό και επιστρέφει γρήγορα σε λειτουργία.</p>
            """)),
        column("1_2", code("""
            <div class="upk-props"><div>Δεν είναι αγώγιμο</div><div>Δεν διαβρώνει</div><div>Δεν αφήνει κατάλοιπα</div><div>Δεν θέλει καθαρισμό</div><div>Μη τοξικό</div><div>Φιλικό προς το περιβάλλον</div></div>
            """))),
)

apps = section(
    "Ζ. Εφαρμογές", "#f3f6fa", "upk-apps-sec",
    row("4_4", column("4_4",
        text("<h2>Πού τα τοποθετούμε</h2>"),
        image("feidias-apps.jpg", "Εφαρμογές: 3D εκτυπωτής, κινητήρας αυτοκινήτου, ηλεκτρολογικός πίνακας", "framed"),
        code('<div class="upk-apps">' + "".join(
            f'<div class="upk-app"><b>{b}</b><span>{s}</span></div>' for b, s in [
                ("Ηλεκτρολογικοί πίνακες", "Βιομηχανία, κτίρια, κατοικίες"),
                ("Server racks", "Δικτυακός εξοπλισμός, UPS, τροφοδοτικά"),
                ("Οχήματα και μηχανήματα", "Κινητήρες, κλαρκ, εκσκαφείς, τρακτέρ"),
                ("Σκάφη", "Μηχανοστάσια, εξωλέμβιες"),
                ("Καταστήματα", "Αυτόματοι πωλητές, ψηφιακές οθόνες"),
                ("Τράπεζες", "ATM και θυρίδες εξυπηρέτησης"),
                ("Μουσεία, αρχεία", "Βιτρίνες και ευαίσθητα εκθέματα"),
                ("Παραγωγή", "3D εκτυπωτές, μηχανήματα παραγωγής"),
            ]) + "</div>"),
    )),
)

cta = section(
    "Η. Επικοινωνία", "#0f1823", "upk-cta",
    row("3_5,2_5",
        column("3_5", text("""
            <h2>Μελέτη, εγκατάσταση και υποστήριξη από την Under Protection Security</h2>
            <p>Ερχόμαστε στον χώρο σας, μετράμε τους όγκους των πινάκων και των μηχανημάτων και σας προτείνουμε τη σωστή λύση, όπως ορίζει το πρότυπο NFPA 2001. Αναλαμβάνουμε την εγκατάσταση και τη σύνδεση με το υπάρχον σύστημα πυρανίχνευσης.</p>
            <div class="upk-btns"><a class="upk-btn primary" href="%s">Κλείστε ραντεβού</a></div>
            """ % BOOKING)),
        column("2_5", text("""
            <div class="upk-contact"><small>Τηλέφωνο</small><a class="big" style="color:#f4f7fb" href="tel:2106096050">210 609 6050</a><small>Email</small><a style="color:#f4f7fb" href="mailto:info@underpro-security.gr">info@underpro-security.gr</a><small>Έδρα</small><span>25ης Μαρτίου 34, Μελίσσια 151 27</span></div>
            """))),
)

sources = section(
    "Θ. Πηγές", "#ffffff", "upk-sources",
    row("4_4", column("4_4", text("""
        <h3>Πηγές στατιστικών</h3>
        <ol>
        <li>UL Fire Safety Research Institute, <a href="https://fsri.org/research/new-comparison-natural-and-synthetic-home-furnishings" target="_blank" rel="noopener">New Comparison of Natural and Synthetic Home Furnishings</a>: flashover σε 4′50″ με συνθετικά έπιπλα, πάνω από 30′ με φυσικά.</li>
        <li>Ready.gov, U.S. Department of Homeland Security, <a href="https://www.ready.gov/home-fires" target="_blank" rel="noopener">Home Fires</a>.</li>
        <li>NFPA, <a href="https://www.nfpa.org/education-and-research/research/nfpa-research/fire-statistical-reports/us-experience-with-sprinklers" target="_blank" rel="noopener">U.S. Experience with Sprinklers</a>: στοιχεία για αυτόματα συστήματα κατάσβεσης (sprinklers).</li>
        <li>IFS, Brandursachenstatistik 2002–2023, όπως παρατίθεται στον κατάλογο AMFE της MOBIAK.</li>
        <li>FEMA, όπως παρατίθεται από το Congressional Research Service, <a href="https://www.congress.gov/crs-product/R47631" target="_blank" rel="noopener">Federal Disaster Assistance for Businesses</a>.</li>
        <li>Α. Γκουρμπάτσης, Αντιστράτηγος ε.α., πρώην Υπαρχηγός Π.Σ., <a href="https://www.eglimata-emprismou.gr/%CE%84%CE%B8%CE%AC%CE%BD%CE%B1%CF%84%CE%BF%CE%B9-%CE%B1%CF%80%CF%8C-%CE%B1%CF%83%CF%84%CE%B9%CE%BA%CE%AD%CF%82-%CF%80%CF%85%CF%81%CE%BA%CE%B1%CE%B3%CE%B9%CE%AD%CF%82/" target="_blank" rel="noopener">Θάνατοι από αστικές πυρκαγιές την εποχή της πανδημίας</a> (2021), με στοιχεία του Αρχηγείου Πυροσβεστικού Σώματος. Τα πλήρη ετήσια στοιχεία δημοσιεύονται στα <a href="https://www.fireservice.gr/synola-dedomenon" target="_blank" rel="noopener">ανοιχτά δεδομένα του Πυροσβεστικού Σώματος</a>.</li>
        <li>ΕΛΙΤΗΕ, όπως δημοσιεύτηκε στη <a href="https://www.naftemporiki.gr/finance/economy/2071111/ilektrosok-elitie-gia-tis-ilektrikes-paroches-sta-ktiria/" target="_blank" rel="noopener">Ναυτεμπορική</a> και στα <a href="https://www.tanea.gr/print/2026/02/11/economy/sos-gia-palia-ktiria-kai-ilektrikes-egkatastaseis/" target="_blank" rel="noopener">ΝΕΑ</a> (Φεβρουάριος 2026).</li>
        <li>ΕΛΙΠΥΚΑ, <a href="https://elipyka.org/elegxoi-ilektrikwn-ktiriakwn-egkatastasewn-gia-prolipsi-meros-a/" target="_blank" rel="noopener">Έλεγχοι ηλεκτρικών κτιριακών εγκαταστάσεων για πρόληψη και προστασία από πυρκαγιά</a>.</li>
        </ol>
        """))),
)

content = hero + speed + feidias + amfe + compare + agent + apps + cta + sources

images = {}
for i, name in enumerate(USED_IMAGES, start=1):
    url = IMG_BASE + name
    images[url] = {
        "encoded": base64.b64encode((IMG_DIR / name).read_bytes()).decode(),
        "url": url,
        "id": 900000 + i,
    }

layout = {
    "context": "et_builder",
    "data": {"1": content},
    "presets": {},
    "global_colors": [],
    "images": images,
    "thumbnails": [],
}

out = HERE / "autokatasvesi-divi.json"
out.write_text(json.dumps(layout, ensure_ascii=False), encoding="utf-8")
print(f"wrote {out.name}: {out.stat().st_size // 1024} KB, {len(USED_IMAGES)} images, "
      f"{content.count('[et_pb_section ')} sections")
