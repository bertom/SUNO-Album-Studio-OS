/** Studio Browser — frontend SPA */

const state = {
  albums: [],
  album: null,
  track: null,
  trackData: null,
  activeTab: 'brief',
  filter: 'all',
  compareA: null,
  compareB: null,
  activeJob: null,
  selectedTags: new Set(),
};

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

async function api(path, opts = {}) {
  const res = await fetch(`/api${path}`, {
    headers: { 'Content-Type': 'application/json', ...opts.headers },
    ...opts,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail?.message || err.detail || res.statusText);
  }
  return res.json();
}

function toast(msg, ms = 3000) {
  const el = $('#toast');
  el.textContent = msg;
  el.classList.remove('hidden');
  setTimeout(() => el.classList.add('hidden'), ms);
}

function showModal(title, body, onConfirm) {
  $('#modal-title').textContent = title;
  $('#modal-body').innerHTML = body;
  $('#modal').classList.remove('hidden');
  const confirm = $('#modal-confirm');
  const cancel = $('#modal-cancel');
  const handler = () => {
    $('#modal').classList.add('hidden');
    confirm.removeEventListener('click', handler);
    onConfirm();
  };
  confirm.onclick = handler;
  cancel.onclick = () => $('#modal').classList.add('hidden');
}

function navigate(hash) {
  const h = hash.startsWith('/') ? hash.slice(1) : hash;
  if (location.hash.slice(1) !== h) {
    location.hash = h ? `#${h}` : '';
  } else {
    route();
  }
}

function route() {
  const hash = location.hash.slice(1) || '/';
  const parts = hash.split('/').filter(Boolean);

  if (parts.length === 0) {
    showView('home');
    loadAlbums();
    return;
  }

  if (parts[0] === 'album' && parts[1]) {
    showView('album');
    loadAlbum(parts[1], parts[3] || null);
    return;
  }

  showView('home');
  loadAlbums();
}

function showView(name) {
  $('#view-home').classList.toggle('hidden', name !== 'home');
  $('#view-album').classList.toggle('hidden', name !== 'album');
}

async function loadCredits() {
  try {
    const data = await api('/credits');
    $('#credits-badge').textContent = data.credits != null ? `${data.credits} credits` : '—';
  } catch {
    $('#credits-badge').textContent = '—';
  }
}

async function loadAlbums() {
  state.albums = await api('/albums');
  renderAlbums();
  $('#breadcrumb').textContent = '';
}

function renderAlbums() {
  const grid = $('#album-grid');
  let albums = state.albums;

  if (state.filter === 'active') {
    albums = albums.filter((a) => ['draft-ready', 'in_progress', 'drafting'].includes(a.status));
  } else if (state.filter === 'draft-ready') {
    albums = albums.filter((a) => a.status === 'draft-ready');
  }

  grid.innerHTML = albums.map((a) => {
    const p = a.progress;
    const pct = p.total ? Math.round((p.with_audio / p.total) * 100) : 0;
    const coverHtml = a.cover
      ? `<img class="album-cover" src="${esc(a.cover.url)}" alt="${esc(a.title)} cover" loading="lazy" />`
      : `<div class="album-cover album-cover-placeholder" aria-hidden="true"></div>`;
    return `
      <div class="album-card" data-slug="${a.slug}">
        ${coverHtml}
        <div class="album-card-body">
          <h2>${esc(a.title)}</h2>
          <div class="slug">${esc(a.slug)}</div>
          <span class="status-badge ${a.status.replace('_', '-')}">${esc(a.status)}</span>
          <div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>
          <div class="progress-stats">
            <span>${p.with_lyrics}/${p.total} lyrics</span>
            <span>${p.with_prompt}/${p.total} prompts</span>
            <span>${p.with_audio}/${p.total} audio</span>
            <span>${p.final} final</span>
          </div>
        </div>
      </div>`;
  }).join('');

  grid.querySelectorAll('.album-card').forEach((card) => {
    card.onclick = () => navigate(`/album/${card.dataset.slug}`);
  });
}

async function loadAlbum(slug, trackSlug) {
  if (!state.album || state.album.slug !== slug) {
    state.album = await api(`/albums/${slug}`);
    $('#breadcrumb').textContent = state.album.title;
  }
  renderTrackList();

  const target = trackSlug || state.track || findNextReviewTrack()?.slug || state.album.tracks[0]?.slug;
  if (target) await loadTrack(target, { fromRoute: true });
}

