// Shared include loader, used by every page. Fetches common/nav.html and
// common/footer.html into [data-include] elements, rewrites relative links
// and images for the page's base path, and wires up the mobile hamburger menu.
// Each page loads this script with a data-base attribute: "./" for the
// homepage, "../" for pages in html/.
(function() {
    var script = document.currentScript;
    var basePath = (script && script.getAttribute('data-base')) || './';

    // Cache-buster for common/nav.html and common/footer.html: bump this when
    // either include changes (no per-page edits needed).
    var includesVers = '013';

    function initIncludes() {
        var includes = document.querySelectorAll('[data-include]');
        includes.forEach(function(element) {
            var file = basePath + 'common/' + element.getAttribute('data-include') + '.html?vers=' + includesVers;
            fetch(file)
                .then(function(response) { return response.text(); })
                .then(function(data) {
                    element.innerHTML = data;
                    element.querySelectorAll('a[href]').forEach(function(a) {
                        var href = a.getAttribute('href');
                        if (href && !href.startsWith('http') && !href.startsWith('#') && !href.startsWith('mailto:')) {
                            a.setAttribute('href', basePath + href);
                        }
                    });
                    element.querySelectorAll('img[src]').forEach(function(img) {
                        var src = img.getAttribute('src');
                        if (src && !src.startsWith('http') && !src.startsWith('/') && !src.startsWith('data:')) {
                            img.setAttribute('src', basePath + src);
                        }
                    });
                    // Initialize hamburger menu after nav loads
                    if (element.getAttribute('data-include') === 'nav') {
                        var btn = element.querySelector('.hamburger');
                        var menu = element.querySelector('.nav-menu');
                        var overlay = document.createElement('div');
                        overlay.className = 'nav-overlay';
                        var closeBtn = document.createElement('button');
                        closeBtn.className = 'nav-menu-close';
                        closeBtn.setAttribute('aria-label', 'Close menu');
                        closeBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
                        var mobileMenu = menu.cloneNode(true);
                        mobileMenu.classList.add('nav-menu-mobile');
                        mobileMenu.insertBefore(closeBtn, mobileMenu.firstChild);
                        document.body.appendChild(overlay);
                        document.body.appendChild(mobileMenu);
                        if (btn && mobileMenu) {
                            function toggleMenu() {
                                var open = mobileMenu.classList.toggle('open');
                                overlay.classList.toggle('open', open);
                                btn.setAttribute('aria-expanded', open);
                                // Lock page scrolling while the menu is open;
                                // the class is styled in css/style.css
                                document.documentElement.classList.toggle('nav-open', open);
                                document.body.classList.toggle('nav-open', open);
                            }
                            btn.addEventListener('click', toggleMenu);
                            overlay.addEventListener('click', toggleMenu);
                            closeBtn.addEventListener('click', toggleMenu);
                            mobileMenu.querySelectorAll('a').forEach(function(a) {
                                a.addEventListener('click', function() {
                                    if (mobileMenu.classList.contains('open')) toggleMenu();
                                });
                            });
                        }
                    }
                })
                .catch(function(error) { console.error('Error loading include:', error); });
        });

        // Add scroll detection for nav border
        var navElement = document.querySelector('[data-include="nav"]');
        window.addEventListener('scroll', function() {
            if (window.scrollY > 100) {
                navElement.classList.add('scrolled');
            } else {
                navElement.classList.remove('scrolled');
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initIncludes);
    } else {
        initIncludes();
    }
})();
