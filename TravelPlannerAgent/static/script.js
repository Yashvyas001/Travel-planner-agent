/**
 * Travel Planner Agent - Frontend JavaScript
 * Handles form submission, API calls, and UI interactions
 */

let currentPlan = null;

// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    const travelForm = document.getElementById('travelForm');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const exportButtons = document.querySelectorAll('.btn-export');

    // Form submission
    if (travelForm) {
        travelForm.addEventListener('submit', handleFormSubmit);
    }

    // Tab switching
    tabButtons.forEach(btn => {
        btn.addEventListener('click', switchTab);
    });

    // Export functionality
    if (exportButtons.length > 0) {
        document.getElementById('exportPDF').addEventListener('click', exportToPDF);
        document.getElementById('exportJSON').addEventListener('click', exportToJSON);
        document.getElementById('printPlan').addEventListener('click', printPlan);
    }
});

/**
 * Handle form submission
 */
async function handleFormSubmit(event) {
    event.preventDefault();

    // Get form data
    const sourceLocation = document.getElementById('sourceLocation').value;
    const destination = document.getElementById('destination').value;
    const days = parseInt(document.getElementById('days').value);
    const budget = parseFloat(document.getElementById('budget').value);
    const travelType = document.getElementById('travelType').value;
    
    // Get selected interests
    const interests = Array.from(document.querySelectorAll('input[name="interests"]:checked'))
        .map(checkbox => checkbox.value);
    
    // Get dietary preferences
    const dietaryPreferences = Array.from(document.querySelectorAll('input[name="dietary_preferences"]:checked'))
        .map(checkbox => checkbox.value);

    // Validation
    if (!destination || days < 1 || budget < 100 || !travelType || interests.length === 0) {
        showError('Please fill all required fields and select at least one interest');
        return;
    }

    // Show loading
    toggleLoading(true);

    try {
        // Call API
        const response = await fetch('/api/plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                source_location: sourceLocation,
                destination: destination,
                days: days,
                budget: budget,
                travel_type: travelType,
                interests: interests,
                dietary_preferences: dietaryPreferences
            })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        const data = await response.json();
        currentPlan = data;

        // Display results
        displayResults(data);
        toggleLoading(false);
        showResultsSection();

    } catch (error) {
        console.error('Error:', error);
        showError(`Error creating travel plan: ${error.message}`);
        toggleLoading(false);
    }
}

/**
 * Display travel plan results
 */
function displayResults(plan) {
    // Display summary
    displaySummary(plan.summary);

    // Display itinerary
    displayItinerary(plan.itinerary);

    // Display budget
    displayBudget(plan.budget);

    // Display hotels
    displayHotels(plan.accommodation);

    // Display weather
    displayWeather(plan.weather);

    // Display food
    displayFood(plan.food);
}

/**
 * Display trip summary
 */
function displaySummary(summary) {
    const summaryContent = document.getElementById('summaryContent');
    summaryContent.innerHTML = `
        <div class="summary-item">
            <strong>📍 Destination:</strong> ${summary.destination}
        </div>
        <div class="summary-item">
            <strong>📅 Duration:</strong> ${summary.duration} days
        </div>
        <div class="summary-item">
            <strong>💰 Budget:</strong> $${summary.total_budget.toFixed(2)}
        </div>
        <div class="summary-item">
            <strong>👥 Travel Type:</strong> ${summary.travel_type}
        </div>
        <div class="summary-item">
            <strong>❤️ Interests:</strong> ${summary.interests.join(', ')}
        </div>
        <div class="summary-item">
            <strong>⏰ Generated:</strong> ${new Date(summary.generated_at).toLocaleString()}
        </div>
    `;
}

/**
 * Display itinerary
 */
