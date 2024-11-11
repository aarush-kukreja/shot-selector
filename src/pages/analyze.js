import { useState } from 'react'
import Head from 'next/head'
import styles from '@/styles/Analyze.module.css'

// Simple prompt analysis logic
const analyzePrompt = (prompt) => {
  const promptLength = prompt.trim().length;
  const wordCount = prompt.trim().split(/\s+/).length;
  
  // Simple heuristic-based analysis
  if (promptLength < 50) {
    return {
      strategy: "Zero-Shot",
      confidence: 0.85,
      explanation: "Short, direct prompt suitable for zero-shot approach. The prompt is concise and likely contains a straightforward request."
    };
  } else if (wordCount > 50) {
    return {
      strategy: "Chain-of-Thought",
      confidence: 0.78,
      explanation: "Complex prompt that would benefit from breaking down the reasoning process step by step."
    };
  } else {
    return {
      strategy: "One-Shot",
      confidence: 0.92,
      explanation: "Moderate complexity prompt that would benefit from a single example to guide the response."
    };
  }
};

export default function Analyze() {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsAnalyzing(true);
    
    // Simulate analysis delay for better UX
    setTimeout(() => {
      const analysis = analyzePrompt(prompt);
      setResult(analysis);
      setIsAnalyzing(false);
    }, 500);
  };

  return (
    <>
      <Head>
        <title>Shot Selector - Analyze Prompt</title>
        <meta name="description" content="Analyze your prompt for optimal strategy" />
      </Head>

      <div className={styles.analysisContainer}>
        <form onSubmit={handleSubmit} className={styles.promptForm}>
          <div className={styles.formGroup}>
            <label htmlFor="prompt">Enter your prompt:</label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows="6"
              required
            />
          </div>
          <button 
            type="submit" 
            className={styles.submitButton}
            disabled={isAnalyzing || !prompt.trim()}
          >
            {isAnalyzing ? 'Analyzing...' : 'Analyze'}
          </button>
        </form>

        {result && (
          <div className={styles.resultContainer}>
            <div className={styles.resultContent}>
              <p>Recommended Strategy: {result.strategy}</p>
              <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
            </div>
            <div className={styles.explanation}>
              <p>{result.explanation}</p>
            </div>
          </div>
        )}
      </div>
    </>
  )
} 