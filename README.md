# Multi-Agent Real Estate Assistant Chatbot

This project implements a multi-agentic real estate chatbot system capable of handling property issue detection (with image analysis) and tenancy FAQ questions. The system uses a router agent to intelligently direct user queries to specialized agents based on the nature of the query and presence of images.

## Features

### 1. Issue Detection & Troubleshooting Agent
- Analyzes uploaded images of property issues
- Detects problems like water damage, mold, cracks, and other maintenance issues
- Provides troubleshooting suggestions and recommendations
- Can ask follow-up questions to better diagnose issues

### 2. Tenancy FAQ Agent
- Answers questions about tenancy laws, agreements, and rental processes
- Provides location-specific guidance when location information is available
- Covers topics like:
  - Notice periods for terminating leases
  - Security deposit regulations
  - Landlord and tenant responsibilities
  - Rent increases
  - Eviction processes

### 3. Intelligent Router
- Automatically determines which agent should handle the query
- Uses context, query content, and image presence to make routing decisions
- Ensures seamless user experience with appropriate agent handoffs

## Technology Stack

The project uses the following technologies:

- **OpenAI API**: For powerful language and vision capabilities
  - GPT-4 Turbo for text processing
  - GPT-4 Vision for image analysis
- **LangGraph**: For agent orchestration and workflow management
- **Streamlit**: For the web interface
- **Python**: For the application backend

## Installation and Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/real-estate-chatbot.git
cd real-estate-chatbot
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the application
```bash
streamlit run app.py
```

## Usage

1. **Property Issues**:
   - Upload an image of the property issue
   - Ask a question about the issue or simply request analysis
   - Review the AI's identification and troubleshooting suggestions

2. **Tenancy Questions**:
   - Type your question about rental agreements, rights, etc.
   - Optionally provide your location for location-specific advice
   - Get detailed answers based on relevant tenancy regulations

## Project Structure

```
real_estate_chatbot/
├── app.py                    # Main Streamlit interface
├── requirements.txt          # Dependencies
├── config.py                 # Configuration settings
├── agents/
│   ├── __init__.py
│   ├── router_agent.py       # Router/Manager agent
│   ├── issue_agent.py        # Issue detection agent
│   ├── tenancy_agent.py      # Tenancy FAQ agent
├── utils/
│   ├── __init__.py
│   ├── image_processor.py    # Image handling utilities
│   ├── langraph_workflow.py  # LangGraph orchestration
│   ├── knowledge_base.py     # Tenancy knowledge and references
├── static/
    └── css/
        └── style.css         # Custom styling
```

## Example Interactions

### Issue Detection Example
**User**: "What's wrong with this wall?" (with uploaded image of wall mold)
**Agent**: "I can see signs of black mold growth near the ceiling joint. This is typically caused by excess moisture and poor ventilation. I recommend:
1. Identify and fix any water leaks
2. Improve ventilation with fans or dehumidifiers
3. Clean the affected area with a mold-killing solution
4. Consider consulting a professional if the mold covers a large area"

### Tenancy FAQ Example
**User**: "Can my landlord increase rent during my lease term?"
**Agent**: "Generally, landlords cannot increase rent during a fixed-term lease unless the lease specifically allows for it. For month-to-month tenancies, landlords typically must provide notice (usually 30-90 days depending on location) before implementing a rent increase. If you're in a rent-controlled area, there may be additional restrictions on how much and how often rent can be increased."

## Future Enhancements

- Integration with property databases for more location-specific information
- Expanded knowledge base for international tenancy laws
- Image comparison features to track property issues over time
- Integration with real estate listing APIs for property recommendations
- Additional agent specializations (e.g., mortgage assistance, property valuation)

## Contributors

This project was created as a proof of concept for multi-agent AI systems in the real estate domain.