function displayItinerary(itinerary) {
    const content = document.getElementById('itineraryContent');
    let html = '';

    itinerary.daily_plans.forEach(day => {
        html += `
            <div class="card">
                <h4>Day ${day.day}</h4>
                <div class="card-details">
                    <strong>Morning:</strong> ${day.morning.activity}
                    <br><small>${day.morning.time}</small>
                </div>
                <div class="card-details">
                    <strong>Afternoon:</strong> ${day.afternoon.activity}
                    <br><small>${day.afternoon.time}</small>
                </div>
                <div class="card-details">
                    <strong>Evening:</strong> ${day.evening.activity}
                    <br><small>${day.evening.time}</small>
                </div>
                <div class="card-details">
                    <strong>Meals:</strong> ${day.meals.breakfast} | ${day.meals.lunch} | ${day.meals.dinner}
                </div>
            </div>
        `;
    });

    // Add highlights
    html += `
        <div class="card" style="grid-column: 1 / -1;">
            <h4>✨ Trip Highlights</h4>
            <ul style="list-style-position: inside; color: #666;">
                ${itinerary.highlights.map(highlight => `<li>${highlight}</li>`).join('')}
            </ul>
        </div>
    `;

    content.innerHTML = html;
}

/**
 * Display budget breakdown
 */
function displayBudget(budget) {
    const content = document.getElementById('budgetContent');
    let html = `
        <div class="budget-breakdown">
            <h3>💰 Budget Breakdown</h3>
            <p><strong>Total Budget:</strong> $${budget.total_budget.toFixed(2)}</p>
            <p><strong>Daily Budget:</strong> $${budget.daily_budget.toFixed(2)}</p>
    `;

    // Breakdown items
    for (const [category, details] of Object.entries(budget.breakdown)) {
        const percentage = details.percentage;
        html += `
            <div class="budget-item">
                <div class="budget-name">
                    <strong>${capitalize(category)}</strong>
                    <small>${details.description}</small>
                </div>
                <div class="budget-amount">
                    <strong>$${details.amount.toFixed(2)}</strong>
                    <small>${percentage}%</small>
                </div>
                <div class="progress-bar" style="width: 100px;">
                    <div class="progress-fill" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    }

    html += `</div>`;

    // Tips
    html += `
        <div class="card" style="background: linear-gradient(135deg, #FFE66D, #FFC93C);">
            <h4>💡 Money Saving Tips</h4>
            <ul style="list-style-position: inside; color: #333;">
                ${budget.money_saving_tips.map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        </div>
    `;

    content.innerHTML = html;
}

/**
 * Display hotel recommendations
 */
function displayHotels(hotels) {
    const content = document.getElementById('hotelsContent');
    let html = '';

    // Budget hotels
    html += '<h3>🏨 Budget Hotels</h3>';
    hotels.budget_hotels.forEach(hotel => {
        html += createHotelCard(hotel);
    });

    // Mid-range hotels
    html += '<h3 style="margin-top: 30px;">🏨 Mid-Range Hotels</h3>';
    hotels.mid_range_hotels.forEach(hotel => {
        html += createHotelCard(hotel);
    });

    // Luxury hotels
    html += '<h3 style="margin-top: 30px;">🏨 Luxury Hotels</h3>';
    hotels.luxury_hotels.forEach(hotel => {
        // Add a luxury class for special styling when applicable
        html += createHotelCard(hotel, true);
    });

    // Tips
    html += `
        <div style="margin-top: 30px; padding: 20px; background: #F3F4F6; border-radius: 12px;">
            <h4>📝 Booking Tips</h4>
            <ul style="list-style-position: inside;">
                ${hotels.booking_tips.map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        </div>
    `;

    // Viral dhabas
    if (hotels.viral_dhabas && hotels.viral_dhabas.length > 0) {
        html += '<h3 style="margin-top:30px;">🔥 Viral Dhabas & Eateries</h3>';
        hotels.viral_dhabas.forEach(d => {
            html += `
                <div class="card">
                    <h4>${d.name}</h4>
                    <p><strong>Location:</strong> ${d.location || 'Unknown'}</p>
                    <p>${d.description}</p>
                </div>
            `;
        });
    }

    // Famous places
    if (hotels.famous_places && hotels.famous_places.length > 0) {
        html += '<h3 style="margin-top:30px;">📍 Famous Places to Visit</h3>';
        html += '<div class="card-grid">';
        hotels.famous_places.forEach(p => {
            html += `
                <div class="card">
                    <h4>${p.title}</h4>
                    <p>${p.snippet || ''}</p>
                    <p><a href="https://www.google.com/search?q=${encodeURIComponent(p.title)}" target="_blank">More info</a></p>
                </div>
            `;
        });
        html += '</div>';
    }

    content.innerHTML = html;
}

/**
 * Create hotel card HTML
 */
function createHotelCard(hotel) {
    // Accept optional luxury flag
    const luxuryClass = hotel && (hotel.name && (hotel.name.toLowerCase().includes('taj') || hotel.name.toLowerCase().includes('raffles') || hotel.name.toLowerCase().includes('palace') || hotel.name.toLowerCase().includes('grand'))) ? 'luxury-hotel' : '';
    return `
        <div class="hotel-card ${luxuryClass}">
            <div class="hotel-header">
                <div>
                    <div class="hotel-name">${hotel.name}</div>
                    <span class="hotel-type">${hotel.type}</span>
                    <div style="margin-top: 5px;">
                        <span class="rating">⭐ ${hotel.rating}/5</span>
                    </div>
                </div>
                <div class="hotel-price">$${hotel.price_per_night.toFixed(2)}</div>
            </div>
            <p><strong>📍 ${hotel.location}</strong></p>
            <div class="amenities">
                ${hotel.amenities.map(amenity => `<span class="amenity">${amenity}</span>`).join('')}
            </div>
            <p><strong>Check-in:</strong> ${hotel.check_in} | <strong>Check-out:</strong> ${hotel.check_out}</p>
            <p><strong>Cancellation:</strong> ${hotel.cancellation}</p>
            <div style="margin-top: 12px; padding: 12px; background: #E8F5E9; border-radius: 8px;">
                <strong>Pros:</strong> ${hotel.pros.join(', ')}
            </div>
            <div style="margin-top: 12px; padding: 12px; background: #FFF3E0; border-radius: 8px;">
                <strong>Cons:</strong> ${hotel.cons.join(', ')}
            </div>
        </div>
    `;
}

// Open map button handler (opens Google Maps search for destination)
document.addEventListener('DOMContentLoaded', function() {
    const openMapBtn = document.getElementById('openMapBtn');
    if (openMapBtn) {
        openMapBtn.addEventListener('click', function() {
            const destinationInput = document.getElementById('destination');
            const destination = destinationInput ? destinationInput.value : '';
            if (!destination) {
                alert('Please enter a destination to open map search.');
                return;
            }
            const url = `https://www.google.com/maps/search/${encodeURIComponent(destination)}`;
            window.open(url, '_blank');
        });
    }
});

