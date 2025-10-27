/**
 * Client-side JavaScript for sidebar interactions
 */

// Function to update sidebar collapsed state
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        // Toggle nav text visibility based on sidebar width
        toggle_nav_text: function(sidebar_style) {
            if (!sidebar_style) return window.dash_clientside.no_update;
            
            const isCollapsed = sidebar_style.width === '60px' || 
                               sidebar_style.minWidth === '60px';
            
            // Get all nav text elements
            const navTexts = document.querySelectorAll('.nav-text');
            const submenu = document.querySelector('.request-review-submenu');
            
            navTexts.forEach(text => {
                text.style.display = isCollapsed ? 'none' : '';
            });
            
            if (submenu && isCollapsed) {
                submenu.style.display = 'none';
            }
            
            return window.dash_clientside.no_update;
        }
    }
});
