import { useEffect, useRef, useState } from "react";
import "./App.css";

const DEFAULT_SUGGESTIONS = [
  "What is a business loan?",
  "What is an MSME loan?",
  "Explain my account breakdown.",
  "What is the percentage distribution of debits, credits, fees, and penalties in my account?",
  "Why am I paying fees and penalties on my account?",
  "How can I save money each month?",
];

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function ChartPanel({ chart }) {
  if (!chart || !Array.isArray(chart.items)) {
    return null;
  }

  return (
    <div className="chart-panel">
      <h3>{chart.title}</h3>
      {chart.items.map((item) => (
        <div key={item.label} className="chart-row">
          <div className="chart-meta">
            <span
              className="chart-swatch"
              style={{ backgroundColor: item.color || "#38bdf8" }}
            />
            <span>{item.label}</span>
          </div>
          <div className="chart-bar-track">
            <div
              className="chart-bar-fill"
              style={{
                width: `${item.value}%`,
                background: item.color || "#38bdf8",
              }}
            />
          </div>
          <span className="chart-value">{item.value}%</span>
        </div>
      ))}
    </div>
  );
}

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "bot",
      text: "Hello! I am the Eazily Done fintech assistant. I can help with account breakdowns, fee explanations, savings guidance, business loans, MSME loans, eligibility, interest rates, and required documents.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [suggestions, setSuggestions] = useState(DEFAULT_SUGGESTIONS);
  const endOfMessagesRef = useRef(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  useEffect(() => {
    const loadSuggestions = async () => {
      try {
        const response = await fetch(`${API_URL}/questions`);
        if (!response.ok) {
          return;
        }
        const data = await response.json();
        if (Array.isArray(data.questions) && data.questions.length > 0) {
          const nextSuggestions = data.questions
            .slice(0, 5)
            .map((item) => item.question);
          setSuggestions(nextSuggestions);
        }
      } catch (error) {
        console.error("Failed to load suggestions", error);
      }
    };

    loadSuggestions();
  }, []);

  const addMessage = (sender, text, chart = null) => {
    setMessages((current) => [
      ...current,
      {
        id: Date.now() + Math.random(),
        sender,
        text,
        chart,
      },
    ]);
  };

  const handleSubmit = async (questionText = input) => {
    const trimmedQuestion = questionText.trim();
    if (!trimmedQuestion || isLoading) {
      return;
    }

    setInput("");
    setError("");
    addMessage("user", trimmedQuestion);
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: trimmedQuestion }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || "Unable to reach the chatbot service right now.",
        );
      }

      const data = await response.json();
      addMessage("bot", data.answer, data.chart || null);
    } catch (err) {
      const message = err.message || "Something went wrong. Please try again.";
      setError(message);
      addMessage(
        "bot",
        "The service is temporarily unavailable. Please check whether the backend is running and try again, or ask a simpler finance question such as business loan eligibility or account fees.",
      );
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: 1,
        sender: "bot",
        text: "Chat cleared. Ask me about business loans, MSME loans, eligibility, interest rates, fees, penalties, or savings guidance.",
      },
    ]);
    setError("");
  };

  return (
    <div className="app-shell">
      <div className="chat-card">
        <header className="topbar">
          <div>
            <p className="eyebrow">Eazily Done</p>
            <h1>Fintech Account Assistant</h1>
          </div>
          <button className="clear-btn" onClick={clearChat} type="button">
            Clear chat
          </button>
        </header>

        <div className="chip-row">
          {suggestions.map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              className="chip"
              onClick={() => handleSubmit(suggestion)}
            >
              {suggestion}
            </button>
          ))}
        </div>

        <main className="message-panel" aria-live="polite">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message-row ${message.sender === "user" ? "is-user" : "is-bot"}`}
            >
              <div className="message-bubble">
                <div>{message.text}</div>
                {message.chart && <ChartPanel chart={message.chart} />}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message-row is-bot">
              <div
                className="message-bubble typing-bubble"
                aria-label="Loading response"
              >
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}

          {error && <div className="error-banner">{error}</div>}
          <div ref={endOfMessagesRef} />
        </main>

        <form
          className="composer"
          onSubmit={(event) => {
            event.preventDefault();
            handleSubmit();
          }}
        >
          <input
            type="text"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask about account breakdowns, debit and credit percentages, fees, penalties, or account services..."
            aria-label="Ask a question"
          />
          <button type="submit" disabled={isLoading || !input.trim()}>
            {isLoading ? "Sending..." : "Send"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
