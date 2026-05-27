Project Writeup

This project is a Hybrid JMeter Script Generator that converts static API captures, such as HAR files and Postman collections, into executable JMeter .jmx load test scripts. It combines a deterministic parsing and JMX-generation core with an optional AI agent layer for smarter traffic filtering, correlation, logical grouping, and self-healing.

Architecture

The system has three main layers:

Frontend UI

Built with plain HTML, CSS, and JavaScript.
Allows users to upload a HAR or Postman collection.
Lets users configure load test parameters such as users, ramp-up, duration, think time, LLM provider, and model.
Displays pipeline results, filtered traffic, correlations, self-healing logs, generated JMX, and download controls.
Backend API

Built with FastAPI.
Exposes endpoints for file-based script generation and LLM provider status.
Orchestrates the full pipeline: parse input, filter traffic, correlate tokens, rebuild logical flow, generate JMX, validate via dry run, and return the generated script.
Generation Engine

Python service modules handle deterministic parsing, schema normalization, JMX XML building, JMeter validation, and optional AI-assisted reasoning.
The AI layer supports multiple providers: Gemini, Claude, OpenAI, Grok, Groq, and GitHub Models.
Technology Used

Frontend: HTML, CSS, JavaScript, Lucide icons
Backend: Python, FastAPI, Uvicorn
Load Testing Output: Apache JMeter .jmx
Input Formats: HAR JSON, Postman Collection v2/v2.1
LLM Providers: Gemini, Claude, OpenAI, Grok, Groq, GitHub Models
Validation: Headless JMeter execution where available, plus XML validation fallback
Config: .env based provider and model configuration
Logical Workflow

The user uploads a HAR file or Postman collection from the frontend.
The backend detects the input type and normalizes all requests into a common internal schema.
The parser extracts request methods, URLs, headers, query params, body data, cookies, timing metadata, response headers, and response bodies.
The traffic filter removes browser noise such as static assets, fonts, analytics, tracking pixels, and third-party CDN calls.
The correlation engine scans downstream requests for dynamic values such as bearer tokens, CSRF tokens, session IDs, cookies, and high-entropy parameters.
It traces those values back to earlier responses and injects JMeter extractors such as JSON Extractor, Boundary Extractor, Regex Extractor, or Header Extractor.
Hardcoded dynamic values in later requests are replaced with JMeter variables like ${c_authToken}.
The logical reconstructor groups requests into business transactions and detects parallel request groups based on browser timing.
The JMX builder creates a complete JMeter test plan with Thread Group, Cookie Manager, HTTP defaults, Transaction Controllers, Parallel Controllers, timers, samplers, headers, request bodies, and extractors.
The self-healing pipeline runs a constrained dry-run JMX with one user and one loop. If failures are detected, the AI layer can inspect the failure and suggest missing extractors or replacements.
The final production-ready JMX is returned to the frontend for preview and download.
Key Value

The core value is that the project does more than simply convert requests. It attempts to turn raw recordings into realistic, maintainable performance scripts by removing noise, preserving user intent, correlating dynamic values, reconstructing browser behavior, and validating the output before download.
