/* -------------------------------------------------------------
   COMMAND PALETTE JS (CTRL+K SEARCH)
   ------------------------------------------------------------- */

(function() {
    const palette = document.getElementById('command-palette');
    const searchInput = document.getElementById('palette-search-input');
    const resultsBox = document.getElementById('palette-results-box');
    const closeZone = document.getElementById('palette-close-zone');
    const triggerBtn = document.getElementById('search-trigger-btn');
    
    if (!palette) return;

    let selectedIndex = -1;
    let items = [];

    // Trigger buttons
    if(triggerBtn) {
        triggerBtn.addEventListener('click', openPalette);
    }
    closeZone.addEventListener('click', closePalette);

    // Global Key Listener
    document.addEventListener('keydown', function(e) {
        // Ctrl+K or Cmd+K
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            if (palette.classList.contains('hidden')) {
                openPalette();
            } else {
                closePalette();
            }
        }
        
        // Esc to close
        if (e.key === 'Escape' && !palette.classList.contains('hidden')) {
            closePalette();
        }

        // Navigation keys if palette is open
        if (!palette.classList.contains('hidden') && items.length > 0) {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                navigateResults(1);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                navigateResults(-1);
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (selectedIndex >= 0 && selectedIndex < items.length) {
                    items[selectedIndex].click();
                }
            }
        }
    });

    // Search Input Listener
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        if (query.length < 2) {
            resultsBox.innerHTML = `
                <div class="palette-placeholder">
                    <p>Type keywords to search portfolio...</p>
                </div>
            `;
            items = [];
            selectedIndex = -1;
            return;
        }

        // Fetch AJAX results
        fetch(`/search/?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                renderResults(data.results);
            })
            .catch(err => {
                console.error("Search query failed: ", err);
            });
    });

    function openPalette() {
        palette.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // Lock scrolling
        setTimeout(() => searchInput.focus(), 50);
    }

    function closePalette() {
        palette.classList.add('hidden');
        document.body.style.overflow = ''; // Unlock scrolling
        searchInput.value = '';
        resultsBox.innerHTML = `
            <div class="palette-placeholder">
                <p>Type keywords to search portfolio...</p>
            </div>
        `;
        items = [];
        selectedIndex = -1;
    }

    function renderResults(results) {
        if (!results || results.length === 0) {
            resultsBox.innerHTML = `
                <div class="palette-placeholder">
                    <p>No results found for "${searchInput.value}"</p>
                </div>
            `;
            items = [];
            selectedIndex = -1;
            return;
        }

        let html = '';
        results.forEach((item, index) => {
            html += `
                <a href="${item.url}" class="palette-item" data-index="${index}">
                    <div class="palette-item-info">
                        <h4>${escapeHTML(item.title)}</h4>
                        <span>${escapeHTML(item.subtitle)}</span>
                    </div>
                    <span class="palette-item-tag">${escapeHTML(item.category)}</span>
                </a>
            `;
        });

        resultsBox.innerHTML = html;
        items = resultsBox.querySelectorAll('.palette-item');
        selectedIndex = 0;
        highlightItem();

        // Mouse click bindings
        items.forEach(el => {
            el.addEventListener('mouseenter', function() {
                selectedIndex = parseInt(this.getAttribute('data-index'));
                highlightItem();
            });
        });
    }

    function navigateResults(direction) {
        selectedIndex += direction;
        if (selectedIndex >= items.length) {
            selectedIndex = 0;
        } else if (selectedIndex < 0) {
            selectedIndex = items.length - 1;
        }
        highlightItem();
    }

    function highlightItem() {
        items.forEach((item, index) => {
            if (index === selectedIndex) {
                item.classList.add('selected');
                item.scrollIntoView({ block: 'nearest' });
            } else {
                item.classList.remove('selected');
            }
        });
    }

    function escapeHTML(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
})();
