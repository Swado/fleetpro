import os
from openai import OpenAI
import logging

class AIFleetAssistant:
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.model = "gpt-4o"

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
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating route suggestions: {str(e)}")
            return "Unable to generate route suggestions at the moment. Please try again later."

    def analyze_performance(self, truck_performance_data):
        """Analyze truck performance data and provide insights."""
        try:
            # Format the performance data for analysis
            prompt = f"""Analyze the following truck performance metrics:
Runtime Hours (avg): {truck_performance_data.get('avg_runtime', 0):.2f} hours/day
Idle Time (avg): {truck_performance_data.get('avg_idle_time', 0):.2f} hours/day
Total Trips: {truck_performance_data.get('total_trips', 0)}

Provide:
1. Efficiency analysis
2. Suggestions for reducing idle time
3. Performance optimization recommendations
4. Comparison with industry standards
Keep the response focused on actionable insights."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250,
                response_format={"type": "text"}
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error analyzing performance: {str(e)}")
            return "Unable to analyze performance at the moment. Please try again later."