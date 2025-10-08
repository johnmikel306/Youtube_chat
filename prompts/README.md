# Prompts Directory

This directory contains all prompts used in the YouTube Q&A agent, organized by version for easy tracking and experimentation.

## 📋 Prompt Versioning

All prompts are versioned to:
- **Track changes** over time
- **Compare performance** between versions
- **Roll back** if needed
- **Experiment** with different approaches
- **Document** what works and what doesn't

## 📁 Current Prompts

### System Prompt

The system prompt defines the agent's behavior and role.

| Version | File | Status | Description |
|---------|------|--------|-------------|
| v1 | `system_prompt_v1.txt` | ✅ Active | Initial system prompt - instructs agent to search video and provide accurate answers |

## 🎯 How to Use

### In Code

The active prompt is loaded from `config/settings.py`:

```python
from config.settings import SYSTEM_PROMPT

# SYSTEM_PROMPT is automatically loaded from prompts/system_prompt_v1.txt
```

### Switching Versions

To use a different prompt version:

1. **Edit `config/settings.py`**:
   ```python
   PROMPT_VERSION = "v2"  # Change version number
   ```

2. **Or directly specify the file**:
   ```python
   SYSTEM_PROMPT_FILE = "prompts/system_prompt_v2.txt"
   ```

## 📝 Creating New Versions

When you want to experiment with a new prompt:

1. **Copy the current version**:
   ```bash
   cp prompts/system_prompt_v1.txt prompts/system_prompt_v2.txt
   ```

2. **Edit the new version** with your changes

3. **Update the version in config**:
   ```python
   # config/settings.py
   PROMPT_VERSION = "v2"
   ```

4. **Test and compare** results

5. **Document your findings** below

## 📊 Version History & Performance

### v1 (Current)
- **Created**: 2025-01-XX
- **Purpose**: Initial system prompt
- **Behavior**: 
  - Instructs agent to use search tool
  - Emphasizes accuracy and grounding in video content
  - Clear and concise instructions
- **Performance**: ✅ Works well for general Q&A
- **Issues**: None identified yet
- **Notes**: Baseline version

### v2 (Future)
- **Created**: TBD
- **Purpose**: [Describe what you're trying to improve]
- **Changes**: [List specific changes from v1]
- **Performance**: [Test results]
- **Issues**: [Any problems encountered]
- **Notes**: [Additional observations]

## 💡 Prompt Engineering Tips

### What Makes a Good System Prompt?

1. **Clear Role Definition**: Tell the agent what it is
2. **Specific Instructions**: Explain what to do and how
3. **Tool Usage Guidance**: When and how to use tools
4. **Output Format**: How to structure responses
5. **Constraints**: What NOT to do

### Example Improvements to Try

**Add Timestamp Information**:
```
When answering, include timestamps from the video when relevant.
```

**Improve Citation**:
```
Always cite which part of the transcript you're using to answer.
```

**Handle Uncertainty**:
```
If the video doesn't contain information to answer the question, say so clearly.
```

**Structured Responses**:
```
Format your answers with:
1. Direct answer
2. Supporting evidence from video
3. Relevant timestamp (if applicable)
```

## 🧪 Testing Prompts

### A/B Testing

To compare two prompt versions:

```python
from src.app import YouTubeQA

# Test v1
qa_v1 = YouTubeQA(api_key="...")
qa_v1.load_video("https://youtube.com/watch?v=...")
answer_v1 = qa_v1.ask("What is this video about?")

# Test v2 (after changing PROMPT_VERSION in config)
qa_v2 = YouTubeQA(api_key="...")
qa_v2.load_video("https://youtube.com/watch?v=...")
answer_v2 = qa_v2.ask("What is this video about?")

# Compare results
print("V1:", answer_v1)
print("V2:", answer_v2)
```

### Metrics to Track

- **Accuracy**: Does it answer correctly?
- **Relevance**: Is the answer on-topic?
- **Completeness**: Does it cover all aspects?
- **Conciseness**: Is it too verbose or too brief?
- **Tool Usage**: Does it search when needed?
- **Hallucination**: Does it make things up?

## 📚 Resources

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [LangChain Prompting Best Practices](https://python.langchain.com/docs/modules/model_io/prompts/)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)

## 🔄 Changelog

| Date | Version | Change | Reason |
|------|---------|--------|--------|
| 2025-01-XX | v1 | Initial prompt | Project creation |

---

**Remember**: Always test new prompts thoroughly before deploying to production!

