import os
import time

from google import genai
from google.genai import errors


# ============================================================
# Configuration
# ============================================================

MODEL_NAME = "gemini-3.6-flash"
API_KEY = os.getenv("GEMINI_API_KEY")

MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 2


# ============================================================
# Tutor instructions
# ============================================================

SYSTEM_INSTRUCTION = """
You are an honest English tutor and DET preparation coach.

Your job is to help the student practice English for the
Duolingo English Test.

SESSION
-------
At the beginning of each session, choose ONE clear topic.

Examples:
- Education
- Technology
- Artificial intelligence
- Science
- Environment
- University
- Work
- Travel
- Social media

Tell the student the topic and ask ONE clear question.

IMPORTANT:
Keep the entire session focused on the SAME main topic.

Do not randomly change topics.

Ask related follow-up questions that become gradually more
challenging.

QUESTION QUALITY
----------------
Questions should make the student:
- Give an opinion
- Explain reasons
- Give examples
- Describe experiences
- Compare ideas
- Discuss advantages and disadvantages
- Explain more complex ideas

Ask only ONE question at a time.

EVALUATION
----------
Evaluate the student's answer based on:

1. Relevance to the question
2. Grammar
3. Vocabulary
4. Coherence
5. Development of ideas

The student is typing their answers, so DO NOT evaluate
pronunciation.

Do not correct every tiny mistake.

Focus on the most important weakness.

DET SCORE ESTIMATE
------------------
Give an estimated DET score RANGE.

Use the DET scale from 10 to 160.
Use 5-point increments.

Examples:
90–100
105–115
120–130

This is ONLY a practice estimate.
It is NOT an official DET score.

Do not pretend that one answer can determine an exact
official DET score.

If there is not enough evidence, say:
"Not enough evidence yet."

As the session continues, use the student's overall
performance to make the estimated range more meaningful.

FEEDBACK FORMAT
---------------
After each answer, use this structure:

DET ESTIMATED SCORE:
[score range]

TOPIC RELEVANCE:
[Pass or Fail]
[brief explanation]

MAIN STRENGTH:
[one specific strength]

MAIN WEAKNESS:
[one important weakness]

GRAMMAR & COHESION:
[important correction or explanation]

VOCABULARY:
[2 useful vocabulary upgrades]

MODEL CORRECTION:
[one improved sentence using the student's original idea]

NEXT QUESTION:
[one question related to the SAME topic]

Keep the feedback concise and useful.

OFF-TOPIC ANSWERS
-----------------
If the student does not answer the question:

- Mark Topic Relevance as Fail.
- Explain briefly why.
- Encourage the student to answer the actual question.
- Do not invent mistakes that are not present.

SPECIAL COMMANDS
----------------
If the student types:

skip
example
I don't know
don't know

Do NOT penalize the student.

Instead:
1. Give a strong model answer to the CURRENT question.
2. Explain 2 useful expressions or structures.
3. Ask ONE new question about the SAME topic.

If the student types "review":

Provide:

SESSION REVIEW
--------------

MAIN TOPIC:
...

ESTIMATED DET RANGE:
...

MAIN STRENGTH:
...

MAIN WEAKNESS:
...

TOP 3 RECURRING MISTAKES:
1.
2.
3.

VOCABULARY TO IMPROVE:
1.
2.

GRAMMAR TO PRACTICE:
1.
2.

NEXT GOAL:
...

Keep the review concise.
"""


# ============================================================
# DET Tutor
# ============================================================

