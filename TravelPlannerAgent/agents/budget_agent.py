"""
Budget Agent
Generates and manages travel budget
"""

from typing import Dict, Any
from services.granite_service import GraniteAgent

class BudgetAgent(GraniteAgent):
    """Agent for budget planning and management"""
    
    def __init__(self, config=None):
        """Initialize Budget Agent"""
        super().__init__("BudgetAgent", config)
    
    def process(self, budget: float, days: int, travel_type: str, 
               destination: str) -> Dict[str, Any]:
        """
        Generate budget breakdown
        
        Args:
            budget: Total budget in currency
            days: Number of days
            travel_type: Type of travel
            destination: Travel destination
            
        Returns:
            Budget breakdown dictionary
        """
        self.log(f"Calculating budget breakdown for ${budget} over {days} days")
        self.log(f"Travel Type: {travel_type}, Destination: {destination}")
        
        # Get budget breakdown from Granite
        breakdown = self.service.generate_budget_breakdown(budget, days, travel_type)
        
        # Structure budget details
        budget_plan = {
            'total_budget': budget,
            'duration': days,
            'travel_type': travel_type,
            'destination': destination,
            'daily_budget': round(budget / days, 2),
            'breakdown': self._create_budget_breakdown(budget, travel_type),
            'expenses_by_day': self._distribute_expenses(budget, days),
            'payment_methods': self._suggest_payment_methods(),
            'money_saving_tips': self._get_money_saving_tips(),
            'budget_alerts': self._get_budget_alerts(budget)
        }
        
        self.log("Budget plan created successfully")
        return budget_plan
    
    def _create_budget_breakdown(self, total_budget: float, travel_type: str) -> Dict[str, Dict[str, Any]]:
        """
        Create detailed budget breakdown
        
        Args:
            total_budget: Total budget
            travel_type: Type of travel
            
        Returns:
            Detailed breakdown
        """
        breakdown = {
            'accommodation': {
                'percentage': 35,
                'amount': round(total_budget * 0.35, 2),
                'description': 'Hotels, hostels, or homestays',
                'tips': 'Book in advance for better rates'
            },
            'food': {
                'percentage': 25,
                'amount': round(total_budget * 0.25, 2),
                'description': 'Meals and dining',
                'tips': 'Mix of restaurants and street food'
            },
            'transportation': {
                'percentage': 15,
                'amount': round(total_budget * 0.15, 2),
                'description': 'Local travel and transfers',
                'tips': 'Use public transport to save money'
            },
            'activities': {
                'percentage': 15,
                'amount': round(total_budget * 0.15, 2),
                'description': 'Tours, attractions, experiences',
                'tips': 'Look for combo deals and discounts'
            },
            'shopping': {
                'percentage': 5,
                'amount': round(total_budget * 0.05, 2),
                'description': 'Souvenirs and shopping',
                'tips': 'Set a limit before shopping'
            },
            'emergency': {
                'percentage': 5,
                'amount': round(total_budget * 0.05, 2),
                'description': 'Contingency fund',
                'tips': 'Keep this for emergencies only'
            }
        }
        
        # Adjust for travel type
        if travel_type == 'Family':
            breakdown['activities']['percentage'] = 20
            breakdown['food']['percentage'] = 30
        elif travel_type == 'Solo':
            breakdown['accommodation']['percentage'] = 40
        elif travel_type == 'Couple':
            breakdown['activities']['percentage'] = 20
        
        return breakdown
    
    def _distribute_expenses(self, total_budget: float, days: int) -> Dict[int, float]:
        """
        Distribute expenses across days
        
        Args:
            total_budget: Total budget
            days: Number of days
            
        Returns:
            Daily expense distribution
        """
        daily_budget = total_budget / days
        distribution = {}
        
        for day in range(1, days + 1):
            # Add some variation to expenses (more on first and last days)
            if day == 1 or day == days:
                distribution[day] = round(daily_budget * 1.2, 2)
            else:
                distribution[day] = round(daily_budget, 2)
        
        return distribution
    
    def _suggest_payment_methods(self) -> Dict[str, list]:
        """Suggest payment methods for travel"""
        return {
            'primary': [
                'Credit/Debit cards',
                'Digital wallets (Apple Pay, Google Pay)',
                'Travel cards with forex benefits'
            ],
            'secondary': [
                'Cash (local currency)',
                'Traveler\'s checks (if needed)',
                'Wire transfer service'
            ],
            'tips': [
                'Notify bank before travel',
                'Carry backup payment methods',
                'Avoid carrying large amounts of cash',
                'Use ATMs to withdraw local currency'
            ]
        }
    
    def _get_money_saving_tips(self) -> list:
        """Get money-saving tips for travel"""
        return [
            'Use public transportation instead of taxis',
            'Eat at local markets and food courts',
            'Look for free walking tours',
            'Visit attractions during discount hours',
            'Book activities in advance for discounts',
            'Travel during off-peak season',
            'Share accommodation with other travelers',
            'Use travel passes for multiple attractions',
            'Carry refillable water bottle',
            'Look for combo deals and packages'
        ]
    
    def _get_budget_alerts(self, budget: float) -> list:
        """Get budget-related alerts"""
        alerts = []
        
        if budget < 500:
            alerts.append('⚠️ Low budget - focus on budget accommodations and local food')
        elif budget < 1000:
            alerts.append('ℹ️ Moderate budget - balance comfort and savings')
        else:
            alerts.append('✓ Good budget for comfortable travel')
        
        alerts.append('💡 Don\'t forget travel insurance')
        alerts.append('💡 Keep emergency fund separate')
        
        return alerts
