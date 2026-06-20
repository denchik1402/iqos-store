.store-logo{display:inline-flex;align-items:center;gap:.75rem;text-decoration:none!important;line-height:1;color:var(--lux-text,var(--text));margin-right:.5rem;flex-shrink:0;white-space:nowrap;transition:opacity .35s var(--lux-ease,cubic-bezier(.22,1,.36,1))}
.store-logo-accent{flex-shrink:0;width:1px;height:1.75rem;background:linear-gradient(180deg,transparent 0%,var(--lux-gold,#c9a962) 20%,var(--lux-gold,#c9a962) 80%,transparent 100%);opacity:.75;transition:opacity .35s ease,box-shadow .35s ease}
.store-logo-wordmark{display:inline-flex;align-items:baseline;gap:.34rem}
.store-logo-word{font-family:var(--lux-font-display,'Syne',system-ui,sans-serif);font-weight:800;font-size:1.42rem;letter-spacing:-.03em;line-height:1;color:var(--lux-text,var(--text));transition:color .35s ease}
.store-logo-word--serif{font-family:var(--lux-font-serif,'Cormorant Garamond',Georgia,serif);font-style:italic;font-weight:400;font-size:1.62rem;letter-spacing:.01em;color:var(--lux-gold,#c9a962);transform:translateY(.05em)}
.store-logo:hover .store-logo-accent{opacity:1;box-shadow:0 0 10px var(--lux-gold-dim,rgba(201,169,98,.35))}
.store-logo:hover .store-logo-word--serif{color:var(--lux-lime,#c8ff4a)}
.store-logo--footer{margin-right:0;margin-bottom:.25rem}
.store-logo--footer .store-logo-accent{height:2rem}
.store-logo--footer .store-logo-word{font-size:1.65rem}
.store-logo--footer .store-logo-word--serif{font-size:1.88rem}
body.luxury-store .navbar .store-logo{color:var(--lux-text)!important}
[data-theme="light"] .store-logo-word--serif{color:var(--lux-gold,#9a7728)}
[data-theme="light"] .store-logo:hover .store-logo-word--serif{color:var(--lux-lime,#7fa800)}
@media (max-width:991px){.store-logo-word{font-size:1.28rem}.store-logo-word--serif{font-size:1.46rem}.store-logo-accent{height:1.55rem}}
@media (max-width:380px){.store-logo-word{font-size:1.15rem}.store-logo-word--serif{font-size:1.32rem}}
@media (prefers-reduced-motion:reduce){.store-logo,.store-logo-accent,.store-logo-word{transition:none}}
