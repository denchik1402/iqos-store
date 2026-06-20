.store-logo{display:inline-flex;align-items:center;gap:.7rem;text-decoration:none!important;line-height:1;color:var(--lux-text,var(--text))}
.store-logo-mark{position:relative;width:40px;height:40px;flex-shrink:0;border-radius:12px;background:linear-gradient(145deg,var(--lux-gold,#c9a962) 0%,#e8d5a3 42%,#9a7728 100%);box-shadow:0 4px 18px var(--lux-gold-dim,rgba(201,169,98,.35)),inset 0 1px 0 rgba(255,255,255,.4);animation:store-logo-glow 3.4s ease-in-out infinite;overflow:hidden}
.store-logo-mark::before{content:'';position:absolute;inset:-2px;border-radius:14px;padding:2px;background:linear-gradient(135deg,rgba(201,169,98,.85),rgba(200,255,74,.25),rgba(201,169,98,.12));-webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;opacity:.9;pointer-events:none}
.store-logo-mark-glow{position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,rgba(255,255,255,.45),transparent 55%);pointer-events:none}
.store-logo-mark-core{position:absolute;inset:9px 11px 9px 9px;border-radius:4px 4px 2px 2px;background:linear-gradient(180deg,rgba(255,255,255,.96) 0%,rgba(255,255,255,.58) 100%);box-shadow:0 1px 4px rgba(0,0,0,.18);transform:rotate(-8deg);transform-origin:bottom center}
.store-logo-mark-core::after{content:'';position:absolute;left:50%;bottom:-3px;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:rgba(255,255,255,.92);box-shadow:0 0 8px rgba(255,255,255,.75)}
.store-logo-text{display:flex;flex-direction:column;gap:.06rem}
.store-logo-brand{font-family:var(--lux-font-display,'Syne',system-ui,sans-serif);font-weight:600;font-size:.56rem;letter-spacing:.32em;text-indent:.32em;color:var(--lux-gold,#c9a962);line-height:1.1}
.store-logo-name{font-family:var(--lux-font-display,'Syne',system-ui,sans-serif);font-weight:800;font-size:1.18rem;letter-spacing:.08em;color:var(--lux-text,var(--text));line-height:1.02;transition:color .25s ease}
.store-logo-tag{font-family:var(--lux-font-display,'Syne',system-ui,sans-serif);font-weight:500;font-size:.5rem;letter-spacing:.24em;text-indent:.24em;color:var(--lux-muted,var(--text-muted));margin-top:.12rem;opacity:.92}
.store-logo:hover .store-logo-name{color:var(--lux-lime,#c8ff4a)}
.store-logo:hover .store-logo-mark{transform:translateY(-1px);transition:transform .25s var(--lux-ease,cubic-bezier(.22,1,.36,1))}
.store-logo--footer .store-logo-mark{width:46px;height:46px}
.store-logo--footer .store-logo-name{font-size:1.38rem}
.store-logo--footer .store-logo-tag{font-size:.56rem}
[data-theme="light"] .store-logo-mark{background:linear-gradient(145deg,#b8922e 0%,#dcc98a 45%,#7a5c18 100%);box-shadow:0 4px 16px var(--lux-gold-dim,rgba(154,119,40,.22)),inset 0 1px 0 rgba(255,255,255,.5)}
[data-theme="light"] .store-logo:hover .store-logo-name{color:var(--lux-gold,#9a7728)}
@keyframes store-logo-glow{0%,100%{box-shadow:0 4px 16px var(--lux-gold-dim,rgba(201,169,98,.28)),inset 0 1px 0 rgba(255,255,255,.35)}50%{box-shadow:0 8px 24px rgba(200,255,74,.18),0 4px 20px var(--lux-gold-dim,rgba(201,169,98,.42)),inset 0 1px 0 rgba(255,255,255,.45)}}
@media (prefers-reduced-motion:reduce){.store-logo-mark{animation:none}.store-logo:hover .store-logo-mark{transform:none}}
@media (max-width:380px){.store-logo-tag{display:none}.store-logo-name{font-size:1.05rem}}