async function loadTrack(slug, { fromRoute = false, resetTab = false } = {}) {
  if (fromRoute && state.track === slug && state.trackData?.slug === slug) {
    renderTrackList();
    renderTrackDetail();
    return;
  }

  state.track = slug;
  if (resetTab) {
    state.activeTab = 'brief';
    state.selectedTags.clear();
  }

  if (!fromRoute) {
    const hash = `/album/${state.album.slug}/track/${slug}`;
    if (location.hash.slice(1) !== hash) {
      location.hash = hash;
      return;
    }
  }

  try {
    state.trackData = await api(`/albums/${state.album.slug}/tracks/${slug}`);
  } catch (e) {
    toast(e.message);
    return;
  }

  renderTrackList();
  renderTrackDetail();
}

function findNextReviewTrack() {
  return state.album.tracks.find(
    (t) => ['suno', 'shortlist'].includes(t.status) && !t.has_listening_notes
  );
}

function renderTrackList() {
  const sidebar = $('#track-list');
  const d = state.album.dashboard;
  const coverHtml = state.album.cover
    ? `<div class="album-sidebar-cover"><img src="${esc(state.album.cover.url)}" alt="${esc(state.album.title)} cover" /></div>`
    : '';

  sidebar.innerHTML = `
    ${coverHtml}
    <div class="dashboard">
      <strong>Review dashboard</strong>
      <div class="dashboard-grid">
        <span>Lyrics</span><span>${d.with_lyrics}/${d.total}</span>
        <span>Prompts</span><span>${d.with_prompt}/${d.total}</span>
        <span>Audio</span><span>${d.with_audio}/${d.total}</span>
        <span>Needs review</span><span>${d.needs_review}</span>
        ${d.status_mismatches ? `<span class="mismatch-warn" style="grid-column:1/-1">⚠ ${d.status_mismatches} status mismatch</span>` : ''}
      </div>
    </div>
    ${state.album.tracks.map((t) => `
      <div class="track-item ${state.track === t.slug ? 'active' : ''}" data-slug="${t.slug}">
        <span class="track-num">${t.number}</span>
        <span class="track-title">${esc(t.title)}</span>
        <span class="track-icons">
          <span class="icon-dot ${t.has_lyrics ? 'on' : ''}" title="Lyrics"></span>
          <span class="icon-dot ${t.has_prompt ? 'on' : ''}" title="Prompt"></span>
          <span class="icon-dot audio ${t.has_audio ? 'on' : ''}" title="Audio"></span>
        </span>
        <span class="status-chip ${t.status}">${t.status}</span>
      </div>`).join('')}
  `;

  sidebar.querySelectorAll('.track-item').forEach((item) => {
    item.onclick = () => selectTrack(item.dataset.slug);
  });
}

async function selectTrack(slug) {
  await loadTrack(slug, { resetTab: true });
}

function renderTrackDetail() {
  const d = state.trackData;
  const el = $('#track-detail');

  el.innerHTML = `
    ${d.status_mismatch ? `<div class="mismatch-warn">Status mismatch: track_map says <strong>${d.status}</strong>, track.md says <strong>${d.track_md_status}</strong></div>` : ''}
    <div class="track-header">
      <h2>${esc(d.title)}</h2>
      <div class="track-meta">
        #${d.number} · ${esc(d.album_role)} · ${esc(d.energy)} · <span class="status-chip ${d.status}">${d.status}</span>
      </div>
    </div>
    <div class="tabs">
      ${['brief', 'lyrics', 'style', 'audio', 'notes', 'actions'].map((t) =>
        `<button class="tab ${state.activeTab === t ? 'active' : ''}" data-tab="${t}">${cap(t)}</button>`
      ).join('')}
    </div>
    <div class="tab-content">
      <div class="tab-pane ${state.activeTab !== 'brief' ? 'hidden' : ''}" id="pane-brief">${renderBrief(d)}</div>
      <div class="tab-pane ${state.activeTab !== 'lyrics' ? 'hidden' : ''}" id="pane-lyrics">${renderLyrics(d)}</div>
      <div class="tab-pane ${state.activeTab !== 'style' ? 'hidden' : ''}" id="pane-style">${renderStyle(d)}</div>
      <div class="tab-pane ${state.activeTab !== 'audio' ? 'hidden' : ''}" id="pane-audio">${renderAudio(d)}</div>
      <div class="tab-pane ${state.activeTab !== 'notes' ? 'hidden' : ''}" id="pane-notes">${renderNotes(d)}</div>
      <div class="tab-pane ${state.activeTab !== 'actions' ? 'hidden' : ''}" id="pane-actions">${renderActions(d)}</div>
    </div>
  `;

  el.querySelectorAll('.tab').forEach((tab) => {
    tab.onclick = () => {
      state.activeTab = tab.dataset.tab;
      renderTrackDetail();
    };
  });

  bindTabEvents(d);
}