/**
 * Display weather information
 */
function displayWeather(weather) {
    const content = document.getElementById('weatherContent');
    const current = weather.current_weather;

    let html = `
        <div class="weather-card">
            <div class="weather-icon">
                ${getWeatherEmoji(current.weather)}
            </div>
            <div class="weather-temp">${current.temperature}°C</div>
            <div class="weather-desc">${current.description}</div>
            <div class="weather-details">
                <div class="weather-detail">
                    <div class="weather-detail-label">Feels Like</div>
                    <div class="weather-detail-value">${current.feels_like}°C</div>
                </div>
                <div class="weather-detail">
                    <div class="weather-detail-label">Humidity</div>
                    <div class="weather-detail-value">${current.humidity}%</div>
                </div>
                <div class="weather-detail">
                    <div class="weather-detail-label">Wind Speed</div>
                    <div class="weather-detail-value">${current.wind_speed} m/s</div>
                </div>
                <div class="weather-detail">
                    <div class="weather-detail-label">Visibility</div>
                    <div class="weather-detail-value">${(current.visibility / 1000).toFixed(1)} km</div>
                </div>
            </div>
        </div>
    `;

    // Suitability
    html += `
        <div class="card">
            <h4>🎯 Travel Suitability</h4>
            <p><strong>Score:</strong> ${weather.suitability.score}/100</p>
            <p><strong>Rating:</strong> <span class="badge">${weather.suitability.rating}</span></p>
            <div style="margin-top: 15px;">
                <strong>Recommendations:</strong>
                <ul style="list-style-position: inside; margin-top: 10px;">
                    ${weather.suitability.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;

    // Clothing suggestions
    const clothing = weather.clothing_suggestions;
    html += `
        <div class="card">
            <h4>👔 Clothing Suggestions</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                ${Object.entries(clothing).map(([category, items]) => `
                    <div>
                        <strong>${capitalize(category.replace(/_/g, ' '))}</strong>
                        <ul style="list-style-position: inside; margin-top: 8px;">
                            ${items.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    // Alerts
    html += `
        <div class="card" style="background: #FFF3E0;">
            <h4>⚠️ Weather Alerts</h4>
            <ul style="list-style-position: inside;">
                ${weather.weather_alerts.map(alert => `<li>${alert}</li>`).join('')}
            </ul>
        </div>
    `;

    content.innerHTML = html;
}

/**
 * Display food recommendations
 */
function displayFood(food) {
    const content = document.getElementById('foodContent');
    let html = '';

    // Must-try dishes
    html += '<h3>🍽️ Must-Try Dishes</h3>';
    html += '<div class="card-grid">';
    food.must_try_dishes.forEach(dish => {
        html += `
            <div class="card">
                <h4>${dish.name}</h4>
                <p><strong>Description:</strong> ${dish.description}</p>
                <p><strong>Best at:</strong> ${dish.best_place}</p>
                <p><strong>Price:</strong> ${dish.price_range}</p>
                <p><strong>Vegetarian:</strong> ${dish.vegetarian ? '✓ Yes' : '✗ No'}</p>
            </div>
        `;
    });
    html += '</div>';

    // Street food
    html += '<h3>🌮 Street Food</h3>';
    html += '<div class="card-grid">';
    food.street_food.forEach(item => {
        html += `
            <div class="card">
                <h4>${item.name}</h4>
                <p><strong>Location:</strong> ${item.location}</p>
                <p><strong>Price:</strong> ${item.price}</p>
                <p><strong>Hygiene:</strong> <span class="badge success">${item.hygiene_level}</span></p>
                <p>${item.description}</p>
            </div>
        `;
    });
    html += '</div>';

    // Safety tips
    html += `
        <div class="card">
            <h4>🛡️ Food Safety Tips</h4>
            <ul style="list-style-position: inside;">
                ${food.food_safety_tips.map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        </div>
    `;

    content.innerHTML = html;
}

/**
 * Switch tabs
 */
function switchTab(event) {
    const tabName = event.target.getAttribute('data-tab');
    
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const selectedTab = document.getElementById(`${tabName}-tab`);
    if (selectedTab) {
        selectedTab.style.display = 'block';
        selectedTab.classList.add('active');
    }

    // Add active class to clicked button
    event.target.classList.add('active');
}

/**
 * Toggle loading state
 */
function toggleLoading(show) {
    const loadingSection = document.getElementById('loadingSection');
    if (loadingSection) {
        loadingSection.style.display = show ? 'flex' : 'none';
    }
}

/**
 * Show results section
 */
function showResultsSection() {
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('errorSection').style.display = 'none';
    document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
    setTimeout(() => document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' }), 500);
}

/**
 * Show error message
 */
function showError(message) {
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Export to PDF
 */
function exportToPDF() {
    if (!currentPlan) return;
    alert('📥 PDF export would be generated here. In production, use a library like jsPDF.');
}

/**
 * Export to JSON
 */
function exportToJSON() {
    if (!currentPlan) return;
    
    const dataStr = JSON.stringify(currentPlan, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `travel_plan_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
}

/**
 * Print travel plan
 */
function printPlan() {
    if (!currentPlan) return;
    window.print();
}

/**
 * Utility function to capitalize string
 */
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Get weather emoji
 */
function getWeatherEmoji(weather) {
    const weatherLower = weather.toLowerCase();
    
    if (weatherLower.includes('rain')) return '🌧️';
    if (weatherLower.includes('cloud')) return '☁️';
    if (weatherLower.includes('sunny') || weatherLower.includes('clear')) return '☀️';
    if (weatherLower.includes('snow')) return '❄️';
    if (weatherLower.includes('wind')) return '💨';
    if (weatherLower.includes('storm')) return '⛈️';
    if (weatherLower.includes('thunder')) return '🌩️';
    
    return '⛅';
}
