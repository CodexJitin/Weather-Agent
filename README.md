# 🌤️ Weather Agent CLI

An **AI-powered conversational weather assistant** built with [LangChain](https://www.langchain.com/), [Rich](https://github.com/Textualize/rich), and OpenAI models.
It provides real-time weather, air quality, forecasts, and location-aware insights — all wrapped in a modern CLI experience inspired by Gemini-style UIs.

## ✨ Features

* Conversational interaction — ask questions naturally.
* Current weather conditions for any location.
* Real-time air quality data (AQI).
* 5-day / hourly forecasts.
* Automatic detection of current location.
* Modern CLI visuals with Rich (panels, colors, typing effect).
* Error handling with graceful fallback messages.

## 🛠️ Project Structure


weather-agent/
│
├── Tools/
│   ├── Current_Weather.py
│   ├── Air_Pollution.py
│   ├── Current_Location.py
│   ├── W3H5D_Forecast.py
│   └── Location_Coordinates.py
│
├── LLm.py                # LLM configuration
├── main.py               # Entry point (Weather Agent CLI)
└── README.md
```

## ⚙️ Tech Stack

* **LangChain Agents** — reasoning + tool orchestration.
* **Rich** — modern CLI visuals.
* **OpenAI (or compatible LLMs)** — natural language generation.
* **Weather & Pollution APIs** — for live meteorological data.

## 📌 Notes

* The assistant **only answers weather-related queries**.
  Non-weather prompts trigger:
  `"I can only assist with weather-related queries."`


## 🌍 Author

Developed by **CodexJitin**
*“AI-powered weather intelligence at your fingertips.”*