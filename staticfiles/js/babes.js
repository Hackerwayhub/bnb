document.addEventListener('DOMContentLoaded', function() {
    // More/Less functionality for filters
    const filtersRow = document.querySelector('.filters-row');
    const allFilterItems = document.querySelectorAll('.filter-item');

    // Check if More/Less button already exists to prevent duplicates
    const existingMoreButton = filtersRow.querySelector('.more-button');
    if (existingMoreButton) {
        existingMoreButton.remove();
    }

    // Set items per row based on device type
    let itemsPerRow;
    if (window.innerWidth < 768) {
        itemsPerRow = 2; // Mobile
    } else {
        itemsPerRow = 8; // Desktop/Laptop
    }

    // Hide all items beyond the limit for both mobile and desktop
    allFilterItems.forEach((item, index) => {
        if (index >= itemsPerRow) {
            item.style.display = 'none';
        } else {
            item.style.display = 'inline-block';
        }
    });

    // Create "More" button if there are hidden items
    if (allFilterItems.length > itemsPerRow) {
        const moreButton = document.createElement('a');
        moreButton.href = '#';
        moreButton.className = 'filter-item more-button';
        moreButton.innerHTML = '<i class="fa fa-chevron-down" aria-hidden="true"></i> more locations ';
        moreButton.style.cssText = `
            cursor: pointer !important;
            font-weight: bold !important;
            font-size: 10px !important;
            background-color: #FF0000 !important;
            color: white !important;
            border: 1px solid #FF0000 !important;
            padding: 8px 16px !important;
            border-radius: 20px !important;
            text-decoration: none !important;
            display: inline-block !important;
            margin: 4px !important;
            transition: all 0.3s ease !important;
        `;

        // Initialize state
        moreButton.setAttribute('data-expanded', 'false');

        moreButton.addEventListener('click', function(e) {
            e.preventDefault();
            const isExpanded = moreButton.getAttribute('data-expanded') === 'true';

            if (!isExpanded) {
                // Show all hidden items
                allFilterItems.forEach((item, index) => {
                    if (index >= itemsPerRow) {
                        item.style.display = 'inline-block';
                    }
                });
                moreButton.innerHTML = '<i class="fa fa-chevron-up" aria-hidden="true"></i>  ';
                moreButton.setAttribute('data-expanded', 'true');
            } else {
                // Hide items beyond the limit
                allFilterItems.forEach((item, index) => {
                    if (index >= itemsPerRow) {
                        item.style.display = 'none';
                    }
                });
                moreButton.innerHTML = '<i class="fa fa-chevron-down" aria-hidden="true"></i> ';
                moreButton.setAttribute('data-expanded', 'false');
            }
        });

        filtersRow.appendChild(moreButton);
    }

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Update page title dynamically for better UX
    if (typeof location_display !== 'undefined' && location_display) {
        document.title = `Escort Girls in ${location_display} | bnb.co.ke`;
    }

    // Track filter clicks for analytics
    document.querySelectorAll('.filter-item').forEach(item => {
        item.addEventListener('click', function() {
            const location = this.textContent.trim();
            if (typeof gtag !== 'undefined' && !this.classList.contains('more-button')) {
                gtag('event', 'location_filter_click', {
                    'event_category': 'Filter',
                    'event_label': location
                });
            }
        });
    });
});