function renderBrief(d) {
  if (!d.song_brief_html) return '<p class="placeholder">No song brief yet.</p>';
  return `<div class="markdown-body">${d.song_brief_html}</div>`;
}

function renderLyrics(d) {
  if (!d.lyrics_files?.length) return '<p class="placeholder">No lyrics yet.</p>';
  return d.lyrics_files.map((lf, i) => `
    <details ${i === 0 ? 'open' : ''}>
      <summary>${esc(lf.name)}</summary>
      <div class="markdown-body">${lf.html || esc(lf.content)}</div>
    </details>
  `).join('');
}

function renderStyle(d) {
  let html = '';

  if (d.validation) {
    const v = d.validation;
    html += `<div class="validation ${v.ok ? 'ok' : 'fail'}">
      ${v.ok ? '✓ Prompt validates OK' : '✗ Validation errors'}
      ${v.errors?.length ? `<ul>${v.errors.map((e) => `<li>${esc(e)}</li>`).join('')}</ul>` : ''}
      ${v.warnings?.length ? `<p>Warnings:</p><ul>${v.warnings.map((w) => `<li>${esc(w)}</li>`).join('')}</ul>` : ''}
    </div>`;
  }

  if (d.style_directions_html) {
    html += `<h3>Style directions</h3><div class="markdown-body">${d.style_directions_html}</div><hr style="margin:1rem 0;border-color:var(--border)">`;
  }

  if (d.prompt?.fields) {
    const fields = [
      ['Lyrics', d.prompt.fields.lyrics],
      ['Styles', d.prompt.fields.styles],
      ['Exclude styles', d.prompt.fields.exclude_styles],
      ['Vocal Gender', d.prompt.fields.vocal_gender],
      ['Weirdness %', d.prompt.fields.weirdness_pct + '%'],
      ['Style influence %', d.prompt.fields.style_influence_pct + '%'],
      ['Song Title', d.prompt.fields.title],
    ];
    html += `<p style="font-size:0.85rem;color:var(--text-muted);margin-bottom:0.75rem">From ${esc(d.prompt.file)}</p>
      <div class="field-grid">${fields.map(([label, val]) => `
        <div class="field-block">
          <header><h4>${label}</h4><button class="btn small copy-btn" data-copy="${escAttr(String(val))}">Copy</button></header>
          <pre>${esc(String(val))}</pre>
        </div>`).join('')}
      </div>`;
  } else {
    html += '<p class="placeholder">No SUNO prompt yet.</p>';
  }

  return html;
}

