.store-logo{display:inline-flex;align-items:stretch;gap:.85rem;text-decoration:none!important;line-height:1;color:var(--lux-text,var(--text));padding:.15rem 0;transition:opacity .35s var(--lux-ease,cubic-bezier(.22,1,.36,1))}
.store-logo-accent{flex-shrink:0;width:1px;align-self:stretch;min-height:2.15rem;background:linear-gradient(180deg,transparent 0%,var(--lux-gold,#c9a962) 18%,var(--lux-gold,#c9a962) 82%,transparent 100%);opacity:.72;transition:opacity .35s ease,box-shadow .35s ease}
.store-logo-stack{display:flex;flex-direction:column;justify-content:center;gap:.38rem;min-width:0}
.store-logo-eyebrow{display:inline-flex;align-items:center;gap:.55rem;font-family:var(--lux-font-display,'Syne',system-ui,sans-serif);font-size:.5rem;font-weight:600;letter-spacing:.28em;text-transform:uppercase;color:var(--lux-gold,#c9a962);white-space:nowrap;opacity:.88}
.store-logo-eyebrow::before{content:'';width:18px;height:1px;background:currentColor;opacity:.65;flex-shrink:0}
.store-logo-wordmark{display:flex;flex-wrap:wrap;align-items:baseline;gap:.28rem .32rem}
.store-logo-word{font-family:var(--lux-font-display,'Syne',system-ui,sans-serif);font-weight:800;font-size:1.12rem;letter-spacing:-.025em;line-height:1;color:var(--lux-text,var(--text));transition:color .35s ease}
.store-logo-word--serif{font-family:var(--lux-font-serif,'Cormorant Garamond',Georgia,serif);font-style:italic;font-weight:400;font-size:1.28rem;letter-spacing:.01em;color:var(--lux-gold,#c9a962);transform:translateY(.04em)}
.store-logo:hover{opacity:1}
.store-logo:hover .store-logo-accent{opacity:1;box-shadow:0 0 12px var(--lux-gold-dim,rgba(201,169,98,.35))}
.store-logo:hover .store-logo-eyebrow{color:var(--lux-lime,#c8ff4a)}
.store-logo:hover .store-logo-eyebrow::before{background:var(--lux-lime,#c8ff4a)}
.store-logo--footer{padding:.25rem 0}
.store-logo--footer .store-logo-accent{min-height:2.55rem}
.store-logo--footer .store-logo-eyebrow{font-size:.54rem;letter-spacing:.3em}
.store-logo--footer .store-logo-word{font-size:1.32rem}
.store-logo--footer .store-logo-word--serif{font-size:1.52rem}
body.luxury-store .navbar .store-logo{color:var(--lux-text)!important}
[data-theme="light"] .store-logo-eyebrow{color:var(--lux-gold,#9a7728)}
[data-theme="light"] .store-logo-word--serif{color:var(--lux-gold,#9a7728)}
[data-theme="light"] .store-logo:hover .store-logo-eyebrow{color:var(--lux-lime,#7fa800)}
@media (max-width:991px){.store-logo-eyebrow{font-size:.46rem;letter-spacing:.22em}.store-logo-word{font-size:1.02rem}.store-logo-word--serif{font-size:1.16rem}}
@media (max-width:380px){.store-logo-eyebrow{display:none}.store-logo-accent{min-height:1.65rem}}
@media (prefers-reduced-motion:reduce){.store-logo,.store-logo-accent,.store-logo-word,.store-logo-eyebrow{transition:none}}
