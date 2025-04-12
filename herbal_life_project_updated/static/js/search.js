// Create a namespace for search functionality to avoid global scope pollution
// Check if HerbalLifeSearch is already defined
if (typeof window.HerbalLifeSearch === 'undefined') {
    window.HerbalLifeSearch = {
        searchTimeout: null,
        searchHistory: JSON.parse(localStorage.getItem('searchHistory') || '[]')
    };
}

function debounceSearch(searchTerm) {
    clearTimeout(window.HerbalLifeSearch.searchTimeout);
    window.HerbalLifeSearch.searchTimeout = setTimeout(() => performSearch(searchTerm), 300);
}

async function performSearch(searchTerm) {
    if (searchTerm.length < 2) {
        document.querySelector('.search-results').innerHTML = '';
        return;
    }

    try {
        // Use the API endpoint instead of static JSON file
        const response = await fetch(`/api/plants?search=${encodeURIComponent(searchTerm)}`);
        const data = await response.json();
        
        if (!data.plants || data.plants.length === 0) {
            document.querySelector('.search-results').innerHTML = `
                <div class="p-3 text-center">
                    <p class="text-muted">No results found for "${searchTerm}"</p>
                </div>
            `;
            return;
        }
        
        displaySearchResults(data.plants);
        updateSearchHistory(searchTerm);
    } catch (error) {
        console.error('Error performing search:', error);
        document.querySelector('.search-results').innerHTML = `
            <div class="p-3 text-center">
                <p class="text-danger">Error searching. Please try again.</p>
            </div>
        `;
    }
}

function displaySearchResults(results) {
    const resultsContainer = document.querySelector('.search-results');
    
    // Limit to 5 results for quick search
    const limitedResults = results.slice(0, 5);
    
    resultsContainer.innerHTML = limitedResults.map(plant => `
        <div class="p-2 border-bottom hover-effect" onclick="window.location.href='/plants'">
            <h6>${plant.name}</h6>
            <small class="text-muted">${plant.scientific_name || ''}</small>
        </div>
    `).join('');
    
    // Add a "View all results" link if there are more
    if (results.length > 5) {
        resultsContainer.innerHTML += `
            <div class="p-2 text-center">
                <a href="/plants" class="text-success">View all ${results.length} results</a>
            </div>
        `;
    }
}

function updateSearchHistory(searchTerm) {
    if (!window.HerbalLifeSearch.searchHistory.includes(searchTerm)) {
        window.HerbalLifeSearch.searchHistory.unshift(searchTerm);
        if (window.HerbalLifeSearch.searchHistory.length > 5) window.HerbalLifeSearch.searchHistory.pop();
        localStorage.setItem('searchHistory', JSON.stringify(window.HerbalLifeSearch.searchHistory));
    }
}