function renderAudio(d) {
  const fav = d.review_state?.favorite_take;
  const runs = d.runs || [];
  const allAudio = d.audio_files || [];

  if (!runs.length && !allAudio.length) {
    const msg = d.read_only
      ? 'No master WAV in repo — see track_map for expected filename in masters/.'
      : 'No audio yet — generate from Actions tab.';
    return `<p class="placeholder">${msg}</p>`;
  }

  let html = '';
  if (allAudio.length >= 2) {
    html += `
      <div class="compare-bar">
        <label>A/B compare:</label>
        <select id="compare-a">${audioOptions(allAudio)}</select>
        <span>vs</span>
        <select id="compare-b">${audioOptions(allAudio, 1)}</select>
        <button class="btn small" id="btn-compare-play">Play A → B</button>
      </div>
    `;
  }

  // Released albums — master WAV only
  if (d.read_only && allAudio.length) {
    for (const f of allAudio) {
      const url = mediaUrl(d.album, d.slug, f.name, f.path);
      html += `<div class="run-group">
        <div class="run-header"><span>Master</span><span>${esc(f.name)}</span></div>
        <div class="take-row">
          <audio controls src="${url}"></audio>
        </div>
      </div>`;
    }
    return html;
  }

  for (const run of runs) {
    const runNum = run.run;
    html += `<div class="run-group">
      <div class="run-header">
        <span>Run ${runNum} · ${run.date || ''} · ${run.status || ''}</span>
        <span>${run.prompt_version || ''}</span>
      </div>`;

    for (const take of run.takes || []) {
      const filename = take.mp3 || take.wav || `run${runNum}_take_${take.take}.mp3`;
      const isFav = fav && fav.run === runNum && fav.take === take.take;
      const url = mediaUrl(d.album, d.slug, filename.split('/').pop(), filename);

      html += `<div class="take-row ${isFav ? 'favorite' : ''}">
        <strong>Take ${take.take.toUpperCase()}</strong>
        ${take.duration ? `<span style="color:var(--text-muted);font-size:0.8rem"> · ${Math.round(take.duration)}s</span>` : ''}
        <audio controls src="${url}" data-take="${take.take}" data-run="${runNum}" data-file="${escAttr(filename)}"></audio>
        <div class="take-actions">
          <button class="btn small verdict-btn" data-verdict="favorite" data-run="${runNum}" data-take="${take.take}">★ Favorite</button>
          <button class="btn small verdict-btn" data-verdict="shortlist" data-run="${runNum}" data-take="${take.take}">♥ Shortlist</button>
          <button class="btn small verdict-btn" data-verdict="pass" data-run="${runNum}" data-take="${take.take}">✗ Pass</button>
          <button class="btn small secondary wav-btn" data-run="${runNum}" data-take="${take.take}">WAV</button>
        </div>
      </div>`;
    }
    html += '</div>';
  }

  return html;
}

function audioOptions(files, defaultIdx = 0) {
  return files.map((f, i) =>
    `<option value="${escAttr(f.name)}" ${i === defaultIdx ? 'selected' : ''}>${esc(f.name)}</option>`
  ).join('');
}

function renderNotes(d) {
  if (d.read_only) {
    return '<p class="placeholder">Listening notes not used for released archive albums.</p>';
  }
  const run = d.runs?.[0];
  const runNum = run?.run || '001';
  const tags = ['body yes', 'vocal warm', 'too sleepy', 'groove alive', 'retry', 'shortlist'];

  return `
    ${d.listening_notes_html ? `<div class="markdown-body" style="margin-bottom:1rem;max-height:200px;overflow-y:auto">${d.listening_notes_html}</div><hr style="margin:1rem 0;border-color:var(--border)">` : ''}
    <h3>Add listening notes — Run ${runNum}</h3>
    <div class="tag-chips">${tags.map((t) =>
      `<button class="tag-chip" data-tag="${escAttr(t)}">${esc(t)}</button>`
    ).join('')}</div>
    <div class="form-group"><label>First feeling</label><textarea id="note-feeling"></textarea></div>
    <div class="form-group"><label>What worked</label><textarea id="note-worked"></textarea></div>
    <div class="form-group"><label>What failed</label><textarea id="note-failed"></textarea></div>
    <div class="form-group"><label>Decision</label>
      <select id="note-decision">
        <option>keep exploring</option>
        <option>shortlist</option>
        <option>retry</option>
        <option>select final</option>
      </select>
    </div>
    <div class="form-group"><label>Next prompt move</label><textarea id="note-next"></textarea></div>
    <button class="btn" id="btn-save-notes">Save notes</button>
  `;
}

function renderActions(d) {
  if (d.read_only) {
    return `
      <h3>Released archive</h3>
      <p style="font-size:0.85rem;color:var(--text-muted)">
        Read-only browse for released albums. Lyrics and style archives are in the tabs above.
        SUNO generate and final selection apply to active track workspaces only.
      </p>
    `;
  }
  const run = d.runs?.[0];
  return `
    <h3>SUNO workflow</h3>
    <p style="font-size:0.85rem;color:var(--text-muted);margin-bottom:1rem">
      One song at a time. Files on sunoapi.org expire after 15 days — download promptly.
    </p>
    <div class="actions-row">
      <button class="btn" id="btn-validate">Validate prompt</button>
      <button class="btn primary" id="btn-generate">Generate (2 takes)</button>
    </div>
    <div id="job-log" class="job-log hidden"></div>

    <h3 style="margin-top:1.5rem">Final selection</h3>
    <div class="form-group"><label>Reason it won</label><textarea id="final-reason"></textarea></div>
    <div class="form-group"><label>Run</label><input id="final-run" value="${run?.run || ''}" /></div>
    <div class="form-group"><label>Take</label>
      <select id="final-take"><option value="a">a</option><option value="b">b</option></select>
    </div>
    <div class="actions-row">
      <button class="btn" id="btn-select-final">Select final</button>
      <button class="btn secondary" id="btn-archive">Archive track</button>
    </div>
  `;
}