class DETTutor:
    """Terminal-based English practice tutor for DET preparation."""

    def __init__(self, api_key, model_name):
        self.api_key = api_key
        self.model_name = model_name
        self.client = None
        self.chat = None

    def initialize(self):
        """Create the Gemini client and chat session."""

        if not self.api_key:
            print("\n❌ GEMINI_API_KEY is not set.")
            print("\nIn PowerShell, run:")
            print('$env:GEMINI_API_KEY="YOUR_NEW_API_KEY"')
            return False

        try:
            self.client = genai.Client(api_key=self.api_key)

            self.chat = self.client.chats.create(
                model=self.model_name,
                config={
                    "system_instruction": SYSTEM_INSTRUCTION
                },
            )

            return True

        except Exception as error:
            print(f"\n❌ Initialization error: {error}")
            return False

    def send_message(self, message):
        """
        Send a message to Gemini.

        Temporary 503/429 errors are retried with exponential backoff.
        """

        delay = INITIAL_RETRY_DELAY

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                return self.chat.send_message(message=message)

            except errors.APIError as error:

                # Temporary server/rate-limit errors.
                if error.code in (429, 500, 503) and attempt < MAX_RETRIES:
                    print(
                        f"\n⚠️ Gemini is temporarily unavailable."
                        f" Retrying in {delay} seconds..."
                    )

                    time.sleep(delay)
                    delay *= 2

                else:
                    raise

    def start_session(self):
        """Generate the first topic and question."""

        prompt = """
Start a new DET English practice session.

Choose ONE realistic topic.

Display:

📝 MAIN TOPIC: [topic]

Then ask ONE clear DET-style question.

Do not give feedback yet.
"""

        response = self.send_message(prompt)

        print(f"\n🤖 Tutor:\n{response.text}")

    def evaluate_answer(self, answer):
        """Evaluate the student's answer."""

        prompt = f"""
Evaluate the student's answer to the current question.

Student answer:
"{answer}"

Follow the feedback format from your instructions.

Remember:
- Stay on the SAME main topic.
- Check whether the answer directly addresses the question.
- Give an estimated DET score RANGE.
- Identify one main strength.
- Identify one main weakness.
- Give useful grammar/cohesion feedback.
- Give two useful vocabulary upgrades.
- Give one model correction.
- Ask ONE related follow-up question.
- Keep the response concise.
"""

        response = self.send_message(prompt)

        print("\n" + "=" * 60)
        print(response.text)
        print("=" * 60)

    def show_example(self):
        """Give a model answer without penalizing the student."""

        prompt = """
The student requested an example.

Do not penalize them.

For the CURRENT question:

1. Give a strong natural model answer.
2. Keep the answer realistic for a strong DET response.
3. Explain two useful expressions or structures.
4. Ask ONE new question related to the SAME topic.

Do not change the topic.
"""

        response = self.send_message(prompt)

        print(f"\n🤖 Model Answer:\n{response.text}")

    def review_session(self):
        """Summarize the student's performance."""

        prompt = """
Review my performance throughout this session.

Use this structure:

SESSION REVIEW
--------------

MAIN TOPIC:
...

ESTIMATED DET RANGE:
...

MAIN STRENGTH:
...

MAIN WEAKNESS:
...

TOP 3 RECURRING MISTAKES:
1.
2.
3.

VOCABULARY TO IMPROVE:
1.
2.

GRAMMAR TO PRACTICE:
1.
2.

NEXT GOAL:
...

Be honest and concise.
"""

        response = self.send_message(prompt)

        print(f"\n📊 {response.text}")

    @staticmethod
    def show_help():
        """Display available commands."""

        print(
            """
COMMANDS
--------
help       Show commands
skip       Get a model answer
example    Get a model answer
review     Review your session
quit       Exit
exit       Exit
"""
        )

    def run(self):
        """Run the interactive tutor."""

        if not self.initialize():
            return

        print("\n" + "=" * 60)
        print("          DUOLINGO ENGLISH TEST PRACTICE")
        print("=" * 60)
        print("• Main-topic focused practice")
        print("• Estimated DET score range")
        print("• Grammar and vocabulary feedback")
        print("• Topic relevance checking")
        print("• Type 'skip' or 'example' for help")
        print("• Type 'review' for a session summary")
        print("• Type 'quit' to exit")
        print("=" * 60)

        try:
            self.start_session()

        except errors.APIError as error:
            print(f"\n❌ Could not start the session: {error}")
            return

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if not user_input:
                    print("⚠️ Please enter an answer.")
                    continue

                command = user_input.lower()

                if command in {"quit", "exit"}:
                    print("\nGoodbye! Keep practicing! 👋")
                    break

                if command == "help":
                    self.show_help()
                    continue

                if command == "review":
                    print("\n📊 Reviewing your session...")
                    self.review_session()
                    continue

                if command in {
                    "skip",
                    "example",
                    "i don't know",
                    "dont know",
                    "don't know",
                }:
                    print("\n🤖 Generating a model answer...")
                    self.show_example()
                    continue

                print("\n🤖 Evaluating your answer...")
                self.evaluate_answer(user_input)

            except errors.APIError as error:
                print(f"\n❌ Gemini API error: {error}")

                if error.code == 503:
                    print(
                        "Gemini is temporarily unavailable. "
                        "Please wait a little and try again."
                    )

            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break

            except Exception as error:
                print(f"\n❌ Unexpected error: {error}")


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    tutor = DETTutor(
        api_key=API_KEY,
        model_name=MODEL_NAME,
    )

    tutor.run()
