# LLM Image Measurement Evaluation

## Overview

This project evaluates the performance of various Large Language Models (LLMs) in performing precise image measurement tasks on technical drawings. Specifically, it tests the models' ability to measure dimensions from piping drawings by identifying pixel coordinates, performing scale conversions, and calculating real-world measurements.

**What it tests:**
- Accuracy in locating pixel coordinates from images (compares LLM output to actual values)

**Evaluation Method:**
The system uses [Promptfoo](https://www.promptfoo.dev/) to run automated evaluations across multiple AI providers, comparing their outputs against known actual values with a defined tolerance threshold.

For detailed information about the measurement methodology, see [docs/process.md](docs/process.md).

---

## Prerequisites

Before getting started, ensure you have:
- **Node.js** (required for Promptfoo)
- API keys for at least one of the following providers:
  - OpenAI (GPT models)
  - Anthropic (Claude models)
  - Google (Gemini models)

---

## Getting Started

### 1. Install Promptfoo

Follow the [official installation guide](https://www.promptfoo.dev/docs/installation/):

```bash
npm install -g promptfoo
```

Verify the installation:

```bash
promptfoo --version
```

### 2. Configure API Keys

Create a `.env` file in the project root with your API keys:

```bash
# .env file
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GEMINI_API_KEY=your_google_key_here
```

> **Note:** If you don't have access to all providers, comment out the unavailable providers in `promptfooconfig.yaml`.

### 3. Review Configuration

The evaluation configuration is defined in `promptfooconfig.yaml`. Current providers being tested:

| Provider | Model |
|----------|-------|
| Anthropic | claude-opus-4-5 |
| Anthropic | claude-sonnet-4-5 |
| Anthropic | claude-haiku-4-5 |

---

## Project Structure

```
measure-eval/
├── README.MD                 # This file
├── promptfooconfig.yaml      # Evaluation configuration
├── prompt.py                 # Image prompt formatting for different providers
├── compare_values.py         # Validation logic (work in progress)
├── .env                      # API keys (create this)
├── docs/
│   └── process.md           # Detailed measurement process documentation
├── image/
│   └── piping-red-full-1268x951-600.png  # Test image
└── pdf/
    └── piping-red-full.pdf  # Original PDF drawing
```

---

## Running Evaluations

### Run the Evaluation

Execute the evaluation across all configured providers:

```bash
promptfoo eval
```

**What happens during evaluation:**
1. Promptfoo loads the test configuration
2. For each provider, it sends the image with measurement instructions
3. Models analyze the image and return measurements in JSON format
4. Results are collected and can be compared across providers

### View Results

After the evaluation completes, launch the interactive results viewer:

```bash
promptfoo view
```

This opens a web interface where you can:
- Compare outputs from different models
- Review individual responses
- Analyze accuracy and consistency
- Export results for further analysis

---

## Understanding the Measurement Process

The evaluation tests the LLM's ability to execute a 6-step measurement process.

For the complete process with detailed examples, see [docs/process.md](docs/process.md).

---

## Next Steps

- Configure assertion logic in `promptfooconfig.yaml`
- Update `compare_values.py` to match new JSON output format
- Implement comprehensive accuracy metrics
- Add additional test images with varying complexity