function bindTabEvents(d) {
  document.querySelectorAll('.copy-btn').forEach((btn) => {
    btn.onclick = () => {
      navigator.clipboard.writeText(btn.dataset.copy);
      toast('Copied to clipboard');
    };
  });

  document.querySelectorAll('.verdict-btn').forEach((btn) => {
    btn.onclick = async () => {
      try {
        await api(`/albums/${d.album}/tracks/${d.slug}/verdict`, {
          method: 'POST',
          body: JSON.stringify({
            verdict_type: btn.dataset.verdict,
            run_number: btn.dataset.run,
            take: btn.dataset.take,
          }),
        });
        toast(`Marked: ${btn.dataset.verdict}`);
        loadTrack(d.slug, { fromRoute: true });
      } catch (e) { toast(e.message); }
    };
  });

  document.querySelectorAll('.wav-btn').forEach((btn) => {
    btn.onclick = () => {
      showModal(
        'Request WAV',
        `<p>Convert run ${btn.dataset.run} take ${btn.dataset.take} to WAV? Uses API credits.</p>`,
        async () => {
          try {
            const res = await api(`/albums/${d.album}/tracks/${d.slug}/wav`, {
              method: 'POST',
              body: JSON.stringify({ run_number: btn.dataset.run, take: btn.dataset.take }),
            });
            toast(res.ok ? 'WAV downloaded' : 'WAV request failed');
            if (res.ok) loadTrack(d.slug, { fromRoute: true });
          } catch (e) { toast(e.message); }
        }
      );
    };
  });

  $('#btn-save-notes')?.addEventListener('click', async () => {
    const run = d.runs?.[0];
    try {
      await api(`/albums/${d.album}/tracks/${d.slug}/notes`, {
        method: 'POST',
        body: JSON.stringify({
          run_number: run?.run || '001',
          take: 'a',
          prompt_version: d.prompt?.file || '',
          audio_file: d.audio_files?.[0]?.path || '',
          first_feeling: $('#note-feeling')?.value,
          what_worked: $('#note-worked')?.value,
          what_failed: $('#note-failed')?.value,
          decision: $('#note-decision')?.value,
          next_move: $('#note-next')?.value,
          quick_tags: [...state.selectedTags],
        }),
      });
      toast('Notes saved');
      loadTrack(d.slug, { fromRoute: true });
    } catch (e) { toast(e.message); }
  });

  document.querySelectorAll('.tag-chip').forEach((chip) => {
    chip.onclick = () => {
      const tag = chip.dataset.tag;
      if (state.selectedTags.has(tag)) {
        state.selectedTags.delete(tag);
        chip.classList.remove('selected');
      } else {
        state.selectedTags.add(tag);
        chip.classList.add('selected');
      }
    };
  });

  $('#btn-validate')?.addEventListener('click', async () => {
    try {
      const res = await api(`/albums/${d.album}/tracks/${d.slug}/validate`, { method: 'POST', body: '{}' });
      toast(res.ok ? 'Validation OK' : `Errors: ${res.errors?.join(', ')}`);
      loadTrack(d.slug, { fromRoute: true });
    } catch (e) { toast(e.message); }
  });

  $('#btn-generate')?.addEventListener('click', () => {
    showModal(
      'Generate SUNO run',
      '<p>Submit prompt and wait for 2 MP3 takes? Uses API credits. Only one job at a time.</p>',
      () => startGenerate(d)
    );
  });

  $('#btn-select-final')?.addEventListener('click', async () => {
    const reason = $('#final-reason')?.value;
    if (!reason) { toast('Add a reason'); return; }
    try {
      const res = await api(`/albums/${d.album}/tracks/${d.slug}/select-final`, {
        method: 'POST',
        body: JSON.stringify({
          run_number: $('#final-run')?.value,
          take: $('#final-take')?.value,
          reason,
        }),
      });
      toast(`Final selected — ${res.changed_files?.length} files updated`);
      loadAlbum(d.album, d.slug);
    } catch (e) { toast(e.message); }
  });

  $('#btn-archive')?.addEventListener('click', async () => {
    const audio = d.review_state?.favorite_take
      ? `run${d.review_state.favorite_take.run}_take_${d.review_state.favorite_take.take}.mp3`
      : d.audio_files?.[0]?.name;
    if (!audio) { toast('No audio to archive'); return; }
    try {
      await api(`/albums/${d.album}/tracks/${d.slug}/archive`, {
        method: 'POST',
        body: JSON.stringify({ final_audio: audio, track_number: d.number }),
      });
      toast('Track archived');
    } catch (e) { toast(e.message); }
  });

  $('#btn-compare-play')?.addEventListener('click', () => {
    const a = $('#compare-a')?.value;
    const b = $('#compare-b')?.value;
    if (!a || !b) return;
    const pathA = d.audio_files?.find((f) => f.name === a)?.path;
    const pathB = d.audio_files?.find((f) => f.name === b)?.path;
    playCompare(d.album, d.slug, a, b, pathA, pathB);
  });
}

