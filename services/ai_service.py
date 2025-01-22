import os
from openai import OpenAI
import logging

class AIFleetAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.model = "gpt-4"  # Using standard GPT-4 model

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
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating route suggestions: {str(e)}")
            error_msg = str(e)
            if "API key" in error_msg:
                return "API configuration error. Please contact support."
            elif "model" in error_msg:
                return "AI model temporarily unavailable. Please try again later."
            return f"Unable to generate route suggestions: {error_msg}"

    def analyze_performance(self, truck_performance_data):
        """Analyze truck performance data and provide insights."""
        try:
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
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error analyzing performance: {str(e)}")
            error_msg = str(e)
            if "API key" in error_msg:
                return "API configuration error. Please contact support."
            elif "model" in error_msg:
                return "AI model temporarily unavailable. Please try again later."
            return f"Unable to analyze performance: {error_msg}"