import os
from openai import OpenAI
import logging

class AIFleetAssistant:
    def __init__(self):
        # Ensure OPENAI_API_KEY is available
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            logging.error("OpenAI API key not found in environment variables")
            raise ValueError("OPENAI_API_KEY environment variable must be set")

        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"  # Using GPT-3.5-turbo for better availability
        logging.info(f"Initializing AI Fleet Assistant with model: {self.model}")

    def get_route_suggestion(self, start_city, start_state, destination_city, destination_state, truck_data):
        """Get AI-powered route suggestions and insights."""
        try:
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

            logging.debug(f"Sending route suggestion request for {start_city} to {destination_city}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            logging.debug("Successfully received route suggestion response")
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating route suggestions: {str(e)}", exc_info=True)
            error_msg = str(e)
            if "api_key" in error_msg.lower():
                return "API configuration error. Please check your API key configuration."
            elif "model" in error_msg.lower():
                return "AI model temporarily unavailable. Try using a different model."
            elif "rate limit" in error_msg.lower():
                return "Rate limit exceeded. Please try again in a few moments."
            return "An error occurred while generating suggestions. Please try again later."

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

            logging.debug("Sending performance analysis request")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            logging.debug("Successfully received performance analysis response")
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error analyzing performance: {str(e)}", exc_info=True)
            error_msg = str(e)
            if "api_key" in error_msg.lower():
                return "API configuration error. Please check your API key configuration."
            elif "model" in error_msg.lower():
                return "AI model temporarily unavailable. Try using a different model."
            elif "rate limit" in error_msg.lower():
                return "Rate limit exceeded. Please try again in a few moments."
            return "An error occurred while analyzing performance. Please try again later."