async function startGenerate(d) {
  const logEl = $('#job-log');
  logEl?.classList.remove('hidden');
  logEl.textContent = 'Starting…';

  try {
    const { job_id } = await api(`/albums/${d.album}/tracks/${d.slug}/generate`, {
      method: 'POST',
      body: '{}',
    });
    state.activeJob = job_id;
    pollJob(job_id, d);
  } catch (e) {
    logEl.textContent = e.message;
    toast(e.message);
  }
}

async function pollJob(jobId, d) {
  const logEl = $('#job-log');
  const poll = async () => {
    const job = await api(`/jobs/${jobId}`);
    logEl.textContent = job.logs.join('\n') || job.status;
    if (job.status === 'running' || job.status === 'pending') {
      setTimeout(poll, 2000);
    } else {
      toast(job.status === 'complete' ? 'Generation complete' : 'Generation failed');
      loadTrack(d.slug, { fromRoute: true });
    }
  };
  poll();
}

function playCompare(album, track, fileA, fileB, pathA, pathB) {
  const a = new Audio(mediaUrl(album, track, fileA, pathA));
  a.play();
  a.onended = () => new Audio(mediaUrl(album, track, fileB, pathB)).play();
}

function mediaUrl(album, track, filename, filePath) {
  if (filePath && String(filePath).startsWith('masters/')) {
    return `/api/media/${album}/masters/${encodeURIComponent(filename)}`;
  }
  return `/api/media/${album}/${track}/${encodeURIComponent(filename)}`;
}

function esc(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

function escAttr(s) {
  return s.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function cap(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
  if (e.target.matches('input, textarea, select')) return;
  if (!state.album) return;

  const tracks = state.album.tracks;
  const idx = tracks.findIndex((t) => t.slug === state.track);

  if (e.key === 'j' && idx < tracks.length - 1) {
    selectTrack(tracks[idx + 1].slug);
  } else if (e.key === 'k' && idx > 0) {
    selectTrack(tracks[idx - 1].slug);
  } else if (e.key >= '1' && e.key <= '6') {
    const tabs = ['brief', 'lyrics', 'style', 'audio', 'notes', 'actions'];
    state.activeTab = tabs[parseInt(e.key) - 1];
    renderTrackDetail();
  }
});

// Search
let searchTimeout;
$('#search-input')?.addEventListener('input', (e) => {
  clearTimeout(searchTimeout);
  const q = e.target.value.trim();
  if (q.length < 2) return;
  searchTimeout = setTimeout(async () => {
    const { results } = await api(`/search?q=${encodeURIComponent(q)}`);
    if (results.length && state.album) {
      const r = results[0];
      navigate(`/album/${r.album}/track/${r.track}`);
    }
  }, 400);
});

$$('.filter').forEach((btn) => {
  btn.onclick = () => {
    $$('.filter').forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    state.filter = btn.dataset.filter;
    renderAlbums();
  };
});

$('#btn-home').onclick = () => navigate('/');
window.addEventListener('hashchange', route);

loadCredits();
route();
