# Image Studio AI

A Streamlit app for photorealistic image generation and iterative refinement using OpenAI's `gpt-image-1` model.

## Features

- **Generate from scratch** — describe an image and create it
- **Edit existing images** — upload a source image and iteratively refine it with prompts
- **Iterative refinement** — each prompt builds on the previous result
- **Before / After comparison** — see the original vs. the latest iteration side by side
- **Multiple downloads** — export any iteration as PNG or JPEG
- **Photorealism system prompt** — enforces realistic output while preserving source colors
- **Dark theme** — premium, mild dark UI optimized for desktop and mobile

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/YUWE-3637/Image_processing.git
cd Image_processing

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your OpenAI API key
cp .env.example .env
# Then edit .env and add your real OPENAI_API_KEY

# 4. Run the app
streamlit run Streamlite_app.py
```

The app will be live at `http://localhost:8501`.

## Configuration

Adjust output **size** (`1024x1024`, `1536x1024`, `1024x1536`) and **quality** (`high`, `medium`, `low`, `auto`) from the sidebar.

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [OpenAI `gpt-image-1`](https://platform.openai.com/docs/guides/image-generation) — image generation & editing
- [Pillow](https://python-pillow.org/) — image processing
