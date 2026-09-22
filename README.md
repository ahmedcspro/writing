# writing
This tool has helped me a lot to improve my writing because I want to prepare for the DET.
I see a lot of teachers' website have systems that help students practice with unlimited questions, and get little feedback. However, the biggest challenge was every week I need to pay for this tool, or for one month, this makes me feel frustrate because I do not have a credit card, I only use my father's credit card. That's why I take care of this, I also start deep thinking how their websites work. I have much experience in Python I discovered that I have already known how I can use Artificial intelligence. Nevertheless, I built this tool. It helps me practice with many types of questions and get feedback quickly for every answer. 






# DET English Practice Tutor

A terminal-based English practice tutor powered by the Google Gemini API. It helps me prepare for the Duolingo English Test by asking topic-focused questions and providing concise feedback on grammar, vocabulary, coherence, and answer development.

## Features

- Starts each session with one realistic DET-style topic
- Keeps follow-up questions focused on the same topic
- Evaluates answers for:
  - Relevance
  - Grammar
  - Vocabulary
  - Coherence
  - Development of ideas
- Provides a practice DET score range from 10 to 160
- Gives grammar corrections and vocabulary upgrades
- Generates model answers when you type `skip` or `example`
- Provides a session review with recurring mistakes and improvement goals
- Automatically retries temporary Gemini API and rate-limit errors
- Runs directly in the terminal

> The estimated DET score is for practice only and is not an official Duolingo English Test score.

## Requirements

- Python 3.9 or newer
- A Google Gemini API key
- The `google-genai` Python package

## Installation

Clone the repository:

```bash
git clone https://github.com/ahmedcspro/writing.git
cd writing
```

Install the required dependency:

```bash
pip install google-genai
```

## API Key Setup

Create a Gemini API key and store it in the `GEMINI_API_KEY` environment variable.

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

### macOS or Linux

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Never commit your API key to the repository.

## Usage

Run the tutor with:

```bash
python app.py
```

The tutor will start a session, choose a topic, and ask your first question. Type your answer to receive feedback and a related follow-up question.

## Available Commands

| Command | Description |
|---|---|
| `help` | Display the available commands |
| `skip` | Show a model answer for the current question |
| `example` | Show a model answer for the current question |
| `review` | Review your performance during the session |
| `quit` | Exit the tutor |
| `exit` | Exit the tutor |

## Example Feedback

After answering a question, the tutor provides:

- An estimated DET score range
- Topic relevance
- Your main strength
- Your main weakness
- Grammar and cohesion feedback
- Two vocabulary upgrades
- An improved version of one sentence
- The next question on the same topic

## Project Structure

```text
.
├── app.py
└── README.md
```
