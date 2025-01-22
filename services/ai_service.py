import os
from openai import OpenAI
from datetime import datetime

class AIFleetAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    def get_route_suggestion(self, start_city, start_state, destination_city, destination_state, truck_data):
        """Get AI-powered route suggestions and insights."""
        prompt = f"""As a fleet management AI assistant, analyze the following route:
From: {start_city}, {start_state}
To: {destination_city}, {destination_state}

Truck Details:
- Model: {truck_data.get('model')}
- Last Maintenance: {truck_data.get('last_maintenance')}
- Status: {truck_data.get('status')}

Provide:
1. Estimated travel time and suggested rest stops
2. Weather-related considerations
3. Route optimization suggestions
4. Maintenance recommendations based on the trip
Keep the response concise and practical."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Unable to generate route suggestions at the moment: {str(e)}"

    def analyze_performance(self, truck_performance_data):
        """Analyze truck performance data and provide insights."""
        performance_summary = f"""
Runtime Hours: {truck_performance_data.get('avg_runtime', 0)} hours/day
Idle Time: {truck_performance_data.get('avg_idle_time', 0)} hours/day
Total Trips: {truck_performance_data.get('total_trips', 0)}
"""

        prompt = f"""As a fleet management AI assistant, analyze this truck's performance:
{performance_summary}

Provide:
1. Efficiency analysis
2. Suggestions for reducing idle time
3. Maintenance recommendations
4. Performance optimization tips
Keep the response focused on actionable insights."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Unable to analyze performance at the moment: {str(e)}"
