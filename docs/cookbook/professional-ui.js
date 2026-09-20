/* SavorShelf 0.6: a single presentation layer over the existing recipe engine.
 * No migration, provider calls, or recipe mutations occur when a screen is drawn.
 * The original actions, import validation, formula resolution and storage stay intact.
 */
(function () {
  'use strict';
  const categories = ['All', 'Dinner', 'Breakfast', 'Desserts', 'Sides', 'Sauces', 'Other'];
  const sortOptions = [['rank', 'Your order'], ['rating', 'Highest rated'], ['cooked', 'Most cooked'], ['newest', 'Recently saved'], ['az', 'A–Z']];
  const themeQuery = window.matchMedia('(prefers-color-scheme: dark)');
  let compactFiltersOpen = false;
  let settingsOpen = new Set();
  const recipeSectionsOpen = new Map();
  const oldRender = render;
  const oldCreator = creator;
  const oldCook = cook;
  const oldShopping = shopping;
  const oldModal = modal;
  const originalCards = renderCards;
  let nativeAppearance = '';
  const nav = [['recipes', 'book', 'Recipes'], ['favorites', 'heart', 'Favorites'], ['create', 'plus', 'Create'], ['shopping', 'bag', 'Shopping'], ['settings', 'settings', 'Settings']];

  function applyAppearance() {
    const mode = ['light', 'dark', 'system'].includes(state.uiPreferences?.theme) ? state.uiPreferences.theme : 'system';
    let systemDark = themeQuery.matches;
    try { if (window.AndroidBridge?.isSystemDark) systemDark = AndroidBridge.isSystemDark(); } catch (_) {}
    const resolved = mode === 'system' ? (systemDark ? 'dark' : 'light') : mode;
    document.documentElement.dataset.theme = resolved;
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', resolved === 'dark' ? '#172330' : '#f7f1e8');
    if (nativeAppearance !== resolved) {
      try { window.AndroidBridge?.setAppearance?.(resolved); nativeAppearance = resolved; } catch (_) {}
    }
    document.documentElement.dataset.cookingText = state.uiPreferences?.cookingText === 'large' ? 'large' : 'standard';
  }
  themeQuery.addEventListener('change', applyAppearance);
  window.addEventListener('savorshelf-system-theme', applyAppearance);

  function section(id, title, description, content, opened = false) {
    return `<details class="panel settings-section" data-settings-section="${id}" ${opened || settingsOpen.has(id) ? 'open' : ''}><summary><span><strong>${title}</strong><span class="small">${description}</span></span>${icon('next')}</summary><div class="section-content">${content}</div></details>`;
  }

  shell = function (content) {
    const focus = view.type === 'cook' || view.type === 'edit';
    const screen = view.type === 'home' ? tab : view.type;
    return `<div class="shell ${focus ? 'focus-shell' : ''}" data-screen="${esc(screen)}"><header class="header"><a class="brand" href="#" data-action="home" aria-label="SavorShelf, my recipes"><span class="brand-mark"><img class="brand-logo" src="icon.svg" alt="" width="40" height="40"></span><span class="brand-word">SavorShelf</span></a><span class="header-status">${icon(focus ? 'chef' : 'shield')}<span>${focus ? (view.type === 'cook' ? 'Cooking mode' : 'Recipe editor') : 'Saved on device'}</span></span></header>${storageProblem ? `<div class="error" role="alert">${esc(storageProblem)}</div>` : ''}<main id="main-content" tabindex="-1">${content}</main></div>${focus ? '' : `<nav class="bottom-nav five-tabs" aria-label="Main navigation">${nav.map(([key, glyph, label]) => `<button type="button" class="nav-item ${tab === key ? 'active' : ''}" data-action="tab" data-tab="${key}" ${tab === key ? 'aria-current="page"' : ''}><span class="nav-symbol">${icon(glyph)}</span><span>${label}</span></button>`).join('')}</nav>`}`;
  };

  home = function () {
    const favorites = tab === 'favorites';
    const total = favorites ? state.recipes.filter(r => r.favorite).length : state.recipes.length;
    return `<section class="library-heading"><div><p class="eyebrow">${favorites ? 'YOUR GO-TO COLLECTION' : 'YOUR EVERYDAY COOKBOOK'}</p><h1>${favorites ? 'Worth making again.' : 'Your recipe shelf.'}</h1><p class="small">${total} saved ${total === 1 ? 'recipe' : 'recipes'} · ${favorites ? 'The ones you love, all together.' : 'Good food, made your way.'}</p></div></section>
    <section class="shelf-start" aria-label="Find or add a recipe"><div class="row search-row"><label class="search">${icon('search')}<input id="search" type="search" placeholder="Search recipes or ingredients" aria-label="Search recipes and ingredients" value="${esc(query)}" autocomplete="off"></label>${button(icon('plus'), 'new', 'primary add-recipe-button', 'aria-label="Add recipe" title="Add recipe"')}</div><div class="quick-paths">${button(icon('bag') + 'Use my ingredients', 'pantry-find')}${button(icon('chef') + 'Dinner ideas', 'tonight-pick')}</div></section>
    <div class="library-toolbar"><details class="library-filters" ${compactFiltersOpen ? 'open' : ''}><summary>${icon('settings')}<span>${filter === 'All' ? 'Filter recipes' : esc(filter)}</span><span class="filter-caret" aria-hidden="true">⌄</span></summary><div class="filter-row" aria-label="Recipe categories">${categories.map(c => `<button type="button" class="chip ${filter === c ? 'active' : ''}" data-action="filter" data-value="${c}" aria-pressed="${filter === c}">${c}</button>`).join('')}</div></details><div class="shelf-controls"><label class="sr-only" for="sort-recipes">Sort recipes</label><select id="sort-recipes">${sortOptions.map(([v, label]) => `<option value="${v}" ${state.sort === v ? 'selected' : ''}>${label}</option>`).join('')}</select></div></div>
    <div class="section-label library-results"><h2>${query ? 'Search results' : filter === 'All' ? (favorites ? 'Your favorites' : 'All recipes') : esc(filter)}</h2><span id="recipe-count" class="small" role="status" aria-live="polite"></span></div><div id="recipe-grid" class="grid library-grid"></div>
    <section class="inspiration-footer" aria-label="More recipe ideas"><span class="inspiration-mark">${icon('leaf')}</span><div><h2>A little inspiration.</h2><p class="small">Explore suggested recipes before adding them to your shelf.</p><div class="row wrap">${button('Browse 10 recipe ideas', 'tailored-browse')}${button('Explore similar recipes', 'discovery-ideas')}</div></div></section><p class="footer-note">Recipes worth making again.</p>`;
  };

  renderCards = function () {
    // Keep the existing search, ranking and deduplication behavior as the source of truth.
    originalCards();
    const grid = $('#recipe-grid');
    if (!grid) return;
    grid.querySelector('.add-card')?.remove();
    for (const card of grid.querySelectorAll('.card')) {
      const copy = card.querySelector('.card-copy');
      const description = copy?.querySelector('p.small');
      if (description) description.classList.add('recipe-description');
      const row = copy?.querySelector('.row');
      if (row) row.classList.add('card-eyebrow');
      const rating = copy?.querySelector('.rating-small');
      if (rating?.textContent === 'Not rated') rating.textContent = '';
      const art = card.querySelector('.recipe-jacket');
      if (art) {
        art.querySelector('.cover-label')?.remove();
        art.querySelector('.jacket-rule')?.remove();
        art.querySelector('.jacket-initial')?.remove();
      }
    }
    const empty = grid.querySelector('.empty');
    if (empty) {
      const filtered = query.trim() || filter !== 'All';
      empty.innerHTML = `${icon(tab === 'favorites' ? 'heart' : 'book')}<h2>${filtered ? 'No matches this time.' : tab === 'favorites' ? 'Keep your favorites here.' : 'Start with something you love.'}</h2><p>${filtered ? 'Try a broader search or clear your filters.' : tab === 'favorites' ? 'Tap the heart on a recipe to add it to this collection.' : 'Write a recipe or bring one in from your notes.'}</p>${filtered ? button('Clear search & filters', 'clear-recipe-search', 'primary') : button(tab === 'favorites' ? 'Browse recipes' : 'Add a recipe', tab === 'favorites' ? 'home' : 'new', 'primary')}`;
    }
  };

  detail = function () {
    const base = current(), r = activeRecipe();
    if (!base || !r) { view = {type: 'home'}; return home(); }
    const ingredients = C.scaled(r, detailYield).filter(i => !(i.amount === 0 && i.name === 'Omitted'));
    const done = [...checkedIngredients].filter(n => n < ingredients.length).length;
    const notes = esc(r.notes || 'No notes yet. Use Edit recipe to record what you would change next time.');
    const version = V.name(base, choice(base).variant && choice(base).variant !== 'original' ? 'variant:' + choice(base).variant : 'original');
    const selected = choice(base);
    const actualDairy = {regular:'Regular dairy option',regularDairy:'Regular dairy option',lactoseFree:'Lactose-free',dairyFree:'Dairy-free'}[selected.dairy];
    const actualSugar = {noAddedSugar:'No added sugar',sugarFree:'Plain unsweetened ingredient version'}[selected.sugar];
    const actualModes = [actualDairy, actualSugar].filter(Boolean).join(' · ');
    const summary = r.activeNotes?.length ? r.activeNotes.join(' ') : 'Named versions and available dietary adaptations';
    const extra = recipeSectionsOpen.get(base.id) || new Set();
    return `<div class="recipe-topbar">${button(icon('arrow') + 'My recipes', 'home', 'quiet')}${button('Recipe tools ' + icon('settings'), 'recipe-tools', 'quiet')}</div>
    ${RecipePresentation.header(r,{category:(r.category||'Other')+(base.sourceStatus==='rebuilt'?' · REBUILT RECIPE':''),facts:`<span>${icon('clock')}${r.minutes ? 'About ' + C.fmt(r.minutes) + ' min' : 'Time not set'}</span><span>${icon('people')}${C.fmt(detailYield)} ${esc(r.yieldUnit || 'servings')}</span>${base.rating ? `<span aria-label="Your rating: ${base.rating} out of 5">★ ${base.rating}/5</span>` : ''}`,extra:`<p class="selected-version"><span class="small">Selected version</span><strong>${esc(version)}</strong>${actualModes ? `<span class="small dietary-meaning">${esc(actualModes)}</span>` : ''}${r.activeNotes?.length ? `<span class="small">${esc(summary)}</span>` : ''}</p>`})}
    <div class="detail-actions" aria-label="Cook or plan this recipe">${button(icon('chef') + 'Start cooking', 'cook', 'primary')}${button(icon('bag') + 'Add to list', 'add-batch')}</div>
    <details class="recipe-versions" data-recipe-section="versions" data-recipe-owner="${esc(base.id)}" ${extra.has('versions') ? 'open' : ''}><summary><span>${icon('leaf')}<strong>Versions & dietary options</strong></span><span aria-hidden="true">⌄</span></summary>${optionsPanel(r, base)}</details>
    <div class="recipe-content-grid">${RecipePresentation.ingredients({progress:`<span id="ingredient-progress" class="small" role="status" aria-live="polite">${done} of ${ingredients.length} ready</span>`,control:`<div class="yield-control"><label for="yield"><strong>Make it for</strong><span class="small yield-unit">${esc(r.yieldUnit || 'servings')}</span></label><div class="gap"><button type="button" class="icon-btn" data-action="yield-down" aria-label="Decrease yield">−</button><input id="yield" type="number" min="1" max="1000" value="${detailYield}" aria-label="Recipe yield"><button type="button" class="icon-btn" data-action="yield-up" aria-label="Increase yield">+</button></div></div>`,rows:`${ingredients.map((i, n) => `<label class="ingredient"><input type="checkbox" data-ingredient="${n}" ${checkedIngredients.has(n) ? 'checked' : ''}><span class="ingredient-text"><span class="amount">${esc(K.ingredientText(i))}</span>${i.substitution ? `<span class="substitution">(${esc(noteText(i.substitution, r, detailYield))})</span>` : ''}</span></label>`).join('')}`,footer:`<details class="scaling-note"><summary>How serving adjustments work</summary><p class="small">Linked amounts in the steps follow your serving size. Times, temperatures and pan sizes do not multiply. Plain-text amounts in older recipes need linking in the editor. For part of an egg, beat it and measure the required fraction.</p></details>`})}
    ${RecipePresentation.method(r,detailYield)}</div>
    <section class="panel recipe-notes"><h2>Your kitchen notes</h2><p class="notes">${notes}</p><div class="row wrap"><span class="small">Updated ${date(r.updatedAt)}</span>${button(icon('edit') + 'Edit recipe', 'edit', 'quiet')}</div></section>
    <section class="panel rating-panel"><h2>Make it a keeper.</h2><p class="small">Your ratings help your best recipes rise to the top.</p>${ratingStars(base)}<div class="row wrap">${button(base.pinned ? 'Unpin from the top' : 'Pin to the top', 'pin', 'soft')}<span class="small">${base.cookCount ? base.cookCount + ' times cooked' : 'Not marked cooked yet'}</span></div></section>
    ${r.source ? `<details class="source-details"><summary>Recipe source & status</summary><p class="small source-note">${esc(r.source)}</p><p class="small">Adaptations and rebuilt recipes are not kitchen-tested or certified dietary advice.</p></details>` : ''}`;
  };

  creator = function () {
    // Reorganize existing controls rather than duplicate provider or import logic.
    const template = document.createElement('template');
    template.innerHTML = oldCreator();
    const root = template.content;
    root.querySelector('.creation-route')?.remove();
    const title = root.querySelector('.page-title');
    if (title) title.innerHTML = '<p class="eyebrow">FROM AN IDEA TO A KEEPER</p><h1>Create a recipe.</h1><p class="small">Describe it, refine it, then save the version you love.</p>';
    const prompt = root.querySelector('#maker-prompt');
    if (prompt) { prompt.rows = 3; prompt.placeholder = 'Chicken thighs for 8, with a creamy lactose-free sauce…'; }
    const actions = root.querySelector('.maker-actions');
    if (actions) {
      const primary = actions.querySelector('[data-action="puter-create"]');
      const secondary = [...actions.children].filter(el => el !== primary);
      actions.replaceChildren();
      if (primary) { primary.innerHTML = icon('chef') + 'Create with Puter'; actions.append(primary); }
      const info = document.createElement('p'); info.className = 'creator-connection-note small';
      info.textContent = state.creatorPageUrl ? 'Opens your saved creator page in the browser. Puter sign-in and its usage limits apply.' : 'Set up a creator page first. Local recipes do not require an account.';
      actions.after(info);
      const alternatives = document.createElement('details'); alternatives.className = 'alternative-creators';
      alternatives.innerHTML = '<summary>Other ways to create or import</summary><div class="alternative-actions"></div>';
      const container = alternatives.querySelector('.alternative-actions');
      for (const btn of secondary) { btn.classList.remove('primary'); container.append(btn); }
      const originalInfo = info.nextElementSibling;
      if (originalInfo?.matches('p.small')) { originalInfo.classList.add('creator-explainer'); alternatives.append(originalInfo); }
      info.after(alternatives);
    }
    const manual = document.createElement('section'); manual.className = 'panel manual-create';
    manual.innerHTML = `<div>${icon('book')}<h2>Already have a recipe?</h2><p class="small">Keep a family favorite or bring in a recipe you already use.</p></div><div class="row wrap">${button('Write a recipe', 'new')}${button('Paste or import', 'chatgpt-import')}</div>`;
    const panel = root.querySelector('.maker-panel'); if (panel) panel.after(manual);
    return template.innerHTML;
  };

  cook = function () {
    const template = document.createElement('template'); template.innerHTML = oldCook();
    const root = template.content, r = cooking?.recipe || activeRecipe();
    const h1 = root.querySelector('h1');
    if (h1 && cooking && r) { h1.textContent = 'Step ' + (cooking.step + 1); h1.removeAttribute('style'); }
    const progress = root.querySelector('.progress');
    if (progress && cooking && r) {
      progress.setAttribute('role', 'progressbar'); progress.setAttribute('aria-label', 'Recipe progress');
      progress.setAttribute('aria-valuemin', '0'); progress.setAttribute('aria-valuemax', String(r.steps.length)); progress.setAttribute('aria-valuenow', String(cooking.step + 1));
    }
    const step = root.querySelector('.cook-step'); if (step) { step.setAttribute('aria-live', 'polite'); step.setAttribute('aria-atomic', 'true'); }
    const next = root.querySelector('[data-action="next-step"]'); next?.parentElement.classList.add('cook-navigation');
    return template.innerHTML;
  };

  shopping = function () {
    const template = document.createElement('template'); template.innerHTML = oldShopping();
    const title = template.content.querySelector('.page-title');
    if (title) { title.querySelector('h1').textContent = 'Shopping list.'; title.querySelector('.eyebrow').textContent = 'READY FOR YOUR NEXT SHOP'; }
    const items = C.shopping(state.recipes, state.batches, state.extras);
    const done = items.filter(i => state.checked.includes(i.key)).length;
    if (items.length) {
      const meter = document.createElement('div'); meter.className = 'shopping-progress';
      meter.innerHTML = `<progress max="${items.length}" value="${done}" aria-label="Shopping items collected">${done} of ${items.length}</progress><span class="small">${done} of ${items.length} collected</span>`;
      title?.after(meter);
    }
    return template.innerHTML;
  };

  settings = function () {
    const theme = state.uiPreferences?.theme || 'system';
    const text = state.uiPreferences?.cookingText || 'standard';
    return `<section class="page-title"><p class="eyebrow">MAKE YOURSELF AT HOME</p><h1>Settings.</h1><p class="small">Your recipes, preferences and connections.</p></section><div class="settings-grid professional-settings">
    <section class="panel backup-priority"><span class="backup-symbol">${icon('shield')}</span><div><h2>Keep your recipes safe.</h2><p class="small">Your collection is stored on this device, not automatically in the cloud. Export a backup before uninstalling, clearing storage or testing an update.</p><div class="row wrap">${button(icon('download') + 'Export recipe backup', 'export', 'primary')}${button(icon('upload') + 'Import a backup', 'import')}</div><p class="small backup-footnote">Recipe backups include saved recipes, photos and versions. They are not a complete phone backup; shopping lists and app preferences do not transfer.</p></div></section>
    <section class="panel appearance-panel"><h2>Appearance & cooking</h2><div class="form-grid"><label class="field">Theme<select id="appearance-theme">${[['system', 'Follow phone setting'], ['light', 'Light'], ['dark', 'Dark']].map(([key, label]) => `<option value="${key}" ${theme === key ? 'selected' : ''}>${label}</option>`).join('')}</select></label><label class="field">Cooking instructions<select id="cooking-text-size">${[['standard', 'Standard text'], ['large', 'Extra-large text']].map(([key, label]) => `<option value="${key}" ${text === key ? 'selected' : ''}>${label}</option>`).join('')}</select></label></div><p class="small">Extra-large text applies to step-by-step cooking. Your phone’s own text-size setting remains available.</p></section>
    ${section('recipes', 'Recipe tools', 'Import, organize and revisit your cooking history', `<div class="settings-actions">${button('Paste or import a recipe', 'chatgpt-import')}${button('Arrange recipes', 'rank-recipes')}${button('Browse cooking history', 'browse-originals')}${button('Review incomplete recipes', 'recovery-list')}</div><p class="small">Your bundled collection includes recovered and rebuilt recipes. The history archive contains notes and partial requests, not a verified complete set of original recipes.</p>`)}
    ${section('creator', 'Recipe creator', 'Puter and optional connections', `<p class="small">${state.creatorPageUrl ? 'A creator address is saved. This does not mean sign-in or generation has been tested with your account.' : 'No creator page address is saved.'}</p><div class="settings-actions">${button('Creator page settings', 'creator-page-settings')}${button('Optional private AI server', 'ai-settings')}</div><p class="small">Puter opens in the external browser. It uses your Puter account and allowance. The private-server option is separate. No provider key belongs in this app.</p>`)}
    ${section('privacy', 'Privacy & storage', 'What stays here and what you choose to share', `<p class="small">Recipes and photos are stored locally. There are no ads or analytics in this build. Only an explicitly submitted request or selected recipe is handed to an external creator. Exporting or sharing a backup shares the recipes inside it.</p><p class="small">There is no automatic syncing between devices. Timers alert while the app is open; use the phone’s Clock app for reliable background alarms.</p>`)}
    ${section('about', 'About SavorShelf', 'Version 0.16.0 · Personal preview', `<p class="small">Recipes worth making again. This is an update to your existing SavorShelf app, not a separate paid or “Pro” app. It is not a Google Play release.</p><div class="settings-actions">${button('How app updates work', 'update-help')}${button('Copy next-update brief', 'update-brief')}${button('Recipe & dietary references', 'sources')}</div><p class="small">Lactose-free is not dairy-free. No added sugar does not mean sugar-free. Suggested variations are not kitchen-tested or certified dietary advice.</p>`)}
    ${storageProblem ? `<section class="panel"><h2>Storage recovery</h2><p class="small">Save the unreadable original file before any reset.</p>${button('Export raw recovery file', 'recovery')}${button('Reset after backup', 'reset-storage', 'danger')}</section>` : ''}</div>`;
  };

  modal = function (html) {
    oldModal(html);
    const dialog = $('#modal');
    const heading = dialog.querySelector('h2,h1,h3');
    if (heading) { heading.id = 'dialog-title'; dialog.setAttribute('aria-labelledby', heading.id); }
    else dialog.setAttribute('aria-label', 'SavorShelf dialog');
  };

  function updateBottomSpace() {
    const height = document.querySelector('.bottom-nav')?.getBoundingClientRect().height || 0;
    document.documentElement.style.setProperty('--nav-height', height + 'px');
  }
  const navObserver = new ResizeObserver(updateBottomSpace);

  render = function () {
    // Read live accordion state before rebuilding; queued toggle events may not
    // have fired yet when a select immediately triggers rendering.
    for (const panel of document.querySelectorAll('[data-recipe-owner]')) {
      const saved = recipeSectionsOpen.get(panel.dataset.recipeOwner) || new Set();
      panel.open ? saved.add(panel.dataset.recipeSection) : saved.delete(panel.dataset.recipeSection);
      recipeSectionsOpen.set(panel.dataset.recipeOwner, saved);
    }
    for (const panel of document.querySelectorAll('[data-settings-section]')) {
      panel.open ? settingsOpen.add(panel.dataset.settingsSection) : settingsOpen.delete(panel.dataset.settingsSection);
    }
    const previousScreen = document.querySelector('.shell')?.dataset.screen;
    const active = document.activeElement;
    const activeId = active?.id;
    const shoppingKey = active?.dataset.shoppingKey;
    const activeAction = active?.dataset.action;
    const activeDataId = active?.dataset.id;
    const oldScroll = window.scrollY;
    applyAppearance(); oldRender();
    const nextScreen = document.querySelector('.shell')?.dataset.screen;
    if (previousScreen === nextScreen) {
      let target = activeId ? document.getElementById(activeId) : null;
      if (!target && shoppingKey) target = [...document.querySelectorAll('[data-shopping-key]')].find(el => el.dataset.shoppingKey === shoppingKey);
      if (!target && activeAction && activeDataId) target = [...document.querySelectorAll('[data-action]')].find(el => el.dataset.action === activeAction && el.dataset.id === activeDataId);
      target?.focus({preventScroll: true});
      if (oldScroll > 0 && view.type === 'home') window.scrollTo(0, oldScroll);
    }
    navObserver.disconnect();
    const bar = document.querySelector('.bottom-nav'); if (bar) navObserver.observe(bar);
    updateBottomSpace();
  };

  document.addEventListener('toggle', e => {
    if (!e.target.isConnected) return;
    if (e.target.matches?.('.library-filters')) compactFiltersOpen = e.target.open;
    const settingsKey = e.target.dataset?.settingsSection;
    if (settingsKey) e.target.open ? settingsOpen.add(settingsKey) : settingsOpen.delete(settingsKey);
    const recipeKey = e.target.dataset?.recipeSection;
    if (recipeKey && current()) {
      const set = recipeSectionsOpen.get(current().id) || new Set();
      e.target.open ? set.add(recipeKey) : set.delete(recipeKey); recipeSectionsOpen.set(current().id, set);
    }
  }, true);
  document.addEventListener('change', e => {
    if (e.target.dataset.ingredient !== undefined) {
      const inputs = [...document.querySelectorAll('#ingredient-list input[type="checkbox"]')];
      const text = $('#ingredient-progress'); if (text) text.textContent = inputs.filter(i => i.checked).length + ' of ' + inputs.length + ' ready';
    }
    if (e.target.id === 'appearance-theme' || e.target.id === 'cooking-text-size') {
      const key = e.target.id === 'appearance-theme' ? 'theme' : 'cookingText';
      const allowed = key === 'theme' ? ['system', 'light', 'dark'] : ['standard', 'large'];
      if (allowed.includes(e.target.value) && commit(s => { s.uiPreferences = {...s.uiPreferences, [key]: e.target.value}; })) render();
    }
  });
  document.addEventListener('click', e => {
    const target = e.target.closest('[data-action]'); if (!target) return;
    const action = target.dataset.action;
    if (action === 'clear-recipe-search') { query = ''; filter = 'All'; compactFiltersOpen = false; render(); $('#search')?.focus(); }
    else if (action === 'recipe-tools') {
      modal(`<h2>Recipe tools</h2><p class="small">Manage this recipe without changing the original unless you save an edit.</p><div class="recipe-tool-grid">${button(icon('edit') + 'Edit recipe', 'edit')}${button('Rename versions', 'version-names')}${button(icon('history') + 'Version history', 'history')}${button('Similar recipes', 'similar-saved')}${button('Send recipe to ChatGPT', 'recipe-to-chatgpt')}${button('Delete recipe', 'delete', 'danger')}</div>${button('Close', 'close-modal')}`);
    }
  });
  // Existing capture handlers own these actions; close only the tools sheet first.
  // This listener is on window, ahead of document handlers, so no action is duplicated.
  window.addEventListener('click', e => {
    const target = e.target.closest?.('[data-action]');
    if (target?.closest('#modal .recipe-tool-grid') && ['edit', 'delete'].includes(target.dataset.action)) closeModal();
  }, true);
  window.addEventListener('resize', updateBottomSpace);
  applyAppearance(); render();
})();
