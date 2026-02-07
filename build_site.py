#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import datetime as _dt
import zipfile


# =========================
# Config
# =========================
SITE_URL = "https://1zerobyte1.github.io/"
BUILD_ID = _dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# ✅ روابطك كما طلبت (بنفس أسماء المفاتيح)
LINKS = {
    "github": "https://github.com/1ZeroByte1",
    "linkedin": "https://www.linkedin.com/in/husseinalyafeai",
    "YouTube": "https://www.youtube.com/@1ZeroByte1",
    "X": "https://github.com/1ZeroByte1",
    "certificates": "https://drive.google.com/drive/folders/18SYLIKeETIyENgRCTukXRsq3a09OQ0d9",
}

# =========================
# Files content
# =========================

ICON_SVG = r"""<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 64 64">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#00ff88"/>
      <stop offset="1" stop-color="#00d4ff"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="#000"/>
  <path d="M14 20h36v24H14z" fill="none" stroke="url(#g)" stroke-width="2"/>
  <text x="32" y="39" text-anchor="middle" font-family="Courier New, monospace" font-size="18" fill="#00ff88">0x</text>
</svg>
"""

MANIFEST = r"""{
  "name": "ZeroByte :: Terminal",
  "short_name": "ZeroByte",
  "start_url": "./",
  "display": "standalone",
  "background_color": "#050607",
  "theme_color": "#00ff88",
  "icons": [
    { "src": "assets/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable" }
  ]
}
"""

SERVICE_WORKER = r"""/* ZeroByte PWA Service Worker (simple + safe cache) */
const CACHE = "zerobyte-terminal-v1";
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./service-worker.js",
  "./robots.txt",
  "./sitemap.xml",
  "./assets/icon.svg"
];

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await cache.addAll(ASSETS);
    self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.map(k => (k === CACHE ? null : caches.delete(k))));
    self.clients.claim();
  })());
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  // network-first for navigations, cache-first for static
  if (req.mode === "navigate") {
    event.respondWith((async () => {
      try {
        const fresh = await fetch(req);
        const cache = await caches.open(CACHE);
        cache.put("./", fresh.clone());
        return fresh;
      } catch {
        const cached = await caches.match("./");
        return cached || caches.match("./index.html");
      }
    })());
    return;
  }

  event.respondWith((async () => {
    const cached = await caches.match(req);
    if (cached) return cached;
    try {
      const fresh = await fetch(req);
      const cache = await caches.open(CACHE);
      cache.put(req, fresh.clone());
      return fresh;
    } catch {
      return cached;
    }
  })());
});
"""

ROBOTS = r"""User-agent: *
Allow: /
Sitemap: https://1zerobyte1.github.io/sitemap.xml
"""

SITEMAP = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{SITE_URL}</loc>
    <lastmod>{_dt.date.today().isoformat()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""

README = f"""# ZeroByte Terminal Portfolio (GitHub Pages)

This repo powers: {SITE_URL}

## Features
- Terminal-style portfolio (fast, single-page, no dependencies)
- SEO meta + structured data
- PWA (installable) + offline cache
- Command history + autocomplete (Tab) + shortcuts

## Commands
Type in the terminal:
- help, about, skills, exp, projects, edu, vol, courses, links, contact
- open <target>, copy <target>, theme, clear, banner, status, pwa, shortcuts

## Deploy
Just push to `main`. GitHub Pages will publish automatically.

Build: {BUILD_ID}
"""

INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="color-scheme" content="dark" />
  <meta name="theme-color" content="#00ff88" />
  <meta name="description" content="ZeroByte (Hussein W. Al-yafeai) — Security Researcher focused on reverse engineering and binary exploitation." />
  <meta name="keywords" content="ZeroByte, Hussein Al-yafeai, reverse engineering, binary exploitation, exploit development, CTF, bug bounty" />
  <meta name="author" content="ZeroByte" />
  <link rel="canonical" href="https://1zerobyte1.github.io/" />

  <!-- OpenGraph / Twitter -->
  <meta property="og:title" content="ZeroByte :: terminal" />
  <meta property="og:description" content="Reverse Engineering • Pwn • Exploit Dev • Bug Bounty" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://1zerobyte1.github.io/" />
  <meta name="twitter:card" content="summary" />

  <title>ZeroByte :: terminal</title>

  <!-- Favicon (inline SVG) -->
  <link rel="icon" href='data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="%23000"/><text x="50%25" y="52%25" font-size="28" text-anchor="middle" fill="%2300ff88" font-family="Courier New, monospace">0x</text></svg>'/>

  <!-- PWA -->
  <link rel="manifest" href="./manifest.webmanifest" />

  <style>
    :root{
      --bg:#050607;
      --panel:#0b0d10;
      --border:#1b2330;
      --text:#d5fbe8;
      --muted:#9bb1a6;
      --accent:#00ff88;
      --accent2:#00d4ff;
      --danger:#ff3b30;
      --warn:#ffcc00;
      --ok:#34c759;
      --shadow: 0 10px 35px rgba(0,0,0,.55);
      --radius: 18px;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono","Courier New", monospace;
    }
    [data-theme="amber"]{ --accent:#ffcc00; --accent2:#ff7a00; }
    [data-theme="ice"]{ --accent:#00d4ff; --accent2:#a855f7; }

    *{ box-sizing:border-box; }
    body{
      margin:0;
      min-height:100vh;
      background:
        radial-gradient(1200px 700px at 15% 10%, rgba(0,255,136,.12), transparent 60%),
        radial-gradient(900px 600px at 85% 30%, rgba(0,212,255,.10), transparent 55%),
        radial-gradient(900px 700px at 60% 90%, rgba(168,85,247,.08), transparent 55%),
        var(--bg);
      color:var(--text);
      font-family: var(--mono);
      display:flex;
      align-items:center;
      justify-content:center;
      padding: 28px;
    }

    .wrap{ width:min(1024px, 100%); }
    .topbar{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      margin-bottom: 14px;
      opacity:.95;
    }
    .brand{
      display:flex;
      align-items:center;
      gap:10px;
      color:var(--muted);
      font-size:14px;
      letter-spacing:.2px;
    }
    .pill{
      border:1px solid var(--border);
      background: rgba(0,0,0,.22);
      padding:8px 12px;
      border-radius:999px;
      display:inline-flex;
      gap:10px;
      align-items:center;
      box-shadow: 0 6px 18px rgba(0,0,0,.28);
    }
    .dot{ width:10px;height:10px;border-radius:50%; display:inline-block; }
    .dot.r{ background:var(--danger); }
    .dot.y{ background:var(--warn); }
    .dot.g{ background:var(--ok); }

    .actions{
      display:flex;
      gap:8px;
      flex-wrap:wrap;
      justify-content:flex-end;
    }
    button, .btn{
      cursor:pointer;
      font-family:var(--mono);
      font-size:13px;
      color:var(--text);
      background: rgba(0,0,0,.25);
      border:1px solid var(--border);
      padding:8px 10px;
      border-radius:12px;
      transition: transform .08s ease, border-color .2s ease, background .2s ease;
    }
    button:hover, .btn:hover{ border-color: rgba(0,255,136,.35); transform: translateY(-1px); }
    button:active, .btn:active{ transform: translateY(0px); }

    .terminal{
      border:1px solid var(--border);
      background: linear-gradient(180deg, rgba(11,13,16,.96), rgba(7,8,10,.92));
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow:hidden;
    }
    .term-head{
      display:flex;
      align-items:center;
      justify-content:space-between;
      padding: 12px 14px;
      border-bottom:1px solid var(--border);
      background: rgba(0,0,0,.25);
    }
    .title{
      font-size:13px;
      color:var(--muted);
      display:flex;
      align-items:center;
      gap:10px;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }
    .kbd{
      font-size:12px;
      color:var(--muted);
      border:1px solid var(--border);
      padding:2px 8px;
      border-radius:999px;
      background: rgba(0,0,0,.25);
    }

    .term-body{ padding: 18px 16px 12px; }
    #out{
      white-space:pre-wrap;
      word-break:break-word;
      line-height: 1.55;
      font-size: 14px;
      min-height: 52vh;
      max-height: 62vh;
      overflow:auto;
      padding-right: 6px;
    }
    .line{ margin: 0 0 2px 0; }
    .prompt{ color: var(--accent); }
    .cmd{ color: var(--accent2); }
    .muted{ color: var(--muted); }
    .hr{ height:1px; background: var(--border); margin: 10px 0 12px; opacity:.9; }
    .link{ color: var(--accent); text-decoration:none; }
    .link:hover{ text-decoration:underline; }

    .chips{ display:flex; flex-wrap:wrap; gap:8px; margin: 10px 0 2px; }
    .chip{
      border:1px solid var(--border);
      background: rgba(0,0,0,.18);
      padding:6px 10px;
      border-radius:999px;
      font-size:12px;
      color: var(--muted);
      cursor:pointer;
      user-select:none;
    }
    .chip:hover{ border-color: rgba(0,255,136,.35); }

    .input-row{
      display:flex;
      align-items:center;
      gap:10px;
      border-top:1px solid var(--border);
      padding: 12px 14px;
      background: rgba(0,0,0,.18);
    }
    .ps1{ color: var(--accent); font-size: 14px; white-space:nowrap; }
    input{
      width:100%;
      background: transparent;
      border:0;
      outline:none;
      color: var(--text);
      font-family: var(--mono);
      font-size: 14px;
    }

    .toast{
      position: fixed;
      bottom: 18px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(0,0,0,.65);
      border: 1px solid var(--border);
      padding: 10px 12px;
      border-radius: 14px;
      color: var(--text);
      font-size: 13px;
      box-shadow: var(--shadow);
      opacity: 0;
      pointer-events:none;
      transition: opacity .18s ease, transform .18s ease;
    }
    .toast.show{ opacity:1; transform: translateX(-50%) translateY(-2px); }

    @media (prefers-reduced-motion: reduce){
      button, .btn{ transition:none; }
      .toast{ transition:none; }
    }
  </style>

  <script type="application/ld+json">
  {
    "@context":"https://schema.org",
    "@type":"Person",
    "name":"Hussein W. Al-yafeai",
    "alternateName":"ZeroByte",
    "jobTitle":"Security Researcher",
    "knowsAbout":[
      "Reverse engineering",
      "Binary exploitation",
      "Exploit development",
      "CTF",
      "Bug bounty"
    ],
    "address":{
      "@type":"PostalAddress",
      "addressLocality":"Marib",
      "addressCountry":"Yemen"
    }
  }
  </script>
</head>

<body data-theme="green">
  <div class="wrap">
    <div class="topbar">
      <div class="brand pill">
        <span class="dot r" aria-hidden="true"></span>
        <span class="dot y" aria-hidden="true"></span>
        <span class="dot g" aria-hidden="true"></span>
        <span>ZeroByte / <span class="muted">1ZeroByte1</span></span>
      </div>
      <div class="actions">
        <button id="btnHelp" title="Show commands">help</button>
        <button id="btnCopyEmail" title="Copy email">copy email</button>
        <button id="btnTheme" title="Toggle theme">theme</button>
      </div>
    </div>

    <div class="terminal" role="application" aria-label="Terminal portfolio">
      <div class="term-head">
        <div class="title">
          <span class="pill" style="padding:6px 10px;border-radius:12px;">
            <span class="prompt">root@zerobyte</span>:<span class="cmd">~</span># portfolio
          </span>
          <span class="kbd">Tab autocomplete • Ctrl+L clear</span>
        </div>
        <div class="kbd">Build: {{BUILD_ID}}</div>
      </div>

      <div class="term-body">
        <div class="chips" id="chips"></div>
        <div id="out" aria-live="polite"></div>
      </div>

      <div class="input-row">
        <div class="ps1"><span class="prompt">root@zerobyte</span>:<span class="cmd">~</span>#</div>
        <input id="in" autocomplete="off" spellcheck="false" placeholder="help | about | skills | exp | projects | edu | courses | contact | links" />
      </div>
    </div>
  </div>

  <div class="toast" id="toast">copied</div>

  <noscript>
    <div style="position:fixed;top:10px;left:10px;background:#000;color:#00ff88;border:1px solid #1b2330;padding:10px;border-radius:12px;">
      This site works best with JavaScript enabled.
    </div>
  </noscript>

  <script>
    // ====== Config ======
    const PROFILE = {
      handle: "ZeroByte",
      realName: "Hussein W. Al-yafeai",
      title: "Security Researcher | Exploit Dev & Binary Exploitation",
      location: "Marib, Yemen",
      email: "7hussein.alyafeai7@gmail.com",
      motto: "0x0 is where they see nothing; I see the beginning."
    };

    // ✅ Your real URLs (keys exactly as you requested)
    const LINKS = {
      github: "{{GITHUB}}",
      linkedin: "{{LINKEDIN}}",
      YouTube: "{{YOUTUBE}}",
      X: "{{X}}",
      certificates: "{{CERTS}}"
    };

    // ====== PWA ======
    if ("serviceWorker" in navigator) {
      window.addEventListener("load", () => {
        navigator.serviceWorker.register("./service-worker.js").catch(()=>{});
      });
    }

    // ====== Terminal engine ======
    const out = document.getElementById("out");
    const input = document.getElementById("in");
    const toast = document.getElementById("toast");
    const chips = document.getElementById("chips");

    const THEMES = ["green", "amber", "ice"];
    let themeIdx = 0;

    const history = [];
    let histIdx = 0;

    const COMMANDS = [
      "help","about","skills","exp","projects","edu","vol","courses","links","contact",
      "open","copy","theme","clear","banner","status","pwa","shortcuts","search"
    ];

    const CHIP_CMDS = ["help","about","skills","links","contact","projects","status","theme"];

    function nowISO(){
      const d = new Date();
      return d.toISOString().replace("T"," ").replace("Z"," UTC");
    }

    function line(html, cls="line"){
      const div = document.createElement("div");
      div.className = cls;
      div.innerHTML = html;
      out.appendChild(div);
      out.scrollTop = out.scrollHeight;
    }

    function hr(){
      const div = document.createElement("div");
      div.className = "hr";
      out.appendChild(div);
      out.scrollTop = out.scrollHeight;
    }

    function toastMsg(msg){
      toast.textContent = msg;
      toast.classList.add("show");
      setTimeout(() => toast.classList.remove("show"), 900);
    }

    async function copyToClipboard(text){
      try{
        await navigator.clipboard.writeText(text);
        toastMsg("copied ✓");
      }catch{
        toastMsg("copy failed");
      }
    }

    function setTheme(name){
      document.body.setAttribute("data-theme", name);
      localStorage.setItem("zb_theme", name);
      toastMsg("theme: " + name);
    }

    function restoreTheme(){
      const saved = localStorage.getItem("zb_theme");
      if(saved && (saved === "green" || saved === "amber" || saved === "ice")){
        setTheme(saved);
        themeIdx = THEMES.indexOf(saved);
        if(themeIdx < 0) themeIdx = 0;
      }
    }

    function escapeHTML(s){
      return String(s)
        .replaceAll("&","&amp;")
        .replaceAll("<","&lt;")
        .replaceAll(">","&gt;")
        .replaceAll('"',"&quot;")
        .replaceAll("'","&#039;");
    }

    function printCmd(raw){
      line(`<span class="prompt">root@zerobyte</span>:<span class="cmd">~</span># <span class="cmd">${escapeHTML(raw)}</span>`);
    }

    function banner(){
      const art = [
        " ________                         ______        __        __        ",
        "/_  __/ /  ___ ___ _  ___  ___  /_  __/__ ____/ /  ___  / /__ ____ ",
        " / / / _ \\/ -_) _ \\\\ |/ / _ \\/ _ \\\\  / / / -_) __/ _ \\/ _ \\/ / -_) __/",
        "/_/ /_//_/\\__/\\___/___/_//_/\\___/ /_/  \\__/\\__/_//_/\\___/_/\\__/_/   "
      ].join("\\n");

      line(`<span class="muted">${nowISO()}</span>`);
      line(`<span class="cmd">${escapeHTML(art).replace(/\\n/g,"<br>")}</span>`);
      line(`<span class="muted">boot:</span> <span class="prompt">${PROFILE.handle}</span> (<span class="muted">${PROFILE.realName}</span>) — <span class="muted">${PROFILE.location}</span>`);
      line(`<span class="muted">role:</span> <span class="cmd">${PROFILE.title}</span>`);
      line(`<span class="muted">motto:</span> <span class="prompt">${escapeHTML(PROFILE.motto)}</span>`);
      hr();
      line(`Type <span class="cmd">help</span> to list commands. Try: <span class="cmd">about</span>, <span class="cmd">skills</span>, <span class="cmd">exp</span>, <span class="cmd">projects</span>.`);
      line(`<span class="muted">Tip:</span> <span class="cmd">Tab</span> autocomplete • <span class="cmd">Ctrl+L</span> clear • <span class="cmd">open github</span>`);
    }

    function help(){
      hr();
      line(`<span class="cmd">help</span>                 show commands`);
      line(`<span class="cmd">about</span>                summary`);
      line(`<span class="cmd">skills</span>               technical + professional skills`);
      line(`<span class="cmd">exp</span>                  bug bounty + ctf experience`);
      line(`<span class="cmd">projects</span>             highlighted work`);
      line(`<span class="cmd">edu</span>                  education + achievements`);
      line(`<span class="cmd">vol</span>                  volunteering / clubs`);
      line(`<span class="cmd">courses</span>              training list`);
      line(`<span class="cmd">links</span>                social links`);
      line(`<span class="cmd">contact</span>              email (copy-ready)`);
      line(`<span class="cmd">open</span> <span class="muted">&lt;github|linkedin|youtube|x|certs&gt;</span> open a link`);
      line(`<span class="cmd">copy</span> <span class="muted">&lt;email|github|linkedin|youtube|x|certs&gt;</span> copy to clipboard`);
      line(`<span class="cmd">search</span> <span class="muted">&lt;word&gt;</span> find command`);
      line(`<span class="cmd">theme</span>                toggle terminal palette`);
      line(`<span class="cmd">banner</span>               print banner again`);
      line(`<span class="cmd">status</span>               site status`);
      line(`<span class="cmd">pwa</span>                  offline/install info`);
      line(`<span class="cmd">shortcuts</span>            keyboard shortcuts`);
      line(`<span class="cmd">clear</span>                clear screen (or Ctrl+L)`);
      hr();
    }

    function about(){
      hr();
      line(`<span class="muted">Summary</span>`);
      line(`Security researcher with hands-on experience in <span class="cmd">CTFs</span>, <span class="cmd">bug bounty</span>, and <span class="cmd">exploit development</span>, focusing on <span class="cmd">binary exploitation</span> and <span class="cmd">reverse engineering</span>.`);
      line(`<span class="muted">Core focus</span> → RE, Pwn, exploit primitives, and vulnerability lifecycle.`);
      hr();
    }

    function skills(){
      hr();
      line(`<span class="muted">Technical</span>`);
      line(`• Reverse Engineering`);
      line(`• PWN / Binary Exploitation`);
      line(`• Penetration Testing (Web/Desktop/Network)`);
      line(`• Assembly, C, Python`);
      line(`<span class="muted">Professional</span>`);
      line(`• Analytical Thinking • Problem Solving • Self-Motivation • Team Collaboration`);
      line(`<span class="muted">Languages</span>`);
      line(`• Arabic (Native) • English (Fluent)`);
      hr();
    }

    function exp(){
      hr();
      line(`<span class="muted">Bug Bounty</span> — <span class="cmd">HackerOne</span> & <span class="cmd">Bugcrowd</span> (Jan 2025 → Present)`);
      line(`• Reported issues (XSS, subdomain takeover, sensitive data exposure).`);
      line(`• Hands-on vulnerability lifecycle: triage → report → remediation verification.`);
      line(`<span class="muted">CTF</span> — HTB & practice platforms`);
      line(`• Advanced pwn/reverse challenges to sharpen exploit development.`);
      hr();
    }

    function projects(){
      hr();
      line(`<span class="muted">Highlighted</span>`);
      line(`• <span class="cmd">Game By C program</span> — text-based strategy game (C)`);
      line(`  Implemented to apply DS/Algo; demonstrates C proficiency.`);
      line(`<span class="muted">Tip:</span> add more repos later, or type <span class="cmd">open github</span>.`);
      hr();
    }

    function edu(){
      hr();
      line(`<span class="muted">Education</span>`);
      line(`High School — Marib, Yemen (Aug 2022 → Jun 2025)`);
      line(`Highlights: strong STEM performance; 1st place in an inter-school scientific competition.`);
      hr();
    }

    function vol(){
      hr();
      line(`<span class="muted">Volunteering / Clubs</span>`);
      line(`• Volunteer — Human Access, Marib (Jun 2023)`);
      line(`• IT Member — local cultural/sports clubs (various dates)`);
      hr();
    }

    function courses(){
      hr();
      line(`<span class="muted">Courses & Training</span>`);
      const items = [
        "pwn.college (practice)",
        "CS50x / CS50AI",
        "OSCP prep (self-study)",
        "CCNA fundamentals",
        "Security+ fundamentals",
        "Assembly practice"
      ];
      items.forEach(x => line("• " + escapeHTML(x)));
      hr();
    }

    function links(){
      hr();
      line(`<span class="muted">Links</span>`);
      line(`• GitHub: <a class="link" href="${LINKS.github}" target="_blank" rel="noopener">${LINKS.github}</a>`);
      line(`• LinkedIn: <a class="link" href="${LINKS.linkedin}" target="_blank" rel="noopener">${LINKS.linkedin}</a>`);
      line(`• YouTube: <a class="link" href="${LINKS.YouTube}" target="_blank" rel="noopener">${LINKS.YouTube}</a>`);
      line(`• X: <a class="link" href="${LINKS.X}" target="_blank" rel="noopener">${LINKS.X}</a>`);
      line(`• Certificates: <a class="link" href="${LINKS.certificates}" target="_blank" rel="noopener">Google Drive</a>`);
      hr();
    }

    function contact(){
      hr();
      line(`<span class="muted">Contact</span>`);
      line(`Email: <span class="cmd">${escapeHTML(PROFILE.email)}</span>  <span class="muted">(try: copy email)</span>`);
      hr();
    }

    function clear(){ out.innerHTML = ""; }

    function theme(){
      themeIdx = (themeIdx + 1) % THEMES.length;
      setTheme(THEMES[themeIdx]);
    }

    function status(){
      hr();
      line(`<span class="muted">status</span> ok`);
      line(`build: <span class="cmd">{{BUILD_ID}}</span>`);
      line(`pwa: <span class="cmd">${("serviceWorker" in navigator) ? "supported" : "not supported"}</span>`);
      line(`theme: <span class="cmd">${document.body.getAttribute("data-theme") || "green"}</span>`);
      hr();
    }

    function pwa(){
      hr();
      line(`<span class="muted">PWA / Offline</span>`);
      line(`• Works offline after first load (service worker cache).`);
      line(`• On mobile: "Add to Home Screen" to install.`);
      hr();
    }

    function shortcuts(){
      hr();
      line(`<span class="muted">Shortcuts</span>`);
      line(`• Tab → autocomplete`);
      line(`• Arrow Up/Down → history`);
      line(`• Ctrl+L → clear`);
      hr();
    }

    function openTarget(t){
      const key = t.toLowerCase();
      const map = {
        "github": LINKS.github,
        "linkedin": LINKS.linkedin,
        "youtube": LINKS.YouTube,
        "x": LINKS.X,
        "certs": LINKS.certificates,
        "certificates": LINKS.certificates
      };
      const url = map[key];
      if(!url){ line(`<span class="muted">Usage:</span> open github|linkedin|youtube|x|certs`); return; }
      window.open(url, "_blank", "noopener");
      line(`<span class="muted">Opened</span> <a class="link" href="${url}" target="_blank" rel="noopener">${escapeHTML(url)}</a>`);
    }

    function copyTarget(t){
      const key = t.toLowerCase();
      const map = {
        "email": PROFILE.email,
        "github": LINKS.github,
        "linkedin": LINKS.linkedin,
        "youtube": LINKS.YouTube,
        "x": LINKS.X,
        "certs": LINKS.certificates,
        "certificates": LINKS.certificates
      };
      const val = map[key];
      if(!val){ line(`<span class="muted">Usage:</span> copy email|github|linkedin|youtube|x|certs`); return; }
      copyToClipboard(val);
      line(`<span class="muted">copied:</span> ${escapeHTML(key)}`);
    }

    function searchCmd(word){
      const w = (word||"").toLowerCase();
      if(!w){ line(`<span class="muted">Usage:</span> search <word>`); return; }
      const matches = COMMANDS.filter(c => c.includes(w));
      hr();
      line(`<span class="muted">matches:</span> ${matches.length ? matches.map(m=>`<span class="cmd">${m}</span>`).join(", ") : "none"}`);
      hr();
    }

    function handle(raw){
      const cmd = raw.trim();
      if(!cmd) return;

      const [base, ...rest] = cmd.split(/\s+/);
      const arg = rest.join(" ").trim();

      switch(base.toLowerCase()){
        case "help": help(); break;
        case "about": about(); break;
        case "skills": skills(); break;
        case "exp":
        case "experience": exp(); break;
        case "projects":
        case "proj": projects(); break;
        case "edu":
        case "education": edu(); break;
        case "vol":
        case "volunteer": vol(); break;
        case "courses": courses(); break;
        case "links":
        case "social": links(); break;
        case "contact": contact(); break;
        case "clear": clear(); break;
        case "theme": theme(); break;
        case "banner": banner(); break;
        case "status": status(); break;
        case "pwa": pwa(); break;
        case "shortcuts": shortcuts(); break;
        case "open": openTarget(arg); break;
        case "copy": copyTarget(arg); break;
        case "search": searchCmd(arg); break;
        case "whoami": line(PROFILE.handle + " (" + PROFILE.realName + ")"); break;
        case "uname": line("ZeroByte Terminal Portfolio :: GitHub Pages"); break;
        case "echo": line(escapeHTML(arg || "")); break;
        default:
          line(`<span class="muted">Command not found:</span> ${escapeHTML(base)}  — try <span class="cmd">help</span>`);
      }
    }

    function renderChips(){
      chips.innerHTML = "";
      CHIP_CMDS.forEach(c => {
        const el = document.createElement("div");
        el.className = "chip";
        el.textContent = c;
        el.addEventListener("click", () => {
          printCmd(c);
          handle(c);
          input.focus();
        });
        chips.appendChild(el);
      });
    }

    function autocomplete(){
      const v = input.value.trim().toLowerCase();
      if(!v) return;
      const match = COMMANDS.find(c => c.startsWith(v));
      if(match) input.value = match + " ";
    }

    // Buttons
    document.getElementById("btnHelp").addEventListener("click", () => { printCmd("help"); help(); input.focus(); });
    document.getElementById("btnCopyEmail").addEventListener("click", () => { printCmd("copy email"); copyTarget("email"); input.focus(); });
    document.getElementById("btnTheme").addEventListener("click", () => { printCmd("theme"); theme(); input.focus(); });

    // Input handling
    input.addEventListener("keydown", (e) => {
      if(e.key === "Enter"){
        const raw = input.value;
        history.push(raw);
        histIdx = history.length;
        printCmd(raw);
        handle(raw);
        input.value = "";
      } else if(e.key === "ArrowUp"){
        if(histIdx > 0){ histIdx--; input.value = history[histIdx] ?? ""; }
        e.preventDefault();
      } else if(e.key === "ArrowDown"){
        if(histIdx < history.length){ histIdx++; input.value = history[histIdx] ?? ""; }
        e.preventDefault();
      } else if(e.key === "Tab"){
        e.preventDefault();
        autocomplete();
      } else if((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "l"){
        e.preventDefault();
        clear();
      }
    });

    // Boot
    window.addEventListener("click", () => input.focus());
    window.addEventListener("load", () => {
      restoreTheme();
      renderChips();
      banner();
      input.focus();
    });
  </script>
</body>
</html>
"""

def _write(p: Path, content: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def main() -> None:
    root = Path(".").resolve()

    # Replace tokens
    html = INDEX_HTML.replace("{{BUILD_ID}}", BUILD_ID)
    html = html.replace("{{GITHUB}}", LINKS["github"])
    html = html.replace("{{LINKEDIN}}", LINKS["linkedin"])
    html = html.replace("{{YOUTUBE}}", LINKS["YouTube"])
    html = html.replace("{{X}}", LINKS["X"])
    html = html.replace("{{CERTS}}", LINKS["certificates"])

    _write(root / "index.html", html)
    _write(root / "README.md", README)
    _write(root / "manifest.webmanifest", MANIFEST)
    _write(root / "service-worker.js", SERVICE_WORKER)
    _write(root / "robots.txt", ROBOTS)
    _write(root / "sitemap.xml", SITEMAP)
    _write(root / "assets" / "icon.svg", ICON_SVG)

    # Make a zip (optional convenience)
    zip_name = root / "zerobyte_terminal_site.zip"
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in [
            "index.html",
            "README.md",
            "manifest.webmanifest",
            "service-worker.js",
            "robots.txt",
            "sitemap.xml",
            "assets/icon.svg",
        ]:
            z.write(root / rel, arcname=rel)

    print("[+] Built site files in repo root")
    print("[+] ZIP:", zip_name.name)
    print("[+] Build:", BUILD_ID)

if __name__ == "__main__":
    main()
